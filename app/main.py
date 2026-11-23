"""FastAPI 应用入口。

W1-D5 做了 /health；W1-D6 把 CLI 的记录通过 /entries 暴露成 HTTP 接口，
让命令行和 Web 共用同一份数据。
"""

from fastapi import FastAPI
from pydantic import BaseModel

from weekly_log import storage

app = FastAPI(title="weekly-log API", version="0.2.0")


class EntryOut(BaseModel):
    """API 返回的一条记录。

    Pydantic 负责两件事：校验字段类型、把对象序列化成 JSON。
    """

    id: int
    title: str
    minutes: int
    date: str


@app.get("/health")
def health() -> dict[str, str]:
    """健康检查：服务活着就返回 ok。

    部署平台（Docker、云服务器、负载均衡）会定时请求这个地址判断服务是否正常。
    """
    return {"status": "ok"}


@app.get("/entries", response_model=list[EntryOut])
def list_entries(limit: int = 0) -> list[EntryOut]:
    """返回所有记录；带 ?limit=N 时只返回最近 N 条。"""
    entries = storage.load()
    if limit > 0:
        entries = entries[-limit:]
    return [EntryOut(**entry.to_dict()) for entry in entries]
