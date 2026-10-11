"""Direct, anonymous MCP tool calls; no model or client credentials are loaded."""
import argparse
import asyncio
from datetime import timedelta
import json
import uuid

import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


URL = "https://search.parallel.ai/mcp"
USER_AGENT = "AI-Coding-Guide-Zh/parallel-search-lab"


def arguments():
    parser = argparse.ArgumentParser(description="匿名 MCP 搜索与网页读取练习")
    commands = parser.add_subparsers(dest="command", required=True)
    search = commands.add_parser("search", help="搜索公开网页")
    search.add_argument("objective", help="要查找的信息")
    search.add_argument("--query", action="append", required=True, help="关键词，可重复")
    fetch = commands.add_parser("fetch", help="读取指定公开网页")
    fetch.add_argument("urls", nargs="+", help="公开 HTTP/HTTPS URL，最多 20 个")
    args = parser.parse_args()
    if args.command == "fetch":
        try:
            urls = [httpx.URL(url) for url in args.urls]
        except httpx.InvalidURL:
            parser.error("fetch URL 格式无效")
        if len(urls) > 20 or any(
            url.scheme not in {"http", "https"} or not url.host for url in urls
        ):
            parser.error("fetch 需要 1–20 个有效的 HTTP/HTTPS URL")
    return args


async def run(args):
    tool = "web_search" if args.command == "search" else "web_fetch"
    params = {"session_id": str(uuid.uuid4())}
    if args.command == "search":
        params.update(objective=args.objective, search_queries=args.query)
    else:
        params.update(urls=args.urls, full_content=False)

    # Explicit headers only: neither environment API keys nor saved client auth.
    async with httpx.AsyncClient(
        headers={"User-Agent": USER_AGENT}, timeout=60.0
    ) as client:
        async with streamable_http_client(URL, http_client=client) as (read, write, _):
            async with ClientSession(
                read, write, read_timeout_seconds=timedelta(seconds=60)
            ) as session:
                await session.initialize()
                available = await session.list_tools()
                if tool not in {item.name for item in available.tools}:
                    raise RuntimeError(f"服务器未提供 {tool}")
                result = await session.call_tool(tool, params)
                data = result.structuredContent
                print(json.dumps(
                    data if data is not None else result.model_dump(mode="json"),
                    ensure_ascii=False, indent=2,
                ))
                # Extraction can return partial successes plus per-URL errors.
                return int(bool(result.isError or (data and data.get("errors"))))


if __name__ == "__main__":
    raise SystemExit(asyncio.run(run(arguments())))
