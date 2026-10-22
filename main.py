#!/usr/bin/env python3
"""项目一键入口：python main.py <command>。"""

from __future__ import annotations

import sys
from pathlib import Path

# 允许从项目根目录直接运行，无需先安装为包。
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from error_guard import run_cli  # noqa: E402
from ess_ai.cli import main  # noqa: E402  (路径注入后再导入)

if __name__ == "__main__":
    raise SystemExit(run_cli(main, "main"))
