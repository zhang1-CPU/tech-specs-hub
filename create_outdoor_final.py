#!/usr/bin/env python3
"""Generate final Outdoor Power batch: pages 7-10."""

import os, json, html, re

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

template = open("/workspace/pages/specs/portable-power-station-eco-mode.html").read()
BODY_HEADER = template.split('''<body class="bg-navy-950 text-white min-h-screen font-display">''')[1].split('''  <!-- BREADCRUMB -->''')[0]
FOOTER = template.split('''  <!-- FOOTER -->''')[1].replace("<!-- FOOTER -->", "  <!-- FOOTER -->")

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

def std_related():
    return [
        {"href": "portable-power-station-not-charging.html", "badge": "CHARGING", "badge_class": "bg-yellow-500/20 text-yellow-400", "border_class": "border-yellow-500/30", "badge2": "Troubleshoot", "title": "Not Charging", "desc": "Troubleshoot why your power station is not charging — common causes and step-by-step fixes."},
        {"href": "portable-power-station-eco-mode.html", "badge": "ECO&nbsp;MODE", "badge_class": "bg-green-500/20 text-green-400", "border_class": "border-green-500/30", "badge2": "Guide", "title": "ECO Mode Guide", "desc": "What is ECO mode, how much battery it saves, how to disable it, and optimization tips."},
        {"href": "how-to-store-portable-power-station.html", "badge": "STORAGE", "badge_class": "bg-blue-500/20 text-blue-400", "border_class": "border-blue-500/30", "badge2": "Guide", "title": "Storage Guide", "desc": "How to store a portable power station long-term — ideal charge level, temperature, cycling schedule."},
        {"href": "lifepo4-vs-lithium-ion-power-station.html", "badge": "LFP&nbsp;vs&nbsp;NMC", "badge_class": "bg-purple-500/20 text-purple-400", "border_class": "border-purple-500/30", "badge2": "Comparison", "title": "LFP vs Lithium-Ion", "desc": "Complete comparison of LiFePO4 vs lithium-ion batteries — cycle life, safety, cost, and density."},
        {"href": "can-portable-power-station-charge-while-in-use.html", "badge": "PASS-THROUGH", "badge_class": "bg-electric-500/20 text-electric-400", "border_class": "border-electric-500/30", "badge2": "FAQ", "title": "Charge While Using", "desc": "Can you charge and discharge at the same time? How pass-through charging works and which brands support it."},
        {"href": "outdoor-power.html", "badge": "ALL&nbsp;GUIDES", "badge_class": "bg-electric-500/20 text-electric-400", "border_class": "border-electric-500/30", "badge2": "Category", "title": "Outdoor Power Hub", "desc": "Browse all portable power station guides, comparisons, specs, and troubleshooting resources."},
    ]

# =================== PAGE 7: OVERHEATING ===================

