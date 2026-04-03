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

## References
- 项目概览与版本信息：`README.md`