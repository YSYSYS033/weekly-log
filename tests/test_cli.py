"""cli.py 的测试：命令行骨架 + add/list/update/delete/search。"""

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
    for command in ("add", "list", "update", "delete", "search"):
        assert command in out


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


def test_add_rejects_empty_title(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """空标题应该被拒绝，并且返回非 0 退出码。"""
    monkeypatch.setattr(storage, "DEFAULT_PATH", tmp_path / "data.json")

    assert main(["add", "   "]) == 1
    assert "标题不能为空" in capsys.readouterr().err


def test_update_changes_minutes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """update 能按编号改掉分钟数。"""
    monkeypatch.setattr(storage, "DEFAULT_PATH", tmp_path / "data.json")
    assert main(["add", "学 FastAPI", "-m", "30"]) == 0
    capsys.readouterr()

    assert main(["update", "--id", "1", "-m", "90"]) == 0
    out = capsys.readouterr().out
    assert "90 分钟" in out


def test_update_unknown_id_returns_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """改一个不存在的编号要报错。"""
    monkeypatch.setattr(storage, "DEFAULT_PATH", tmp_path / "data.json")

    assert main(["update", "--id", "99", "-m", "10"]) == 1
    assert "没有编号为 99" in capsys.readouterr().err


def test_delete_removes_entry(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """delete 之后 list 里就不该有这条了。"""
    monkeypatch.setattr(storage, "DEFAULT_PATH", tmp_path / "data.json")
    assert main(["add", "要删的", "-m", "10"]) == 0
    assert main(["add", "要留的", "-m", "20"]) == 0
    capsys.readouterr()

    assert main(["delete", "--id", "1"]) == 0
    capsys.readouterr()

    assert main(["list"]) == 0
    out = capsys.readouterr().out
    assert "要删的" not in out
    assert "要留的" in out


def test_delete_unknown_id_returns_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """删一个不存在的编号要报错。"""
    monkeypatch.setattr(storage, "DEFAULT_PATH", tmp_path / "data.json")

    assert main(["delete", "--id", "99"]) == 1
    assert "没有编号为 99" in capsys.readouterr().err


def test_search_finds_keyword(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """search 只返回标题里包含关键词的记录。"""
    monkeypatch.setattr(storage, "DEFAULT_PATH", tmp_path / "data.json")
    assert main(["add", "学 FastAPI", "-m", "30"]) == 0
    assert main(["add", "写 pytest 测试", "-m", "20"]) == 0
    capsys.readouterr()

    assert main(["search", "fastapi"]) == 0
    out = capsys.readouterr().out
    assert "学 FastAPI" in out
    assert "写 pytest 测试" not in out
    assert "共找到 1 条" in out


def test_stats_shows_totals(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """stats 应该给出总条数、总分钟和本周数据。"""
    monkeypatch.setattr(storage, "DEFAULT_PATH", tmp_path / "data.json")
    assert main(["add", "学 FastAPI", "-m", "30"]) == 0
    assert main(["add", "写测试", "-m", "20"]) == 0
    capsys.readouterr()

    assert main(["stats"]) == 0
    out = capsys.readouterr().out
    assert "总记录：2 条" in out
    assert "合计 50 分钟" in out
    assert "本周" in out
