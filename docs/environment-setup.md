# Python 环境配置（Micromamba）

本项目推荐使用 Micromamba 统一管理环境，目标平台为 Win11、macOS、Ubuntu。

## 1. 安装 Micromamba

- Windows（PowerShell）：
  - `winget install mamba.Micromamba`
- macOS（Homebrew）：
  - `brew install micromamba`
- Ubuntu（Homebrew 或官方脚本）：
  - `brew install micromamba`

> 安装后建议按 Micromamba 提示执行 shell 初始化命令。

## 2. 创建环境

在仓库根目录执行：

`micromamba create -f environment.yml -y`

## 3. 激活环境

- Windows：`micromamba activate kumquat-py311`
- macOS/Linux：`micromamba activate kumquat-py311`

## 4. 验证

- `python --version`
- `python -c "import pandas, matplotlib, openpyxl; print('ok')"`

预期：Python 3.11.5 且输出 `ok`。

## 5. 运行项目

- 启动查看器：`python StockDataShower.py`
- 清理目标后缀文件：`python StockFileClear.py`

## 6. 团队协作建议

- 将 `environment.yml` 纳入 Git 版本控制。
- 不提交本地环境目录（见 `.gitignore`）。
- 后续如需完全锁定版本，可新增 conda-lock 多平台锁文件。