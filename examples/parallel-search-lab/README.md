# 匿名 MCP 搜索与网页读取练习

用 [Parallel Search MCP](https://docs.parallel.ai/integrations/mcp/search-mcp) 完成一次真实的远程工具调用：初始化连接、发现工具，再搜索公开网页或读取指定 URL。匿名端点免费提供 `web_search` 和 `web_fetch`，不需要 Parallel 账号或 API Key；搜索使用 Fast 模式，免费访问有速率限制。

本练习用 Python MCP SDK 直接调用工具，不调用模型，不修改 Codex / Claude Code 的配置。它验证的是 Streamable HTTP 连接和工具结果；App 中的可见性与模型是否会调用工具，仍需按 [CX-05](../../docs/codex/CX-05-Codex-MCP外部工具完整指南.md) 在自己的客户端中核对。

## 1. 安装

需要 Python 3.10 或更高版本，以及能访问 `https://search.parallel.ai/mcp` 的网络。在仓库根目录打开终端：

```bash
cd examples/parallel-search-lab
python -m venv .venv
```

macOS / Linux：

```bash
source .venv/bin/activate
```

Windows PowerShell：

```powershell
.venv\Scripts\Activate.ps1
```

激活后安装本练习的依赖：

```bash
python -m pip install -r requirements.txt
```

## 2. 搜索，核对来源

```bash
python search.py search "查找 Python venv 官方创建与激活说明" --query "Python venv documentation activate"
```

成功时会输出 JSON，`results` 中包含来源 `url`、标题和 `excerpts` 摘录。打开来源核对：是否是 Python 官方文档？创建与激活命令是否适用于你的系统？结果和排序可能随时间变化，不要把一次搜索当成固定参考答案。可重复传入 `--query`，为同一个目标补充相关关键词。

## 3. 读取一页公开文档

```bash
python search.py fetch https://docs.python.org/3/library/venv.html
```

在返回的 `results` 中查看 URL 与摘录，把创建虚拟环境的说明和第二步的搜索结果对照。默认只取摘录，避免整页内容过长；`errors` 应为空。也可以把第二步找到的公开 URL 作为参数，但不要提交带有私密 token 的 URL 或内部资料。查询和 URL 会发送给 Parallel。

脚本每次运行生成一个会话标识，不读取本地客户端凭据或环境中的 API Key。HTTP 请求与工具调用的超时均为 60 秒，按 `Ctrl+C` 可停止。不要为同一次受限请求不停重跑。

## 4. 排查与撤销

| 现象 | 下一步 |
|---|---|
| `ModuleNotFoundError` | 确认已激活 `.venv`，再用同一个 `python` 安装依赖 |
| 连接失败或超时 | 核对网络、代理和服务状态；不要改成关闭 TLS 校验 |
| HTTP `429` 或限流提示 | 按服务返回的等待时间稍后重试；免费不等于无限调用 |
| `errors` 非空或工具报错 | 核对 URL 是否公开可访问；脚本会保留结果并以非零状态退出 |
| 搜索结果不相关 | 收窄目标与关键词，优先核对一手来源 |

结束后运行 `deactivate`。如不再使用，删除本练习的 `.venv` 即可；没有客户端配置或账号授权需要撤销。所有样例采用仓库的 [MIT License](../../LICENSE)。
