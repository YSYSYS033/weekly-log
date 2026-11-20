"""API 的测试：/health 正常返回，未知路径返回 404。"""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

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
