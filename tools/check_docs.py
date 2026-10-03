"""Read-only Markdown local link audit. Python standard library only.

Usage: python tools/check_docs.py [ROOT] [--output audit-links.json]
Ignores fenced code and inline code examples; handles inline/reference links,
images, HTML anchors and GitHub Unicode heading IDs including duplicate slugs.
This is a static approximation: GitHub renderer remains authoritative.
"""
import argparse
import csv
from contextlib import contextmanager
import hashlib
import html
import json
import re
import shutil
import subprocess
import tempfile
import unicodedata
import uuid
from pathlib import Path
from urllib.parse import unquote, urlsplit


def visible_lines(text):
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        m = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if m:
            marker = m.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence) and not line[m.end():].strip():
                fence = None
            yield number, ""
            continue
        if fence:
            yield number, ""
        else:
            # Preserve text in code spans for headings but strip code links later.
            yield number, line


def slugify(title):
    title = re.sub(r"!?(?:\[([^\]]*)\])\([^)]*\)", r"\1", title)
    title = re.sub(r"<[^>]*>", "", title)
    title = html.unescape(title).lower().replace("`", "")
    title = "".join(c for c in title if c in " -_" or unicodedata.category(c)[0] in "LN M".replace(" ", ""))
    return title.replace(" ", "-")


def anchors(lines):
    result, used = set(), set()
    for i, (number, line) in enumerate(lines):
        for m in re.finditer(r'<(?:a|h[1-6])\b[^>]*\b(?:id|name)=["\']([^"\']+)', line, re.I):
            result.add(m.group(1))
        heading = re.match(r"^\s{0,3}#{1,6}\s+(.+?)(?:\s+#+)?\s*$", line)
        title = heading.group(1) if heading else None
        if title is None and i + 1 < len(lines) and line.strip() and re.match(r"^\s{0,3}(?:=+|-+)\s*$", lines[i + 1][1]):
            title = line.strip()
        if title is not None:
            base = slugify(title)
            slug, suffix = base, 0
            while slug in used:
                suffix += 1
                slug = f"{base}-{suffix}"
            used.add(slug)
            result.add(slug)
    return result


def scan(root):
    # Only public course content: local PRDs and ignored handoff notes are excluded.
    files = sorted(
        [p for p in (root / "README.md", root / "CHANGELOG.md") if p.exists()]
        + list((root / "docs").rglob("*.md"))
        + list((root / "examples").rglob("*.md"))
    )
    contents, structure_errors = {}, []
    for path in files:
        try:
            raw = path.read_text(encoding="utf-8-sig")
        except UnicodeError:
            structure_errors.append({"file": str(path.relative_to(root)).replace("\\", "/"), "reason": "invalid-utf8"})
            continue
        if "\ufffd" in raw:
            structure_errors.append({"file": path.relative_to(root).as_posix(), "reason": "replacement-character"})
        contents[path] = list(visible_lines(raw))
        fence, opening = None, None
        for number, line in enumerate(raw.splitlines(), 1):
            match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
            if match:
                marker = match.group(1)
                if fence is None:
                    fence, opening = marker, number
                elif marker[0] == fence[0] and len(marker) >= len(fence) and not line[match.end():].strip():
                    fence = None
        if fence:
            structure_errors.append({"file": str(path.relative_to(root)).replace("\\", "/"), "line": opening, "reason": "unclosed-fence"})
    ids = {p.resolve(): anchors(lines) for p, lines in contents.items()}
    broken, external, local = [], [], []
    skipped = 0
    for source, lines in contents.items():
        refs = {}
        for number, line in lines:
            m = re.match(r"^\s{0,3}\[([^\]]+)\]:\s*(?:<([^>]+)>|(\S+))", line)
            if m:
                refs[m.group(1).strip().lower()] = m.group(2) or m.group(3)
        for number, raw in lines:
            if re.match(r"^(<<<<<<< |=======\s*$|>>>>>>> )", raw):
                structure_errors.append({"file": source.relative_to(root).as_posix(), "line": number, "reason": "merge-marker"})
            line = re.sub(r"(`+).*?\1", "", raw)
            if re.match(r"^\s{0,3}\[[^\]]+\]:", line):
                continue
            destinations = []
            destinations.extend(html.unescape(m.group(1)) for m in re.finditer(r'<(?:a|img)\b[^>]*\b(?:href|src)=["\']([^"\']+)', line, re.I))
            pattern = r"!?\[[^\]]*\]\(\s*(?:<([^>]+)>|([^\s)]+(?:\([^)]*\)[^\s)]*)?))(?:\s+[\"'][^\"']*[\"'])?\s*\)"
            destinations.extend((m.group(1) or m.group(2)) for m in re.finditer(pattern, line))
            for m in re.finditer(r"!?\[([^\]]+)\]\[([^\]]*)\]", line):
                key = (m.group(2) or m.group(1)).strip().lower()
                if key in refs:
                    destinations.append(refs[key])
            for destination in destinations:
                record = {"file": str(source.relative_to(root)).replace("\\", "/"), "line": number, "target": destination}
                url = urlsplit(destination)
                if url.scheme or destination.startswith("//"):
                    if url.scheme in ("https", "http"):
                        external.append(record)
                    else:
                        skipped += 1
                    continue
                if destination.startswith("/"):
                    # GitHub repo-absolute paths are resolved to this repository.
                    target = root / unquote(url.path.lstrip("/"))
                else:
                    target = source.parent / unquote(url.path) if url.path else source
                target = target.resolve()
                if not target.exists():
                    record["reason"] = "missing-path"
                    broken.append(record)
                elif url.fragment and target.suffix.lower() == ".md" and unquote(url.fragment) not in ids.get(target, set()):
                    record["reason"] = "missing-anchor"
                    record["available_anchors"] = sorted(ids.get(target, set()))
                    broken.append(record)
                else:
                    local.append(record)
    return {"markdown_files": len(files), "local_links": len(local), "external_links": len(external), "skipped_other_schemes": skipped, "structure_errors": structure_errors, "broken": broken, "external": external}


