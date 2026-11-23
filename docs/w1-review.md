# W1 周复盘（2026-11-16 ～ 11-22）

> 本周目标：把「工程化 + Git + 测试 + 打包 + Web 服务」这套动作完整跑一遍。
> 实际从 11-13 就开始装环境，属于提前起跑。

## 一、本周交付

| 项目 | 成果 |
|---|---|
| CLI 工具 `weekly-log` | 6 个命令：`add` / `list` / `update` / `delete` / `search` / `stats` |
| HTTP 接口 | `GET /health`、`GET /entries`、`GET /docs`（Swagger） |
| 数据存储 | JSON 文件（`~/.weekly-log.json`），老数据自动补 id |
| 测试 | **22 个**，全部通过 |
| 代码检查 | `ruff check` 0 error，`ruff format` 全部符合 |
| Pull Request | **4 个**已合并（#1 stats、#2 list --json、#3 list --limit、#4 health） |
| 提交数 | 22+ |

## 二、每天做了什么

| 天 | 内容 |
|---|---|
| D0（11-13～11-15） | 装环境：Python 3.12、uv、Git、Docker；PATH 修复；项目骨架 |
| D1（11-16） | `uv init`、pytest/ruff、`.gitignore`、`cli.py` 骨架、首次提交 |
| D2（11-16） | `Entry` 模型 + JSON 存储 + `add`/`list` 真正可用 |
| D3（11-17） | `update`/`delete`/`search` + id 机制 + 老数据迁移 |
| D4（11-17） | Git 工作流：3 个分支、3 个 PR、合并后删分支 |
| D5（11-20） | FastAPI + `/health` + `/docs` + 状态码 |
| D6（11-23） | `/entries` 接口（Pydantic 模型）+ 本周复盘 |

## 三、踩过的坑（都已解决）

| 问题 | 原因 | 解决 |
|---|---|---|
| `python` 报"找不到文件" | 系统 PATH 里有旧账户的坏记录排前面 | 管理员改系统 PATH，把 `D:\python` 提到最前 |
| Git 整个消失 | 误点了安装目录里的 `unins000.exe`（卸载程序） | 重装便携版到 `D:\app\git`，PATH 加 `ucrt64\bin` |
| 弹 `Credential Helper Selector` | 便携版默认 `helper-selector`，且 GCM 不在 PATH | 系统 gitconfig 改成 `helper = manager` |
| `uv` 报 `Invalid statement (line 1, column 1)` | PowerShell 的 `Set-Content -Encoding UTF8` 给 pyproject 加了 BOM | 去掉 BOM；以后用 VS Code 改配置文件 |
| `ModuleNotFoundError: No module named 'app'` | pytest 不自动把项目根目录加进 import 路径 | `pyproject.toml` 加 `pythonpath = ["."]` |
| `StarletteDeprecationWarning: install httpx2` | 新版 TestClient 不再用 httpx | 测试依赖换成 `httpx2` |
| Docker 占内存 | WSL2 默认最多占物理内存 50% | 停止 Docker、`.wslconfig` 限 4GB、取消开机自启 |

## 四、学到的核心概念

1. **分层**：models（数据长什么样）/ storage（怎么存）/ cli（怎么用）/ api（怎么对外暴露）
2. **序列化**：对象 → 字典 → JSON；反过来是反序列化
3. **数据迁移**：老数据没有 id 时自动补并回写，不能让用户手动改
4. **退出码**：0 成功、非 0 失败，脚本和 CI 靠它判断
5. **HTTP 状态码**：4xx 是客户端错、5xx 是服务端错；FastAPI 参数校验失败返回 **422**
6. **Git 工作流**：分支隔离 → 小提交 → PR 描述三要素（改了什么/为什么/怎么验证）→ 合并后删分支

## 五、自评

**做得好的：**
- 每天都有可运行的增量，没有一天是"只看不写"
- 每个功能都有测试，改动后能立刻知道有没有弄坏别的
- 提交信息规范（feat / test / docs / fix / build）

**需要改进的：**
- 环境折腾花了太多时间（Git 被误删、PATH、BOM），W2 要减少这类消耗
- 还没有录讲解视频（面试要用，补在 W2 周末）

## 六、下周（W2）计划

- **主题**：FastAPI + Pydantic + SQLite/PostgreSQL → 项目 `notes-api`
- **交付**：带增删改查、参数校验、数据库迁移、15 个测试的 REST API
- **重点**：Pydantic 模型、依赖注入、SQLAlchemy、Alembic 迁移、错误处理
