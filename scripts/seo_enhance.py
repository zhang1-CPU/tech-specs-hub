#!/usr/bin/env python3
"""
TechSpecsHub SEO 增强脚本
- 添加完整的 <head> SEO 标签
- 添加 Schema.org JSON-LD 结构化数据
- 添加面包屑导航
- 为 Coming Soon 页面添加 noindex
"""

import os
import re
import json
import glob
from datetime import datetime

DOMAIN = "https://powerspecshub.com"
OG_IMAGE = f"{DOMAIN}/assets/og-image.jpg"
TODAY = datetime.now().strftime("%Y-%m-%d")

# ============================================================
# 页面元数据配置
# ============================================================
PAGES_META = {
    "index.html": {
        "url": "/",
        "title": "TechSpecsHub — Technical Specs, Error Codes & Repair Data",
        "description": "Authoritative reference for portable power station specs, hybrid battery parameters, drone motor data, and fault code diagnostics. Verified against OEM documentation.",
        "is_coming_soon": False,
        "category": "Home",
        "breadcrumb": [],
    },
    "pages/index.html": {
        "url": "/pages/index.html",
        "title": "TechSpecsHub | Specs Database & Repair Guides",
        "description": "Browse technical specifications and repair guides for portable power stations, hybrid batteries, drones, and smart home devices. TechSpecsHub tech reference.",
        "is_coming_soon": False,
        "category": "Home",
        "breadcrumb": [],
    },
    "pages/about.html": {
        "url": "/pages/about.html",
        "title": "About TechSpecsHub | Our Mission & Data Sources",
        "description": "Learn about TechSpecsHub mission to provide verified technical specifications and repair data for power stations, hybrid batteries, drones, and smart home devices.",
        "is_coming_soon": False,
        "category": "About",
        "breadcrumb": ["About"],
    },
    "pages/contact.html": {
        "url": "/pages/contact.html",
        "title": "Contact TechSpecsHub | Report Errors",
        "description": "Contact TechSpecsHub to report data errors, suggest coverage, or request technical specifications. We respond within 48 hours to all verified reports.",
        "is_coming_soon": False,
        "category": "Contact",
        "breadcrumb": ["Contact"],
    },
    "pages/master-specs.html": {
        "url": "/pages/master-specs.html",
        "title": "Master Specs Comparison | TechSpecsHub",
        "description": "Compare technical specifications across brands: EcoFlow, Jackery, Bluetti, Tesla, Toyota, DJI. Side-by-side capacity, output, and battery data tables.",
        "is_coming_soon": False,
        "category": "Data",
        "breadcrumb": ["Master Specs"],
    },
    "pages/brand-index.html": {
        "url": "/pages/brand-index.html",
        "title": "Brand Index A-Z | TechSpecsHub",
        "description": "Complete brand directory for portable power stations, hybrid batteries, drones, and smart home devices. Browse all manufacturers with verified specs.",
        "is_coming_soon": False,
        "category": "Data",
        "breadcrumb": ["Brand Index"],
    },
    "pages/error-code-db.html": {
        "url": "/pages/error-code-db.html",
        "title": "Error Code Database | TechSpecsHub",
        "description": "Searchable database of fault codes for hybrid cars, drones, and power stations. P0A80, MOTOR_HOT, CHG_SLOW and more with diagnostic steps.",
        "is_coming_soon": False,
        "category": "Data",
        "breadcrumb": ["Error Code Database"],
    },
    "pages/specs/outdoor-power.html": {
        "url": "/pages/specs/outdoor-power.html",
        "title": "Outdoor Power Station Specs | TechSpecsHub",
        "description": "Comprehensive outdoor power station specifications from EcoFlow, Jackery, Bluetti, Anker. Compare capacity, output, cycle life, and battery chemistry.",
        "is_coming_soon": True,
        "category": "Specs",
        "breadcrumb": ["Specs", "Outdoor Power"],
    },
    "pages/specs/ecoflow-delta-pro-3.html": {
        "url": "/pages/specs/ecoflow-delta-pro-3.html",
        "title": "EcoFlow Delta Pro 3 Specs | TechSpecsHub",
        "description": "EcoFlow Delta Pro 3 complete specifications: 4096Wh capacity, 4000W output, LFP battery, 6500+ cycles. OEM-verified data and error codes.",
        "is_coming_soon": True,
        "category": "Specs",
        "breadcrumb": ["Specs", "EcoFlow Delta Pro 3"],
    },
    "pages/specs/hybrid-cars.html": {
        "url": "/pages/specs/hybrid-cars.html",
        "title": "Hybrid & EV Battery Specs | TechSpecsHub",
        "description": "Hybrid and EV battery specifications for Toyota, Honda, Ford, Tesla. Internal resistance standards, cell voltages, and P0A80 fault code diagnosis.",
        "is_coming_soon": True,
        "category": "Specs",
        "breadcrumb": ["Specs", "Hybrid Cars"],
    },
    "pages/specs/drones.html": {
        "url": "/pages/specs/drones.html",
        "title": "Drone & UAV Specs | TechSpecsHub",
        "description": "Drone specifications for DJI, Autel, Skydio. Motor KV ratings, ESC current limits, flight controller fault codes, and battery parameters.",
        "is_coming_soon": True,
        "category": "Specs",
        "breadcrumb": ["Specs", "Drones"],
    },
    "pages/specs/smart-home.html": {
        "url": "/pages/specs/smart-home.html",
        "title": "Smart Home Device Specs | TechSpecsHub",
        "description": "Smart home device specifications: Roborock, Ecovacs, Dyson, Husqvarna. Teardown data, motor specs, battery parameters, and repair guides.",
        "is_coming_soon": True,
        "category": "Specs",
        "breadcrumb": ["Specs", "Smart Home"],
    },
    "pages/specs/ebike-micromobility.html": {
        "url": "/pages/specs/ebike-micromobility.html",
        "title": "E-Bike & Micromobility Specs | TechSpecsHub",
        "description": "E-bike and micromobility specifications: Bosch, Bafang, Segway-Ninebot motors. Battery parameters, controller specs, and OEM documentation.",
        "is_coming_soon": True,
        "category": "Specs",
        "breadcrumb": ["Specs", "E-Bike"],
    },
    "pages/specs/3d-printers.html": {
        "url": "/pages/specs/3d-printers.html",
        "title": "3D Printers | TechSpecsHub",
        "description": "3D printer specifications for Bambu Lab, Prusa, Creality, Anycubic, Elegoo. Build volume, hotend specs, firmware features, and material compatibility.",
        "is_coming_soon": True,
        "category": "Specs",
        "breadcrumb": ["Specs", "3D Printers"],
    },
    "pages/specs/navigation.html": {
        "url": "/pages/specs/navigation.html",
        "title": "Navigation & Marine | TechSpecsHub",
        "description": "Navigation and marine electronics specifications. GPS, chartplotter, sonar technical data and OEM documentation.",
        "is_coming_soon": True,
        "category": "Specs",
        "breadcrumb": ["Specs", "Navigation"],
    },
    "pages/specs/bluetti-ac200max.html": {
        "url": "/pages/specs/bluetti-ac200max.html",
        "title": "Bluetti AC200MAX Specs & Troubleshooting",
        "description": "Bluetti AC200MAX complete specifications: 2048Wh capacity, 2200W output, LFP battery, 3500+ cycles. Error codes and diagnostic procedures.",
        "is_coming_soon": True,
        "category": "Specs",
        "breadcrumb": ["Specs", "Bluetti AC200MAX"],
    },
    "pages/specs/jackery-explorer-2000-plus.html": {
        "url": "/pages/specs/jackery-explorer-2000-plus.html",
        "title": "Jackery Explorer 2000 Plus Specs",
        "description": "Jackery Explorer 2000 Plus complete specifications: 2042Wh capacity, 3000W output, LFP battery, 4000 cycles. OEM-verified data.",
        "is_coming_soon": True,
        "category": "Specs",
        "breadcrumb": ["Specs", "Jackery Explorer 2000 Plus"],
    },
    "pages/specs/dji-mavic-3-pro.html": {
        "url": "/pages/specs/dji-mavic-3-pro.html",
        "title": "DJI Mavic 3 Pro Specs & Camera",
        "description": "DJI Mavic 3 Pro specifications: 4/3 CMOS Hasselblad camera, 43-min flight time, O3+ transmission, omnidirectional obstacle sensing.",
        "is_coming_soon": True,
        "category": "Specs",
        "breadcrumb": ["Specs", "DJI Mavic 3 Pro"],
    },
    "pages/specs/dji-air-3.html": {
        "url": "/pages/specs/dji-air-3.html",
        "title": "DJI Air 3 Specs 2026",
        "description": "DJI Air 3 specifications: dual primary cameras, 46-min flight time, O4 video transmission, omnidirectional obstacle sensing.",
        "is_coming_soon": True,
        "category": "Specs",
        "breadcrumb": ["Specs", "DJI Air 3"],
    },
    "pages/specs/toyota-prius-2022-battery.html": {
        "url": "/pages/specs/toyota-prius-2022-battery.html",
        "title": "Toyota Prius HV Battery Specs | P0A80",
        "description": "Toyota Prius Gen 4 (2016-2022) hybrid battery specifications: 201.6V pack voltage, NiMH chemistry, module voltages, P0A80 diagnosis.",
        "is_coming_soon": True,
        "category": "Specs",
        "breadcrumb": ["Specs", "Toyota Prius"],
    },
    "pages/tools/best-multimeters-2026.html": {
        "url": "/pages/tools/best-multimeters-2026.html",
        "title": "Best Multimeters 2026 | TechSpecsHub",
        "description": "Top 4 multimeters for EV and electronics work in 2026: Fluke 87V, Klein MM700, Fluke 117, UNI-T UT61E+. CAT III/IV rated picks for technicians.",
        "is_coming_soon": False,
        "category": "Tools",
        "breadcrumb": ["Tools", "Best Multimeters 2026"],
    },
    "pages/tools/runtime-calculator.html": {
        "url": "/pages/tools/runtime-calculator.html",
        "title": "Power Station Runtime Calculator | TechSpecsHub",
        "description": "Calculate how long a portable power station will run your devices. Account for inverter efficiency, capacity derating, and device power draw.",
        "is_coming_soon": False,
        "category": "Tools",
        "breadcrumb": ["Tools", "Runtime Calculator"],
    },
    "pages/tools/unit-converter.html": {
        "url": "/pages/tools/unit-converter.html",
        "title": "Unit Converter | TechSpecsHub",
        "description": "Technical unit converter for power stations, batteries, and electronics: watts, volts, amp-hours, watt-hours, temperature, and pressure.",
        "is_coming_soon": False,
        "category": "Tools",
        "breadcrumb": ["Tools", "Unit Converter"],
    },
    "pages/guides/drone-battery-care-guide.html": {
        "url": "/pages/guides/drone-battery-care-guide.html",
        "title": "DJI Drone Battery Care Guide 2026",
        "description": "Complete DJI drone battery care guide: charging best practices, storage temperature, cycle life extension, and LiPo safety for 2026.",
        "is_coming_soon": False,
        "category": "Guides",
        "breadcrumb": ["Guides", "Drone Battery Care"],
    },
    "pages/guides/hybrid-battery-replacement-cost.html": {
        "url": "/pages/guides/hybrid-battery-replacement-cost.html",
        "title": "Prius Hybrid Battery Replacement Cost 2026",
        "description": "Toyota Prius hybrid battery replacement cost 2026: OEM vs aftermarket options, labor rates, when to replace, and warranty considerations.",
        "is_coming_soon": False,
        "category": "Guides",
        "breadcrumb": ["Guides", "Hybrid Battery Cost"],
    },
    "pages/guides/portable-power-station-buying-guide.html": {
        "url": "/pages/guides/portable-power-station-buying-guide.html",
        "title": "Portable Power Station Buying Guide 2026",
        "description": "How to choose the right portable power station: capacity, output, solar input, battery chemistry, and brand comparison for 2026.",
        "is_coming_soon": False,
        "category": "Guides",
        "breadcrumb": ["Guides", "Power Station Buying Guide"],
    },
    "pages/compare/ecoflow-vs-bluetti-vs-jackery.html": {
        "url": "/pages/compare/ecoflow-vs-bluetti-vs-jackery.html",
        "title": "EcoFlow vs Bluetti vs Jackery | Power Station Comparison",
        "description": "Head-to-head comparison of EcoFlow, Bluetti, and Jackery portable power stations. Capacity, output, cycle life, and value analysis.",
        "is_coming_soon": False,
        "category": "Compare",
        "breadcrumb": ["Compare", "EcoFlow vs Bluetti vs Jackery"],
    },
    "pages/troubleshooting/p0a80-replace-hybrid-battery.html": {
        "url": "/pages/troubleshooting/p0a80-replace-hybrid-battery.html",
        "title": "P0A80 Repair Guide | Hybrid Battery",
        "description": "P0A80 fault code complete repair guide: Toyota Prius hybrid battery replacement with internal resistance testing, cell selection, and installation.",
        "is_coming_soon": False,
        "category": "Troubleshooting",
        "breadcrumb": ["Troubleshooting", "P0A80"],
    },
    "pages/privacy-policy.html": {
        "url": "/pages/privacy-policy.html",
        "title": "Privacy Policy | TechSpecsHub",
        "description": "TechSpecsHub privacy policy. How we collect, use, and protect your data. GDPR and CCPA compliant. Last updated May 2026.",
        "is_coming_soon": False,
        "category": "Legal",
        "breadcrumb": ["Privacy Policy"],
    },
}

