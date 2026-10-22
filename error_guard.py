"""全局异常捕获与错误日志。

所有 CLI / Streamlit 入口都通过本模块记录未捕获异常，便于面试演示时
快速定位问题。日志写入 ``outputs/logs/errors.log`` 和 ``errors.jsonl``。
"""

from __future__ import annotations

import json
import os
import platform
import sys
import threading
import traceback
from collections.abc import Callable, Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import utils

PROJECT_ROOT = Path(__file__).resolve().parent
LOG_DIR = PROJECT_ROOT / "outputs" / "logs"
HUMAN_LOG = LOG_DIR / "errors.log"
JSONL_LOG = LOG_DIR / "errors.jsonl"


def log_exception(
    exc: BaseException,
    *,
    app: str,
    context: Mapping[str, Any] | None = None,
    argv: Sequence[str] | None = None,
) -> Path:
    """记录异常到人类可读日志和 JSONL；自身失败也不抛出。"""

    timestamp = datetime.now(UTC).isoformat()
    trace = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    record = {
        "timestamp": timestamp,
        "app": app,
        "exception_type": type(exc).__name__,
        "message": str(exc),
        "argv": list(argv if argv is not None else sys.argv),
        "cwd": os.getcwd(),
        "python": sys.version,
        "platform": platform.platform(),
        "context": dict(context or {}),
        "traceback": trace,
    }
    try:
        utils.ensure_dir(LOG_DIR)
        utils.write_text(
            HUMAN_LOG,
            f"\n{'=' * 80}\n[{timestamp}] {app} / {type(exc).__name__}: {exc}\n"
            f"{trace}\n",
            append=True,
        )
        utils.write_text(
            JSONL_LOG,
            json.dumps(record, ensure_ascii=False, default=str) + "\n",
            append=True,
        )
    except Exception as log_error:  # 日志失败不能覆盖原始异常
        print(f"[error_guard] 无法写入错误日志: {log_error}", file=sys.stderr)
    return HUMAN_LOG


def install_global_handler(app: str) -> None:
    """安装 sys/threading 未捕获异常钩子。"""

    original_hook = sys.excepthook

    def sys_hook(exc_type: type[BaseException], exc: BaseException, tb: Any) -> None:
        if not issubclass(exc_type, KeyboardInterrupt):
            log_exception(
                exc,
                app=app,
                context={"hook": "sys.excepthook"},
            )
        original_hook(exc_type, exc, tb)

    sys.excepthook = sys_hook

    def thread_hook(args: threading.ExceptHookArgs) -> None:
        if args.exc_value is not None:
            log_exception(
                args.exc_value,
                app=app,
                context={"hook": "threading.excepthook", "thread": args.thread.name if args.thread else ""},
            )

    threading.excepthook = thread_hook


def run_cli(
    main_func: Callable[[Sequence[str] | None], int],
    app: str,
    argv: Sequence[str] | None = None,
) -> int:
    """包装 CLI main：捕获未处理异常、写日志、返回非零退出码。"""

    install_global_handler(app)
    try:
        return int(main_func(argv))
    except KeyboardInterrupt:
        print("\n已中断。", file=sys.stderr)
        return 130
    except Exception as exc:
        log_path = log_exception(
            exc,
            app=app,
            context={"hook": "run_cli"},
        )
        print(f"✗ 未捕获异常：{type(exc).__name__}: {exc}", file=sys.stderr)
        print(f"  错误日志：{log_path}", file=sys.stderr)
        return 1


def log_command_error(
    app: str,
    command: Sequence[str],
    returncode: int,
    stdout: str,
    stderr: str,
) -> Path:
    """记录子进程失败（Streamlit 一键运行时使用）。"""

    exc = RuntimeError(f"命令执行失败，退出码 {returncode}: {' '.join(command)}")
    return log_exception(
        exc,
        app=app,
        context={
            "hook": "subprocess",
            "returncode": returncode,
            "stdout_tail": stdout[-4000:],
            "stderr_tail": stderr[-4000:],
        },
        argv=command,
    )
