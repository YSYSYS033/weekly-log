"""storage.py 的测试：存进去、读回来、老数据自动补 id。"""

from __future__ import annotations

import json
from pathlib import Path

from weekly_log.models import Entry
from weekly_log.storage import load, save


def test_save_then_load_roundtrip(tmp_path: Path) -> None:
    """存两条记录再读回来，内容应该一模一样。"""
    data_file = tmp_path / "data.json"
    entries = [
        Entry("学 FastAPI", 60, "2026-11-16", 1),
        Entry("写测试", 30, "2026-11-17", 2),
    ]

    save(entries, data_file)
    loaded = load(data_file)

    assert loaded == entries


def test_load_missing_file_returns_empty(tmp_path: Path) -> None:
    """文件不存在时返回空列表，而不是报错。"""
    assert load(tmp_path / "nope.json") == []


def test_load_assigns_ids_to_legacy_records(tmp_path: Path) -> None:
    """没有 id 的老数据要自动补编号，并写回文件。"""
    data_file = tmp_path / "data.json"
    data_file.write_text(
        json.dumps([{"title": "老记录", "minutes": 10, "date": "2026-11-01"}]),
        encoding="utf-8",
    )

    entries = load(data_file)

    assert entries[0].id == 1
    saved = json.loads(data_file.read_text(encoding="utf-8"))
    assert saved[0]["id"] == 1