# ============================================================
# Helper Functions
# ============================================================
def get_robots_meta(is_coming_soon: bool) -> str:
    if is_coming_soon:
        return '<meta name="robots" content="noindex, nofollow">'
    return '<meta name="robots" content="index, follow">'


def get_canonical_tag(page_url: str) -> str:
    return f'<link rel="canonical" href="{DOMAIN}{page_url}">'


def get_og_tags(title: str, description: str, page_url: str) -> str:
    return f'''  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{DOMAIN}{page_url}">
  <meta property="og:type" content="article">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:site_name" content="TechSpecsHub">
  <meta property="og:locale" content="en_US">'''


def get_twitter_tags(title: str, description: str) -> str:
    return f'''  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{OG_IMAGE}">'''


def get_breadcrumb_schema(fpath: str) -> str:
    """生成 BreadcrumbList Schema"""
    if fpath not in PAGES_META:
        return ""

    meta = PAGES_META[fpath]
    if not meta["breadcrumb"]:
        return ""

    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": f"{DOMAIN}/"}]

    position = 2
    if len(meta["breadcrumb"]) == 1:
        items.append({
            "@type": "ListItem",
            "position": 2,
            "name": meta["breadcrumb"][0],
            "item": f"{DOMAIN}{meta['url']}"
        })
    else:
        # 构建多级面包屑
        for i, crumb in enumerate(meta["breadcrumb"]):
            if i == len(meta["breadcrumb"]) - 1:
                # 最后一个是当前页
                items.append({
                    "@type": "ListItem",
                    "position": position,
                    "name": crumb,
                    "item": f"{DOMAIN}{meta['url']}"
                })
            else:
                # 中间层级，构造路径
                items.append({
                    "@type": "ListItem",
                    "position": position,
                    "name": crumb,
                    "item": f"{DOMAIN}{meta['url']}"
                })
            position += 1

    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items
    }
    return json.dumps(schema, indent=2)


