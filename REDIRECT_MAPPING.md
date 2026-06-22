# 301 Redirect Mapping Table for TechSpecsHub
# Last Updated: 2026-06-22
# Format: Apache/Nginx compatible

# ═══════════════════════════════════════════════════════════════════════════════
# CORE PAGES
# ═══════════════════════════════════════════════════════════════════════════════

# Homepage
Redirect 301 /index.html /

# Pages Directory Index
Redirect 301 /pages/index.html /pages/

# Legacy URL (if any old URLs existed)
Redirect 301 /home /


# ═══════════════════════════════════════════════════════════════════════════════
# SPECS PAGES - SEMANTIC URL MAPPING
# ═══════════════════════════════════════════════════════════════════════════════

# Outdoor Power / Power Stations
Redirect 301 /pages/specs/outdoor-power.html /outdoor-power-stations/
Redirect 301 /pages/specs/ecoflow-delta-pro-3.html /ecoflow-delta-pro-3-specs/
Redirect 301 /pages/specs/budget-500w-power-station-comparison.html /budget-power-stations-under-300/
Redirect 301 /pages/specs/bluetti-ac200max.html /bluetti-ac200max-specs/
Redirect 301 /pages/specs/jackery-explorer-2000-plus.html /jackery-explorer-2000-plus-specs/

# Hybrid & EV
Redirect 301 /pages/specs/hybrid-cars.html /hybrid-ev-battery-specs/
Redirect 301 /pages/specs/toyota-prius-2022-battery.html /toyota-prius-battery-specs/

# Drones
Redirect 301 /pages/specs/drones.html /drone-specs/
Redirect 301 /pages/specs/dji-mavic-3-pro.html /dji-mavic-3-pro-specs/
Redirect 301 /pages/specs/dji-air-3.html /dji-air-3-specs/

# Smart Home & Other
Redirect 301 /pages/specs/smart-home.html /smart-home-device-specs/
Redirect 301 /pages/specs/ebike-micromobility.html /ebike-specs/
Redirect 301 /pages/specs/3d-printers.html /3d-printer-specs/
Redirect 301 /pages/specs/navigation.html /gps-navigation-specs/


# ═══════════════════════════════════════════════════════════════════════════════
# TROUBLESHOOTING PAGES - ERROR CODES
# ═══════════════════════════════════════════════════════════════════════════════

# Hybrid Battery Error Codes
Redirect 301 /pages/troubleshooting/p0a80-replace-hybrid-battery.html /error-codes/p0a80-hybrid-battery-replacement/
Redirect 301 /pages/troubleshooting/p0a7f-hybrid-battery-deterioration.html /error-codes/p0a7f-hybrid-battery-deterioration/
Redirect 301 /pages/troubleshooting/p3000-battery-control-malfunction.html /error-codes/p3000-battery-control/
Redirect 301 /pages/troubleshooting/p3004-hv-battery-module-fault.html /error-codes/p3004-hv-battery-module/
Redirect 301 /pages/troubleshooting/p3009-battery-cooling-fault.html /error-codes/p3009-battery-cooling/
Redirect 301 /pages/troubleshooting/c1259-hv-system-disable.html /error-codes/c1259-hv-system/

# Power Station Error Codes
Redirect 301 /pages/troubleshooting/e1-overload-ecoflow-jackery-blutti-anker.html /error-codes/e1-overload-power-station/
Redirect 301 /pages/troubleshooting/e2-high-temperature-power-station.html /error-codes/e2-high-temperature/
Redirect 301 /pages/troubleshooting/e3-ac-overload-power-station.html /error-codes/e3-ac-overload/
Redirect 301 /pages/troubleshooting/e6-battery-fault-power-station.html /error-codes/e6-battery-fault/
Redirect 301 /pages/troubleshooting/e7-fan-blocked-power-station.html /error-codes/e7-fan-blocked/
Redirect 301 /pages/troubleshooting/power-station-solar-input-not-working.html /troubleshooting/solar-input-not-working/
Redirect 301 /pages/troubleshooting/hybrid-battery-cooling-fan-noise.html /troubleshooting/cooling-fan-noise/

# Drone Error Codes
Redirect 301 /pages/troubleshooting/gimbal-motor-overload-dji.html /error-codes/gimbal-motor-overload/
Redirect 301 /pages/troubleshooting/gimbal-imu-calibration-dji.html /error-codes/gimbal-imu-calibration/
Redirect 301 /pages/troubleshooting/vision-system-error-dji.html /error-codes/vision-system-error/
Redirect 301 /pages/troubleshooting/compass-error-drone.html /error-codes/compass-error/
Redirect 301 /pages/troubleshooting/battery-temperature-error-drone.html /error-codes/drone-battery-temperature/
Redirect 301 /pages/troubleshooting/drone-wont-connect-controller.html /troubleshooting/drone-connection-issues/

# Smart Home & 3D Printer
Redirect 301 /pages/troubleshooting/smart-home-device-offline.html /troubleshooting/smart-home-offline/
Redirect 301 /pages/troubleshooting/3d-printer-thermal-runaway.html /troubleshooting/3d-printer-thermal-runaway/


# ═══════════════════════════════════════════════════════════════════════════════
# DATABASE & TOOLS
# ═══════════════════════════════════════════════════════════════════════════════

# Error Code Database
Redirect 301 /pages/error-code-db.html /error-codes/

# Master Specs
Redirect 301 /pages/master-specs.html /specs/

# Brand Index
Redirect 301 /pages/brand-index.html /brands/


# ═══════════════════════════════════════════════════════════════════════════════
# GUIDES & TOOLS
# ═══════════════════════════════════════════════════════════════════════════════

# Guides
Redirect 301 /pages/guides/portable-power-station-buying-guide.html /guides/power-station-buying-guide/
Redirect 301 /pages/guides/hybrid-battery-replacement-cost.html /guides/hybrid-battery-cost/
Redirect 301 /pages/guides/drone-battery-care-guide.html /guides/drone-battery-care/

# Tools
Redirect 301 /pages/tools/best-multimeters-2026.html /tools/best-multimeters/
Redirect 301 /pages/tools/runtime-calculator.html /tools/runtime-calculator/
Redirect 301 /pages/tools/unit-converter.html /tools/unit-converter/

# Compare
Redirect 301 /pages/compare/ecoflow-vs-bluetti-vs-jackery.html /compare/power-stations/


# ═══════════════════════════════════════════════════════════════════════════════
# STATIC PAGES
# ═══════════════════════════════════════════════════════════════════════════════

Redirect 301 /pages/about.html /about/
Redirect 301 /pages/contact.html /contact/
Redirect 301 /pages/privacy-policy.html /privacy-policy/


# ═══════════════════════════════════════════════════════════════════════════════
# NGINX CONFIGURATION EXAMPLE
# ═══════════════════════════════════════════════════════════════════════════════
# For Nginx, use the following format in your server block:
#
# location = /index.html {
#     return 301 /;
# }
#
# location /pages/specs/outdoor-power.html {
#     return 301 /outdoor-power-stations/;
# }
#
# Or use a map directive for bulk redirects:
#
# map $request_uri $new_uri {
#     /pages/specs/outdoor-power.html /outdoor-power-stations/;
#     /pages/specs/ecoflow-delta-pro-3.html /ecoflow-delta-pro-3-specs/;
#     ...
#     default "";
# }
#
# server {
#     if ($new_uri != "") {
#         return 301 $new_uri;
#     }
# }


# ═══════════════════════════════════════════════════════════════════════════════
# TOTAL REDIRECT RULES: 47
# ═══════════════════════════════════════════════════════════════════════════════
