@echo off
echo ============================================
echo TechSpecsHub 一键部署脚本
echo ============================================
echo.

REM 检查是否已经初始化 Git
if exist ".git" (
    echo [INFO] Git 仓库已存在，跳过初始化
) else (
    echo [INFO] 初始化 Git 仓库...
    git init
    if errorlevel 1 goto error
)

echo [INFO] 添加所有文件...
git add .
if errorlevel 1 goto error

echo [INFO] 创建提交...
git commit -m "Initial commit - full tech specs database"
if errorlevel 1 goto error

REM 检查是否已添加远程仓库
git remote -v | findstr /C:"origin" >nul
if %errorlevel% == 0 (
    echo [INFO] 远程仓库已存在
) else (
    echo [INFO] 添加远程仓库...
    git remote add origin https://github.com/zhang1-CPU/tech-specs-hub.git
    if errorlevel 1 goto error
)

echo [INFO] 设置主分支...
git branch -M main
if errorlevel 1 goto error

echo.
echo ============================================
echo 准备推送文件到 GitHub！
echo ============================================
echo.
echo 请确保你已经在 GitHub 上创建了仓库：
echo   仓库名: tech-specs-hub
echo   地址: https://github.com/zhang1-CPU/tech-specs-hub
echo.
echo 按任意键继续推送...
pause >nul

echo [INFO] 正在推送到 GitHub...
git push -u origin main

if errorlevel 1 (
    echo.
    echo ============================================
    echo 推送失败！
    echo ============================================
    echo 可能的原因：
    echo 1. 你还没有在 GitHub 上创建 tech-specs-hub 仓库
    echo 2. 需要先登录 GitHub
    echo 3. 分支冲突
    echo.
    echo 请先在 GitHub 上创建仓库后再运行此脚本！
    echo.
    goto end
) else (
    echo.
    echo ============================================
    echo ✅ 部署成功！
    echo ============================================
    echo.
    echo 你的网站将很快上线：
    echo   https://zhang1-CPU.github.io/tech-specs-hub/
    echo.
    echo 下一步：启用 GitHub Pages
    echo   1. 访问 https://github.com/zhang1-CPU/tech-specs-hub/settings/pages
    echo   2. Branch 选择 main，点击 Save
    echo.
)

goto end

:error
echo.
echo ============================================
echo ❌ 执行失败
echo ============================================
:end
pause
