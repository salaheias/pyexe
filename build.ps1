# PowerShell script to build and package the jmcomic project into an .exe file

$ErrorActionPreference = "Stop"

# Output executable name (可通过修改此变量改变输出名)
$outputExe = "jmcomic.exe"

Write-Host "创建虚拟环境并安装依赖..."
$venv = Join-Path -Path $PSScriptRoot -ChildPath ".venv-build"
if (-Not (Test-Path $venv)) {
    python -m venv $venv
}

& "$venv\Scripts\Activate.ps1"
python -m pip install --upgrade pip
python -m pip install -r (Join-Path $PSScriptRoot "requirements.txt")

Write-Host "使用 PyInstaller 打包..."
Set-Location -Path (Join-Path $PSScriptRoot "src")
pyinstaller --onefile --name "$(Split-Path -Leaf $outputExe -Resolve)" main.py

# 将 exe 移动回项目根目录并清理
Move-Item -Path ".\dist\$(Split-Path -Leaf $outputExe -Resolve)" -Destination (Join-Path $PSScriptRoot $outputExe) -Force

Write-Host "清理中（保留 dist 中产物）..."
Remove-Item -Recurse -Force ".\build" "main.spec" -ErrorAction SilentlyContinue

Write-Host "构建完成，exe 位于：" (Join-Path $PSScriptRoot $outputExe)