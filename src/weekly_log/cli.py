"""weekly-log 的命令行入口。"""

from __future__ import annotations

import argparse
import sys
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
    parser.add_argument("--version", action="version", version="weekly-log 0.2.0")

    sub = parser.add_subparsers(dest="command", metavar="<command>")

    p_add = sub.add_parser("add", help="新增一条记录")
    p_add.add_argument("title", help="今天做了什么（一句话）")
    p_add.add_argument("-m", "--minutes", type=int, default=0, help="花了多少分钟")
    p_add.add_argument("-d", "--date", default=None, help="日期，默认今天（YYYY-MM-DD）")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="列出记录")
    p_list.add_argument("--week", action="store_true", help="只看本周")
    p_list.set_defaults(func=cmd_list)

    p_update = sub.add_parser("update", help="修改一条记录")
    p_update.add_argument("--id", type=int, required=True, help="记录编号（用 list 查看）")
    p_update.add_argument("-t", "--title", default=None, help="新标题")
    p_update.add_argument("-m", "--minutes", type=int, default=None, help="新的分钟数")
    p_update.add_argument("-d", "--date", default=None, help="新日期")
    p_update.set_defaults(func=cmd_update)

    p_delete = sub.add_parser("delete", help="删除一条记录")
    p_delete.add_argument("--id", type=int, required=True, help="记录编号（用 list 查看）")
    p_delete.set_defaults(func=cmd_delete)

    p_search = sub.add_parser("search", help="按关键词搜索记录")
    p_search.add_argument("keyword", help="关键词（不区分大小写）")
    p_search.set_defaults(func=cmd_search)

    p_stats = sub.add_parser("stats", help="统计概览")
    p_stats.set_defaults(func=cmd_stats)

    return parser


def _format(entry: Entry) -> str:
    """把一条记录格式化成一行文字。"""
    return f"#{entry.id:<3} {entry.date}  {entry.minutes:>4} 分钟  {entry.title}"


def _next_id(entries: list[Entry]) -> int:
    """算出下一个可用编号。"""
    return max((entry.id for entry in entries), default=0) + 1


def cmd_add(args: argparse.Namespace) -> int:
    """新增一条记录并立刻存盘。"""
    entries = storage.load()
    try:
        entry = Entry(
            title=args.title,
            minutes=args.minutes,
            date=args.date or "",
            id=_next_id(entries),
        )
    except ValueError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 1

    entries.append(entry)
    path = storage.save(entries)
    print(f"已记录：{_format(entry)}")
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
        print(_format(entry))
    total = sum(entry.minutes for entry in entries)
    print(f"\n共 {len(entries)} 条，合计 {total} 分钟")
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    """按编号修改一条记录。"""
    entries = storage.load()
    target = next((entry for entry in entries if entry.id == args.id), None)
    if target is None:
        print(f"错误：没有编号为 {args.id} 的记录", file=sys.stderr)
        return 1

    try:
        updated = Entry(
            title=args.title if args.title is not None else target.title,
            minutes=args.minutes if args.minutes is not None else target.minutes,
            date=args.date if args.date is not None else target.date,
            id=target.id,
        )
    except ValueError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 1

    entries[entries.index(target)] = updated
    storage.save(entries)
    print(f"已更新：{_format(updated)}")
    return 0


def cmd_delete(args: argparse.Namespace) -> int:
    """按编号删除一条记录。"""
    entries = storage.load()
    kept = [entry for entry in entries if entry.id != args.id]
    if len(kept) == len(entries):
        print(f"错误：没有编号为 {args.id} 的记录", file=sys.stderr)
        return 1

    storage.save(kept)
    print(f"已删除编号 {args.id}")
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    """按关键词搜索标题。"""
    entries = storage.load()
    keyword = args.keyword.casefold()
    hits = [entry for entry in entries if keyword in entry.title.casefold()]
    if not hits:
        print(f"没有找到包含「{args.keyword}」的记录")
        return 0

    for entry in hits:
        print(_format(entry))
    print(f"\n共找到 {len(hits)} 条，合计 {sum(entry.minutes for entry in hits)} 分钟")
    return 0


def _is_this_week(day: str) -> bool:
    """判断某个日期是否落在本周（周一到周日）。"""
    try:
        parsed = date.fromisoformat(day)
    except ValueError:
        return False
    return parsed.isocalendar()[:2] == date.today().isocalendar()[:2]


def cmd_stats(args: argparse.Namespace) -> int:
    """打印总量和本周的统计。"""
    entries = storage.load()
    this_week = [entry for entry in entries if _is_this_week(entry.date)]
    total_minutes = sum(entry.minutes for entry in entries)
    week_minutes = sum(entry.minutes for entry in this_week)

    print(f"总记录：{len(entries)} 条，合计 {total_minutes} 分钟")
    print(f"本周：  {len(this_week)} 条，合计 {week_minutes} 分钟")
    return 0


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