def get_organization_schema() -> str:
    """首页 Organization Schema"""
    schema = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "TechSpecsHub",
        "url": f"{DOMAIN}/",
        "logo": f"{DOMAIN}/assets/images/logo.png",
        "description": "Technical specification database and fault-diagnosis reference for portable power stations, hybrid batteries, drones, and smart home devices.",
        "foundingDate": "2024",
        "sameAs": []
    }
    return json.dumps(schema, indent=2)


def get_howto_schema_p0a80() -> str:
    """P0A80 页面 HowTo Schema"""
    schema = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": "How to Diagnose and Replace a Hybrid Battery (P0A80 Code)",
        "description": "Step-by-step guide to diagnose P0A80 fault code and replace a Toyota Prius hybrid battery pack with internal resistance testing.",
        "totalTime": "PT4H",
        "estimatedCost": {
            "@type": "MonetaryAmount",
            "currency": "USD",
            "value": "2000-4500"
        },
        "tool": [
            {"@type": "HowToTool", "name": "Digital multimeter"},
            {"@type": "HowToTool", "name": "Insulated socket set (10mm, 12mm)"},
            {"@type": "HowToTool", "name": "Torque wrench"},
            {"@type": "HowToTool", "name": "High-voltage safety gloves (Class 0)"},
            {"@type": "HowToTool", "name": "OBD-II scanner"}
        ],
        "step": [
            {
                "@type": "HowToStep",
                "position": 1,
                "name": "Verify P0A80 code with OBD-II scanner",
                "text": "Connect an OBD-II scanner to the diagnostic port under the dashboard. Read the P0A80 code and confirm there are no related HV system faults (P0A7F, P0A82) that must be addressed first."
            },
            {
                "@type": "HowToStep",
                "position": 2,
                "name": "Disconnect 12V battery and wait 10 minutes",
                "text": "Turn off the ignition, remove the key, and disconnect the negative terminal of the 12V auxiliary battery. Wait at least 10 minutes for the high-voltage system capacitors to discharge before touching any HV components."
            },
            {
                "@type": "HowToStep",
                "position": 3,
                "name": "Remove hybrid battery cover",
                "text": "Fold down the rear seats and lift the cargo floor carpet. Remove the plastic battery cover by unscrewing the 4 retaining bolts. Set the cover aside in a clean area."
            },
            {
                "@type": "HowToStep",
                "position": 4,
                "name": "Test individual module voltages",
                "text": "With the battery exposed, use a digital multimeter to measure voltage across each of the 28 NiMH modules. Good modules read 7.0-7.5V. Any module reading below 6.5V or more than 0.3V below the average is suspect."
            },
            {
                "@type": "HowToStep",
                "position": 5,
                "name": "Test internal resistance of each module",
                "text": "Switch to milliohm mode on the multimeter. Probe each module's terminals. Healthy NiMH modules show 4-15 milliohms internal resistance. Replace modules exceeding 25 milliohms."
            },
            {
                "@type": "HowToStep",
                "position": 6,
                "name": "Source replacement modules or pack",
                "text": "Match modules from the same generation (Gen 2, 3, or 4) and similar production date code. Refurbished packs from reputable rebuilders are cost-effective; OEM new packs run $2,500-$4,500."
            },
            {
                "@type": "HowToStep",
                "position": 7,
                "name": "Install replacement pack and torque bus bars",
                "text": "Lower the replacement pack into the battery tray. Reconnect the bus bars in the original sequence, torquing each to 8 Nm (71 in-lb). Do not over-torque; the brass threads strip easily."
            },
            {
                "@type": "HowToStep",
                "position": 8,
                "name": "Reconnect 12V battery and clear P0A80",
                "text": "Reconnect the 12V battery negative terminal. Start the vehicle. Use the OBD-II scanner to clear P0A80. Drive the vehicle for at least 15 minutes to allow the BMS to recalibrate the new pack state of charge."
            }
        ]
    }
    return json.dumps(schema, indent=2)


