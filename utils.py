"""全局通用工具模块（项目唯一基础设施入口）。

本模块只依赖 Python 标准库，``PyYAML`` 仅在调用 YAML 读写函数时惰性导入。
因此它可以被任意业务层、脚本或测试直接复用，而不会引入循环依赖。

覆盖能力：
    1. 路径与文件名处理；
    2. 文本 / JSON / JSONL / YAML / CSV 的原子读写；
    3. 日志初始化（控制台 + 滚动文件）；
    4. 哈希、分块、深层次配置读取等小型通用函数。

设计原则：
    - 任何写操作先写临时文件，再通过 ``os.replace`` 原子替换；
    - 所有路径默认相对当前工作目录解析，调用方可传入绝对路径；
    - 日志 API 幂等，重复调用 ``setup_logging`` 不会重复挂载 handler。
"""

from __future__ import annotations

import csv
import hashlib
import json
import logging
import os
import re
import tempfile
import time
from collections.abc import Iterable, Iterator, Mapping, Sequence
from contextlib import contextmanager
from datetime import UTC, datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

__all__ = [
    "APP_LOGGER_NAME",
    "DEFAULT_ENCODING",
    "FileIOError",
    "UtilError",
    "atomic_write_text",
    "chunked",
    "deep_get",
    "deep_merge",
    "ensure_dir",
    "file_sha256",
    "get_logger",
    "human_size",
    "load_any",
    "read_csv",
    "read_json",
    "read_jsonl",
    "read_text",
    "read_yaml",
    "safe_filename",
    "save_any",
    "setup_logging",
    "timer",
    "timestamp",
    "utc_now",
    "utc_now_iso",
    "write_csv",
    "write_json",
    "write_jsonl",
    "write_text",
    "write_yaml",
]

DEFAULT_ENCODING = "utf-8"
APP_LOGGER_NAME = "outdoor_ess_ai"
_MISSING = object()
_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
_CONFIGURED = False


class UtilError(RuntimeError):
    """通用工具异常基类。"""


class FileIOError(UtilError):
    """文件读取、解析或写入失败。"""


# ---------------------------------------------------------------------------
# 路径与时间
# ---------------------------------------------------------------------------
def ensure_dir(path: str | os.PathLike[str]) -> Path:
    """确保目录存在并返回其绝对 ``Path``。"""

    target = Path(path).expanduser().resolve()
    try:
        target.mkdir(parents=True, exist_ok=True)
    except OSError as exc:  # pragma: no cover - 依赖操作系统错误
        raise FileIOError(f"无法创建目录: {target}") from exc
    return target


def safe_filename(name: str, *, default: str = "untitled", max_length: int = 120) -> str:
    """把任意字符串转为安全的跨平台文件名（不含路径分隔符）。"""

    cleaned = re.sub(r"[^\w.\-]+", "_", str(name), flags=re.UNICODE).strip(" ._-")
    cleaned = re.sub(r"_{2,}", "_", cleaned)
    if not cleaned:
        cleaned = default
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length].rstrip(" ._-")
    return cleaned or default


def utc_now() -> datetime:
    """返回带 UTC 时区的当前时间。"""

    return datetime.now(UTC)


def timestamp(fmt: str = "%Y%m%d_%H%M%S", *, dt: datetime | None = None) -> str:
    """返回 UTC 时间戳字符串，默认适合拼接到文件名。"""

    return (dt or utc_now()).strftime(fmt)


def utc_now_iso() -> str:
    """返回 ISO-8601 UTC 时间字符串（秒级）。"""

    return utc_now().replace(microsecond=0).isoformat()


@contextmanager
def timer() -> Iterator[dict[str, float]]:
    """计时上下文，用法：``with timer() as t: ...; t['elapsed_ms']``。"""

    result: dict[str, float] = {}
    started = time.perf_counter()
    try:
        yield result
    finally:
        result["elapsed_ms"] = round((time.perf_counter() - started) * 1000, 2)


