---
name: shfe-data-normalization
description: "Use when: 处理上期所 Excel 到按合约 JSON 的多步清洗、补全与合并流程；排查字段映射、入口函数与路径参数化问题"
---

# SHFE Data Normalization Skill

## Purpose
将上期所原始 Excel 数据稳定转换为按合约聚合的 JSON 文件，并确保流程可复现。

## Workflow
1. 识别输入输出目录与后缀链路：`.title` -> `.value` -> `.finished` -> `.temp` -> `.json`。
2. 校验字段映射链路：`交易日期` 到 `日期`，以及价格与成交字段的一致性。
3. 校验合约补全逻辑：空值、NaN 处理与前值填充行为。
4. 校验按合约聚合逻辑：非法文件名字符替换、分组合并正确性。
5. 校验清理逻辑：仅删除预期后缀，避免误删。

## Guardrails
- 不破坏现有脚本式结构。
- 保留中文字段名。
- 避免导入即执行；示例调用放入 `if __name__ == "__main__":`。
- 优先参数化路径，不新增硬编码目录。

## Done Criteria
- 主流程可从原始 Excel 走到按合约 JSON。
- 关键字段读取一致，且无明显路径或删除风险。
- 改动具备最小验证步骤（示例命令或检查点）。
