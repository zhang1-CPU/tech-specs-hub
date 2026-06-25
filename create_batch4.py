#!/usr/bin/env python3
"""Generate batch 4: pages 6-8 - slow charging, overheating, extension cords."""

import os, json, html, re
from typing import List, Dict, Any

OUTPUT_DIR = "/workspace/pages/specs"
BASE_URL = "https://powerspecshub.com/pages/specs"
SITE_NAME = "TechSpecsHub"
UPDATED_DATE = "2026-06-25"

def p(text): return f'<p class="text-gray-300 leading-relaxed mb-4">{text}</p>'
def alert(t, icon, title, text):
    return f'<div class="alert alert-{t}"><i data-lucide="{icon}" style="width:1rem;height:1rem;flex-shrink:0;margin-top:0.1rem"></i><p class="text-sm"><strong>{title}:</strong> {text}</p></div>'
def specs_table(headers, rows):
    thead = "".join(f"<th>{h}</th>" for h in headers)
    tbody = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="overflow-x-auto mb-6"><table class="specs-table w-full text-sm"><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table></div>'
def step_grid(steps, color="green"):
    s = '<div class="space-y-4">'
    for i, st in enumerate(steps, 1):
        s += f'<div class="flex items-start gap-3"><div class="w-10 h-10 bg-{color}-500/20 rounded-full flex items-center justify-center flex-shrink-0"><span class="font-mono font-bold text-{color}-400">{i}</span></div><div><h4 class="font-semibold text-white">{st["title"]}</h4><p class="text-sm text-gray-400">{st["desc"]}</p></div></div>'
    s += "</div>"
    return s
def grid_cards(cards, cols=2):
    s = f'<div class="grid md:grid-cols-{cols} gap-4">'
    for c in cards:
        s += f'<div class="bg-navy-900/80 border border-white/10 rounded-xl p-5"><h4 class="font-semibold {c.get("color","text-electric-400")} mb-2">{c["title"]}</h4><p class="text-sm text-gray-300">{c["desc"]}</p></div>'
    s += "</div>"
    return s
def section(sid, title, content):
    return f'  <section id="{sid}" class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6"><h2 class="font-bold text-3xl mb-5">{title}</h2><div class="glass-card p-6 md:p-8">{content}</div></section>'

def build_header(title, meta_desc, canonical, article_json, faq_json, breadcrumb_json):
    og_image = "https://powerspecshub.com/assets/images/og-default.png"
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)} | {SITE_NAME}</title>
  <meta name="description" content="{html.escape(meta_desc)}">
  <meta name="theme-color" content="#0a1628">
  <style>html,body{{background-color:#0a1628;color:#ffffff;margin:0;padding:0;min-height:100vh;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;line-height:1.5;-webkit-font-smoothing:antialiased}}a{{color:#22d3ee;text-decoration:none}}code,pre{{font-family:ui-monospace,monospace}}</style>
  <link rel="preconnect" href="https://cdn.tailwindcss.com">
  <link rel="preconnect" href="https://unpkg.com">
  <link rel="dns-prefetch" href="https://cdn.tailwindcss.com">
  <link rel="dns-prefetch" href="https://unpkg.com">
  <link rel="dns-prefetch" href="https://fonts.gstatic.com">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{html.escape(title)} | {SITE_NAME}">
  <meta property="og:description" content="{html.escape(meta_desc)}">
  <meta property="og:type" content="Article">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{og_image}">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="article:published_time" content="{UPDATED_DATE}T00:00:00Z">
  <meta property="article:modified_time" content="{UPDATED_DATE}T00:00:00Z">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)} | {SITE_NAME}">
  <meta name="twitter:description" content="{html.escape(meta_desc)}">
  <meta name="twitter:image" content="{og_image}">
  <meta name="twitter:site" content="@TechSpecsHub">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com" defer></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          colors: {{
            navy: {{ 950:'#0a1628', 900:'#0f1d32', 800:'#162544', 700:'#1e3259' }},
            electric: {{ 300:'#67e8f9', 400:'#22d3ee', 500:'#06b6d4', 600:'#0891b2' }}
          }},
          fontFamily: {{
            display: ['Space Grotesk','system-ui','sans-serif'],
            mono: ['JetBrains Mono','monospace']
          }}
        }}
      }}
    }}
  </script>
  <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js" defer></script>
  <link rel="stylesheet" href="../../assets/css/main.css">
  <script type="application/ld+json">
  {json.dumps(article_json, indent=2)}
  </script>
  <script type="application/ld+json">
  {json.dumps(faq_json, indent=2)}
  </script>
  <script type="application/ld+json">
  {json.dumps(breadcrumb_json, indent=2)}
  </script>