# ---------------------------------------------------------------------------
# 文本读写
# ---------------------------------------------------------------------------
def atomic_write_text(
    path: str | os.PathLike[str],
    content: str,
    *,
    encoding: str = DEFAULT_ENCODING,
) -> Path:
    """原子写入文本：写同目录临时文件后 ``os.replace``，避免半截文件。"""

    target = Path(path).expanduser().resolve()
    ensure_dir(target.parent)
    tmp_name: str | None = None
    try:
        fd, tmp_name = tempfile.mkstemp(
            prefix=f".{target.name}.", suffix=".tmp", dir=str(target.parent)
        )
        with os.fdopen(fd, "w", encoding=encoding, newline="") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, target)
        tmp_name = None
        return target
    except (OSError, UnicodeError) as exc:
        raise FileIOError(f"原子写入失败: {target}") from exc
    finally:
        if tmp_name and Path(tmp_name).exists():
            try:
                Path(tmp_name).unlink()
            except OSError:  # pragma: no cover - 清理失败不覆盖原异常
                pass


def write_text(
    path: str | os.PathLike[str],
    content: str,
    *,
    encoding: str = DEFAULT_ENCODING,
    append: bool = False,
) -> Path:
    """写入文本；``append=True`` 时追加，否则原子覆盖。"""

    if append:
        target = Path(path).expanduser().resolve()
        ensure_dir(target.parent)
        try:
            with target.open("a", encoding=encoding, newline="") as handle:
                handle.write(content)
        except (OSError, UnicodeError) as exc:
            raise FileIOError(f"追加文本失败: {target}") from exc
        return target
    return atomic_write_text(path, content, encoding=encoding)


def read_text(
    path: str | os.PathLike[str],
    *,
    encoding: str = DEFAULT_ENCODING,
    default: Any = _MISSING,
) -> str:
    """读取文本；文件不存在且提供 ``default`` 时返回默认值。"""

    target = Path(path).expanduser().resolve()
    try:
        return target.read_text(encoding=encoding)
    except FileNotFoundError as exc:
        if default is not _MISSING:
            return default
        raise FileIOError(f"文件不存在: {target}") from exc
    except (OSError, UnicodeError) as exc:
        raise FileIOError(f"读取文本失败: {target}") from exc


# ---------------------------------------------------------------------------
# JSON / JSONL / YAML / CSV
# ---------------------------------------------------------------------------
def write_json(
    path: str | os.PathLike[str],
    data: Any,
    *,
    indent: int = 2,
    ensure_ascii: bool = False,
) -> Path:
    """将对象序列化为 JSON 并原子写入。"""

    try:
        payload = json.dumps(data, ensure_ascii=ensure_ascii, indent=indent, default=str)
    except (TypeError, ValueError) as exc:
        raise FileIOError(f"JSON 序列化失败: {path}") from exc
    return atomic_write_text(path, payload + "\n")


def read_json(path: str | os.PathLike[str], default: Any = _MISSING) -> Any:
    """读取 JSON；解析失败抛出 ``FileIOError``，缺失时按需返回默认值。"""

    target = Path(path).expanduser().resolve()
    if not target.exists() and default is not _MISSING:
        return default
    try:
        return json.loads(target.read_text(encoding=DEFAULT_ENCODING))
    except FileNotFoundError as exc:
        raise FileIOError(f"JSON 文件不存在: {target}") from exc
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise FileIOError(f"读取或解析 JSON 失败: {target}") from exc


def write_jsonl(path: str | os.PathLike[str], rows: Iterable[Mapping[str, Any]]) -> Path:
    """将可迭代映射写成 JSON Lines（UTF-8，一行一个对象）。"""

    lines: list[str] = []
    for index, row in enumerate(rows, start=1):
        try:
            lines.append(json.dumps(dict(row), ensure_ascii=False, default=str))
        except (TypeError, ValueError) as exc:
            raise FileIOError(f"JSONL 第 {index} 行序列化失败: {path}") from exc
    return atomic_write_text(path, "\n".join(lines) + ("\n" if lines else ""))


def read_jsonl(path: str | os.PathLike[str], default: Any = _MISSING) -> list[dict[str, Any]]:
    """读取 JSON Lines，忽略空行；任一行损坏即报错并给出行号。"""

    target = Path(path).expanduser().resolve()
    if not target.exists() and default is not _MISSING:
        return default
    rows: list[dict[str, Any]] = []
    line_no = 0
    try:
        with target.open("r", encoding=DEFAULT_ENCODING) as handle:
            for line in handle:
                line_no += 1
                line = line.strip()
                if not line:
                    continue
                value = json.loads(line)
                if not isinstance(value, dict):
                    raise ValueError("每行必须是 JSON 对象")
                rows.append(value)
        return rows
    except FileNotFoundError as exc:
        raise FileIOError(f"JSONL 文件不存在: {target}") from exc
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        raise FileIOError(f"读取 JSONL 失败（约第 {line_no} 行）: {target}") from exc


