"""weekly-log 的命令行入口。"""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from datetime import date

from weekly_log import storage
from weekly_log.models import Entry


def build_parser() -> argparse.ArgumentParser:
    """构造命令行解析器（单独拆出来，方便测试）。"""
    parser = argparse.ArgumentParser(
        prog="weekly-log",
        description="记录每天学了什么、花了多久。",
    )
    parser.add_argument("--version", action="version", version="weekly-log 0.1.0")

    sub = parser.add_subparsers(dest="command", metavar="<command>")

    p_add = sub.add_parser("add", help="新增一条记录")
    p_add.add_argument("title", help="今天做了什么（一句话）")
    p_add.add_argument("-m", "--minutes", type=int, default=0, help="花了多少分钟")
    p_add.add_argument("-d", "--date", default=None, help="日期，默认今天（YYYY-MM-DD）")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="列出记录")
    p_list.add_argument("--week", action="store_true", help="只看本周")
    p_list.set_defaults(func=cmd_list)

    return parser


def cmd_add(args: argparse.Namespace) -> int:
    """新增一条记录并立刻存盘。"""
    entry = Entry(title=args.title, minutes=args.minutes, date=args.date or "")
    entries = storage.load()
    entries.append(entry)
    path = storage.save(entries)
    print(f"已记录：{entry.date}  {entry.minutes} 分钟  {entry.title}")
    print(f"（保存在 {path}）")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    """列出记录，可选只看本周。"""
    entries = storage.load()
    if args.week:
        entries = [entry for entry in entries if _is_this_week(entry.date)]
    if not entries:
        print("还没有记录，先用 add 加一条吧")
        return 0
    for entry in entries:
        print(f"{entry.date}  {entry.minutes:>4} 分钟  {entry.title}")
    total = sum(entry.minutes for entry in entries)
    print(f"\n共 {len(entries)} 条，合计 {total} 分钟")
    return 0


def _is_this_week(day: str) -> bool:
    """判断某个日期是否落在本周（周一到周日）。"""
    try:
        parsed = date.fromisoformat(day)
    except ValueError:
        return False
    return parsed.isocalendar()[:2] == date.today().isocalendar()[:2]


def main(argv: Sequence[str] | None = None) -> int:
    """程序入口：解析参数并分发到子命令。"""
    parser = build_parser()
    args = parser.parse_args(argv)

    if not getattr(args, "command", None):
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
