#!/usr/bin/env bash
set -euo pipefail

# 简单的打包脚本：创建虚拟环境，安装依赖，用 PyInstaller 打包为单文件。
# 注意：在 Linux 下直接运行 PyInstaller 会生成 Linux 可执行文件；要生成 Windows 的 .exe
# 最可靠的方式是在 Windows 上运行此脚本，或使用带有 Windows 运行时的容器（或 Wine）进行交叉编译。

VENV_DIR=".venv-build"
PYINSTALLER_NAME="jmcomic-cli"

usage() {
	echo "用法: $0 [--clean] [--name NAME]"
	echo
	echo "--clean   : 清理之前的构建产物和虚拟环境"
	echo "--name    : 指定输出可执行文件名（默认: ${PYINSTALLER_NAME}）"
	echo
	echo "提示：在 Windows 上直接运行 'build.ps1' 可生成 .exe。"
}

if [[ ${1:-} == "--help" || ${1:-} == "-h" ]]; then
	usage
	exit 0
fi

if [[ ${1:-} == "--clean" ]]; then
	echo "清理构建产物..."
	rm -rf build dist ${VENV_DIR} *.spec
	echo "已清理"
	exit 0
fi

while [[ $# -gt 0 ]]; do
	case "$1" in
		--clean) shift ;;
		--name) PYINSTALLER_NAME="$2"; shift 2 ;;
		*) echo "未知参数: $1"; usage; exit 1 ;;
	esac
done

echo "创建虚拟环境: ${VENV_DIR}"
python3 -m venv "${VENV_DIR}"
source "${VENV_DIR}/bin/activate"
pip install --upgrade pip
pip install -r requirements.txt

echo "使用 PyInstaller 打包..."
# 生成单文件，可在 Windows 上直接得到 .exe（在 Windows 环境）。
pyinstaller --onefile --name "${PYINSTALLER_NAME}" src/main.py

echo "打包完成：请查看 dist/ 目录下的可执行文件。"
deactivate || true