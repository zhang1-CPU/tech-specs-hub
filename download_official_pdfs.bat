@echo off
chcp 65001 >nul
echo ========================================
echo  TechSpecsHub 官方PDF文档下载工具
echo ========================================
echo.

:: 创建下载目录
set "DOWNLOAD_DIR=%USERPROFILE%\Desktop\TechSpecsHub_PDFs"
mkdir "%DOWNLOAD_DIR%" 2>nul

echo 正在下载到: %DOWNLOAD_DIR%
echo.

:: EcoFlow Delta Pro 3 官方手册
echo [1/6] 下载 EcoFlow Delta Pro 3 用户手册...
powershell -command "Invoke-WebRequest -Uri 'https://manuals.ecoflow.com/cn/product/delta-pro-3-smart-extra-battery?lang=zh_CN' -OutFile '%DOWNLOAD_DIR%\EcoFlow_Delta_Pro3_Manual.pdf'"

:: DJI Mini 5 Pro 用户手册
echo [2/6] 下载 DJI Mini 5 Pro 用户手册...
powershell -command "Invoke-WebRequest -Uri 'https://www.dji.com/dk/mini-5-pro/downloads' -OutFile '%DOWNLOAD_DIR%\DJI_Mini5Pro_Manual.pdf'"

:: Bosch eBike Performance CX
echo [3/6] 下载 Bosch Performance Line CX 规格表...
powershell -command "Invoke-WebRequest -Uri 'https://www.bosch-ebike.com/en/products/performance-line-cx/' -OutFile '%DOWNLOAD_DIR%\Bosch_Performance_CX_Specs.pdf'"

:: Roborock S8 MaxV Ultra
echo [4/6] 下载 Roborock S8 MaxV Ultra 手册...
powershell -command "Invoke-WebRequest -Uri 'https://us.roborock.com/pages/s8-maxv-ultra' -OutFile '%DOWNLOAD_DIR%\Roborock_S8_MaxV_Ultra_Manual.pdf'"

:: Toyota Prius 2025
echo [5/6] 下载 Toyota Prius 手册...
powershell -command "Invoke-WebRequest -Uri 'https://www.toyota.com/owners/resources/warranty-owner-manuals' -OutFile '%DOWNLOAD_DIR%\Toyota_Prius_Manual.pdf'"

:: Shimano STEPS
echo [6/6] 下载 Shimano STEPS 手册...
powershell -command "Invoke-WebRequest -Uri 'https://www.shimano-steps.com/' -OutFile '%DOWNLOAD_DIR%\Shimano_STEPS_Manual.pdf'"

echo.
echo ========================================
echo  下载完成！
echo  文件保存在: %DOWNLOAD_DIR%
echo ========================================
pause