page7 = {
    "filename": "portable-power-station-overheating-hot.html",
    "title": "Portable Power Station Overheating & Getting Hot? Causes & Fixes (2026)",
    "headline": "Portable Power Station Overheating & Getting Hot? Causes & Fixes (2026)",
    "meta_desc": "Why is your portable power station getting hot or overheating? Normal operating temperature, causes, cooling system issues, temperature protection, hot/cold weather tips, and safety concerns.",
    "category": "Outdoor Power",
    "category_link": "outdoor-power.html",
    "breadcrumb_title": "Overheating Guide",
    "hero_blur": "bg-red-500/5",
    "hero_badges": '''<div class="px-3 py-1.5 bg-red-500/20 text-red-400 font-mono font-bold text-sm rounded-md border border-red-500/30">OVERHEATING</div>
        <span class="badge badge-info"><i data-lucide="thermometer" style="width:0.75rem;height:0.75rem"></i>Temperature</span>
        <span class="badge badge-info"><i data-lucide="shield" style="width:0.75rem;height:0.75rem"></i>Safety</span>''',
    "h1": 'Portable Power Station Overheating? &mdash; <span class="gradient-text">Causes &amp; Fixes 2026</span>',
    "hero_desc": "A warm power station is normal — they generate heat during charging and discharging. But when it gets too hot to touch, shuts down unexpectedly, or shows temperature error codes, you have a problem. Overheating reduces battery life, triggers safety shutdowns, and in extreme cases can be dangerous. This guide covers normal operating temperatures, common overheating causes, cooling system issues, temperature protection systems, and how to keep your station cool in hot weather.",
    "hero_stats": f'''<div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="thermometer" style="width:0.9rem;height:0.9rem"></i>Normal (idle)</div>
          <div class="font-mono font-bold text-xl text-green-400">20&ndash;35&deg;C</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="thermometer" style="width:0.9rem;height:0.9rem"></i>Normal (full load)</div>
          <div class="font-bold text-xl text-yellow-400">40&ndash;55&deg;C</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="thermometer" style="width:0.9rem;height:0.9rem"></i>Warning Zone</div>
          <div class="font-bold text-xl text-orange-400">55&ndash;65&deg;C</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="thermometer" style="width:0.9rem;height:0.9rem"></i>Shutdown</div>
          <div class="font-mono font-bold text-xl text-red-400">65&deg;C+</div>
        </div>''',
    "qa_gradient": "from-red-950/20 to-navy-900 border-red-500/20",
    "qa_icon_color": "#f87171",
    "qa_title": "Why Is My Power Station Getting Hot?",
    "qa_text": '<strong class="text-white">Some warmth during charging or high-output use is completely normal — power stations typically run at 40-55°C under full load.</strong> The inverter, charging circuits, and battery all generate heat as a byproduct of converting electricity. But if the case is too hot to comfortably touch, if the fan is running at full speed constantly, or if the station shuts down from over-temperature, there is a problem. Common causes include: blocked ventilation fans, running at very high output for extended periods, hot ambient temperatures, direct sunlight, faulty cooling fans, or battery internal resistance issues from age.',
    "qa_extra": f'''<div class="grid md:grid-cols-2 gap-3 mt-4">
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-green-400 font-semibold mb-1 flex items-center gap-2"><i data-lucide="check" style="width:1rem;height:1rem"></i>Normal warmth</div>
          <p class="text-sm text-gray-300">Slightly warm to the touch, fan runs occasionally, no error codes, temperature under 55°C — this is expected behavior</p>
        </div>
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-red-400 font-semibold mb-1 flex items-center gap-2"><i data-lucide="alert-triangle" style="width:1rem;height:1rem"></i>Overheating signs</div>
          <p class="text-sm text-gray-300">Too hot to touch, fan always at max speed, temperature errors, shutdowns, burning smell — stop using and investigate</p>
        </div>
      </div>''',
    "sections": [
        {
            "id": "normal-temp",
            "title": "Normal Operating Temperature Range",
            "content": p("Before you panic about your power station feeling warm, it is important to understand what 'normal' is. Portable power stations generate heat — they cannot avoid it. The question is whether the temperature is within the safe design range.") +
            specs_table(
                ["Condition", "Typical Temperature", "Fan Behavior", "What It Means"],
                [
                    ["<strong>Idle / standby</strong>", "20-35°C (68-95°F)", "Off or very slow", "Completely normal, no heat being generated"],
                    ["<strong>Light use (<30% load)</strong>", "25-40°C (77-104°F)", "Usually off", "Minimal heat from small load"],
                    ["<strong>Moderate use (30-70% load)</strong>", "35-50°C (95-122°F)", "Low to medium speed", "Normal operating temperature"],
                    ["<strong>Heavy use (70-100% load)</strong>", "45-55°C (113-131°F)", "Medium to high speed", "Getting warm but still safe"],
                    ["<strong>Max output / surge</strong>", "50-60°C (122-140°F)", "Full speed", "Hot but within design limits for short periods"],
                    ["<strong>Warning zone</strong>", "55-65°C (131-149°F)", "Full blast", "Reduce load immediately"],
                    ["<strong>Shutdown / fault</strong>", "65°C+ (149°F+)", "Max cooling, then shutdown", "Thermal protection activates — station turns off to prevent damage"],
                ]
            ) +
            p("These are general ranges — exact numbers vary by brand and model. Premium stations with better cooling can run cooler. Budget stations often run hotter because they skimp on heat sinks and fan size.") +
            alert("info", "thermometer", "How to measure temperature", "Most smart power stations show battery and/or inverter temperature in the companion app or on the display. If yours does not, you can use an infrared thermometer (temp gun) pointed at the vent area to get a rough estimate. Case temperature is usually 5-15°C cooler than internal component temperature.")
        },
        {
            "id": "overheating-causes",
            "title": "Common Overheating Causes",
            "content": p("If your power station is running hotter than normal, one of these is likely the cause:") +
            step_grid([
                {"title": "Blocked Vents / Airflow Restrictions", "desc": "The #1 cause of overheating. Power stations need airflow to cool. If the intake or exhaust vents are blocked — by dust, debris, a blanket, being placed against a wall, or stacked with other items — hot air cannot escape and temperatures rise rapidly. Always keep at least 6-12 inches of clear space around all vent openings."},
                {"title": "Running at Maximum Output Continuously", "desc": "Power stations can handle max output, but not forever. The inverter generates the most heat of any component. Running at 90-100% load for hours pushes the cooling system to its limits. If you need sustained high output, consider a larger station or reducing the load slightly."},
                {"title": "High Ambient Temperature", "desc": "If it is 35-40°C (95-104°F) outside and your station is in the sun, it has a lot less cooling headroom. The cooling system has to dissipate internal heat into already-hot air, which is less effective. On hot days, keep the station in shade and avoid max output for long periods."},
                {"title": "Direct Sunlight", "desc": "The sun beating down on the case adds a surprising amount of heat. A black power station in direct sun can be 15-25°C (27-45°F) hotter than the air temperature. Always keep your station shaded. Even a simple canopy or umbrella makes a huge difference."},
                {"title": "Dust Buildup / Dirty Fan", "desc": "Over time, dust builds up inside the unit — on the heat sinks, fan blades, and inside the vents. Dust acts as insulation, preventing heat from dissipating. It can also slow down or clog the cooling fan. This is especially common in dusty environments like deserts, construction sites, or if you use it off-road a lot."},
                {"title": "Faulty or Failing Cooling Fan", "desc": "If the cooling fan is not working properly — seized bearing, broken blade, failed motor, or control circuit issue — the station cannot properly cool itself. You might hear grinding, rattling, or notice the fan never comes on even under heavy load. A broken fan leads to rapid overheating."},
                {"title": "Aging Battery / High Internal Resistance", "desc": "As batteries age, their internal resistance increases. Higher resistance means more energy is lost as heat during charging and discharging. An old, degraded battery runs hotter than a new one, even at the same load. This is a gradual change — you will notice it getting warmer over months or years."},
                {"title": "Charging + Discharging Simultaneously", "desc": "Running pass-through charging (charging and discharging at the same time) generates more heat than either alone. Both the charging circuit and the inverter are active, producing heat. High-power pass-through especially pushes the thermal design. Some stations get noticeably warm in pass-through mode — this is usually normal but worth knowing."},
            ], "orange") +
            alert("warning", "flame", "Burning smell is serious", "If you smell burning plastic, electrical burning, or any unusual chemical smells from your power station, turn it off immediately, unplug everything, and move it to a fire-safe location (concrete floor, away from flammables). Do not turn it back on. Contact the manufacturer for service. A burning smell indicates something is actually failing and could be a fire risk.")
        },
        {
            "id": "cooling-systems",
            "title": "Cooling Systems Explained",
            "content": p("Portable power stations use various cooling methods, and the design has a big impact on how hot they get and how loud they are. Here are the main approaches:") +
            specs_table(
                ["Cooling Type", "How It Works", "Noise Level", "Cooling Performance", "Found In"],
                [
                    ["<strong>Passive (heatsink only)</strong>", "Heat dissipates through metal fins with no fan", "Completely silent", "Low — only for low-power units", "Small stations (<500W), some budget models"],
                    ["<strong>Single fan + heatsink</strong>", "One fan blows air over heat sinks", "Quiet to moderate", "Good for mid-range power", "Most 500-2,000W stations"],
                    ["<strong>Dual fan</strong>", "Two fans for better airflow", "Moderate at high load", "Good for high-power units", "2,000W+ stations"],
                    ["<strong>Variable speed fan</strong>", "Fan speed adjusts based on temperature", "Very quiet at low load", "Excellent — matches cooling to need", "Most premium stations (EcoFlow, Bluetti, etc.)"],
                    ["<strong>Liquid cooling (rare)</strong>", "Coolant circulates through cooling plates", "Very quiet", "Excellent cooling", "Very high-end / large systems only"],
                ]
            ) +
            p("Nearly all modern portable power stations use variable-speed fans that ramp up as temperature increases. This means they are nearly silent at low load but get noticeably louder when you are pushing them hard. This is normal and expected — the fan speed is proportional to how much cooling is needed.") +
            step_grid([
                {"title": "How Variable-Speed Fans Work", "desc": "The BMS (Battery Management System) and inverter controller monitor temperatures at multiple points inside the unit. As temperatures rise past a threshold, the fan turns on at low speed. If temperature keeps rising, fan speed increases. At max temperature, the fan runs at full speed. This intelligent approach balances noise and cooling efficiency."},
                {"title": "Fan Speed Curves by Brand", "desc": "Each brand programs their fan curve differently. EcoFlow tends to keep fans off longer and ramp up more aggressively when needed. Bluetti fans often come on earlier and run at lower speed. Jackery is generally quieter but can run hotter. Anker has some of the quietest fans in the industry. There is no single 'best' — it is a tradeoff between noise and temperature."},
            ], "blue") +
            alert("info", "volume-2", "What is 'too loud'?", "Most power stations produce 30-45 dB at low/medium load (library to normal conversation level) and 50-65 dB at full load (vacuum cleaner range). If your station is making unusual noises — grinding, rattling, buzzing, or high-pitched whine — that indicates a fan problem, not just normal operation.")
        },
        {
            "id": "temperature-protection",
            "title": "Temperature Protection Systems",
            "content": p("All modern portable power stations have multiple layers of temperature protection to prevent damage and safety issues. These systems are part of the BMS (Battery Management System) and inverter controller:") +
            '<div class="space-y-4 mb-6">' +
            step_grid([
                {"title": "Level 1: Fan Speed Increase", "desc": "First line of defense. As temperature rises, fan speed increases to provide more cooling. This is the normal response to higher load or higher ambient temperature. You will notice the fan getting louder, but the station continues operating normally. No error codes, no performance reduction."},
                {"title": "Level 2: Power Reduction / Throttling", "desc": "If temperature keeps rising despite maximum fan speed, some stations will automatically reduce output power to lower heat generation. The station does not shut off — it just cannot deliver full power until it cools down. This is less common than direct shutdown but is a feature on some premium models."},
                {"title": "Level 3: Charging Slowdown / Cutback", "desc": "When the battery gets too hot (or too cold), the BMS reduces or stops charging to protect the cells. Charging generates heat, so reducing charging current helps lower temperature. This is very common — you might notice charging slows down or pauses on hot days. It starts again automatically when it cools."},
                {"title": "Level 4: Output Shutdown", "desc": "If inverter temperature reaches the safety limit, the station shuts down AC/DC output to prevent component damage. The battery itself might still be fine, but the inverter cannot safely run at that temperature. After cooling down (usually 10-30 minutes), you can turn it back on. Some stations beep or show an error code before shutting down."},
                {"title": "Level 5: Full System Shutdown", "desc": "In extreme cases — very high battery temperature, or a fault condition — the entire station shuts down completely. This is a last-resort safety measure. Do not try to turn it back on immediately. Let it cool down for at least 30-60 minutes. If it happens repeatedly or without obvious cause, contact customer support."},
            ], "yellow") + "</div>" +
            p("These protection systems exist for your safety and to protect the battery and inverter from damage. While it can be frustrating when your station shuts down mid-use, it is much better than the alternative — permanent damage or even fire.") +
            alert("critical", "shield", "Thermal runaway is the big risk", "The ultimate safety concern is thermal runaway — when one battery cell gets hot enough to trigger a self-sustaining chemical reaction that spreads to other cells. This is what causes lithium battery fires. The BMS and thermal protection systems are specifically designed to prevent thermal runaway by catching overheating early and shutting down before it reaches dangerous levels. LFP batteries are much more resistant to thermal runaway than NMC.")
        },
        {
            "id": "hot-weather-tips",
            "title": "Hot Weather Cooling Tips",
            "content": p("When it is hot outside, you need to take extra steps to keep your power station cool. Here are proven tips for hot-weather use:") +
            grid_cards([
                {"title": "Keep It in Shade", "color": "text-yellow-400", "desc": "This is the #1 thing you can do. Direct sun adds 15-25°C to the case temperature. Place the station under a canopy, umbrella, awning, or inside a shaded vehicle (with ventilation). Even partial shade helps. If you are camping, set up your power station in the shadiest spot you can find."},
                {"title": "Ensure Airflow Around Vents", "color": "text-green-400", "desc": "Never block the intake or exhaust vents. Keep at least 6-12 inches of clear space on all sides. Do not set it on a soft surface like a bed or couch that can block bottom vents. Do not cover it with a blanket, towel, or solar panel. Elevate it slightly if the bottom has vents."},
                {"title": "Reduce Load During Peak Heat", "color": "text-orange-400", "desc": "If it is the hottest part of the day (2-5 PM), try to avoid running the station at full output. Save high-power tasks for morning or evening when it is cooler. Stagger high-wattage usage so you are not running everything at once during peak heat."},
                {"title": "Charge During Cooler Hours", "color": "text-blue-400", "desc": "If you can choose when to charge, do it in the morning or evening when temperatures are lower. Charging generates heat, and adding that heat on top of already-hot ambient conditions pushes the station closer to its limits. Solar charging naturally peaks at midday when it is hottest — this is unavoidable, but you can limit AC fast charging to cooler times."},
                {"title": "Use a Fan to Help Cool", "color": "text-purple-400", "desc": "If you have access to extra power, pointing a small fan at the intake vents helps cooling significantly. Even a small USB fan can improve airflow and lower operating temperature by 5-10°C. This is helpful in extreme heat or if you need sustained high output."},
                {"title": "Avoid Enclosed Spaces", "color": "text-red-400", "desc": "Never run a power station in a sealed box, closed cabinet, or enclosed storage compartment without ventilation. Enclosed spaces trap heat and temperatures skyrocket quickly. If you must put it in a cabinet, add vent fans and ensure good airflow."},
            ], 2) +
            p("For people living or camping in very hot climates (35°C+ / 95°F+), consider sizing up your power station. A larger station running at 30% load runs much cooler than a smaller station running at 80% load, even if they are powering the exact same devices. The overcapacity means less stress on the components and lower temperatures.") +
            alert("warning", "car", "Never leave in a hot car", "Never leave a portable power station in a parked car in direct sun on a hot day. Inside car temperatures can reach 60-70°C (140-160°F) in as little as 30 minutes — far above the safe operating range. This can damage the battery and potentially cause safety issues. If you must transport it in a car, keep the AC on, or put it in the coolest part of the vehicle."),
        },
        {
            "id": "cold-weather",
            "title": "Cold Weather Issues",
            "content": p("While this guide is primarily about overheating, cold weather also causes problems — and some people confuse cold weather charging issues with overheating. Here is what you need to know about cold weather:") +
            specs_table(
                ["Temperature", "Charging", "Discharging", "What Happens"],
                [
                    ["<strong>10-25°C (50-77°F)</strong>", "Normal speed", "Normal performance", "Optimal range"],
                    ["<strong>0-10°C (32-50°F)</strong>", "Reduced speed", "Slightly reduced capacity", "BMS limits charging current"],
                    ["<strong>-10-0°C (14-32°F)</strong>", "Very slow / may pause", "Noticeably reduced capacity", "Battery heater may activate if equipped"],
                    ["<strong>Below -10°C (14°F)</strong>", "Charging stops", "Significantly reduced capacity", "May show low battery error, limited output"],
                    ["<strong>Below -20°C (-4°F)</strong>", "No charging", "Severely limited or shutdown", "Risk of permanent damage from charging"],
                ]
            ) +
            p("The biggest cold weather issue is charging, not discharging. Discharging a cold battery works fine (just with less capacity), but charging a cold lithium battery can cause permanent damage (lithium plating on the anode). This is why the BMS strictly limits charging when the battery is cold.") +
            step_grid([
                {"title": "How to Warm Up a Cold Battery", "desc": "If your battery is too cold to charge, warm it up first. Bring it inside a heated space, put it in an insulated bag with a hand warmer (be careful — do not apply direct heat), or run a light load for a while (discharging generates a small amount of heat). Some premium stations have built-in battery heaters that automatically warm the battery before charging. Never try to force charging when the BMS is preventing it — that protection exists for a reason."},
                {"title": "Cold Weather Capacity Loss", "desc": "Expect 20-40% less usable capacity in very cold weather (-10°C / 14°F range). This is temporary — capacity returns to normal when the battery warms up. If you use your power station in cold weather regularly, plan for this reduced capacity and size your battery accordingly. LFP batteries handle cold better than NMC in terms of cycle life, but both lose capacity when cold."},
            ], "blue") +
            alert("info", "snowflake", "Freezing and charging", "Never charge a frozen lithium battery. Charging below 0°C (32°F) causes lithium metal to plate onto the anode, which permanently reduces capacity and can create internal short circuits over time. The BMS will prevent this, but if you somehow bypass it (don't), you could permanently damage the battery or cause a safety hazard.")
        },
        {
            "id": "troubleshoot-overheat",
            "title": "Troubleshooting Overheating Step by Step",
            "content": p("If your power station is overheating, follow these steps in order to diagnose and fix the problem:") +
            step_grid([
                {"title": "Step 1: Stop Using and Let It Cool", "desc": "First, turn off all output, unplug everything, and move the station to a cool, well-ventilated area. Let it cool down completely (30-60 minutes). This prevents further stress and gives you time to investigate. If it was showing an error code, write the code down before resetting."},
                {"title": "Step 2: Check for Blocked Vents", "desc": "Inspect all vent openings — intake and exhaust. Are they clogged with dust, dirt, or debris? Is anything blocking them (a blanket, other equipment, packed in a bag too tightly)? Clear any obstructions. Vacuum the vents gently with a soft brush attachment if they are dusty."},
                {"title": "Step 3: Check Ambient Conditions", "desc": "Is it very hot where you are using it? Was it in direct sun? Was it in an enclosed space? If the answer is yes, the overheating was probably caused by environmental conditions, not a fault. Move it to a cooler location with shade and ventilation and try again."},
                {"title": "Step 4: Listen to the Fan", "desc": "Run a moderate load and listen for the cooling fan. Does it come on? Is the speed normal, or does it sound different (grinding, rattling, squealing)? If the fan never comes on even under heavy load, the fan or its controller might be faulty. If it makes unusual noises, the fan bearing might be failing."},
                {"title": "Step 5: Monitor Temperature", "desc": "Use the app or display to monitor battery and inverter temperature under different load levels. What is the temperature at idle? At 50% load? At full load? Compare to the normal ranges we listed earlier. If it runs 10-15°C hotter than expected for the same load, there might be an issue."},
                {"title": "Step 6: Check for Error Codes", "desc": "Look up any error codes in the manual or on the manufacturer's website. Temperature-related codes usually start with 'T' or 'TEMP' or mention 'overheat'. The exact meaning tells you whether it is battery overheating, inverter overheating, or charging over-temperature."},
                {"title": "Step 7: Test at Different Load Levels", "desc": "Try running at low load (10-20%), medium load (50%), and high load (80-100%). Does it overheat at all load levels, or only at very high output? If it overheats even at low load, there is likely a hardware problem (fan failure, internal short, etc.). If it only overheats at max output for extended periods, it might be within normal limits for that model."},
                {"title": "Step 8: Contact Support If Needed", "desc": "If you have tried everything and the station still overheats at normal loads, or if the fan is clearly not working, contact customer support. If it is under warranty, you should get a repair or replacement. Have your model number, serial number, purchase date, and a description of the issue ready."},
            ], "red") +
            alert("critical", "fire", "If you suspect a battery fire risk", "If the battery is swollen, there is a burning smell, you see smoke, or the unit is extremely hot and getting hotter — treat it as a potential fire hazard. Move it outdoors onto concrete or dirt, away from anything flammable. Keep a fire extinguisher (Class B/C or ABC) nearby. Do not spray water on a lithium battery fire — it can make it worse. Call your local fire department if there is any active fire or smoke.")
        },
    ],
    "faqs": [
        {"q": "Is it normal for a portable power station to get hot?", "a": "Yes, some warmth is completely normal. Power stations generate heat from the inverter, charging circuits, and battery during operation. Under full load, case temperatures of 40-55°C (104-131°F) are typical. The fan should be running at medium to high speed. It becomes a problem if: it is too hot to comfortably touch (above ~55-60°C), the fan runs at max speed constantly, you see temperature error codes, or it shuts down from over-temperature."},
        {"q": "What temperature is too hot for a power station?", "a": "As a general rule: if the case is too hot to keep your hand on for more than 3-5 seconds, it is probably running too hot. Internal component temperatures above 60-65°C (140-149°F) usually trigger thermal protection shutdowns. Battery temperature above 55-60°C is a concern — lithium batteries degrade much faster at high temperatures, and prolonged high temperature can be a safety risk. Check the app or display for exact internal temperatures."},
        {"q": "Why does my power station fan run so much?", "a": "The cooling fan runs more when the station is generating a lot of heat — during high-power output, fast charging, or pass-through charging. If the fan runs constantly even at idle or light load, it could be: high ambient temperature, clogged vents/dust buildup, a faulty fan controller, or the temperature sensor reading incorrectly. Start by checking for blocked vents and ensuring the station is in a cool location."},
        {"q": "Can a power station overheat and catch fire?", "a": "It is extremely rare with modern, properly functioning power stations from reputable brands. All good stations have multiple layers of thermal protection — temperature sensors, BMS monitoring, fan cooling, and automatic shutdowns — designed to prevent dangerous overheating. That said, no lithium battery is 100% risk-free. Defects, physical damage, water damage, or extreme abuse can cause thermal runaway. Always buy from reputable brands and follow safety guidelines."},
        {"q": "How do I cool down my power station faster?", "a": "To cool an overheating power station quickly: turn off all output and charging, move it to a cool shaded area, make sure all vents are clear and unobstructed, elevate it slightly if bottom vents exist, and point a small fan at the intake vents to help airflow. Do not put it in the freezer or pour water on it — rapid temperature change can cause condensation and damage. Let it cool gradually at room temperature."},
        {"q": "Is it bad to leave a power station in the sun?", "a": "Yes, prolonged direct sun is bad for power stations. The sun heats the case significantly — a black unit in direct sun can be 15-25°C (27-45°F) hotter than the air temperature. This adds extra heat that the cooling system has to deal with, reduces battery life over time, and can trigger thermal shutdowns. Always keep your station shaded when in use. Use a canopy, umbrella, or park it in the shade."},
        {"q": "Does overheating damage the battery?", "a": "Yes, sustained high temperatures accelerate battery degradation. Heat is the #1 enemy of lithium batteries. Every 10°C (18°F) increase in temperature roughly doubles the rate of chemical degradation. Occasional short periods of high temperature are fine, but weeks or months of running hot will noticeably shorten battery life. This is why proper cooling and avoiding extreme heat is so important for long-term battery health."},
        {"q": "Why does my station shut off when it is hot outside?", "a": "This is the thermal protection system working as designed. When internal temperature reaches the safety limit (usually around 55-65°C for the battery or inverter), the station automatically shuts down to prevent damage. It is frustrating but necessary. To prevent this: keep the station in shade, ensure good airflow, reduce your power draw during the hottest part of the day, and consider a larger station so you are not running at max load."},
        {"q": "Can I use a fan to cool my power station?", "a": "Yes! Pointing a small fan at the intake vents is a great way to improve cooling, especially in hot weather or when running at high output. Even a small USB fan can lower operating temperature by 5-10°C. Just make sure you are blowing air INTO the intake vents, not against the exhaust (check your manual for which vents are which). Do not use compressed air — it can push dust deeper into the unit."},
        {"q": "How do I clean dust out of my power station?", "a": "To clean dust from vents and fans: first turn off and unplug the station. Use a soft brush (like a clean paintbrush or makeup brush) to gently brush dust from the vent openings. You can use a vacuum cleaner with a brush attachment on low suction to pull dust out. Do NOT use compressed air — it pushes dust deeper inside and can damage fan bearings or components. If the inside is very dusty, consider professional service."},
    ],
    "related": std_related(),
}

PAGES = [page7]

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
