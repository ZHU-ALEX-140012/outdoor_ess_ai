#!/usr/bin/env python3
"""把项目源码导出为单个可复制 Markdown 文件。

只导出源码、配置、文档与 mock 数据；不包含 outputs、日志、缓存、虚拟环境。
用法：
    python scripts/export_bundle.py
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

INCLUDE_SUFFIXES = {
    ".py",
    ".yaml",
    ".yml",
    ".toml",
    ".md",
    ".txt",
    ".ps1",
    ".sh",
    ".json",
}
INCLUDE_NAMES = {".env.example", "requirements.txt", "start.sh", "start.ps1"}
SKIP_DIRS = {
    ".git",
    ".venv",
    ".vendor",
    "venv",
    "__pycache__",
    "node_modules",
    "outputs",
    "logs",
    "raw",
    "processed",
    "external",
    ".ruff_cache",
    ".pytest_cache",
    ".mypy_cache",
    ".taste-skill",
    "htmlcov",
    "_artifacts",
}
SKIP_FILES = {"FULL_CODE.md"}
LANG = {
    ".py": "python",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".toml": "toml",
    ".md": "markdown",
    ".json": "json",
    ".ps1": "powershell",
    ".sh": "bash",
}


def _selected(path: Path) -> bool:
    if path.name in SKIP_FILES:
        return False
    if path.name in INCLUDE_NAMES:
        return True
    return path.suffix.lower() in INCLUDE_SUFFIXES


def _ordered_files(root: Path) -> list[Path]:
    priority = [
        "README.md",
        "requirements.txt",
        "main.py",
        "utils.py",
        "pyproject.toml",
        ".env.example",
        "start.ps1",
        "start.sh",
    ]
    all_files = [
        path
        for path in root.rglob("*")
        if path.is_file()
        and _selected(path)
        and not any(part in SKIP_DIRS or part.startswith(".pytest") for part in path.parts)
        and (path.name == ".env.example" or not path.name.startswith(".env."))
    ]
    ordered: list[Path] = []
    for name in priority:
        candidate = root / name
        if candidate in all_files:
            ordered.append(candidate)
    remainder = sorted(
        (path for path in all_files if path not in ordered),
        key=lambda p: (0 if p.parts[-1] == "__init__.py" else 1, str(p).lower()),
    )
    return ordered + remainder


def build(root: Path, output: Path) -> tuple[int, int]:
    files = _ordered_files(root)
    chunks = [
        "# 欧美轻量化户外储能全链路 AI 自动化系统 · 全量源码",
        "",
        "> 本文件由 `python scripts/export_bundle.py` 自动生成。",
        "> 所有代码均为离线模拟版，不接入任何电商平台真实店铺 API。",
        "",
        f"- 项目根目录：`{root}`",
        f"- 文件数量：{len(files)}",
        "",
        "## 文件索引",
        "",
    ]
    for path in files:
        chunks.append(f"- `{path.relative_to(root).as_posix()}`")
    chunks.extend(["", "---", ""])

    for path in files:
        relative = path.relative_to(root).as_posix()
        suffix = path.suffix.lower()
        language = LANG.get(suffix, "")
        content = path.read_text(encoding="utf-8")
        chunks.extend(
            [
                f"## `{relative}`",
                "",
                f"````{language}",
                content.rstrip("\n"),
                "````",
                "",
            ]
        )
    text = "\n".join(chunks) + "\n"
    output.write_text(text, encoding="utf-8", newline="\n")
    return len(files), len(text.encode("utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="导出全量源码 Markdown")
    parser.add_argument("--root", default=".", help="项目根目录")
    parser.add_argument("--output", default="FULL_CODE.md", help="输出文件名")
    args = parser.parse_args(argv)
    root = Path(args.root).expanduser().resolve()
    output = (root / args.output).resolve()
    count, size = build(root, output)
    print(f"✓ 已导出 {count} 个文件 -> {output}（{size / 1024:.1f} KB）")
    return 0


if __name__ == "__main__":
    from error_guard import run_cli

    raise SystemExit(run_cli(main, "export_bundle"))
