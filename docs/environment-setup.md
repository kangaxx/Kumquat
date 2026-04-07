# Python 环境配置（Micromamba）

本项目推荐使用 Micromamba 统一管理环境，目标平台为 Win11、macOS、Ubuntu。

环境文件说明：

- `environment.yml`：核心脚本通用基线，适用于数据处理与非 GUI 脚本。
- `environment.win11.yml`：Win11 图形查看器环境，包含 Tkinter 所需 `tk` 依赖。
- `environment.ubuntu-22.04.yml`：Ubuntu 22.04.5 LTS 64 位服务器版图形环境。
- `environment.macos.yml`：macOS 图形环境。

## 1. 安装 Micromamba

- Windows（PowerShell）：
  - `winget install mamba.Micromamba`
- macOS（Homebrew）：
  - `brew install micromamba`
- Ubuntu（Homebrew 或官方脚本）：
  - `brew install micromamba`

> Windows PowerShell 安装后请先执行 `micromamba shell init -s powershell -r "$env:USERPROFILE\micromamba"`，然后重开终端；否则 `micromamba activate` 会报错。

## 2. 创建环境

在仓库根目录执行对应平台命令：

- Win11 图形查看器：`micromamba create -f environment.win11.yml -y`
- 通用核心脚本：`micromamba create -f environment.yml -y`
- Ubuntu：`micromamba create -f environment.ubuntu-22.04.yml -y`
- macOS：`micromamba create -f environment.macos.yml -y`

## 3. 激活环境

- Windows 查看器：`micromamba activate kumquat-py311-win11`
- 通用核心脚本：`micromamba activate kumquat-py311`
- Ubuntu：`micromamba activate kumquat-py311-ubuntu2204`
- macOS：`micromamba activate kumquat-py311-macos`

若 PowerShell 尚未完成 shell 初始化，可先用 `micromamba run -n <环境名> <命令>` 做验证，例如：

- `micromamba run -n kumquat-py311-win11 python --version`
- `micromamba run -n kumquat-py311-win11 python -c "import tkinter; import matplotlib; print('gui-ok')"`

## 4. 验证

- `python --version`
- `python -c "import pandas, matplotlib, openpyxl; print('ok')"`

Win11 查看器环境建议额外验证：

- `python -c "import tkinter; import matplotlib; print('gui-ok')"`

预期：Python 3.11.5；核心环境输出 `ok`；Win11 查看器环境额外输出 `gui-ok`。

## 5. 运行项目

- 启动查看器：`python StockDataShower.py`
- 清理目标后缀文件：`python StockFileClear.py`

说明：`StockDataShower.py` 依赖 Tkinter 图形能力，Win11 请优先使用 `environment.win11.yml`，不要直接将 `environment.yml` 视为查看器运行环境。

## 6. 团队协作建议

- 将 `environment.yml` 纳入 Git 版本控制。
- 将 `environment.win11.yml` 纳入 Git 版本控制。
- 不提交本地环境目录（见 `.gitignore`）。
- 后续如需完全锁定版本，可新增 conda-lock 多平台锁文件。