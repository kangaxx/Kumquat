# 环境创建说明（根目录）

为便于跨平台调试与部署，本项目提供以下 Micromamba 环境文件：

- `environment.yml`：核心脚本通用基线（数据处理与非 GUI 脚本）
- `environment.win11.yml`：Win11 图形查看器环境
- `environment.ubuntu-22.04.yml`：Ubuntu 22.04.5 LTS 64 位服务器版
- `environment.macos.yml`：最新 macOS 64 位系统

## 1. 安装 Micromamba

- Windows: `winget install mamba.Micromamba`
- macOS: `brew install micromamba`
- Ubuntu: `brew install micromamba` 或按官方脚本安装

Windows PowerShell 安装后需执行一次 shell 初始化，否则 `micromamba activate ...` 会直接报错：

`micromamba shell init -s powershell -r "$env:USERPROFILE\micromamba"`

执行后请重开 PowerShell。

## 2. 创建环境

### Win11 图形查看器环境
`micromamba create -f environment.win11.yml -y`

### Ubuntu 22.04.5 LTS 64 位
`micromamba create -f environment.ubuntu-22.04.yml -y`

### macOS 64 位
`micromamba create -f environment.macos.yml -y`

### 通用基线
`micromamba create -f environment.yml -y`

## 3. 激活环境

- Win11: `micromamba activate kumquat-py311-win11`
- Ubuntu: `micromamba activate kumquat-py311-ubuntu2204`
- macOS: `micromamba activate kumquat-py311-macos`
- 通用: `micromamba activate kumquat-py311`

如果只是验证环境是否创建成功，也可以绕过激活直接执行：

- Win11: `micromamba run -n kumquat-py311-win11 python --version`
- 通用: `micromamba run -n kumquat-py311 python --version`

## 4. 验证

- `python --version`
- `python -c "import pandas, matplotlib, openpyxl; print('ok')"`

Win11 查看器环境建议额外验证：

- `python -c "import tkinter; import matplotlib; print('gui-ok')"`

预期：Python 版本为 3.11.5，核心环境输出 `ok`，Win11 查看器环境额外输出 `gui-ok`。

## 5. 运行项目

- 启动查看器: `python StockDataShower.py`（Win11/macOS/Ubuntu GUI 环境建议使用各自专项环境）
- 清理目标后缀文件: `python StockFileClear.py`
