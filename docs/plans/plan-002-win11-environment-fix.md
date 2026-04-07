# 任务计划

## 元信息
- 序号（从1开始的整数）：2
- 任务名称：Win11 Micromamba 环境修正
- 发起时间：2026-04-03 21:33:06
- 负责人：GitHub Copilot
- 当前 Git 版本：fb9d1e3

## 目标
- 业务目标：修复 Win11 用户按现有文档创建环境时的高频报错，确保能稳定完成环境创建并运行查看器。
- 技术目标：新增 Win11 专项环境定义，修正文档中通用基线的适用范围，并补充 PowerShell 初始化与免激活验证命令。

## 范围
- 包含：新增 Win11 环境文件、更新根目录环境说明、更新环境部署文档、追加会议回查记录。
- 不包含：安装 Micromamba 本体、生成锁文件、接入 CI。

## 执行步骤
1. [x] 复核 Win11 报错高风险点（缺少 tk、缺少 shell init、文档口径过宽）。
2. [x] 新增 Win11 专项环境定义文件。
3. [x] 更新根目录与 docs 下的环境说明，区分通用基线与 Win11 GUI 环境。
4. [x] 补充 Windows PowerShell 初始化与免激活验证方式。
5. [x] 追加会议回查记录。

## 风险与回滚
- 风险点：若用户本机未安装 Micromamba，仍需先完成工具安装；若 PowerShell 未重启，`micromamba activate` 仍会失败。
- 回滚策略：删除 Win11 专项环境文件，并恢复 CREATE_ENVIRONMENT.md、docs/environment-setup.md、docs/change-meeting-log.md 到上一版本。

## 验证
- 命令验证：人工核对 Win11 文档已包含 `micromamba shell init -s powershell` 与 `micromamba run -n ...` 示例；Win11 环境文件已包含 `tk`。
- 人工验证：检查文档不再将 `environment.yml` 表述为 Win11 GUI 运行基线。

## 决策记录
- 决策1：保留 `environment.yml` 作为核心脚本基线，不再将其声明为 Win11 查看器运行环境。
- 决策2：为 Win11 单独提供 `environment.win11.yml`，避免 GUI 依赖与通用脚本基线混用。

## 结束状态
- 结束时间：2026-04-03 21:33:06
- 结果摘要：已补齐 Win11 专项环境文件，并修正文档中关于通用基线、PowerShell 激活与 Tkinter 依赖的说明。
- 后续动作：如需进一步提升复现性，可补充 win-64 锁文件并在 Win11 上做一次实际建环境验证。