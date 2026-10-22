"""pytest 路径与临时项目夹具。"""

from __future__ import annotations

import re
import shutil
import sys
import uuid
from collections.abc import Iterator
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
VENDOR_DIR = PROJECT_ROOT / ".vendor"
if VENDOR_DIR.is_dir() and str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ess_ai.config import Settings, load_settings  # noqa: E402


@pytest.fixture()
def workspace_tmp(request: pytest.FixtureRequest) -> Iterator[Path]:
    """在工作区内创建隔离目录。

    不使用 pytest 默认 ``tmp_path``，因为某些 Windows 沙箱/受限 ACL 环境
    不允许 pytest 对系统临时目录执行清理。这里保留产物、不自动删除。
    """

    safe_name = re.sub(r"[^\w.\-]+", "_", request.node.name)[:60]
    target = PROJECT_ROOT / "tests" / "_artifacts" / f"{safe_name}_{uuid.uuid4().hex[:8]}"
    target.mkdir(parents=True, exist_ok=True)
    yield target
    shutil.rmtree(target, ignore_errors=True)


@pytest.fixture()
def temp_settings(workspace_tmp: Path) -> Settings:
    """复制配置与 mock 数据到临时目录，避免污染真实 outputs。"""

    shutil.copytree(PROJECT_ROOT / "config", workspace_tmp / "config")
    shutil.copytree(PROJECT_ROOT / "data" / "mock", workspace_tmp / "data" / "mock")
    settings = load_settings(root=workspace_tmp)
    settings.ensure_directories()
    return settings
