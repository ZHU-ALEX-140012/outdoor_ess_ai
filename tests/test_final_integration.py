"""最终整合：全局异常捕获、Streamlit 启动与入口文件测试。"""

from __future__ import annotations

from pathlib import Path

import pytest

import error_guard

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_error_guard_writes_human_and_jsonl(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(error_guard, "LOG_DIR", tmp_path)
    monkeypatch.setattr(error_guard, "HUMAN_LOG", tmp_path / "errors.log")
    monkeypatch.setattr(error_guard, "JSONL_LOG", tmp_path / "errors.jsonl")
    error_guard.log_exception(RuntimeError("demo failure"), app="test", context={"step": "unit"})
    assert "demo failure" in (tmp_path / "errors.log").read_text(encoding="utf-8")
    assert '"app": "test"' in (tmp_path / "errors.jsonl").read_text(encoding="utf-8")


def test_run_cli_catches_unhandled(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(error_guard, "LOG_DIR", tmp_path)
    monkeypatch.setattr(error_guard, "HUMAN_LOG", tmp_path / "errors.log")
    monkeypatch.setattr(error_guard, "JSONL_LOG", tmp_path / "errors.jsonl")

    def broken(_argv):
        raise RuntimeError("boom")

    assert error_guard.run_cli(broken, "broken_entry") == 1
    output = capsys.readouterr().err
    assert "未捕获异常" in output
    assert "boom" in (tmp_path / "errors.log").read_text(encoding="utf-8")


def test_streamlit_app_boots_without_exception() -> None:
    pytest.importorskip("streamlit")
    from streamlit.testing.v1 import AppTest

    app = AppTest.from_file(str(PROJECT_ROOT / "app.py"), default_timeout=90)
    app.run()
    assert not app.exception
    nav = next(radio for radio in app.radio if "总览" in radio.options)
    assert nav.options == ["总览", "选品研究", "上架素材", "竞品监控", "合规校验", "经营报表", "面试演示"]
    assert "运行全链路" in [button.label for button in app.button]

    expected = {
        "选品研究": "运行选品",
        "上架素材": "生成 Listing",
        "竞品监控": "巡检竞品",
        "合规校验": "合规筛查",
        "经营报表": "生成报表",
        "面试演示": "生成演示脚本",
    }
    for page, action in expected.items():
        nav = next(radio for radio in app.radio if "总览" in radio.options)
        nav.set_value(page).run()
        assert not app.exception
        assert action in [button.label for button in app.button]
        if page == "经营报表":
            assert len(app.tabs) == 3