def get_faq_schema() -> str:
    """错误代码数据库页 FAQPage Schema"""
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "What does the P0A80 error code mean on a Toyota Prius?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "P0A80 indicates 'Replace Hybrid Battery Pack' on Toyota Prius models. The HV ECU has detected that the hybrid battery pack has degraded below its operational threshold. Common causes include individual module voltage deviation exceeding 0.3V from the pack average, internal resistance above 25 milliohms per module, or capacity loss exceeding 30% of nominal."
                }
            },
            {
                "@type": "Question",
                "name": "How do I fix the MOTOR_HOT error on a DJI drone?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "MOTOR_HOT indicates the motor ESC has triggered thermal protection. Land immediately and power cycle. If persistent: (1) Inspect propellers for chips, cracks, or balance issues. (2) Check motor bearings for roughness. (3) Verify ESC firmware matches motor KV. (4) Test windings with a multimeter (all three phases should show 0.1-0.5 ohm). (5) Replace motor or ESC if winding resistance is open or shorted."
                }
            },
            {
                "@type": "Question",
                "name": "Why is my EcoFlow Delta Pro charging slowly after 2 years?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Slow charging on an aging EcoFlow LFP station is normal capacity fade, not a fault. LFP cells lose 2-3% capacity per year. Verify with: (1) Settings > AC charging speed should be on 'Max' not 'Custom'. (2) Charge at ambient 15-35 deg C; cold packs throttle. (3) Check BMS with EcoFlow app for cell voltage deviation. If one cell is >50mV below others, contact warranty."
                }
            },
            {
                "@type": "Question",
                "name": "What is the cycle life of an LFP battery vs NMC?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "LFP (LiFePO4) cells typically deliver 3,000-6,500 cycles to 80% capacity, while NMC (Nickel Manganese Cobalt) cells deliver 500-1,500 cycles. LFP operates safely at higher temperatures and is non-thermal-runaway. NMC has higher energy density (Wh/kg) but shorter life. For daily cycling, LFP is more cost-effective despite higher upfront cost."
                }
            },
            {
                "@type": "Question",
                "name": "How do I check internal resistance of a hybrid battery module?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Use a milliohm meter or a quality multimeter with milliohm mode (Fluke 87V recommended). Disconnect the module from the pack. Apply a 1A test current via the meter's test leads. Healthy Gen 3/4 Prius NiMH modules read 4-15 milliohms. Replace modules above 25 milliohms. Always wear Class 0 HV gloves and verify the system is de-energized."
                }
            },
            {
                "@type": "Question",
                "name": "What tools are required to diagnose drone motor issues?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Essential diagnostic tools: (1) Digital multimeter with continuity mode - test motor windings (3 phases should read balanced 0.1-0.5 ohm). (2) Propeller balancer - detect imbalance causing vibration. (3) Infrared thermometer - identify hot motors/ESCs under load. (4) Oscilloscope (advanced) - view ESC PWM signal integrity. (5) FC configurator software (Betaflight, INAV) - verify ESC protocol and motor direction."
                }
            }
        ]
    }
    return json.dumps(schema, indent=2)


