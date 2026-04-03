---
applyTo: "{StockDataSpliter.py,StockJsonTransfer.py,StockTempFile.py,StockCombineFile.py,StockFileTotallyProcess.py}"
description: "上期所数据流水线改动规范：字段、后缀、路径与可复现性"
---

# Data Pipeline Instructions

## 目标
- 任何改动都要保证从 Excel 到按合约 JSON 的主流程可执行、可复现。
- 优先保证数据正确性，再考虑风格优化。

## 输入输出约定
- `StockDataSpliter.py`：输入 Excel，输出 `.title` 与 `.value`。
- `StockJsonTransfer.py`：读取 `.title` 与 `.value`，输出 `.finished`。
- `StockTempFile.py`：读取 `.finished`，补全合约后输出 `.temp`。
- `StockCombineFile.py`：读取 `.temp`，按 `合约` 聚合输出 `.json`，并清理 `.temp`。

## 字段约定
- 保留中文字段名，不做英文化重命名。
- 涉及字段映射时，至少同步检查 `日期`、`开盘价`、`最高价`、`最低价`、`收盘价`、`合约`、`成交量`、`持仓量` 的读取链路。
- 若调整映射逻辑，必须同时核对 `StockJsonTransfer.py` 与 `StockProcessData.py` 的字段一致性。

## 安全与稳定性
- 避免导入即执行：新增逻辑应放入函数，示例调用放在 `if __name__ == "__main__":` 下。
- 尽量避免新增硬编码路径；优先参数化，至少集中在常量区。
- 涉及删除文件时，必须先确认目标目录与后缀，避免误删。

## 改动要求
- 保持脚本式结构，不无故重构为复杂包结构。
- 新增逻辑优先拆成小函数，并补充必要的异常处理与错误信息。
- 修改主流程入口时，先确认被调用模块是否提供对应入口函数。