</head>'''

template = open("/workspace/pages/specs/portable-power-station-eco-mode.html").read()
BODY_HEADER = template.split('''<body class="bg-navy-950 text-white min-h-screen font-display">''')[1].split('''  <!-- BREADCRUMB -->''')[0]
FOOTER = template.split('''  <!-- FOOTER -->''')[1].replace("<!-- FOOTER -->", "  <!-- FOOTER -->")

def faq_details(faqs):
    s = '''  <section id="faq" class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="text-center mb-10">
      <h2 class="font-bold text-3xl md:text-4xl mb-4">Frequently Asked Questions</h2>
      <p class="text-gray-400">Common questions answered by our experts.</p>
    </div>
    <div class="space-y-3">'''
    for q in faqs:
        s += f'''      <details class="glass-card p-5 group">
        <summary class="cursor-pointer font-semibold flex items-center justify-between gap-4">
          <span>{q["q"]}</span>
          <i data-lucide="chevron-down" style="width:1rem;height:1rem" class="text-gray-500 group-open:rotate-180 transition-transform flex-shrink-0"></i>
        </summary>
        <p class="mt-3 text-gray-400 text-sm leading-relaxed">{q["a"]}</p>
      </details>'''
    s += '''    </div>
  </section>'''
    return s

def related_guides(cards):
    s = '''  <section id="related" class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h2 class="font-bold text-3xl mb-5">Related Guides &amp; Resources</h2>
    <div class="grid md:grid-cols-3 gap-4">'''
    for c in cards:
        s += f'''      <a href="{c["href"]}" class="glass-card p-6 block hover:border-electric-400/50 transition-all group">
        <div class="flex items-start gap-3 mb-3">
          <div class="px-2.5 py-1 {c["badge_class"]} font-mono font-semibold text-sm rounded-md border {c["border_class"]}">{c["badge"]}</div>
          <span class="badge badge-info">{c["badge2"]}</span>
        </div>
        <h3 class="font-bold text-lg mb-2 group-hover:text-electric-400 transition-colors">{c["title"]}</h3>
        <p class="text-sm text-gray-400">{c["desc"]}</p>
      </a>'''
    s += '''    </div>
  </section>'''
    return s

def build_page(pd):
    canonical = f"{BASE_URL}/{pd['filename']}"
    article_json = {"@context":"https://schema.org","@type":"Article","headline":pd["headline"],"description":pd["meta_desc"],"url":canonical,"datePublished":UPDATED_DATE,"dateModified":UPDATED_DATE,"author":{"@type":"Organization","name":SITE_NAME},"publisher":{"@type":"Organization","name":SITE_NAME,"url":"https://powerspecshub.com/"},"image":{"@type":"ImageObject","url":"https://powerspecshub.com/assets/images/og-default.png"}}
    faq_json = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q["q"],"acceptedAnswer":{"@type":"Answer","text":q["a"]}} for q in pd["faqs"]]}
    breadcrumb_json = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://powerspecshub.com/"},{"@type":"ListItem","position":2,"name":pd["category"],"item":f"https://powerspecshub.com/pages/specs/{pd['category_link']}"},{"@type":"ListItem","position":3,"name":pd["breadcrumb_title"]}]}
    head = build_header(pd["title"], pd["meta_desc"], canonical, article_json, faq_json, breadcrumb_json)
    breadcrumb_html = f'''  <!-- BREADCRUMB -->
  <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 pb-4">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="../../index.html">Home</a>
      <span class="breadcrumb-sep">/</span>
      <a href="{pd["category_link"]}">{pd["category"]}</a>
      <span class="breadcrumb-sep">/</span>
      <span class="breadcrumb-current">{pd["breadcrumb_title"]}</span>
    </nav>
  </div>'''
    hero_html = f'''  <!-- HERO -->
  <section class="relative max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-4 pb-6">
    <div class="glass-card p-8 md:p-10 overflow-hidden relative">
      <div class="absolute top-0 right-0 w-[420px] h-[420px] {pd["hero_blur"]} rounded-full blur-3xl pointer-events-none"></div>
      <div class="relative flex flex-wrap items-center gap-3 mb-5">{pd["hero_badges"]}</div>
      <h1 class="font-bold text-4xl md:text-5xl mb-4 leading-tight">{pd["h1"]}</h1>
      <p class="text-gray-400 text-lg leading-relaxed mb-6 max-w-3xl">{pd["hero_desc"]}</p>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8">{pd["hero_stats"]}</div>
    </div>
  </section>'''
    qa_html = f'''  <!-- QUICK ANSWER -->
  <section class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div class="glass-card p-6 md:p-8 bg-gradient-to-br {pd["qa_gradient"]}">
      <h2 class="font-bold text-2xl mb-4 flex items-center gap-2"><i data-lucide="zap" style="width:1.25rem;height:1.25rem;color:{pd["qa_icon_color"]}"></i>Quick Answer: {pd["qa_title"]}</h2>
      <p class="text-gray-300 leading-relaxed mb-4">{pd["qa_text"]}</p>
      {pd["qa_extra"]}
    </div>
  </section>'''
    toc_items = "".join(f'<a href="#{s["id"]}" class="flex items-center gap-2 p-2 rounded-lg hover:bg-white/5 text-gray-300 hover:text-white transition-all"><span class="text-electric-400 font-mono">{i:02d}</span>{s["title"]}</a>' for i, s in enumerate(pd["sections"], 1))
    toc_html = f'''  <!-- TABLE OF CONTENTS -->
  <section class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div class="glass-card p-6 md:p-8">
      <h2 class="font-bold text-2xl mb-4 flex items-center gap-2"><i data-lucide="list" style="width:1.25rem;height:1.25rem;color:#22d3ee"></i>Table of Contents</h2>
      <div class="grid md:grid-cols-2 gap-2 text-sm">
        {toc_items}
        <a href="#faq" class="flex items-center gap-2 p-2 rounded-lg hover:bg-white/5 text-gray-300 hover:text-white transition-all"><span class="text-electric-400 font-mono">{len(pd["sections"])+1:02d}</span>Frequently Asked Questions</a>
        <a href="#related" class="flex items-center gap-2 p-2 rounded-lg hover:bg-white/5 text-gray-300 hover:text-white transition-all"><span class="text-electric-400 font-mono">{len(pd["sections"])+2:02d}</span>Related Guides</a>
      </div>
    </div>
  </section>'''
    sections_html = "\n".join(section(s["id"], s["title"], s["content"]) for s in pd["sections"])
    return head + BODY_HEADER + breadcrumb_html + hero_html + qa_html + toc_html + sections_html + faq_details(pd["faqs"]) + related_guides(pd["related"]) + FOOTER

def gen_related_basic(cat="outdoor-power.html"):
    return [
        {"href": "portable-power-station-not-charging.html", "badge": "CHARGING", "badge_class": "bg-yellow-500/20 text-yellow-400", "border_class": "border-yellow-500/30", "badge2": "Troubleshoot", "title": "Not Charging", "desc": "Troubleshoot why your power station is not charging — common causes and step-by-step fixes."},
        {"href": "portable-power-station-eco-mode.html", "badge": "ECO&nbsp;MODE", "badge_class": "bg-green-500/20 text-green-400", "border_class": "border-green-500/30", "badge2": "Guide", "title": "ECO Mode Guide", "desc": "What is ECO mode, how much battery it saves, how to disable it, and optimization tips."},
        {"href": "how-to-store-portable-power-station.html", "badge": "STORAGE", "badge_class": "bg-blue-500/20 text-blue-400", "border_class": "border-blue-500/30", "badge2": "Guide", "title": "Storage Guide", "desc": "How to store a portable power station long-term — ideal charge level, temperature, cycling schedule."},
        {"href": "lifepo4-vs-lithium-ion-power-station.html", "badge": "LFP&nbsp;vs&nbsp;NMC", "badge_class": "bg-purple-500/20 text-purple-400", "border_class": "border-purple-500/30", "badge2": "Comparison", "title": "LFP vs Lithium-Ion", "desc": "Complete comparison of LiFePO4 vs lithium-ion batteries — cycle life, safety, cost, and density."},
        {"href": "portable-power-station-output-not-working.html", "badge": "OUTPUT", "badge_class": "bg-red-500/20 text-red-400", "border_class": "border-red-500/30", "badge2": "Troubleshoot", "title": "Output Not Working", "desc": "Troubleshoot AC, USB, and DC port failures — ECO mode, overload, app settings, inverter issues."},
        {"href": cat, "badge": "ALL&nbsp;GUIDES", "badge_class": "bg-electric-500/20 text-electric-400", "border_class": "border-electric-500/30", "badge2": "Category", "title": "Outdoor Power Hub", "desc": "Browse all portable power station guides, comparisons, specs, and troubleshooting resources."},
    ]

# =================== PAGE 6: SLOW CHARGING ===================

page6 = {
    "filename": "why-is-my-power-station-charging-so-slow.html",
    "title": "Why Is My Power Station Charging So Slow? Causes & Fixes (2026)",
    "headline": "Why Is My Power Station Charging So Slow? Causes & Fixes (2026)",
    "meta_desc": "Why is your portable power station charging so slow? Complete troubleshooting guide covering solar angle, cable gauge, temperature, charge mode, battery health, and how to speed up charging.",
    "category": "Outdoor Power",
    "category_link": "outdoor-power.html",
    "breadcrumb_title": "Slow Charging Fixes",
    "hero_blur": "bg-orange-500/5",
    "hero_badges": '''<div class="px-3 py-1.5 bg-orange-500/20 text-orange-400 font-mono font-bold text-sm rounded-md border border-orange-500/30">SLOW&nbsp;CHARGE</div>
        <span class="badge badge-info"><i data-lucide="zap" style="width:0.75rem;height:0.75rem"></i>Troubleshooting</span>
        <span class="badge badge-info"><i data-lucide="sun" style="width:0.75rem;height:0.75rem"></i>Solar &amp; AC</span>''',
    "h1": 'Why Is My Power Station Charging So Slow? &mdash; <span class="gradient-text">Causes &amp; Fixes 2026</span>',
    "hero_desc": "Slow charging is one of the most frustrating issues with portable power stations. You plug it in, wait hours, and it barely gained any charge. But before you assume the worst (battery failure!), there are many common causes that are easy to fix. This guide walks through every possible reason for slow charging — from solar panel angle to cable thickness to temperature — with step-by-step troubleshooting and tips to maximize charging speed.",
    "hero_stats": f'''<div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="thermometer" style="width:0.9rem;height:0.9rem"></i>Temp Range</div>
          <div class="font-mono font-bold text-xl text-green-400">10&ndash;35&deg;C</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="sun" style="width:0.9rem;height:0.9rem"></i>Solar Angle</div>
          <div class="font-bold text-xl text-yellow-400">Perpendicular</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="cable" style="width:0.9rem;height:0.9rem"></i>Cable Gauge</div>
          <div class="font-mono font-bold text-xl text-electric-400">12&ndash;10&nbsp;AWG</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="activity" style="width:0.9rem;height:0.9rem"></i>Charge Modes</div>
          <div class="font-bold text-xl text-purple-400">2&ndash;4 modes</div>
        </div>''',
    "qa_gradient": "from-orange-950/20 to-navy-900 border-orange-500/20",
    "qa_icon_color": "#fb923c",
    "qa_title": "Why Is Charging So Slow?",
    "qa_text": '<strong class="text-white">The most common causes of slow charging are: incorrect solar panel angle, dirty panels, thin/long cables, extreme temperatures, wrong charge mode settings, and partial shading.</strong> For AC charging, slow speeds are usually caused by using the wrong charger, charging mode set to silent/eco, or battery temperature being too hot or cold. Before worrying about battery health, check the simple stuff first: solar angle, cable connections, temperature, and charge settings. 80% of slow charging issues are easy fixes that take 5 minutes.',
    "qa_extra": f'''<div class="grid md:grid-cols-2 gap-3 mt-4">
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-green-400 font-semibold mb-1 flex items-center gap-2"><i data-lucide="check" style="width:1rem;height:1rem"></i>Quick checks first</div>
          <p class="text-sm text-gray-300">Solar angle, cable connections, panel cleanliness, charge mode setting, app notifications, temperature display</p>
        </div>
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-yellow-400 font-semibold mb-1 flex items-center gap-2"><i data-lucide="alert-triangle" style="width:1rem;height:1rem"></i>When to worry</div>
          <p class="text-sm text-gray-300">If you have ruled out all simple causes and charging is still 50%+ slower than it used to be, battery degradation may be the cause.</p>
        </div>
      </div>''',
    "sections": [
        {
            "id": "solar-angle",
            "title": "Solar Panel Angle & Orientation",
            "content": p("If you are charging via solar, the #1 cause of slow charging is incorrect panel angle. Solar panels produce the most power when sunlight hits them directly (perpendicular to the panel surface). Even a small angle difference can significantly reduce output.") +
            specs_table(
                ["Angle Off Perfect", "Power Output Loss", "Real-World Impact"],
                [
                    ["<strong>0° (perfect)</strong>", "0% loss", "Full rated output"],
                    ["<strong>15° off</strong>", "~3.5% loss", "Almost unnoticeable"],
                    ["<strong>30° off</strong>", "~13% loss", "Noticeable but not terrible"],
                    ["<strong>45° off</strong>", "~30% loss", "Significant slowdown"],
                    ["<strong>60° off</strong>", "~50% loss", "Half the charging speed"],
                    ["<strong>90° (edge-on)</strong>", "~90%+ loss", "Barely charges at all"],
                ]
            ) +
            p("This is why laying solar panels flat on the ground is usually not optimal. The sun is low in the morning and evening, so flat panels get indirect light. Angling the panels toward the sun makes a huge difference in total daily production.") +
            step_grid([
                {"title": "How to Optimize Solar Angle", "desc": "Tilt your panels so they face the sun directly. For fixed setups, angle = your latitude (roughly). For portable panels, adjust them every 1-2 hours as the sun moves. Even better: use a solar panel stand or mount that lets you easily adjust the angle throughout the day."},
                {"title": "Direction Matters Too", "desc": "In the northern hemisphere, panels should face true south (not magnetic south — there is a small difference). In the southern hemisphere, face north. East-facing panels produce more in the morning, west-facing more in the afternoon. South-facing gives the most total daily production."},
                {"title": "Seasonal Adjustments", "desc": "The sun is higher in summer and lower in winter. In summer, tilt your panels at a shallower angle (latitude - 15°). In winter, steeper angle (latitude + 15°). For year-round use, set it to your latitude and adjust seasonally."},
            ], "yellow") +
            alert("info", "sun", "Pro tip for portable panels", "If you have portable folding panels, do not just lay them on the ground. Prop them up at an angle using the built-in kickstand (if they have one) or lean them against something. Even a 30° angle is way better than flat. You can easily double your daily solar production just by angling the panels properly.")
        },
        {
            "id": "cable-gauge",
            "title": "Cable Gauge & Length — Voltage Drop",
            "content": p("Thin or long charging cables cause voltage drop, which means less power actually reaches your power station. This is especially important for solar charging where the voltage is relatively low to begin with. Using the right cable gauge can make a dramatic difference in charging speed.") +
            specs_table(
                ["Cable Gauge (AWG)", "Max Current (10 ft)", "Max Current (20 ft)", "Max Current (50 ft)"],
                [
                    ["<strong>18 AWG</strong>", "7A", "3.5A", "1.4A", "Low-power devices only"],
                    ["<strong>16 AWG</strong>", "13A", "6.5A", "2.6A", "Small solar setups (≤200W 12V)"],
                    ["<strong>14 AWG</strong>", "20A", "10A", "4A", "Medium solar (≤300W 12V)"],
                    ["<strong>12 AWG</strong>", "30A", "15A", "6A", "Most portable solar setups"],
                    ["<strong>10 AWG</strong>", "50A", "25A", "10A", "High-power solar / fast charging"],
                    ["<strong>8 AWG</strong>", "75A", "37.5A", "15A", "Very high-power systems"],
                ]
            ) +
            p("The general rule: shorter and thicker is always better. If you are using an extension cable between your solar panels and power station, make sure it is thick enough for the current and length. Using a cable that is too thin wastes power as heat — literally throwing away solar energy.") +
            step_grid([
                {"title": "How to Tell What Gauge Cable You Have", "desc": "Most cables have the gauge printed on the insulation. Look for text like '16AWG' or '12AWG'. If it is not printed, you can measure the diameter or look up the cable model online. Cables that came with your panels are usually correctly sized, but cheap aftermarket cables might be thinner than they claim."},
                {"title": "Solar Extension Cables", "desc": "If you need to extend your solar panel cables, use properly rated solar extension cables (PV wire). They are designed for outdoor use, UV-resistant, and correctly sized. Avoid using random extension cords you have lying around — they might be too thin and will waste power."},
                {"title": "AC Charging Cables", "desc": "For AC wall charging, cable gauge is less critical because AC operates at higher voltage (120V), so current is lower for the same power. However, using a very long or thin extension cord can still cause issues, especially with high-wattage charging (1,000W+). Use 14-gauge or thicker for AC charging if using an extension cord."},
            ], "blue") +
            alert("warning", "flame", "Safety note: undersized cables", "Using a cable that is too thin is not just inefficient — it can be dangerous. The wasted power becomes heat, and in extreme cases, undersized cables can melt or cause fires. Always use appropriately sized cables for the current you are carrying. This applies to both solar (DC) and wall (AC) charging.")
        },
        {
            "id": "temperature",
            "title": "Temperature Effects on Charging Speed",
            "content": p("Temperature has a massive effect on both charging speed and battery health. Lithium batteries have an optimal temperature range for charging, and going outside it causes the BMS (Battery Management System) to slow down or stop charging entirely to protect the battery.") +
            '<div class="grid md:grid-cols-2 gap-6 mb-6">' +
            '<div>' +
            '<h3 class="font-bold text-xl mb-4 text-red-400 flex items-center gap-2"><i data-lucide="thermometer-sun" style="width:1.25rem;height:1.25rem"></i>Hot Weather</h3>' +
            '<ul class="space-y-3 text-sm text-gray-300">' +
            '<li>• <strong class="text-white">Above 35°C (95°F):</strong> Charging speed starts to slow down</li>' +
            '<li>• <strong class="text-white">Above 45°C (113°F):</strong> Charging may stop completely</li>' +
            '<li>• <strong class="text-white">Why:</strong> Heat accelerates battery degradation. The BMS slows charging to prevent damage</li>' +
            '<li>• <strong class="text-white">Solar panels also get hot:</strong> Panel efficiency drops by about 0.5% per °C above 25°C. A panel at 50°C produces 10-12% less than at 25°C</li>' +
            '<li>• <strong class="text-white">Fix:</strong> Move the power station to shade, provide ventilation, wait for it to cool down. Charge in the morning or evening when it is cooler</li>' +
            '</ul></div>' +
            '<div>' +
            '<h3 class="font-bold text-xl mb-4 text-blue-400 flex items-center gap-2"><i data-lucide="thermometer-snowflake" style="width:1.25rem;height:1.25rem"></i>Cold Weather</h3>' +
            '<ul class="space-y-3 text-sm text-gray-300">' +
            '<li>• <strong class="text-white">Below 10°C (50°F):</strong> Charging speed starts to slow</li>' +
            '<li>• <strong class="text-white">Below 0°C (32°F):</strong> Most LFP batteries stop charging entirely</li>' +
            '<li>• <strong class="text-white">Why:</strong> Charging lithium batteries when they are too cold causes lithium plating on the anode, which permanently reduces capacity and can cause safety issues</li>' +
            '<li>• <strong class="text-white">Some stations have low-temp charging:</strong> Premium models may have battery heaters that warm the battery before charging</li>' +
            '<li>• <strong class="text-white">Fix:</strong> Bring the station inside to warm up, use a battery warmer, or wait for warmer temperatures. Never force charging below freezing.</li>' +
            '</ul></div></div>' +
            p("The ideal charging temperature range for most lithium batteries is 10-35°C (50-95°F). Within this range, you get full charging speed and minimal battery degradation. Outside this range, expect slower charging as the BMS protects the battery.") +
            alert("info", "thermometer", "Checking battery temperature", "Most smart power stations display the battery temperature in the companion app or on the unit's display. If charging is slow, check the temperature first. If it is outside the optimal range, you know the cause and can take steps to warm up or cool down the unit.")
        },
        {
            "id": "charge-mode",
            "title": "Charge Mode Settings",
            "content": p("Many portable power stations have multiple charging modes that trade off between speed and noise/battery wear. If your station is charging slowly, check if it is set to a slower charging mode.") +
            specs_table(
                ["Charge Mode", "Speed", "Noise Level", "Battery Impact", "Best For"],
                [
                    ["<strong>Silent / Quiet</strong>", "Slowest", "Very quiet", "Gentlest on battery", "Nighttime, indoor use"],
                    ["<strong>Standard / Normal</strong>", "Moderate", "Moderate", "Balanced", "Most situations"],
                    ["<strong>Fast / Turbo</strong>", "Fastest", "Loudest (fan)", "Slightly more wear", "When you need power fast"],
                    ["<strong>Custom / App</strong>", "Adjustable", "Depends", "You control", "Fine-tuning to your needs"],
                ]
            ) +
            p("Higher charging speeds generate more heat, so the fan runs faster and louder. If you charged in silent mode overnight expecting to wake up to a full battery, you might be surprised at how little it charged. The tradeoff is worth it if you value quiet over speed, but it is important to know what mode you are in.") +
            step_grid([
                {"title": "How to Check/Change Charge Mode", "desc": "On most smart stations, you can change the charge mode in the companion app (Settings → Charging → Charge Mode). Some units also have physical buttons or a touchscreen menu. EcoFlow uses Silent/Standard/Turbo. Bluetti uses Quiet/Standard/Fast. Jackery sometimes has a charge speed button. Check your manual for the exact procedure."},
                {"title": "Charging Current Limit", "desc": "Some power stations let you set a custom charging current limit. This is useful if you are plugged into a circuit that cannot handle the full charging current (like a 15A household circuit). But if you accidentally set it low, charging will be slow. Check the app to make sure the current limit is set to maximum for your use case."},
                {"title": "Charge Limit (Not Charging Speed)", "desc": "Do not confuse charge mode (speed) with charge limit (how full the battery charges). Many people set a charge limit of 80-90% to extend battery life and then forget about it. If your station stops at 80% and you wonder why it is 'not charging fully,' check your charge limit setting. This is a feature, not a bug!"},
            ], "purple") +
            alert("info", "settings", "Battery health optimization", "Many newer power stations have a 'battery health optimization' or 'smart charging' feature that limits charging to 80% or charges slowly to extend battery life. If you enabled this feature and then forgot about it, you might think charging is slow or incomplete. Check the app to see if this is enabled and disable it if you need full capacity.")
        },
        {
            "id": "battery-health",
            "title": "Battery Health & Degradation",
            "content": p("After ruling out all the simple causes, the last possibility is that the battery has degraded over time. All lithium batteries lose capacity as they age — this is normal and expected. But significant degradation can cause slower charging in addition to reduced runtime.") +
            specs_table(
                ["Battery Age/Cycles", "Typical Capacity Remaining", "Charging Speed Impact"],
                [
                    ["<strong>New (0-100 cycles)</strong>", "100%", "Full speed"],
                    ["<strong>Light use (100-500 cycles)</strong>", "95-100%", "No noticeable change"],
                    ["<strong>Moderate use (500-1,000 cycles)</strong>", "85-95% (NMC) / 95-98% (LFP)", "Minimal change"],
                    ["<strong>Heavy use (1,000-2,000 cycles)</strong>", "70-85% (NMC) / 88-95% (LFP)", "Slightly slower"],
                    ["<strong>Very heavy (2,000-4,000 cycles)</strong>", "50-70% (NMC) / 75-88% (LFP)", "Noticeably slower"],
                    ["<strong>End of life (5,000+ cycles LFP)</strong>", "<70%", "Significantly slower"],
                ]
            ) +
            p("Why does degradation cause slower charging? As the battery ages, internal resistance increases. Higher resistance means more energy is lost as heat during charging, and the BMS has to slow down to keep temperatures safe. The battery also cannot accept charge as quickly at higher states of charge.") +
            step_grid([
                {"title": "How to Check Battery Health", "desc": "Many smart power stations show battery health in the app or on the display. Look for 'SOH' (State of Health) or 'Battery Health' in the settings. It is usually shown as a percentage. Some brands show cycle count as well. If your app does not show SOH directly, you can estimate it by comparing current capacity to the original rating."},
                {"title": "Is Degradation Covered Under Warranty?", "desc": "Most warranties cover manufacturing defects but not normal wear and tear. Typically, dropping below 60-70% capacity within the warranty period (2-5 years) is considered defective and covered. Normal degradation to 80% capacity after hundreds of cycles is considered normal and not covered. Check your warranty terms for details."},
                {"title": "Can You Fix Degraded Batteries?", "desc": "Unfortunately, you cannot reverse battery degradation. Once capacity is lost, it is gone permanently. The only fix is to replace the battery pack. However, you can slow further degradation by following best practices: avoid extreme temperatures, keep charge between 20-80% for daily use, use slow/standard charging instead of fast charging regularly, and store at 50% charge long-term."},
            ], "orange") +
            alert("warning", "trending-down", "When to replace", "If your battery is below 70% of original capacity and charging is significantly slower than it used to be (50%+ speed reduction), you might need a battery replacement. For premium units, replacement is often worth it. For budget units, you might be better off buying a new station. Check our battery replacement cost guide for more details.")
        },
        {
            "id": "troubleshooting-steps",
            "title": "Step-by-Step Troubleshooting",
            "content": p("Follow these steps in order to diagnose why your power station is charging slowly. Start with the easiest checks and work your way up:") +
            step_grid([
                {"title": "Step 1: Check the Basics", "desc": "Is everything plugged in correctly? Unplug and re-plug all connections. Check for bent pins in connectors. Make sure the power source is working (try plugging something else into the same outlet/panel). If solar, make sure the panel is in direct sun with no shadows. Check the display for error codes or warning messages."},
                {"title": "Step 2: Check Temperature", "desc": "Look at the battery temperature in the app or on the display. Is it outside the 10-35°C (50-95°F) optimal range? If too hot, move to shade and let it cool. If too cold, warm it up. Temperature issues are one of the most common causes of unexpectedly slow charging, and the fix is free — just wait."},
                {"title": "Step 3: Check Charge Settings", "desc": "Open the app and check: what charge mode are you in (Silent/Standard/Turbo)? Is there a charging current limit set? Is there a charge limit (like 80%) enabled? Is battery optimization mode on? Sometimes the simplest explanation is that you (or someone else) changed a setting and forgot about it."},
                {"title": "Step 4: Test with a Different Source/Cable", "desc": "Rule out the power source and cables. If solar: try AC charging and see if it is also slow. If AC: try a different outlet or charger. If AC is fast but solar is slow, the problem is solar-related (panels, cables, shading). If both are slow, the problem is the power station itself."},
                {"title": "Step 5: Inspect Solar Setup", "desc": "If solar is the issue: check for shading (even partial shading on one cell kills output), check panel angle, check cable connections (MC4 connectors click when properly seated), check cable gauge and length, check for dirt/grime on panels, and make sure panels are not damaged (cracks, hot spots)."},
                {"title": "Step 6: Firmware Update & Reset", "desc": "Make sure your power station has the latest firmware. Manufacturers often release updates that improve charging algorithms and fix bugs. You can update through the app. If that does not help, try a factory reset (backup your settings first). Sometimes glitches in the BMS software cause charging issues that a reset fixes."},
                {"title": "Step 7: Check Battery Health", "desc": "If you have tried everything else and charging is still slow, check battery health. If SOH is below 70%, degradation is likely the cause. If SOH is still high (90%+), there might be a different issue — contact customer support for further diagnosis."},
            ], "green") +
            alert("info", "headphones", "Contacting support", "If you need to contact customer support, have this information ready: model number, serial number, purchase date, firmware version, battery health/cycle count, a description of the issue, what troubleshooting steps you have already tried, and photos/videos if relevant. This will speed up the support process significantly.")
        },
        {
            "id": "speed-up-tips",
            "title": "How to Speed Up Charging",
            "content": p("Once you have diagnosed the issue, here are proven ways to maximize charging speed:") +
            grid_cards([
                {"title": "Maximize Solar Input", "color": "text-yellow-400", "desc": "Angle panels directly at the sun, adjust every 1-2 hours, keep panels clean, eliminate all shading, use appropriately sized cables, keep panels cool (good airflow underneath). Consider adding more panels in parallel for higher current."},
                {"title": "Use the Right Charge Mode", "color": "text-electric-400", "desc": "Use Turbo/Fast charging mode when you need speed. Use Standard for everyday use. Only use Silent/Quiet when noise matters. Set the charging current limit to maximum for your power source (don't limit it unnecessarily)."},
                {"title": "Optimize Temperature", "color": "text-green-400", "desc": "Charge within 10-35°C (50-95°F) for fastest speeds. In hot weather, charge in shade or during cooler morning/evening hours. In cold weather, bring the station inside to warm up before charging, or use a battery warmer if available."},
                {"title": "Use Short, Thick Cables", "color": "text-blue-400", "desc": "Minimize cable length — every foot of cable causes some loss. Use the thickest gauge cable that is practical (10-12 AWG for solar). Use high-quality MC4 connectors for solar. Avoid cheap extension cords."},
                {"title": "Charge Before You Get Low", "desc": "Charging from 0-50% is faster than charging from 50-100%. The last 20% (80-100%) is always the slowest as the BMS tapers the charge to protect the battery. If you need a quick top-up, do not wait until the battery is empty." , "color": "text-purple-400"},
                {"title": "Parallel Charging", "color": "text-orange-400", "desc": "If your station supports it, charge from multiple sources simultaneously (AC + solar, solar + car, etc.). Many premium stations support dual or multi-source charging, which can dramatically reduce charge time. Check your manual to see which combinations your model supports."},
            ], 2) +
            p("The most impactful single change for most people is proper solar panel angling. It is free, takes 30 seconds, and can easily double your solar charging speed compared to laying panels flat on the ground.") +
            alert("info", "zap", "Fast charging reality check", "No matter what you do, charging speed is limited by your power station's maximum charging rate and your power source. A station with a 500W max solar input will never charge at 1,000W from solar — not even with 2,000W of panels. The MPPT controller limits input to the station's maximum. Check the specs to know the upper limit.")
        },
    ],
    "faqs": [
        {"q": "Why is my portable power station charging so slowly?", "a": "The most common causes (in order of likelihood): incorrect solar panel angle or shading, dirty solar panels, thin/long cables causing voltage drop, battery temperature too hot or too cold, charge mode set to silent/eco instead of standard/turbo, partially shaded solar panels, and battery degradation from age/use. 80% of slow charging issues are simple fixes that take 5 minutes to check. Start with the easy stuff before worrying about battery health."},
        {"q": "Does temperature affect how fast a power station charges?", "a": "Yes — temperature has a huge effect. Optimal charging temperature is 10-35°C (50-95°F). Below 10°C, charging slows down, and below 0°C (32°F), most lithium batteries stop charging entirely to prevent damage. Above 35°C, charging also slows to prevent overheating and degradation. If your station is charging slowly, check the battery temperature first — it is often the cause."},
        {"q": "How do I make my power station charge faster?", "a": "Top ways to speed up charging: 1) For solar: angle panels directly at the sun, keep them clean, eliminate shading, use short thick cables. 2) Use Turbo/Fast charge mode instead of Silent. 3) Charge within the optimal temperature range (10-35°C). 4) Use the maximum charging current your power source can handle. 5) Charge from multiple sources simultaneously if supported (AC + solar). 6) Do not wait until 0% — charging is faster from 20-80% than 80-100%."},
        {"q": "Why does solar charging slow down in the afternoon?", "a": "Solar charging naturally peaks at midday when the sun is highest. In the afternoon, the sun gets lower in the sky, so the angle relative to your panels becomes worse. If your panels are fixed (not tracking the sun), output drops significantly by late afternoon. Clouds, haze, and shadows from trees/buildings also reduce output. This is normal and not a problem with your equipment."},
        {"q": "Does cable length matter for charging speed?", "a": "Yes, especially for solar (low-voltage DC) charging. Long, thin cables cause voltage drop, meaning less power reaches your power station. For solar, use the shortest cable that works for your setup, and use a thick enough gauge (10-12 AWG for most portable setups). For AC charging, cable length is less critical because the voltage is higher, but very long extension cords can still cause issues with high-power charging."},
        {"q": "Why does my station charge fast at first then slow down?", "a": "This is normal. Lithium batteries charge fastest when they are between 20-80% full. As the battery approaches 100%, the BMS (Battery Management System) gradually reduces the charging current to top off the cells carefully and prevent overcharging. This is called 'CC-CV' charging (Constant Current then Constant Voltage). The last 10-20% can take as long as the first 80%. This is by design and protects the battery."},
        {"q": "Is slow charging a sign my battery is dying?", "a": "Not necessarily. Slow charging has many causes, and battery degradation is actually one of the less common ones — especially if your station is less than 2-3 years old. Rule out all the other causes first: temperature, settings, cables, solar angle, etc. If you have tried everything and charging is still 50%+ slower than when new, and battery health is below 70%, then degradation might be the cause."},
        {"q": "What is the best charge mode for battery health?", "a": "Slower charging is generally easier on the battery and causes slightly less degradation over time. For everyday use, Standard mode is the best balance of speed and battery health. Use Turbo/Fast only when you genuinely need the speed. Use Silent mode for overnight charging or when noise matters. That said, the difference in lifespan between fast and slow charging is relatively small for most people — usually less than 10% difference over the battery's life."},
        {"q": "Can I use a bigger charger to charge faster?", "a": "Your power station has a maximum charging rate that cannot be exceeded, no matter how big the charger is. If your station supports 500W max AC charging, plugging it into a 1,000W charger will still only charge at 500W. The power station's charge controller limits the input. However, using a charger that is too small will make charging slower — make sure your charger can supply at least the maximum input your station supports."},
        {"q": "How fast should my power station charge?", "a": "Charging speed depends on the model and charging method. As a rough guide: AC fast charging usually takes 1-3 hours for 0-80%, solar charging depends on panel size and sun conditions (200W panel on a 1kWh battery = 5-8 hours full sun). Check your model's specifications for the rated charging speed. If you are getting significantly less than the rated speed (30%+ slower), something is wrong and you should troubleshoot."},
    ],
    "related": gen_related_basic(),
}

PAGES = [page6]

os.makedirs(OUTPUT_DIR, exist_ok=True)
for page in PAGES:
    fp = os.path.join(OUTPUT_DIR, page["filename"])
    html_content = build_page(page)
    with open(fp, "w") as f:
        f.write(html_content)
    text = re.sub(r'<[^>]+>', ' ', html_content)
    words = text.split()
    print(f"  Created: {page['filename']}  ({len(words)} words)")
print(f"\nTotal: {len(PAGES)} pages")
