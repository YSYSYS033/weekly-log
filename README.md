# weekly-log

> 一个命令行小工具：记录每天学了什么、花了多久，按周汇总。
> W1 练手项目，用来把「工程化 + Git + 测试 + 打包」这套动作跑一遍。

## 安装

```powershell
cd D:\deepseek\agent-portfolio\weekly-log
uv sync
```

## 用法

```powershell
uv run weekly-log --help
uv run weekly-log add "学 FastAPI 路由" -m 60
uv run weekly-log list
uv run weekly-log list --week
```

> 目前 `add` / `list` 只有命令行骨架，真正读写 JSON 在 W1-D2 实现。

## 开发

```powershell
uv run pytest          # 跑测试
uv run ruff check .    # 代码检查
uv run ruff format .   # 自动格式化
```

## 目录结构

```
weekly-log/
├─ src/weekly_log/     # 包代码
│  ├─ __init__.py
│  └─ cli.py           # 命令行入口（argparse）
├─ tests/              # 测试
├─ pyproject.toml      # 项目配置 + 依赖
└─ uv.lock             # 依赖锁定文件（要提交）
```

## W1 路线图

- [x] D1：项目骨架、依赖、命令行骨架、`--help` 可跑
- [ ] D2：`Entry` 数据模型 + JSON 持久化 + `add` / `list`
- [ ] D3：`update` / `delete` / `search` + 参数校验 + 6 个测试
- [ ] D4：分支 + 3 个 PR
- [ ] D5：FastAPI `/health`
- [ ] D6：重构 + 8 个测试 + README
- [ ] D7：周复盘 + 讲解录屏
