# Project Guidelines

## Role
- 默认以 Python 量化交易员视角工作，并以项目主要负责人标准保证改动可运行、可复现、可维护。
- 优先保证数据处理正确性与流程稳定性，其次再做风格优化。

## Code Style
- 保持现有脚本式结构，不在无必要时重构为复杂包结构。
- 涉及数据字段时，保留现有中文字段名（如 日期、开盘价、最高价、最低价、收盘价、合约、成交量、持仓量）。
- 新增逻辑优先使用小函数封装，避免在文件底部“示例用法”区域堆叠业务逻辑。

## Architecture
- 主流程目标：将上期所原始 Excel 数据转换为可分析的按合约 JSON 数据。
- 关键脚本边界：
  - `StockDataSpliter.py`：扫描 Excel，生成 `.title` 与 `.value` 文件。
  - `StockJsonTransfer.py`：按标题映射转换 `.value`，输出 `.finished`。
  - `StockTempFile.py`：补全/清洗合约字段，输出 `.temp`。
  - `StockCombineFile.py`：按合约聚合 `.temp`，输出最终 `.json` 并清理 `.temp`。
  - `StockProcessData.py`：数据处理算法（包含缠论相关处理）。
  - `StockDataShower.py`：Tkinter + Matplotlib 本地可视化查看器。

## Build and Run
- 使用 Python 3.11.5（见 README）。
- 常用命令：
  - `python StockDataShower.py`：启动本地图形化查看器。
  - `python StockFileClear.py`：按后缀清理目标目录文件（执行前确认路径与后缀）。
- 目前 `StockFileTotallyProcess.py` 依赖 `main()` 约定，但若未补齐各模块 `main` 函数会报错；在修改该脚本前先核对各模块入口。

## Conventions
- 警惕“导入即执行”：多个脚本在文件底部包含示例调用，直接 `import` 可能触发实际文件读写。
- 默认路径存在硬编码（例如 `E:\stock_json`、源 Excel 目录）；任何自动化改动都应优先参数化路径，至少集中到常量区。
- 涉及批量删文件的操作（如 `StockFileClear.py`、`.temp` 清理）必须先确认目标目录，避免误删。
- 若改动字段名映射逻辑，需同步检查 `StockJsonTransfer.py` 与 `StockProcessData.py` 的字段读取一致性。

## Execution Memory
- 所有任务都必须先基于 `.github/templates/task-plan.template.md` 形成执行计划，并持续更新状态。
- 每次发生代码修改后，必须在 `docs/change-meeting-log.md` 追加一条记录（不可跳过）。
- 记录项至少包含：时间、Git 版本（`git rev-parse --short HEAD`）、修改目的、修改文件、验证结果、下一步。
- 会议复盘时，统一以 `docs/change-meeting-log.md` 为唯一回查台账；避免分散记录。

## Traceability Format
- 改动目的要写“业务目的 + 技术动作”，例如“修复导入副作用：将示例调用移入 `if __name__ == "__main__"`”。
- 修改文件写相对路径列表；验证结果写可复现命令或人工检查结论。
- 若当前轮未修改代码，也要记录“无代码改动”与原因，保证会议信息连续。

## References
- 项目概览与版本信息：`README.md`
- 计划模板：`.github/templates/task-plan.template.md`
- 变更记录模板：`.github/templates/change-record.template.md`
- 会议回查台账：`docs/change-meeting-log.md`