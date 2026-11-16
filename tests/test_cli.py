"""cli.py 的测试：命令行骨架 + add/list 真读写。"""

from __future__ import annotations

from pathlib import Path

import pytest

from weekly_log import storage
from weekly_log.cli import build_parser, main


def test_help_exits_zero(capsys: pytest.CaptureFixture[str]) -> None:
    """--help 应该正常退出（退出码 0），并列出子命令。"""
    with pytest.raises(SystemExit) as exc:
        main(["--help"])

    assert exc.value.code == 0
    out = capsys.readouterr().out
    assert "weekly-log" in out
    assert "add" in out
    assert "list" in out


def test_no_args_prints_help(capsys: pytest.CaptureFixture[str]) -> None:
    """不传参数时打印帮助并返回 0，而不是报错。"""
    assert main([]) == 0
    assert "usage" in capsys.readouterr().out.lower()


def test_add_parses_arguments() -> None:
    """add 子命令能正确解析标题和分钟数。"""
    args = build_parser().parse_args(["add", "学 FastAPI", "-m", "60"])

    assert args.command == "add"
    assert args.title == "学 FastAPI"
    assert args.minutes == 60
    assert args.date is None


def test_list_parses_week_flag() -> None:
    """list 子命令的 --week 开关能被识别。"""
    args = build_parser().parse_args(["list", "--week"])

    assert args.command == "list"
    assert args.week is True


def test_add_then_list(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """连着 add 两条，list 应该能看到这两条。"""
    monkeypatch.setattr(storage, "DEFAULT_PATH", tmp_path / "data.json")

    assert main(["add", "学 FastAPI", "-m", "30"]) == 0
    assert main(["add", "写测试", "-m", "15"]) == 0
    capsys.readouterr()  # 清掉 add 的输出

    assert main(["list"]) == 0
    out = capsys.readouterr().out
    assert "学 FastAPI" in out
    assert "写测试" in out
    assert "共 2 条" in out
