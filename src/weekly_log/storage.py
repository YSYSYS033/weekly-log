"""存储层：把记录存成 JSON 文件，再读回来。"""

from __future__ import annotations

import json
from pathlib import Path

from weekly_log.models import Entry

DEFAULT_PATH = Path.home() / ".weekly-log.json"


def save(entries: list[Entry], path: Path | None = None) -> Path:
    """把记录列表写入 JSON 文件，返回写入的路径。"""
    target = Path(path) if path is not None else DEFAULT_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    data = [entry.to_dict() for entry in entries]
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return target


def load(path: Path | None = None) -> list[Entry]:
    """从 JSON 文件读记录；文件不存在或为空时返回空列表。

    如果文件里是老数据（没有 id），会自动补上编号并回写文件。
    """
    target = Path(path) if path is not None else DEFAULT_PATH
    if not target.exists():
        return []
    text = target.read_text(encoding="utf-8").strip()
    if not text:
        return []

    entries = [Entry.from_dict(item) for item in json.loads(text)]
    if any(entry.id <= 0 for entry in entries):
        _assign_ids(entries)
        save(entries, target)
    return entries


def _assign_ids(entries: list[Entry]) -> None:
    """给没有编号的记录补上自增 id（用于兼容老数据）。"""
    next_id = max((entry.id for entry in entries if entry.id > 0), default=0) + 1
    for entry in entries:
        if entry.id <= 0:
            entry.id = next_id
            next_id += 1
