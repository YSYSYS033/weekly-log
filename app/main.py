"""FastAPI 应用入口。

W1-D5 只做一件事：提供 /health 健康检查。
后面 W5～W6 会在这里加鉴权、会话、流式对话。
"""

from fastapi import FastAPI

app = FastAPI(title="weekly-log API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    """健康检查：服务活着就返回 ok。

    部署平台（Docker、云服务器、负载均衡）会定时请求这个地址判断服务是否正常。
    """
    return {"status": "ok"}
