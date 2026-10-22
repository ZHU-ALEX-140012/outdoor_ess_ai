"""命令行入口。

常用：
    python main.py init
    python main.py demo
    python main.py check
    python main.py status
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

import utils
from ess_ai.config import ConfigError, Settings, load_settings
from ess_ai.pipelines.full_chain import FullChainPipeline

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _configure_stdio() -> None:
    """在 Windows GBK 控制台下强制 UTF-8，确保中文提示可读。"""

    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="replace")


def _setup_logging(settings: Settings) -> None:
    settings.ensure_directories()
    log_file = settings.path("paths.logs_dir") / str(
        settings.get("logging.file_name", "outdoor_ess_ai.log")
    )
    utils.setup_logging(
        level=settings.get("logging.level", "INFO"),
        log_file=log_file,
        console=bool(settings.get("logging.console", True)),
        max_bytes=int(settings.get("logging.max_bytes", 5 * 1024 * 1024)),
        backup_count=int(settings.get("logging.backup_count", 5)),
        force=True,
    )


def _cmd_init(settings: Settings) -> int:
    _setup_logging(settings)
    dirs = settings.ensure_directories()
    print(f"✓ 项目：{settings.project_name}")
    print(f"✓ 配置：{settings.config_path}")
    print(f"✓ 已准备 {len(dirs)} 个目录")
    print("下一步：python main.py demo")
    return 0


def _cmd_status(settings: Settings) -> int:
    _setup_logging(settings)
    api_key = bool(os.getenv(str(settings.get("llm.api_key_env", "DEEPSEEK_API_KEY"))))
    print(f"项目      : {settings.project_name} v{settings.get('project.version', '0.1.0')}")
    print(f"运行模式  : {settings.mode}")
    print(f"模型      : {settings.get('llm.model')}")
    print(f"API Key   : {'已配置（仅 live 模式使用）' if api_key else '未配置（离线回退可用）'}")
    print(f"目标市场  : {', '.join(settings.markets)}")
    print(f"项目根目录: {settings.root}")
    print(f"报告目录  : {settings.path('paths.reports_dir')}")
    return 0


def _cmd_demo(settings: Settings, args: argparse.Namespace) -> int:
    _setup_logging(settings)
    markets = None
    if args.markets:
        markets = [item.strip().upper() for item in args.markets.split(",") if item.strip()]
    pipeline = FullChainPipeline(settings, seed=args.seed, markets=markets)
    result = pipeline.run()
    summary = result["summary"]
    print("")
    print("=" * 68)
    print(f"✓ 全链路运行完成：{result['run_id']}")
    print(f"  首选市场：{summary.get('top_market')}（{summary.get('top_market_score')} 分）")
    print(f"  首选单品：{summary.get('top_product')}（{summary.get('top_sku')}）")
    print(f"  Listing ：{summary.get('listing_count')} 条")
    print(f"  内容包  ：{summary.get('content_pack_count')} 个")
    print(
        f"  合规    ：通过 {summary.get('compliance_passed')} / "
        f"需处理 {summary.get('compliance_failed')}（最高风险 {summary.get('highest_risk')}）"
    )
    print(f"  报告    ：{result['report_path']}")
    print(f"  清单    ：{result['manifest_path']}")
    print("=" * 68)
    return 0


def _cmd_check() -> int:
    script = PROJECT_ROOT / "scripts" / "check_syntax.py"
    completed = subprocess.run(
        [sys.executable, str(script), "--root", str(PROJECT_ROOT)],
        cwd=str(PROJECT_ROOT),
        check=False,
    )
    return int(completed.returncode)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="outdoor-ess-ai",
        description="欧美轻量化户外储能全链路 AI 自动化系统（离线模拟版）",
    )
    parser.add_argument("--config", help="自定义 settings.yaml 路径")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="初始化目录与日志")
    sub.add_parser("status", help="查看当前运行配置")
    sub.add_parser("check", help="校验 Python/YAML/JSON 语法与项目结构")

    demo = sub.add_parser("demo", help="运行全链路离线演示")
    demo.add_argument("--seed", type=int, help="覆盖模拟随机种子")
    demo.add_argument("--markets", help="逗号分隔的市场代码，如 US,DE")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    _configure_stdio()
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "check":
        return _cmd_check()
    try:
        settings = load_settings(args.config)
    except (ConfigError, utils.UtilError) as exc:
        print(f"配置加载失败：{exc}", file=sys.stderr)
        return 2

    if args.command == "init":
        return _cmd_init(settings)
    if args.command == "status":
        return _cmd_status(settings)
    if args.command == "demo":
        try:
            return _cmd_demo(settings, args)
        except Exception as exc:
            print(f"运行失败：{type(exc).__name__}: {exc}", file=sys.stderr)
            print(f"详细日志：{settings.path('paths.logs_dir')}", file=sys.stderr)
            return 1
    parser.error(f"未知命令: {args.command}")
    return 2