def get_itemlist_schema_multimeters() -> str:
    """万用表指南页 ItemList Schema"""
    schema = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Best Multimeters 2026 - Top 4 Picks for EV & Electronics",
        "itemListOrder": "https://schema.org/ItemListOrderDescending",
        "numberOfItems": 4,
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "item": {
                    "@type": "Product",
                    "name": "Fluke 87V Digital Multimeter",
                    "description": "Industry-standard CAT III 1000V / CAT IV 600V multimeter with true-RMS, 0.05% DC accuracy, built-in thermometer, and 10,000 uF capacitance range.",
                    "brand": {"@type": "Brand", "name": "Fluke"},
                    "offers": {
                        "@type": "Offer",
                        "priceCurrency": "USD",
                        "price": "429.99",
                        "availability": "https://schema.org/InStock"
                    },
                    "aggregateRating": {
                        "@type": "AggregateRating",
                        "ratingValue": "4.9",
                        "reviewCount": "2847"
                    }
                }
            },
            {
                "@type": "ListItem",
                "position": 2,
                "item": {
                    "@type": "Product",
                    "name": "Klein Tools MM700 Digital Multimeter",
                    "description": "Professional CAT IV 600V / CAT III 1000V auto-ranging multimeter with true-RMS, 40M ohm resistance, and 10A current. Backlit display and magnetic hanger included.",
                    "brand": {"@type": "Brand", "name": "Klein Tools"},
                    "offers": {
                        "@type": "Offer",
                        "priceCurrency": "USD",
                        "price": "199.97",
                        "availability": "https://schema.org/InStock"
                    },
                    "aggregateRating": {
                        "@type": "AggregateRating",
                        "ratingValue": "4.7",
                        "reviewCount": "1523"
                    }
                }
            },
            {
                "@type": "ListItem",
                "position": 3,
                "item": {
                    "@type": "Product",
                    "name": "Fluke 117 Electricians Multimeter",
                    "description": "Compact CAT III 600V multimeter with non-contact voltage detection, low-impedance mode to prevent ghost voltages, and true-RMS. Ideal for electricians and field service.",
                    "brand": {"@type": "Brand", "name": "Fluke"},
                    "offers": {
                        "@type": "Offer",
                        "priceCurrency": "USD",
                        "price": "269.99",
                        "availability": "https://schema.org/InStock"
                    },
                    "aggregateRating": {
                        "@type": "AggregateRating",
                        "ratingValue": "4.8",
                        "reviewCount": "3201"
                    }
                }
            },
            {
                "@type": "ListItem",
                "position": 4,
                "item": {
                    "@type": "Product",
                    "name": "UNI-T UT61E+ Digital Multimeter",
                    "description": "Budget-friendly CAT III 600V true-RMS multimeter with PC connectivity, 22000 counts, and 0.1 milliohm resolution. Excellent value for hobbyists and bench work.",
                    "brand": {"@type": "Brand", "name": "UNI-T"},
                    "offers": {
                        "@type": "Offer",
                        "priceCurrency": "USD",
                        "price": "89.99",
                        "availability": "https://schema.org/InStock"
                    },
                    "aggregateRating": {
                        "@type": "AggregateRating",
                        "ratingValue": "4.5",
                        "reviewCount": "892"
                    }
                }
            }
        ]
    }
    return json.dumps(schema, indent=2)


