"""weekly-log 的命令行入口。

今天是 W1-D1：先把 argparse 的骨架和 --help 跑通。
真正的读写逻辑（Entry 模型 + JSON 持久化）在 W1-D2 补。
"""

from __future__ import annotations

import argparse
from collections.abc import Sequence


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
    """TODO(W1-D2): 写入 JSON 文件。"""
    print(f"[TODO] add: title={args.title!r} minutes={args.minutes} date={args.date}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    """TODO(W1-D2): 从 JSON 文件读取并打印。"""
    print(f"[TODO] list: week_only={args.week}")
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
