# 环境创建说明（根目录）

为便于跨平台调试与部署，本项目提供以下 Micromamba 环境文件：

- `environment.yml`：通用基线（Win11/macOS/Ubuntu）
- `environment.ubuntu-22.04.yml`：Ubuntu 22.04.5 LTS 64 位服务器版
- `environment.macos.yml`：最新 macOS 64 位系统

## 1. 安装 Micromamba

- Windows: `winget install mamba.Micromamba`
- macOS: `brew install micromamba`
- Ubuntu: `brew install micromamba` 或按官方脚本安装

## 2. 创建环境

### Ubuntu 22.04.5 LTS 64 位
`micromamba create -f environment.ubuntu-22.04.yml -y`

### macOS 64 位
`micromamba create -f environment.macos.yml -y`

### 通用基线
`micromamba create -f environment.yml -y`

## 3. 激活环境

- Ubuntu: `micromamba activate kumquat-py311-ubuntu2204`
- macOS: `micromamba activate kumquat-py311-macos`
- 通用: `micromamba activate kumquat-py311`

## 4. 验证

- `python --version`
- `python -c "import pandas, matplotlib, openpyxl; print('ok')"`

预期：Python 版本为 3.11.5 且输出 `ok`。

## 5. 运行项目

- 启动查看器: `python StockDataShower.py`
- 清理目标后缀文件: `python StockFileClear.py`