def get_website_schema() -> str:
    """首页 WebSite Schema (with SearchAction)"""
    schema = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "TechSpecsHub",
        "url": f"{DOMAIN}/",
        "description": "Technical specification database and fault-diagnosis reference for portable power stations, hybrid batteries, drones, and smart home devices.",
        "potentialAction": {
            "@type": "SearchAction",
            "target": {
                "@type": "EntryPoint",
                "urlTemplate": f"{DOMAIN}/search?q={{search_term_string}}"
            },
            "query-input": "required name=search_term_string"
        },
        "publisher": {
            "@type": "Organization",
            "name": "TechSpecsHub",
            "url": f"{DOMAIN}/",
            "logo": {
                "@type": "ImageObject",
                "url": f"{DOMAIN}/assets/images/logo.png"
            }
        }
    }
    return json.dumps(schema, indent=2)


def get_articleschema_for_page(fpath: str) -> str:
    """为内容页生成 Article Schema"""
    if fpath not in PAGES_META:
        return ""

    meta = PAGES_META[fpath]
    schema = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": meta["title"],
        "description": meta["description"],
        "url": f"{DOMAIN}{meta['url']}",
        "datePublished": "2026-05-01",
        "dateModified": TODAY,
        "author": {
            "@type": "Organization",
            "name": "TechSpecsHub",
            "url": f"{DOMAIN}/"
        },
        "publisher": {
            "@type": "Organization",
            "name": "TechSpecsHub",
            "logo": {
                "@type": "ImageObject",
                "url": f"{DOMAIN}/assets/images/logo.png"
            }
        },
        "image": OG_IMAGE
    }
    return json.dumps(schema, indent=2)


