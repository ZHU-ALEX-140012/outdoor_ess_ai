"""公共工具模块测试。"""

from __future__ import annotations

import logging
from pathlib import Path

import pytest

import utils


def test_text_roundtrip_and_default(workspace_tmp: Path) -> None:
    target = workspace_tmp / "nested" / "note.txt"
    utils.write_text(target, "第一行\n第二行\n")
    assert utils.read_text(target) == "第一行\n第二行\n"
    assert utils.read_text(workspace_tmp / "missing.txt", default="fallback") == "fallback"
    with pytest.raises(utils.FileIOError):
        utils.read_text(workspace_tmp / "missing.txt")


def test_json_roundtrip_and_atomic(workspace_tmp: Path) -> None:
    target = workspace_tmp / "data.json"
    payload = {"name": "Nomad 600", "capacity": 600, "tags": ["露营", "solar"]}
    utils.write_json(target, payload)
    assert utils.read_json(target) == payload
    assert not list(workspace_tmp.glob("*.tmp"))


def test_jsonl_roundtrip(workspace_tmp: Path) -> None:
    target = workspace_tmp / "rows.jsonl"
    rows = [{"id": 1, "name": "A"}, {"id": 2, "name": "B"}]
    utils.write_jsonl(target, rows)
    assert utils.read_jsonl(target) == rows


def test_yaml_roundtrip(workspace_tmp: Path) -> None:
    target = workspace_tmp / "config.yaml"
    payload = {"project": {"name": "户外储能", "markets": ["US", "DE"]}}
    utils.write_yaml(target, payload)
    assert utils.read_yaml(target) == payload


def test_csv_roundtrip(workspace_tmp: Path) -> None:
    target = workspace_tmp / "rows.csv"
    rows = [{"market": "US", "price": 499}, {"market": "DE", "price": 541}]
    utils.write_csv(target, rows, fieldnames=["market", "price"])
    loaded = utils.read_csv(target)
    assert loaded[0]["market"] == "US"
    assert loaded[1]["price"] == "541"


def test_file_sha256_and_human_size(workspace_tmp: Path) -> None:
    target = workspace_tmp / "hash.txt"
    utils.write_text(target, "abc")
    assert len(utils.file_sha256(target)) == 64
    assert utils.human_size(2048) == "2.0 KB"


def test_deep_get_and_merge() -> None:
    data = {"a": {"b": [{"c": 3}]}}
    assert utils.deep_get(data, "a.b.0.c") == 3
    assert utils.deep_get(data, "a.missing", default=9) == 9
    merged = utils.deep_merge({"a": {"x": 1}, "keep": True}, {"a": {"y": 2}})
    assert merged == {"a": {"x": 1, "y": 2}, "keep": True}


def test_safe_filename() -> None:
    assert utils.safe_filename("US / Nomad: 600") == "US_Nomad_600"
    assert utils.safe_filename("   ") == "untitled"


def test_logging_writes_file(workspace_tmp: Path) -> None:
    log_file = workspace_tmp / "logs" / "app.log"
    utils.setup_logging(level="INFO", log_file=log_file, console=False, force=True)
    logger = utils.get_logger("test")
    logger.info("hello %s", "world")
    logging.getLogger(utils.APP_LOGGER_NAME).handlers[0].flush()
    content = log_file.read_text(encoding="utf-8")
    assert "hello world" in content
    assert "test" in content
    utils.setup_logging(level="WARNING", log_file=None, console=False, force=True)
