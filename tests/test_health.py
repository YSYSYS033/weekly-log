"""API 的测试：/health 正常返回，未知路径返回 404，/entries 返回记录。"""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from weekly_log import storage
from weekly_log.models import Entry

client = TestClient(app)


def test_health_returns_ok() -> None:
    """健康检查返回 200 和 {"status": "ok"}。"""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_unknown_path_returns_404() -> None:
    """不存在的路径返回 404，而不是 500。"""
    response = client.get("/nope")

    assert response.status_code == 404


def test_entries_returns_saved_records(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """/entries 应该返回存盘里的记录。"""
    monkeypatch.setattr(storage, "DEFAULT_PATH", tmp_path / "data.json")
    storage.save(
        [
            Entry("学 FastAPI", 30, "2026-11-16", 1),
            Entry("写测试", 20, "2026-11-17", 2),
        ]
    )

    response = client.get("/entries")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0] == {"id": 1, "title": "学 FastAPI", "minutes": 30, "date": "2026-11-16"}


def test_entries_limit_returns_latest(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """?limit=1 只返回最后一条。"""
    monkeypatch.setattr(storage, "DEFAULT_PATH", tmp_path / "data.json")
    storage.save(
        [
            Entry("第一条", 10, "2026-11-15", 1),
            Entry("最后一条", 20, "2026-11-16", 2),
        ]
    )

    response = client.get("/entries?limit=1")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "最后一条"


def test_entries_empty_when_no_data(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """没有数据时返回空列表，而不是报错。"""
    monkeypatch.setattr(storage, "DEFAULT_PATH", tmp_path / "nope.json")

    response = client.get("/entries")

    assert response.status_code == 200
    assert response.json() == []