def build_seo_head(fpath: str) -> str:
    """构建完整的 SEO head 注入块"""
    if fpath not in PAGES_META:
        return ""

    meta = PAGES_META[fpath]
    title = meta["title"]
    description = meta["description"]
    page_url = meta["url"]
    is_coming_soon = meta["is_coming_soon"]

    # 基础 SEO 标签
    seo_block = []
    seo_block.append(get_robots_meta(is_coming_soon))
    seo_block.append(get_canonical_tag(page_url))
    seo_block.append(get_og_tags(title, description, page_url))
    seo_block.append(get_twitter_tags(title, description))

    return "\n  ".join(seo_block)


def build_schema_block(fpath: str) -> str:
    """构建页面的所有 Schema 块"""
    if fpath not in PAGES_META:
        return ""

    meta = PAGES_META[fpath]
    schemas = []

    # BreadcrumbList (所有非首页)
    if meta["breadcrumb"]:
        breadcrumb = get_breadcrumb_schema(fpath)
        if breadcrumb:
            schemas.append(f'<script type="application/ld+json">\n{breadcrumb}\n</script>')

    # 特定页面 Schema
    if fpath == "index.html":
        org_schema = get_organization_schema()
        web_schema = get_website_schema()
        schemas.append(f'<script type="application/ld+json">\n{org_schema}\n</script>')
        schemas.append(f'<script type="application/ld+json">\n{web_schema}\n</script>')
    elif fpath == "pages/troubleshooting/p0a80-replace-hybrid-battery.html":
        howto = get_howto_schema_p0a80()
        schemas.append(f'<script type="application/ld+json">\n{howto}\n</script>')
    elif fpath == "pages/error-code-db.html":
        faq = get_faq_schema()
        schemas.append(f'<script type="application/ld+json">\n{faq}\n</script>')
    elif fpath == "pages/tools/best-multimeters-2026.html":
        itemlist = get_itemlist_schema_multimeters()
        schemas.append(f'<script type="application/ld+json">\n{itemlist}\n</script>')
    elif not meta["is_coming_soon"] and meta["breadcrumb"]:
        # 为其他非占位内容页添加 Article Schema
        article = get_articleschema_for_page(fpath)
        if article:
            schemas.append(f'<script type="application/ld+json">\n{article}\n</script>')

    return "\n".join(schemas)


