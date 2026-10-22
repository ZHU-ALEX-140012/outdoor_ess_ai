#!/usr/bin/env python3
"""项目静态校验：Python AST/编译、YAML、JSON、JSONL 与目录结构。

用法：
    python scripts/check_syntax.py
    python scripts/check_syntax.py --root .
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

SKIP_DIRS = {
    ".git",
    ".venv",
    ".vendor",
    "venv",
    "__pycache__",
    "node_modules",
    ".mypy_cache",
    ".ruff_cache",
    ".taste-skill",
}
REQUIRED_FILES = (
    "README.md",
    "requirements.txt",
    "main.py",
    "utils.py",
    "product_research.py",
    "listing_generator.py",
    "competitor_monitor.py",
    "compliance_check.py",
    "report_generator.py",
    "interview_demo.py",
    "error_guard.py",
    "app.py",
    "start_all.ps1",
    "start_all.sh",
    ".streamlit/config.toml",
    "config/settings.yaml",
    "config/product_research.yaml",
    "config/amazon_listing_profile.yaml",
    "config/listing_copy_rules.yaml",
    "config/competitor_monitor.yaml",
    "config/compliance_rules.yaml",
    "config/report_generator.yaml",
)
REQUIRED_DIRS = (
    "config",
    "data/mock",
    "docs",
    "ess_ai",
    "ess_ai/collectors",
    "ess_ai/processing",
    "ess_ai/analysis",
    "ess_ai/listing",
    "ess_ai/content",
    "ess_ai/compliance",
    "ess_ai/reporting",
    "ess_ai/pipelines",
    "ess_ai/integrations",
    "ess_ai/storage",
    "outputs",
    "prompts",
    "scripts",
    "tests",
)
PACKAGE_DIRS = (
    "ess_ai",
    "ess_ai/collectors",
    "ess_ai/processing",
    "ess_ai/analysis",
    "ess_ai/listing",
    "ess_ai/content",
    "ess_ai/compliance",
    "ess_ai/reporting",
    "ess_ai/pipelines",
    "ess_ai/integrations",
    "ess_ai/storage",
)


def _iter_files(root: Path, suffix: str) -> list[Path]:
    return sorted(
        path
        for path in root.rglob(f"*{suffix}")
        if path.is_file()
        and not any(part in SKIP_DIRS for part in path.parts)
        and not any(part.startswith(".pytest") or part == "_artifacts" for part in path.parts)
    )


def check_python(root: Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    files = _iter_files(root, ".py")
    for path in files:
        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
            compile(tree, str(path), "exec")
        except (SyntaxError, UnicodeDecodeError, ValueError) as exc:
            errors.append(f"{path.relative_to(root)}: {type(exc).__name__}: {exc}")
    return len(files), errors


def check_json(root: Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    files = _iter_files(root, ".json")
    for path in files:
        try:
            with path.open("r", encoding="utf-8") as handle:
                json.load(handle)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"{path.relative_to(root)}: JSON 解析失败: {exc}")
    return len(files), errors


def check_jsonl(root: Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    files = _iter_files(root, ".jsonl")
    for path in files:
        line_no = 0
        try:
            with path.open("r", encoding="utf-8") as handle:
                for line in handle:
                    line_no += 1
                    if line.strip():
                        json.loads(line)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"{path.relative_to(root)}: JSONL 解析失败（第 {line_no} 行）: {exc}")
    return len(files), errors


def check_yaml(root: Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    files = _iter_files(root, ".yml") + _iter_files(root, ".yaml")
    try:
        import yaml
    except ImportError:
        return 0, ["PyYAML 未安装，跳过 YAML 校验（pip install PyYAML）"]
    for path in sorted(set(files)):
        try:
            with path.open("r", encoding="utf-8") as handle:
                yaml.safe_load(handle)
        except Exception as exc:  # YAML 异常类型较多，统一收集
            errors.append(f"{path.relative_to(root)}: YAML 解析失败: {exc}")
    return len(set(files)), errors


def check_structure(root: Path) -> list[str]:
    errors: list[str] = []
    for name in REQUIRED_FILES:
        if not (root / name).exists():
            errors.append(f"缺少必需文件: {name}")
    for name in REQUIRED_DIRS:
        if not (root / name).is_dir():
            errors.append(f"缺少必需目录: {name}")
    for name in PACKAGE_DIRS:
        init_file = root / name / "__init__.py"
        if not init_file.exists():
            errors.append(f"缺少包初始化文件: {name}/__init__.py")
    return errors


def _configure_stdio() -> None:
    """在 Windows GBK 控制台下强制 UTF-8，避免中文/符号输出失败。"""

    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="replace")


def main(argv: list[str] | None = None) -> int:
    _configure_stdio()
    parser = argparse.ArgumentParser(description="校验项目语法与结构")
    parser.add_argument("--root", default=".", help="项目根目录")
    args = parser.parse_args(argv)
    root = Path(args.root).expanduser().resolve()

    results: dict[str, Any] = {}
    errors: list[str] = []

    py_count, py_errors = check_python(root)
    results["python_files"] = py_count
    errors.extend(py_errors)

    json_count, json_errors = check_json(root)
    results["json_files"] = json_count
    errors.extend(json_errors)

    jsonl_count, jsonl_errors = check_jsonl(root)
    results["jsonl_files"] = jsonl_count
    errors.extend(jsonl_errors)

    yaml_count, yaml_errors = check_yaml(root)
    results["yaml_files"] = yaml_count
    errors.extend(yaml_errors)

    structure_errors = check_structure(root)
    errors.extend(structure_errors)

    print("=" * 62)
    print("项目静态校验")
    print(f"根目录      : {root}")
    print(f"Python 文件 : {py_count}")
    print(f"JSON 文件   : {json_count}")
    print(f"JSONL 文件  : {jsonl_count}")
    print(f"YAML 文件   : {yaml_count}")
    print(f"结构检查    : {'通过' if not structure_errors else '失败'}")
    print("=" * 62)

    if errors:
        print(f"✗ 发现 {len(errors)} 个问题：")
        for item in errors:
            print(f"  - {item}")
        return 1
    print("✓ 所有 Python 文件可解析、可编译；YAML/JSON 可解析；目录结构完整。")
    return 0


if __name__ == "__main__":
    from error_guard import run_cli

    raise SystemExit(run_cli(main, "check_syntax"))
