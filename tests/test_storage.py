"""storage.py 的测试：存进去、读回来、文件不存在时返回空。"""

from __future__ import annotations

from pathlib import Path

from weekly_log.models import Entry
from weekly_log.storage import load, save


def test_save_then_load_roundtrip(tmp_path: Path) -> None:
    """存两条记录再读回来，内容应该一模一样。"""
    data_file = tmp_path / "data.json"
    entries = [
        Entry("学 FastAPI", 60, "2026-11-16"),
        Entry("写测试", 30, "2026-11-17"),
    ]

    save(entries, data_file)
    loaded = load(data_file)

    assert loaded == entries


def test_load_missing_file_returns_empty(tmp_path: Path) -> None:
    """文件不存在时返回空列表，而不是报错。"""
    assert load(tmp_path / "nope.json") == []