def get_coming_soon_banner() -> str:
    """Coming Soon 页面顶部用户可见提示"""
    return '''
  <div class="coming-soon-banner bg-yellow-500/10 border border-yellow-500/30 text-yellow-300 px-4 py-3 text-center text-sm">
    <i data-lucide="info" class="inline w-4 h-4 mr-1"></i>
    <strong>This page is still being developed.</strong>
    Please visit our <a href="/pages/error-code-db.html" class="underline hover:text-yellow-200">Error Code Database</a> or
    <a href="/pages/master-specs.html" class="underline hover:text-yellow-200">Master Specs Comparison</a> for the most complete data.
  </div>'''


def get_breadcrumb_html(fpath: str) -> str:
    """生成可见的面包屑 HTML"""
    if fpath not in PAGES_META:
        return ""

    meta = PAGES_META[fpath]
    if not meta["breadcrumb"]:
        return ""

    parts = ['<a href="/" class="hover:text-electric-400 transition-colors">Home</a>']
    for i, crumb in enumerate(meta["breadcrumb"]):
        if i == len(meta["breadcrumb"]) - 1:
            # 最后一个，当前页，不可点击
            parts.append(f'<span class="text-gray-500">/</span><span class="text-gray-400">{crumb}</span>')
        else:
            # 中间层级
            parts.append(f'<span class="text-gray-500">/</span><a href="/pages/{meta["category"].lower()}/" class="hover:text-electric-400 transition-colors">{crumb}</a>')

    return f'''
  <nav aria-label="Breadcrumb" class="bg-navy-900/50 border-b border-white/10">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
      <ol class="flex items-center gap-1.5 text-sm text-gray-300" itemscope itemtype="https://schema.org/BreadcrumbList">
        <li><span class="text-gray-500">{"".join(parts[:1])}</span></li>
        {"".join([f'<li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem"><meta itemprop="position" content="{i+1}"><span class="text-gray-500">{p}</span></li>' for i, p in enumerate(parts[1:], 1)])}
      </ol>
    </div>
  </nav>'''


def inject_seo_into_html(fpath: str) -> bool:
    """向 HTML 文件注入 SEO 标签和 Schema"""
    if fpath not in PAGES_META:
        return False

    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    meta = PAGES_META[fpath]
    original = content

    # 1. 注入 head 标签（在 </head> 之前）
    seo_block = build_seo_head(fpath)
    if seo_block:
        # 找到 <head> 结束标签前插入
        if '</head>' in content:
            content = content.replace('</head>', f'  {seo_block}\n</head>', 1)

    # 2. 注入 Schema (在 </body> 之前)
    schema_block = build_schema_block(fpath)
    if schema_block:
        if '</body>' in content:
            content = content.replace('</body>', f'\n{schema_block}\n</body>', 1)

    # 3. Coming Soon 页面：插入提示横幅
    if meta["is_coming_soon"]:
        banner = get_coming_soon_banner()
        if 'coming-soon-banner' not in content:
            # 在 <body> 标签后插入
            content = re.sub(
                r'(<body[^>]*>)',
                r'\1' + banner,
                content,
                count=1
            )

    # 4. 添加面包屑（在 <body> 标签后，但 Coming Soon 横幅前）
    if meta["breadcrumb"]:
        breadcrumb = get_breadcrumb_html(fpath)
        if breadcrumb and 'aria-label="Breadcrumb"' not in content:
            if meta["is_coming_soon"] and 'coming-soon-banner' in content:
                # 在横幅之后插入
                content = content.replace(
                    '</div>\n  <!-- ═',
                    '</div>' + breadcrumb + '\n  <!-- ═',
                    1
                ) if '</div>\n  <!-- ═' in content else content
            else:
                # 在 <body> 后直接插入
                content = re.sub(
                    r'(<body[^>]*>)',
                    r'\1' + breadcrumb,
                    content,
                    count=1
                )

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


# ============================================================
# Main Execution
# ============================================================
if __name__ == "__main__":
    print("="*80)
    print("  TechSpecsHub SEO 增强脚本")
    print("="*80)

    success_count = 0
    skip_count = 0

    for fpath in PAGES_META.keys():
        if not os.path.exists(fpath):
            print(f"  ⚠️  跳过（文件不存在）: {fpath}")
            skip_count += 1
            continue

        if inject_seo_into_html(fpath):
            print(f"  ✓ {fpath}")
            success_count += 1
        else:
            print(f"  - {fpath} (无变化)")
            skip_count += 1

    print(f"\n完成: {success_count} 个文件已增强, {skip_count} 个跳过")
