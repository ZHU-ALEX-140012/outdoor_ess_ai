"""配置加载与路径解析。

优先级：环境变量 > ``.env`` > ``config/settings.yaml`` > 代码内置默认值。
业务代码只依赖本模块暴露的 ``Settings``，不要自行读取 YAML。
"""

from __future__ import annotations

import copy
import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import utils

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "settings.yaml"

_REQUIRED_KEYS = (
    "project.name",
    "project.mode",
    "paths.outputs_dir",
    "paths.logs_dir",
    "llm.model",
    "business.markets",
)


class ConfigError(ValueError):
    """配置缺失、格式错误或取值非法。"""


@dataclass(frozen=True)
class Settings:
    """只读配置对象，提供点号取值和基于项目根目录的路径解析。"""

    root: Path
    data: dict[str, Any]
    config_path: Path

    def get(self, dotted: str, default: Any = None) -> Any:
        """读取配置项，例如 ``settings.get("llm.model")``。"""

        return utils.deep_get(self.data, dotted, default)

    def section(self, name: str) -> dict[str, Any]:
        """读取一个配置段，缺失时返回空字典。"""

        value = self.get(name, {})
        return dict(value) if isinstance(value, Mapping) else {}

    def path(self, dotted: str, default: str | None = None) -> Path:
        """读取路径配置并解析为绝对路径。"""

        raw = self.get(dotted, default)
        if not raw:
            raise ConfigError(f"缺少路径配置: {dotted}")
        candidate = Path(str(raw)).expanduser()
        return candidate if candidate.is_absolute() else (self.root / candidate).resolve()

    @property
    def project_name(self) -> str:
        return str(self.get("project.name", "outdoor-ess-ai"))

    @property
    def mode(self) -> str:
        return str(self.get("project.mode", "offline")).lower()

    @property
    def is_offline(self) -> bool:
        return self.mode != "live"

    @property
    def markets(self) -> list[str]:
        value = self.get("business.markets", [])
        return [str(item).upper() for item in value] if isinstance(value, list) else []

    def ensure_directories(self) -> list[Path]:
        """创建所有以 ``_dir`` 结尾的路径配置，返回去重后的目录列表。"""

        paths_section = self.section("paths")
        created: list[Path] = []
        seen: set[Path] = set()
        for key in paths_section:
            if not key.endswith("_dir"):
                continue
            target = self.path(f"paths.{key}")
            if target not in seen:
                utils.ensure_dir(target)
                seen.add(target)
                created.append(target)
        return created

    def with_root(self, new_root: str | Path) -> Settings:
        """复制配置并切换根目录，主要用于测试隔离。"""

        return Settings(root=Path(new_root).resolve(), data=copy.deepcopy(self.data), config_path=self.config_path)

    def as_dict(self) -> dict[str, Any]:
        return copy.deepcopy(self.data)


def _load_dotenv(root: Path) -> None:
    """加载 ``.env``（不覆盖已存在的环境变量）。"""

    env_file = root / ".env"
    if not env_file.exists():
        return
    try:
        from dotenv import load_dotenv  # type: ignore[import-not-found]

        load_dotenv(env_file, override=False)
        return
    except ImportError:
        pass

    # 没有 python-dotenv 时的最小回退实现
    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        if key:
            os.environ.setdefault(key, value)


def _apply_env_overrides(data: dict[str, Any]) -> None:
    overrides = {
        "ESS_AI_MODE": "project.mode",
        "ESS_AI_LOG_LEVEL": "logging.level",
        "ESS_AI_MODEL": "llm.model",
        "ESS_AI_BASE_URL": "llm.base_url",
        "ESS_AI_OUTPUT_DIR": "paths.outputs_dir",
    }
    for env_name, dotted in overrides.items():
        value = os.getenv(env_name)
        if not value:
            continue
        parts = dotted.split(".")
        cursor = data
        for part in parts[:-1]:
            node = cursor.get(part)
            if not isinstance(node, dict):
                node = {}
                cursor[part] = node
            cursor = node
        cursor[parts[-1]] = value


def _validate(data: Mapping[str, Any]) -> None:
    for key in _REQUIRED_KEYS:
        if utils.deep_get(data, key) in (None, "", []):
            raise ConfigError(f"缺少必填配置: {key}")

    mode = str(utils.deep_get(data, "project.mode", "")).lower()
    if mode not in {"offline", "live"}:
        raise ConfigError("project.mode 只能是 offline 或 live")

    markets = utils.deep_get(data, "business.markets", [])
    if not isinstance(markets, list) or not markets:
        raise ConfigError("business.markets 必须是非空列表")
    allowed = set(str(x).upper() for x in utils.deep_get(data, "business.supported_markets", []))
    if allowed:
        unknown = [m for m in markets if str(m).upper() not in allowed]
        if unknown:
            raise ConfigError(f"存在未支持的市场代码: {unknown}")


def load_settings(
    config_path: str | Path | None = None,
    *,
    root: str | Path | None = None,
) -> Settings:
    """加载并校验配置，返回不可变 ``Settings``。"""

    project_root = Path(root).expanduser().resolve() if root else PROJECT_ROOT
    path = Path(config_path).expanduser() if config_path else project_root / "config" / "settings.yaml"
    if not path.is_absolute():
        path = (project_root / path).resolve()

    _load_dotenv(project_root)
    raw = utils.read_yaml(path)
    if not isinstance(raw, dict):
        raise ConfigError(f"配置文件根节点必须是映射: {path}")

    data = copy.deepcopy(raw)
    _apply_env_overrides(data)
    _validate(data)
    return Settings(root=project_root, data=data, config_path=path)
