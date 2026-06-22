# ============================================================
# TechSpecsHub 301 重定向映射表
# ============================================================
# 格式：旧URL（带 .html）→ 新URL（干净的 slug）
# 用于 Nginx/Apache/Cloudflare Pages 规则配置
#
# 生成日期: 2026-06-22
# 部署位置: https://powerspecshub.com
# ============================================================

# ----------------------------------------------------------------
# 根目录与首页
# ----------------------------------------------------------------
/                                       →  /
/index.html                             →  /

# ----------------------------------------------------------------
# 主导航页
# ----------------------------------------------------------------
/pages/index.html                       →  /pages/
/pages/about.html                       →  /about/
/pages/contact.html                     →  /contact/
/pages/privacy-policy.html              →  /privacy/
/pages/error-code-db.html               →  /error-codes/
/pages/master-specs.html                →  /specs/master/
/pages/brand-index.html                 →  /brands/

# ----------------------------------------------------------------
# 规格页 (Specs)
# ----------------------------------------------------------------
/pages/specs/outdoor-power.html         →  /outdoor-power-stations/
/pages/specs/hybrid-cars.html           →  /hybrid-batteries/
/pages/specs/drones.html                →  /drones/
/pages/specs/smart-home.html            →  /smart-home/
/pages/specs/ebike-micromobility.html   →  /ebike/
/pages/specs/3d-printers.html           →  /3d-printers/
/pages/specs/navigation.html            →  /navigation/

# ----------------------------------------------------------------
# 单独型号规格页
# ----------------------------------------------------------------
/pages/specs/ecoflow-delta-pro-3.html   →  /specs/ecoflow-delta-pro-3/
/pages/specs/bluetti-ac200max.html      →  /specs/bluetti-ac200max/
/pages/specs/jackery-explorer-2000-plus.html → /specs/jackery-explorer-2000-plus/
/pages/specs/dji-mavic-3-pro.html       →  /specs/dji-mavic-3-pro/
/pages/specs/dji-air-3.html             →  /specs/dji-air-3/
/pages/specs/toyota-prius-2022-battery.html → /specs/toyota-prius-battery/

# ----------------------------------------------------------------
# 工具页 (Tools)
# ----------------------------------------------------------------
/pages/tools/best-multimeters-2026.html →  /tools/best-multimeters/
/pages/tools/runtime-calculator.html    →  /tools/runtime-calculator/
/pages/tools/unit-converter.html        →  /tools/unit-converter/

# ----------------------------------------------------------------
# 购买指南 (Guides)
# ----------------------------------------------------------------
/pages/guides/drone-battery-care-guide.html → /guides/drone-battery-care/
/pages/guides/hybrid-battery-replacement-cost.html → /guides/hybrid-battery-cost/
/pages/guides/portable-power-station-buying-guide.html → /guides/power-station-buying/

# ----------------------------------------------------------------
# 对比页 (Compare)
# ----------------------------------------------------------------
/pages/compare/ecoflow-vs-bluetti-vs-jackery.html → /compare/ecoflow-vs-bluetti-vs-jackery/

# ----------------------------------------------------------------
# 故障排查页 (Troubleshooting)
# ----------------------------------------------------------------
/pages/troubleshooting/p0a80-replace-hybrid-battery.html → /troubleshooting/p0a80/

# ----------------------------------------------------------------
# Nginx 配置示例
# ----------------------------------------------------------------
# 在 server { } 块中添加:
#
# location ~ ^/pages/(.*)\.html$ {
#     return 301 /$1/;
# }
# location ~ ^/pages/(.*)$ {
#     return 301 /$1/;
# }
# location = /index.html {
#     return 301 /;
# }
#
# 适用条件: 当实际目录结构改造完成后（将 .html 改为目录 + index.html）
# 当前阶段: 仅作为参考，暂不实施实际重定向（站点仍使用 .html URL）

# ----------------------------------------------------------------
# Apache .htaccess 配置示例
# ----------------------------------------------------------------
# RewriteEngine On
# RewriteCond %{REQUEST_URI} ^/pages/(.*)\.html$
# RewriteRule ^pages/(.*)\.html$ /$1/ [R=301,L]
# RewriteRule ^index\.html$ / [R=301,L]
