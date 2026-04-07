# 任务计划

## 元信息
- 序号（从1开始的整数）：3
- 任务名称：Win11 root_prefix 报错修复
- 发起时间：2026-04-06 19:33:26
- 负责人：GitHub Copilot
- 当前 Git 版本：fb9d1e3

## 目标
- 业务目标：解决 Win11 环境下 `libmamba bad conversion` 导致环境命令不可用的问题。
- 技术目标：给出可执行的环境变量清理/重置方案，并修正文档中的 PowerShell 路径变量写法。

## 范围
- 包含：排查 `MAMBA_ROOT_PREFIX` 变量、修正文档命令、追加会议回查记录。
- 不包含：安装 Micromamba 可执行文件本体与跨机自动化脚本。

## 执行步骤
1. [x] 排查当前会话、用户级、系统级 `MAMBA_ROOT_PREFIX` 变量。
2. [x] 识别并修正文档中的 PowerShell 环境变量写法风险。
3. [x] 追加会议回查记录。

## 风险与回滚
- 风险点：若用户通过其他 shell（CMD/Git Bash/IDE 内置 shell）注入了异常变量，仍可能复现。
- 回滚策略：恢复文档命令到上一版，并按终端类型逐一定位变量来源。

## 验证
- 命令验证：`reg query HKCU\Environment /v MAMBA_ROOT_PREFIX` 与 `reg query HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment /v MAMBA_ROOT_PREFIX` 均未发现该变量；当前会话 `$env:MAMBA_ROOT_PREFIX` 为空。
- 人工验证：文档中 PowerShell 初始化命令已改为 `$env:USERPROFILE` 写法；用户在 Win11 终端按修复脚本重建环境后测试通过（2026-04-07）。

## 决策记录
- 决策1：PowerShell 文档统一使用 `$env:USERPROFILE`，不再混用 CMD 的 `%USERPROFILE%`。

## 结束状态
- 结束时间：2026-04-07 10:47:29
- 结果摘要：已完成变量来源排查、文档修正与 Win11 实机验证，`libmamba bad conversion` 问题已解除。
- 后续动作：将该修复流程沉淀为 Win11 环境排错标准步骤，后续仅在复发时排查 shell 配置注入。