def _import_yaml():
    try:
        import yaml  # type: ignore[import-not-found]
    except ImportError as exc:  # pragma: no cover - 依赖缺失路径
        raise UtilError("需要 PyYAML：pip install PyYAML") from exc
    return yaml


def write_yaml(path: str | os.PathLike[str], data: Any) -> Path:
    """将对象安全序列化为 YAML 并原子写入。"""

    yaml = _import_yaml()
    try:
        payload = yaml.safe_dump(
            data,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
        )
    except (TypeError, ValueError) as exc:
        raise FileIOError(f"YAML 序列化失败: {path}") from exc
    return atomic_write_text(path, payload)


def read_yaml(path: str | os.PathLike[str], default: Any = _MISSING) -> Any:
    """读取 YAML；空文件返回 ``{}`` 或调用方提供的默认值。"""

    target = Path(path).expanduser().resolve()
    if not target.exists() and default is not _MISSING:
        return default
    yaml = _import_yaml()
    try:
        content = target.read_text(encoding=DEFAULT_ENCODING)
        value = yaml.safe_load(content)
    except FileNotFoundError as exc:
        raise FileIOError(f"YAML 文件不存在: {target}") from exc
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise FileIOError(f"读取或解析 YAML 失败: {target}") from exc
    if value is None:
        return {} if default is _MISSING else default
    return value


def write_csv(
    path: str | os.PathLike[str],
    rows: Iterable[Mapping[str, Any]],
    *,
    fieldnames: Sequence[str] | None = None,
) -> Path:
    """写入 CSV；未提供表头时使用首行键名，空数据仅创建空文件。"""

    materialized = [dict(row) for row in rows]
    target = Path(path).expanduser().resolve()
    ensure_dir(target.parent)
    if fieldnames is None and materialized:
        fieldnames = list(materialized[0].keys())
    if fieldnames is None:
        return atomic_write_text(target, "")

    tmp_name: str | None = None
    try:
        fd, tmp_name = tempfile.mkstemp(
            prefix=f".{target.name}.", suffix=".tmp", dir=str(target.parent)
        )
        with os.fdopen(fd, "w", encoding=DEFAULT_ENCODING, newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
            writer.writeheader()
            writer.writerows(materialized)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, target)
        tmp_name = None
        return target
    except (OSError, UnicodeError, csv.Error) as exc:
        raise FileIOError(f"写入 CSV 失败: {target}") from exc
    finally:
        if tmp_name and Path(tmp_name).exists():
            try:
                Path(tmp_name).unlink()
            except OSError:  # pragma: no cover
                pass


def read_csv(path: str | os.PathLike[str], default: Any = _MISSING) -> list[dict[str, str]]:
    """读取 CSV 为字典列表；文件不存在时可按需返回默认值。"""

    target = Path(path).expanduser().resolve()
    if not target.exists() and default is not _MISSING:
        return default
    try:
        with target.open("r", encoding=DEFAULT_ENCODING, newline="") as handle:
            return [dict(row) for row in csv.DictReader(handle)]
    except FileNotFoundError as exc:
        raise FileIOError(f"CSV 文件不存在: {target}") from exc
    except (OSError, UnicodeError, csv.Error) as exc:
        raise FileIOError(f"读取 CSV 失败: {target}") from exc


def load_any(path: str | os.PathLike[str], default: Any = _MISSING) -> Any:
    """按扩展名自动读取 .json/.jsonl/.yaml/.yml/.csv，其余按文本读取。"""

    target = Path(path).expanduser().resolve()
    suffix = target.suffix.lower()
    if suffix == ".json":
        return read_json(target, default)
    if suffix == ".jsonl":
        return read_jsonl(target, default)
    if suffix in {".yaml", ".yml"}:
        return read_yaml(target, default)
    if suffix == ".csv":
        return read_csv(target, default)
    return read_text(target, default=default)


def save_any(path: str | os.PathLike[str], data: Any) -> Path:
    """按扩展名自动写入 .json/.jsonl/.yaml/.yml/.csv，其余按文本写入。"""

    target = Path(path)
    suffix = target.suffix.lower()
    if suffix == ".json":
        return write_json(target, data)
    if suffix == ".jsonl":
        return write_jsonl(target, data)
    if suffix in {".yaml", ".yml"}:
        return write_yaml(target, data)
    if suffix == ".csv":
        return write_csv(target, data)
    return write_text(target, str(data))


