@echo off
echo 正在构建 WordStay 可执行文件...
echo.

REM 检查是否已安装依赖
pip install -r requirements.txt

REM 使用 spec 文件进行打包
pyinstaller WordStay.spec --clean

echo.
echo 构建完成！
echo 可执行文件位于 dist\WordStay.exe
pause