@contextmanager
def reference_directory(parent):
    # mkdir's inherited Windows ACL supports sandboxed execution; no sensitive data.
    directory = (parent / ("course-progress-check-" + uuid.uuid4().hex)).resolve()
    if directory.parent != parent.resolve():
        raise ValueError("Temporary directory escaped its parent")
    directory.mkdir()
    try:
        yield directory
    finally:
        # Delete only the two explicitly created files, without recursive deletion.
        for name in ("progress.cjs", "progress.test.cjs"):
            file = directory / name
            if file.exists():
                file.unlink()
        directory.rmdir()


def check_examples(root, temporary_parent=None):
    """Run intentional failure, fix a temporary copy, and verify CSV arithmetic."""
    errors, results = [], {}
    node = shutil.which("node")
    source_dir = root / "examples" / "progress-lab"
    source = source_dir / "progress.cjs"
    original = source.read_bytes()
    results["source_sha256"] = hashlib.sha256(original).hexdigest()
    if not node:
        errors.append("Node.js is required for exercise checks; --links-only skips them")
    else:
        baseline = subprocess.run([node, "progress.test.cjs"], cwd=source_dir, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=20)
        results["initial_exit_code"] = baseline.returncode
        results["initial_expected_failure"] = baseline.returncode != 0 and "NaN !== 0" in baseline.stderr and "AssertionError" in baseline.stderr
        if not results["initial_expected_failure"]:
            errors.append("Intentional NaN / zero failure was not reproduced")
        with reference_directory(temporary_parent or Path(tempfile.gettempdir())) as temporary:
            target_dir = Path(temporary)
            for name in ("progress.cjs", "progress.test.cjs"):
                shutil.copyfile(source_dir / name, target_dir / name)
            fixed = original.decode("utf-8").replace("return Math.round((completed / total) * 100);", "if (total === 0) return 0;\n  return Math.round((completed / total) * 100);", 1)
            (target_dir / "progress.cjs").write_text(fixed, encoding="utf-8")
            passing = subprocess.run([node, "progress.test.cjs"], cwd=target_dir, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=20)
            results["reference_exit_code"] = passing.returncode
            results["reference_stdout"] = passing.stdout.strip()
            variant = subprocess.run([node, "-e", "const assert=require('node:assert/strict');const {progressPercent}=require('./progress.cjs');assert.equal(progressPercent(3,8),38);console.log('3/8 = 38');"], cwd=target_dir, capture_output=True, text=True, timeout=20)
            results["variant_exit_code"] = variant.returncode
            results["variant_stdout"] = variant.stdout.strip()
            if passing.returncode or passing.stdout.strip() != "progress checks passed":
                errors.append("The four original checks did not pass in the reference copy")
            if variant.returncode:
                errors.append("The 3/8 = 38 variant did not pass")
    results["original_unchanged"] = source.read_bytes() == original
    if not results["original_unchanged"]:
        errors.append("Intentional bug source changed during verification")
    with (root / "examples" / "office-lab" / "orders.csv").open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.reader(file))[1:]
    unique, seen = [], set()
    for row in rows:
        key = tuple(row)
        if key not in seen:
            seen.add(key)
            unique.append(row)
    pending = [row[0] for row in unique if row[2] == ""]
    totals = {}
    for row in unique:
        if row[2] == "":
            continue
        total = totals.setdefault(row[1], [0, 0, 0, 0])
        received, refunded = int(row[2]), int(row[3])
        for i, value in enumerate((1, received, refunded, received - refunded)):
            total[i] += value
    results["orders"] = {"raw_rows": len(rows), "duplicate_rows": len(rows) - len(unique), "pending": pending, "by_channel": totals, "total": [sum(t[i] for t in totals.values()) for i in range(4)]}
    expected = sorted([[3, 320, 20, 300], [2, 230, 150, 80]])
    if len(rows) != 7 or pending != ["B202"] or sorted(totals.values()) != expected:
        errors.append("Office CSV differs from documented 7-row exercise arithmetic")
    results["orders_variant_net_total"] = sum(t[3] for t in totals.values()) - 10
    results["errors"] = errors
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, nargs="?", default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--links-only", action="store_true", help="Skip Node.js and office fixture verification")
    parser.add_argument("--temp-parent", type=Path, help="Optional writable parent for the isolated reference copy")
    args = parser.parse_args()
    report = scan(args.root.resolve())
    if not args.links_only:
        report["examples"] = check_examples(args.root.resolve(), args.temp_parent.resolve() if args.temp_parent else None)
    if args.output:
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "external"}, ensure_ascii=True, indent=2))
    raise SystemExit(bool(report["broken"] or report["structure_errors"] or report.get("examples", {}).get("errors")))
