"""本地存储适配器。

当前实现为文件系统 JSON 存储，后续可在不改业务层的前提下替换为
SQLite / 对象存储 / 数据仓库适配器。
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

import utils

logger = utils.get_logger(__name__)


class JsonStore:
    """按名称读写 JSON 快照，默认落在 ``data/processed``。"""

    def __init__(self, root: str | Path) -> None:
        self.root = utils.ensure_dir(root)

    def _path(self, name: str) -> Path:
        safe = utils.safe_filename(name, default="snapshot")
        if not safe.endswith(".json"):
            safe += ".json"
        return self.root / safe

    def save(self, name: str, payload: Any) -> Path:
        path = utils.write_json(self._path(name), payload)
        logger.debug("快照已写入: %s", path)
        return path

    def load(self, name: str, default: Any = None) -> Any:
        return utils.read_json(self._path(name), default)

    def exists(self, name: str) -> bool:
        return self._path(name).exists()

    def list_snapshots(self) -> list[Path]:
        return sorted(self.root.glob("*.json"))


class RunStore:
    """维护每次流水线运行的 manifest，保证阶段结果可追溯。"""

    def __init__(self, root: str | Path) -> None:
        self.root = utils.ensure_dir(root)

    def manifest_path(self, run_id: str) -> Path:
        return self.root / utils.safe_filename(run_id) / "manifest.json"

    def create(self, run_id: str, metadata: Mapping[str, Any]) -> Path:
        manifest = {
            "run_id": run_id,
            "status": "running",
            "created_at": utils.utc_now_iso(),
            "updated_at": utils.utc_now_iso(),
            "metadata": dict(metadata),
            "stages": [],
        }
        return utils.write_json(self.manifest_path(run_id), manifest)

    def _read(self, run_id: str) -> dict[str, Any]:
        manifest = utils.read_json(self.manifest_path(run_id), default={})
        if not isinstance(manifest, dict) or not manifest:
            raise utils.FileIOError(f"运行清单不存在或损坏: {run_id}")
        return manifest

    def load(self, run_id: str) -> dict[str, Any]:
        """读取运行清单。"""

        return self._read(run_id)

    def add_stage(
        self,
        run_id: str,
        *,
        name: str,
        status: str,
        elapsed_ms: float,
        outputs: list[str] | None = None,
        error: str | None = None,
    ) -> Path:
        manifest = self._read(run_id)
        stage: dict[str, Any] = {
            "name": name,
            "status": status,
            "elapsed_ms": round(float(elapsed_ms), 2),
            "outputs": outputs or [],
            "finished_at": utils.utc_now_iso(),
        }
        if error:
            stage["error"] = error
        stages = [
            item
            for item in manifest.setdefault("stages", [])
            if item.get("name") != name
        ]
        stages.append(stage)
        manifest["stages"] = stages
        manifest["updated_at"] = utils.utc_now_iso()
        return utils.write_json(self.manifest_path(run_id), manifest)

    def finalize(self, run_id: str, *, status: str, summary: Mapping[str, Any]) -> Path:
        manifest = self._read(run_id)
        manifest["status"] = status
        manifest["summary"] = dict(summary)
        manifest["updated_at"] = utils.utc_now_iso()
        return utils.write_json(self.manifest_path(run_id), manifest)
