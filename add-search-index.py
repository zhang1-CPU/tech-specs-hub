#!/usr/bin/env python3
import os

missing_entries = [
    { "title": "DJI Mini 5 Pro Specs", "desc": "DJI Mini 5 Pro drone technical specifications", "url": "/pages/specs/dji-mini-5-pro.html" },
    { "title": "P3000 - Hybrid Battery Control Module", "desc": "Hybrid battery control module fault code troubleshooting", "url": "/pages/troubleshooting/p3000-hybrid-battery-control-module.html" },
    { "title": "P0A7B - Hybrid Battery Voltage Sensor", "desc": "Hybrid battery voltage sensor error code diagnosis", "url": "/pages/troubleshooting/p0a7b-hybrid-battery-voltage-sensor.html" },
    { "title": "P0AC4 - Hybrid Battery Temperature Sensor", "desc": "Hybrid battery temperature sensor fault troubleshooting", "url": "/pages/troubleshooting/p0ac4-hybrid-battery-temperature-sensor.html" },
    { "title": "P0A9D - Hybrid Inverter Fault", "desc": "Hybrid inverter fault code diagnosis and repair", "url": "/pages/troubleshooting/p0a9d-hybrid-inverter-fault.html" },
    { "title": "Power Station Solar Input Not Working", "desc": "Troubleshoot solar charging input issues on power stations", "url": "/pages/troubleshooting/power-station-solar-input-not-working.html" },
    { "title": "Power Station Overheating", "desc": "Portable power station overheating troubleshooting guide", "url": "/pages/troubleshooting/power-station-overheating.html" },
    { "title": "Power Station Not Charging", "desc": "Troubleshooting guide for power stations that won't charge", "url": "/pages/troubleshooting/power-station-not-charging.html" },
    { "title": "Power Station BMS Error", "desc": "Battery management system error troubleshooting", "url": "/pages/troubleshooting/power-station-bms-error.html" },
    { "title": "DJI IMU Calibration Error", "desc": "DJI drone IMU calibration error fixes", "url": "/pages/troubleshooting/dji-imu-calibration-error.html" },
    { "title": "DJI Compass Error", "desc": "DJI drone compass error and calibration fixes", "url": "/pages/troubleshooting/dji-compass-error.html" },
    { "title": "DJI Vision Positioning Error", "desc": "DJI vision positioning error troubleshooting", "url": "/pages/troubleshooting/dji-vision-positioning-error.html" },
    { "title": "DJI Battery Not Charging", "desc": "DJI drone battery not charging fixes", "url": "/pages/troubleshooting/dji-battery-not-charging.html" },
    { "title": "3D Printer Thermal Runaway", "desc": "3D printer thermal runaway error fixes", "url": "/pages/troubleshooting/3d-printer-thermal-runaway.html" },
    { "title": "3D Printer Bed Leveling Problems", "desc": "3D printer bed leveling issues and solutions", "url": "/pages/troubleshooting/3d-printer-bed-leveling-problems.html" },
    { "title": "3D Printer Filament Jam", "desc": "3D printer filament jam troubleshooting", "url": "/pages/troubleshooting/3d-printer-filament-jam.html" },
    { "title": "3D Printer Layer Shifting", "desc": "3D printer layer shifting causes and fixes", "url": "/pages/troubleshooting/3d-printer-layer-shifting.html" },
    { "title": "E-Bike Motor Not Working", "desc": "Electric bike motor troubleshooting guide", "url": "/pages/troubleshooting/ebike-motor-not-working.html" },
    { "title": "E-Bike BMS Communication Error", "desc": "E-bike battery management system communication error", "url": "/pages/troubleshooting/ebike-bms-communication-error.html" },
    { "title": "Smart Home Device Offline", "desc": "Smart home device offline troubleshooting", "url": "/pages/troubleshooting/smart-home-device-offline.html" },
    { "title": "Smart Speaker Not Responding", "desc": "Smart speaker not responding fixes", "url": "/pages/troubleshooting/smart-speaker-not-responding.html" },
    { "title": "Privacy Policy", "desc": "TechSpecsHub privacy policy and data handling", "url": "/pages/privacy-policy.html" }
]

main_js_path = "/workspace/assets/js/main.js"

with open(main_js_path, "r", encoding="utf-8") as f:
    content = f.read()

for entry in missing_entries:
    entry_str = f"    {{ title: '{entry['title']}', desc: '{entry['desc']}', url: '{entry['url']}' }},"
    
    if entry_str not in content:
        insert_pos = content.find("  ];")
        if insert_pos != -1:
            content = content[:insert_pos] + "\n" + entry_str + content[insert_pos:]
            print(f"Added: {entry['title']}")
        else:
            print(f"Could not find insertion point for: {entry['title']}")
    else:
        print(f"Already exists: {entry['title']}")

with open(main_js_path, "w", encoding="utf-8") as f:
    f.write(content)

print("\nSearch index updated with all missing pages!")
