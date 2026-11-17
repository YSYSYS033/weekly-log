"""数据模型：一条学习记录。"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date


@dataclass
class Entry:
    """一条记录：某天做了什么、花了多久。"""

    title: str
    minutes: int = 0
    date: str = ""
    id: int = 0

    def __post_init__(self) -> None:
        """创建对象后自动执行的校验。"""
        if not self.title.strip():
            raise ValueError("标题不能为空")
        if self.minutes < 0:
            raise ValueError("分钟数不能是负数")
        if not self.date:
            self.date = date.today().isoformat()

    def to_dict(self) -> dict:
        """转成字典，方便存成 JSON。"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> Entry:
        """从字典还原成 Entry（老数据没有 id 字段时默认为 0）。"""
        return cls(
            title=data["title"],
            minutes=int(data.get("minutes", 0)),
            date=data.get("date", ""),
            id=int(data.get("id", 0)),
        )