# ---------------------------------------------------------------------------
# 其他通用函数
# ---------------------------------------------------------------------------
def file_sha256(path: str | os.PathLike[str], *, chunk_size: int = 1024 * 1024) -> str:
    """计算文件 SHA-256，用于数据快照去重与可追溯。"""

    digest = hashlib.sha256()
    try:
        with Path(path).expanduser().open("rb") as handle:
            for block in iter(lambda: handle.read(chunk_size), b""):
                digest.update(block)
    except OSError as exc:
        raise FileIOError(f"计算文件哈希失败: {path}") from exc
    return digest.hexdigest()


def human_size(size: int) -> str:
    """把字节数转为易读字符串。"""

    value = float(size)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1024 or unit == "TB":
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{value:.1f} TB"


def deep_get(mapping: Mapping[str, Any] | Sequence[Any], dotted: str, default: Any = None) -> Any:
    """按 ``a.b.0.c`` 形式读取嵌套字典 / 列表，缺失时返回默认值。"""

    current: Any = mapping
    for part in str(dotted).split("."):
        if isinstance(current, Mapping) and part in current:
            current = current[part]
        elif isinstance(current, Sequence) and not isinstance(current, (str, bytes)):
            try:
                current = current[int(part)]
            except (ValueError, IndexError):
                return default
        else:
            return default
    return current


def deep_merge(base: Mapping[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    """递归合并字典，``override`` 优先，返回新字典（不修改入参）。"""

    merged: dict[str, Any] = dict(base)
    for key, value in override.items():
        current = merged.get(key)
        if isinstance(current, Mapping) and isinstance(value, Mapping):
            merged[key] = deep_merge(current, value)
        else:
            merged[key] = value
    return merged


def chunked(items: Iterable[Any], size: int) -> Iterator[list[Any]]:
    """把任意可迭代对象切分为固定大小的列表。"""

    if size <= 0:
        raise ValueError("size 必须为正整数")
    bucket: list[Any] = []
    for item in items:
        bucket.append(item)
        if len(bucket) >= size:
            yield bucket
            bucket = []
    if bucket:
        yield bucket


# ---------------------------------------------------------------------------
# 日志
# ---------------------------------------------------------------------------
def setup_logging(
    *,
    level: str | int = "INFO",
    log_file: str | os.PathLike[str] | None = None,
    console: bool = True,
    max_bytes: int = 5 * 1024 * 1024,
    backup_count: int = 5,
    force: bool = False,
) -> logging.Logger:
    """初始化应用日志（控制台 + 可选滚动文件），幂等。

    Args:
        level: 日志级别，字符串或 ``logging`` 常量。
        log_file: 日志文件路径；为 ``None`` 时只输出控制台。
        console: 是否输出到标准输出。
        max_bytes: 单文件上限，超过后滚动。
        backup_count: 保留的历史文件数量。
        force: 为 ``True`` 时关闭并重建 handler（测试常用）。
    """

    global _CONFIGURED
    logger = logging.getLogger(APP_LOGGER_NAME)

    if _CONFIGURED and not force:
        return logger

    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        try:
            handler.close()
        except Exception:  # pragma: no cover - 关闭失败不影响重建
            pass

    logger.setLevel(level if isinstance(level, int) else str(level).upper())
    logger.propagate = False
    formatter = logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT)

    if console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    if log_file is not None:
        target = ensure_dir(Path(log_file).expanduser().resolve().parent) / Path(log_file).name
        file_handler = RotatingFileHandler(
            target,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding=DEFAULT_ENCODING,
            delay=False,
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if not logger.handlers:  # 兜底：至少不让日志调用报错
        logger.addHandler(logging.NullHandler())

    _CONFIGURED = True
    return logger


def get_logger(name: str | None = None) -> logging.Logger:
    """获取应用命名空间下的 logger；调用前建议先执行 ``setup_logging``。"""

    if not name or name == APP_LOGGER_NAME:
        return logging.getLogger(APP_LOGGER_NAME)
    if name.startswith(f"{APP_LOGGER_NAME}."):
        return logging.getLogger(name)
    return logging.getLogger(f"{APP_LOGGER_NAME}.{name}")
