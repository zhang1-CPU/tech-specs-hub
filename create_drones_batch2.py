#!/usr/bin/env python3
"""Generate drone pages batch 2: battery lifespan, rain resistance, photo transfer."""

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

def drone_related():
    return [
        {"href": "how-to-find-lost-dji-drone.html", "badge": "LOST", "badge_class": "bg-red-500/20 text-red-400", "border_class": "border-red-500/30", "badge2": "Guide", "title": "Find Lost Drone", "desc": "Step-by-step guide to finding a lost DJI drone using Find My Drone, GPS, and community help."},
        {"href": "best-memory-card-for-dji-mini-5-pro.html", "badge": "SD&nbsp;CARD", "badge_class": "bg-yellow-500/20 text-yellow-400", "border_class": "border-yellow-500/30", "badge2": "Guide", "title": "Best Memory Card", "desc": "What SD card to use with DJI Mini 5 Pro — speed requirements, recommended brands and sizes."},
        {"href": "dji-mini-drone-under-250g-license-requirements.html", "badge": "FAA", "badge_class": "bg-blue-500/20 text-blue-400", "border_class": "border-blue-500/30", "badge2": "Legal", "title": "License Requirements", "desc": "Do you need a license for a sub-250g DJI Mini? FAA rules, registration, and Remote ID."},
        {"href": "dji-drone-battery-swelling-what-to-do.html", "badge": "SAFETY", "badge_class": "bg-red-500/20 text-red-400", "border_class": "border-red-500/30", "badge2": "Safety", "title": "Battery Swelling", "desc": "What causes DJI drone battery swelling, is it safe, and what to do with swollen batteries."},
        {"href": "dji-drone-atti-mode-how-to-get-out.html", "badge": "ATTI&nbsp;MODE", "badge_class": "bg-purple-500/20 text-purple-400", "border_class": "border-purple-500/30", "badge2": "Troubleshoot", "title": "ATTI Mode Guide", "desc": "What is ATTI mode, why drones enter it, and how to fix GPS issues and land safely."},
        {"href": "drones.html", "badge": "ALL&nbsp;GUIDES", "badge_class": "bg-electric-500/20 text-electric-400", "border_class": "border-electric-500/30", "badge2": "Category", "title": "Drone Hub", "desc": "Browse all drone guides, comparisons, specs, and troubleshooting resources."},
    ]

# =================== PAGE 13: BATTERY LIFESPAN ===================

page13 = {
    "filename": "how-long-do-dji-drone-batteries-last.html",
    "title": "How Long Do DJI Drone Batteries Last? (Cycles & Lifespan 2026)",
    "headline": "How Long Do DJI Drone Batteries Last? (Cycles & Lifespan 2026)",
    "meta_desc": "How long do DJI drone batteries last? Complete guide covering battery cycle life by model, LiPo vs Li-ion, factors affecting lifespan, signs of failing batteries, storage best practices, and replacement cost.",
    "category": "Drones",
    "category_link": "drones.html",
    "breadcrumb_title": "Battery Lifespan",
    "hero_blur": "bg-green-500/5",
    "hero_badges": '''<div class="px-3 py-1.5 bg-green-500/20 text-green-400 font-mono font-bold text-sm rounded-md border border-green-500/30">BATTERY&nbsp;LIFE</div>
        <span class="badge badge-info"><i data-lucide="battery-charging" style="width:0.75rem;height:0.75rem"></i>Cycle Count</span>
        <span class="badge badge-info"><i data-lucide="clock" style="width:0.75rem;height:0.75rem"></i>Lifespan</span>''',
    "h1": 'How Long Do DJI Drone Batteries Last? &mdash; <span class="gradient-text">Cycles & Lifespan 2026</span>',
    "hero_desc": "DJI drone batteries are amazing pieces of technology — they pack enormous energy into a lightweight package, but they do not last forever. Understanding battery lifespan, how to extend it, and when to replace batteries is critical for both safety and performance. In this guide, we cover everything: cycle life by model, LiPo vs Li-ion chemistry, what kills batteries early, how to check battery health, storage best practices, and how much replacement batteries cost.",
    "hero_stats": f'''<div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="battery" style="width:0.9rem;height:0.9rem"></i>Mini Series</div>
          <div class="font-mono font-bold text-xl text-green-400">200-300 cycles</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="battery" style="width:0.9rem;height:0.9rem"></i>Mavic / Air</div>
          <div class="font-bold text-xl text-blue-400">300-400 cycles</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="battery" style="width:0.9rem;height:0.9rem"></i>Inspire / Pro</div>
          <div class="font-mono font-bold text-xl text-purple-400">400+ cycles</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="battery" style="width:0.9rem;height:0.9rem"></i>Shelf Life</div>
          <div class="font-bold text-xl text-yellow-400">3-5 years</div>
        </div>''',
    "qa_gradient": "from-green-950/20 to-navy-900 border-green-500/20",
    "qa_icon_color": "#4ade80",
    "qa_title": "How Long Do DJI Batteries Last?",
    "qa_text": '<strong class="text-white">DJI drone batteries typically last 200-400 charge cycles (or about 2-5 years) before dropping to 80% of their original capacity, depending on the model and how they are used and stored.</strong> The Mini series batteries (Mini 2, Mini 3, Mini 4, Mini 5) are usually rated for ~200-300 cycles. Mavic and Air series batteries are rated for ~300-400 cycles. Higher-end Inspire and Matrice batteries can go 400+ cycles. However, these are just estimates — with poor care (extreme temperatures, deep discharges, bad storage), batteries can degrade much faster. With excellent care (proper storage temperature, avoiding full discharges, not leaving them fully charged for weeks), they can last significantly longer. DJI\'s Intelligent Battery system actively manages each cell to maximize lifespan and safety.',
    "qa_extra": f'''<div class="grid md:grid-cols-2 gap-3 mt-4">
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-green-400 font-semibold mb-1">Extends Life</div>
          <p class="text-sm text-gray-300">Store at 40-60% charge, cool temperature, avoid deep discharge, charge slowly</p>
        </div>
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-red-400 font-semibold mb-1">Shortens Life</div>
          <p class="text-sm text-gray-300">Full charge storage, hot temperatures, deep discharge, fast charging, physical damage</p>
        </div>
      </div>''',
    "sections": [
        {
            "id": "cycle-life-by-model",
            "title": "Battery Cycle Life by DJI Model",
            "content": p("DJI publishes cycle life ratings for most of their drone batteries. Here is how different models compare:") +
            specs_table(
                ["Drone Model", "Battery Type", "Capacity", "Rated Cycles (to 80%)", "Flight Time"],
                [
                    ["<strong>DJI Mini 2 / SE</strong>", "LiPo 2S", "2250 mAh", "~200 cycles", "31 min"],
                    ["<strong>DJI Mini 3 / 4 Pro</strong>", "LiPo 2S", "2453/2590 mAh", "~200-300 cycles", "34-45 min"],
                    ["<strong>DJI Mini 5 Pro</strong>", "LiPo 2S", "2700 mAh", "~300 cycles", "47 min"],
                    ["<strong>DJI Air 2S</strong>", "LiPo 3S", "3500 mAh", "~300 cycles", "31 min"],
                    ["<strong>DJI Air 3</strong>", "LiPo 3S", "4241 mAh", "~300 cycles", "46 min"],
                    ["<strong>DJI Mavic 3 / Classic</strong>", "LiPo 4S", "5000 mAh", "~300-400 cycles", "46 min"],
                    ["<strong>DJI Mavic 3 Pro</strong>", "LiPo 4S", "5000 mAh", "~300-400 cycles", "43 min"],
                    ["<strong>DJI Avata / FPV</strong>", "LiPo 6S", "2000/2420 mAh", "~200-300 cycles", "16-22 min"],
                    ["<strong>DJI Inspire 3</strong>", "LiPo 6S", "4890 mAh (x2)", "~400+ cycles", "28 min"],
                ]
            ) +
            p("These are DJI's rated cycle counts — your mileage may vary. \"Cycles to 80%\" means the battery will retain at least 80% of its original capacity after that many charge cycles, assuming proper use and storage. After 80%, the battery is considered significantly degraded and may cause issues like shorter flight times, sudden voltage drops, or even refusal to fly.")
        },
        {
            "id": "lipo-vs-liion",
            "title": "LiPo vs Li-ion Battery Chemistry",
            "content": p("Nearly all DJI consumer drones use lithium-polymer (LiPo) batteries, while some larger industrial models use lithium-ion (Li-ion). Here is how they compare:") +
            '<div class="grid md:grid-cols-2 gap-6 mb-6">' +
            '<div class="bg-navy-900/80 border border-purple-500/30 rounded-xl p-6">' +
            '<h3 class="font-bold text-xl mb-4 text-purple-400">LiPo (Lithium Polymer)</h3>' +
            '<ul class="space-y-3 text-sm text-gray-300">' +
            '<li>• <strong class="text-white">Used in:</strong> Most DJI consumer drones (Mini, Air, Mavic, Avata)</li>' +
            '<li>• <strong class="text-white">Energy density:</strong> Very high — light weight for the capacity</li>' +
            '<li>• <strong class="text-white">Voltage per cell:</strong> 3.7V nominal (4.2V full, 3.2V empty)</li>' +
            '<li>• <strong class="text-white">Cycle life:</strong> 200-400 cycles typical</li>' +
            '<li>• <strong class="text-white">Safety:</strong> Can be dangerous if damaged or overcharged — risk of fire</li>' +
            '<li>• <strong class="text-white">Charging speed:</strong> Fast charging possible (1C-2C)</li>' +
            '<li>• <strong class="text-white">Sensitivity:</strong> Very sensitive to over-discharge and physical damage</li>' +
            '<li>• <strong class="text-white">Packaging:</strong> Soft pouch or semi-rigid plastic case</li>' +
            '</ul></div>' +
            '<div class="bg-navy-900/80 border border-blue-500/30 rounded-xl p-6">' +
            '<h3 class="font-bold text-xl mb-4 text-blue-400">Li-ion (Lithium Ion)</h3>' +
            '<ul class="space-y-3 text-sm text-gray-300">' +
            '<li>• <strong class="text-white">Used in:</strong> Some larger DJI industrial drones, and many consumer electronics</li>' +
            '<li>• <strong class="text-white">Energy density:</strong> High, but slightly lower than best LiPo</li>' +
            '<li>• <strong class="text-white">Voltage per cell:</strong> 3.6-3.7V nominal</li>' +
            '<li>• <strong class="text-white">Cycle life:</strong> 500-1000+ cycles — longer than LiPo</li>' +
            '<li>• <strong class="text-white">Safety:</strong> Generally safer than LiPo, still requires proper handling</li>' +
            '<li>• <strong class="text-white">Charging speed:</strong> Typically 0.5C-1C (slower than LiPo)</li>' +
            '<li>• <strong class="text-white">Sensitivity:</strong> More durable, less sensitive to mild abuse</li>' +
            '<li>• <strong class="text-white">Packaging:</strong> Rigid cylindrical or prismatic cells</li>' +
            '</ul></div></div>' +
            p("DJI's Intelligent Battery system adds a built-in microcontroller (BMS — Battery Management System) to every battery pack. This BMS monitors each individual cell, balances charging, tracks cycle count, estimates remaining capacity, and implements safety features like overcharge protection, overdischarge protection, temperature monitoring, and self-discharge for long-term storage. This is a big reason DJI batteries last longer than generic LiPo batteries.") +
            alert("warning", "flame", "LiPo batteries require respect", "LiPo batteries can catch fire if they are punctured, overcharged, short-circuited, or deeply discharged. Always store LiPo batteries in a fire-safe container (LiPo bag) when not in use or during charging. Never leave charging batteries unattended. Do not use damaged or swollen batteries. Learn the proper way to dispose of LiPo batteries — do not throw them in the trash.")
        },
        {
            "id": "factors-affecting",
            "title": "Factors That Affect Battery Lifespan",
            "content": p("Many factors affect how long your drone batteries last. Some are under your control, some are not:") +
            grid_cards([
                {"title": "Depth of Discharge (DOD)", "color": "text-red-400", "desc": "How deeply you drain the battery before recharging has a huge impact on lifespan. Draining to 0-10% is much harder on the battery than landing with 20-30% remaining. Each deep discharge cycle shortens the battery's life. Try to land when the battery gets to 20-30% — it is much better for long-term health."},
                {"title": "Temperature Extremes", "color": "text-orange-400", "desc": "Heat is the #1 enemy of lithium batteries. Flying or storing batteries in hot temperatures (above 35°C / 95°F) accelerates degradation dramatically. Cold weather temporarily reduces performance but does not permanently damage batteries as much as heat. Never leave batteries in a hot car in direct sunlight — this can kill a battery in days."},
                {"title": "Storage Charge Level", "color": "text-yellow-400", "desc": "Storing batteries fully charged (100%) for weeks or months causes permanent capacity loss. Storing them fully discharged (0-10%) is even worse and can permanently kill the battery. The ideal storage charge is 40-60% — DJI batteries automatically self-discharge to this level after several days of inactivity."},
                {"title": "Charge Rate / Fast Charging", "color": "text-green-400", "desc": "Charging at higher speeds (higher C-rates) generates more heat and slightly reduces battery lifespan. DJI's standard chargers are designed to be safe, but using the fastest possible charger (like the 65W or 100W chargers) may cause slightly faster degradation over hundreds of cycles. For maximum lifespan, use standard-speed charging when you are not in a hurry."},
                {"title": "Age / Calendar Life", "color": "text-blue-400", "desc": "Lithium batteries degrade over time even if you never use them. A brand new battery that sits on a shelf for 3-5 years will have less capacity than when it was new, even with zero charge cycles. This is called calendar aging. It is better to rotate through your batteries and use them all rather than letting some sit unused for years."},
                {"title": "Physical Damage & Crashes", "color": "text-purple-400", "desc": "Physical impact from crashes can damage battery cells internally even if the outside looks fine. Internal damage can lead to reduced capacity, increased internal resistance, swelling, or even safety issues. If you crash hard, inspect your battery carefully and consider retiring it if you suspect internal damage. Better safe than sorry."},
            ], 2) +
            step_grid([
                {"title": "The #1 Killer of Drone Batteries", "desc": "Heat. Hot temperatures accelerate every degradation mechanism in lithium batteries. Leaving a battery in a hot car dashboard on a sunny day can permanently reduce its capacity by 20-50% in just a few hours. Always store batteries in a cool, shaded place. Never leave them in a closed car in the sun. This single factor is responsible for more premature battery death than anything else."},
            ], "red")
        },
        {
            "id": "signs-failing",
            "title": "Signs Your Battery Is Failing",
            "content": p("How do you know when a battery is reaching the end of its useful life? Watch for these signs:") +
            specs_table(
                ["Sign", "What It Means", "Severity", "What to Do"],
                [
                    ["<strong>Shorter flight time</strong>", "Capacity is degrading — normal with age", "Low-Med", "Monitor, plan for replacement soon"],
                    ["<strong>Sudden voltage drops</strong>", "Battery voltage drops rapidly under load", "High", "Stop using — risk of crash"],
                    ["<strong>Battery swells / puffs up</strong>", "Internal cell damage, gas buildup", "Very High", "Stop using immediately — fire risk"],
                    ["<strong>Drone won't take off</strong>", "Battery health too low, BMS rejects it", "High", "Replace battery"],
                    ["<strong>Error messages in app</strong>", "Battery abnormal, cell imbalance error, etc.", "Med-High", "Inspect, may need replacement"],
                    ["<strong>Cells out of balance</strong>", "Voltage difference between cells >0.1V", "Med", "Try storage mode / cycling, replace if persists"],
                    ["<strong>Won't hold charge</strong>", "Self-discharges quickly when stored", "Med-High", "Battery is aging, plan replacement"],
                    ["<strong>Charges very slowly</strong>", "Internal resistance increasing", "Med", "Normal with age, monitor"],
                ]
            ) +
            step_grid([
                {"title": "How to Check Battery Health in DJI Fly", "desc": "You can check your battery's health directly in the DJI Fly app: 1) Connect to the drone, 2) Go to the battery settings (tap battery icon), 3) Look for 'Battery Health' or 'Battery Information', 4) This shows cycle count, overall health percentage, and cell voltages. Different DJI models show different levels of detail — some show individual cell voltages, some just show an overall health score. Check regularly to track degradation over time."},
                {"title": "What Do Cell Voltages Tell You?", "desc": "A healthy LiPo battery should have all cells within 0.05-0.1V of each other. If one cell is significantly lower or higher than the others (more than 0.1-0.2V difference), the battery is becoming imbalanced. Minor imbalance can sometimes be fixed by running the battery through a few full charge-discharge cycles or using storage mode charging. Severe imbalance means the battery is failing and should be replaced."},
            ], "blue") +
            alert("critical", "flame", "Swollen batteries are dangerous", "If your battery is swollen, puffy, or bulging — stop using it immediately. Swelling is caused by gas buildup inside the cells from chemical breakdown. A swollen battery has a higher risk of catching fire or bursting. Do not charge a swollen battery. Do not puncture it. Store it in a fire-safe container away from flammable materials and dispose of it properly at a battery recycling center. When in doubt, replace the battery — it is not worth the risk.")
        },
        {
            "id": "extend-life",
            "title": "How to Extend Battery Life",
            "content": p("Follow these tips to get the maximum life out of your DJI drone batteries:") +
            step_grid([
                {"title": "Land With 20-30% Battery Remaining", "desc": "Avoid draining the battery all the way to 0-10%. Deep discharges are very hard on LiPo batteries. Set your low battery warning to 25-30% and land when it triggers. The last 10-20% of battery causes a disproportionate amount of wear. Getting in the habit of landing early can double your battery's cycle life."},
                {"title": "Never Leave Batteries in a Hot Car", "desc": "This is the single most important tip. Temperatures inside a closed car in direct sun can reach 60-70°C (140-160°F) in under an hour — hot enough to permanently damage or even destroy LiPo batteries. Always take batteries with you or leave them in a cool, shaded, ventilated place. Heat damage is cumulative and permanent."},
                {"title": "Store at 40-60% Charge", "desc": "Lithium batteries degrade slowest when stored at about 50% charge. DJI Intelligent Batteries automatically self-discharge to about 60% after 10 days of inactivity (you can adjust this in settings). If you know you will not fly for more than a week, discharge or charge to about 50% before storing. Never store fully charged for long periods."},
                {"title": "Store in Cool, Dry Place", "desc": "Ideal storage temperature is 15-25°C (59-77°F). Avoid temperature extremes. A closet or drawer at room temperature is perfect. Do not store in a garage, attic, or outdoor shed where temperatures swing wildly. A LiPo safety bag is recommended for fire safety, though it does not affect lifespan."},
                {"title": "Rotate Your Batteries", "desc": "If you have multiple batteries, rotate through them evenly rather than always using the same one first. This way, all batteries age at roughly the same rate. Label your batteries 1, 2, 3 and use them in order. Batteries that sit unused for months degrade from calendar aging anyway — you might as well use them."},
                {"title": "Use Standard Charging When You Can", "desc": "Fast charging is convenient, but it generates more heat and slightly accelerates degradation. When you are not in a hurry, use the standard charger or a lower-power charger. Charge at 0.5C-1C rather than 2C+ when possible. DJI's standard chargers are already optimized for a good balance of speed and battery health."},
                {"title": "Warm Up Batteries Before Cold Flights", "desc": "Flying in cold weather? Warm up the battery before flight. Put batteries in your pocket next to your body, or use a battery warmer. Cold batteries have reduced performance and voltage — they can sag and cause a crash if you push them hard. DJI batteries have a self-heating function on some newer models — enable it in cold weather."},
                {"title": "Cool Down Before Charging", "desc": "After a flight, the battery is warm from use. Let it cool down to room temperature before putting it on the charger. Charging a warm battery adds extra stress. Similarly, if a battery is very cold from winter flying, let it warm up to room temperature before charging."},
            ], "green") +
            alert("success", "heart", "Good battery habits pay off", "Pilots who follow best practices report getting 500-800+ cycles out of batteries rated for 300 cycles. While results vary, it is not uncommon for well-cared-for DJI batteries to last 4-6 years with moderate use. The extra effort of proper storage and charging habits really does pay for itself in reduced battery replacement costs.")
        },
        {
            "id": "storage-best-practices",
            "title": "Storage Best Practices",
            "content": p("Proper storage is one of the most important factors in battery longevity. Here is how to store DJI batteries correctly:") +
            '<div class="grid md:grid-cols-2 gap-6 mb-6">' +
            '<div>' +
            '<h3 class="font-bold text-xl mb-4 text-green-400">Short-Term Storage (1-4 weeks)</h3>' +
            '<ul class="space-y-3 text-sm text-gray-300">' +
            '<li>• <strong class="text-white">Charge level:</strong> 50-80% is fine for short periods</li>' +
            '<li>• <strong class="text-white">Temperature:</strong> Room temperature (15-25°C / 59-77°F)</li>' +
            '<li>• <strong class="text-white">Location:</strong> Cool, dry place out of direct sun</li>' +
            '<li>• <strong class="text-white">Container:</strong> LiPo bag recommended for fire safety</li>' +
            '<li>• <strong class="text-white">Self-discharge:</strong> DJI batteries will auto-discharge to storage level after ~10 days</li>' +
            '<li>• <strong class="text-white">Check:</strong> Quick visual inspection before each use</li>' +
            '</ul></div>' +
            '<div>' +
            '<h3 class="font-bold text-xl mb-4 text-blue-400">Long-Term Storage (1+ month)</h3>' +
            '<ul class="space-y-3 text-sm text-gray-300">' +
            '<li>• <strong class="text-white">Charge level:</strong> 40-60% — the sweet spot for long storage</li>' +
            '<li>• <strong class="text-white">Temperature:</strong> Cool (10-20°C / 50-68°F) — refrigerator is okay (sealed bag)</li>' +
            '<li>• <strong class="text-white">Location:</strong> Cool, dry, stable temperature</li>' +
            '<li>• <strong class="text-white">Container:</strong> Fire-safe LiPo storage bag or container</li>' +
            '<li>• <strong class="text-white">Check every:</strong> 1-2 months — top up to 50% if discharged</li>' +
            '<li>• <strong class="text-white">Before use:</strong> Full charge, then test fly with caution</li>' +
            '</ul></div></div>' +
            p("DJI Intelligent Batteries have a self-discharge feature that automatically brings the battery down to about 60% charge after 10 days of inactivity (the default can be changed in the app to 2, 4, 6, 8, or 10 days). This is a great feature — it means you do not have to manually discharge batteries before storing them. However, you should still not store batteries fully charged for long periods if you can avoid it.") +
            alert("info", "snowflake", "Can I store batteries in the fridge?", "Yes — storing LiPo batteries in the refrigerator (NOT the freezer) can actually slow down calendar aging and extend lifespan, especially for long-term storage. The cold temperature slows down the chemical reactions that cause degradation. If you do this: put the battery in a sealed plastic bag to prevent condensation, let it warm up to room temperature before opening the bag and using it, and never freeze LiPo batteries — freezing can permanently damage them.")
        },
        {
            "id": "replacement-cost",
            "title": "Battery Replacement Cost",
            "content": p("When the time comes to replace your drone batteries, here is what you can expect to pay (approximate 2026 prices for genuine DJI batteries):") +
            specs_table(
                ["Drone Model", "Battery Price (Single)", "Battery Price (Combo)", "Price per Wh", "Worth It?"],
                [
                    ["<strong>Mini 2 / SE</strong>", "$55-$75", "$140-$170 (3-pack)", "~$1.00/Wh", "Yes — cheap enough"],
                    ["<strong>Mini 3 / 4 Pro</strong>", "$65-$90", "$170-$220 (3-pack)", "~$0.80/Wh", "Yes — reasonable cost"],
                    ["<strong>Mini 5 Pro</strong>", "$75-$100", "$200-$260 (3-pack)", "~$0.85/Wh", "Yes — good value"],
                    ["<strong>Air 2S</strong>", "$90-$120", "$230-$300 (3-pack)", "~$0.80/Wh", "Yes"],
                    ["<strong>Air 3</strong>", "$110-$140", "$280-$360 (3-pack)", "~$0.85/Wh", "Yes"],
                    ["<strong>Mavic 3 series</strong>", "$170-$220", "$450-$550 (3-pack)", "~$0.90/Wh", "Maybe — expensive"],
                    ["<strong>Avata / FPV</strong>", "$75-$120", "$200-$320 (2-3 pack)", "~$1.00/Wh", "Yes"],
                    ["<strong>Inspire 3</strong>", "$400-$600 each", "—", "~$1.50+/Wh", "Depends on use case"],
                ]
            ) +
            grid_cards([
                {"title": "Genuine vs Third-Party Batteries", "color": "text-yellow-400", "desc": "Genuine DJI batteries are more expensive but have the proper BMS, fit perfectly, and are tested for compatibility. Third-party batteries are cheaper but vary wildly in quality. Some are fine, others have poor cells, no real BMS, and can be unsafe. We generally recommend genuine DJI batteries, especially for expensive drones — the cost of a crash from a bad battery is far more than you save on the battery."},
                {"title": "When to Replace vs Keep Using", "color": "text-green-400", "desc": "Replace immediately if: the battery is swollen, has cell imbalance >0.2V, drops out of the sky mid-flight, or throws constant errors. Consider replacing if: capacity is below 70-80% of original, flight time is too short for your needs, or the battery is 4+ years old. Keep using if: capacity is still 80%+, cells are balanced, no error messages, and it flies fine. Use your judgment — safety first."},
            ], 2) +
            alert("info", "recycle", "Recycle your old batteries", "Do not throw old drone batteries in the trash — they contain hazardous materials and can cause fires in garbage trucks and landfills. Take them to a battery recycling center, a home improvement store (Home Depot, Lowes), or an electronics store (Best Buy) that accepts rechargeable batteries for recycling. It is free, easy, and the right thing to do.")
        },
    ],
    "faqs": [
        {"q": "How many cycles do DJI drone batteries last?", "a": "DJI drone batteries are typically rated for 200-400 charge cycles before they drop to 80% of their original capacity. Mini series batteries are rated for ~200-300 cycles. Mavic and Air series batteries are rated for ~300-400 cycles. Higher-end professional models (Inspire, Matrice) are rated for 400+ cycles. These are estimates under ideal conditions — real-world lifespan depends heavily on how you use and store the batteries. With excellent care, many pilots report getting 500-800+ cycles before significant degradation."},
        {"q": "How do I check battery health on DJI drones?", "a": "You can check battery health in the DJI Fly app (or DJI Go 4 for older drones). Connect to your drone, go to the battery settings (tap the battery icon), and look for 'Battery Health' or 'Battery Information'. This shows you the cycle count, overall health percentage, and individual cell voltages. The exact information available varies by drone model — newer and higher-end drones show more detail. You can also see cycle count and voltage info in the battery details menu on the drone's own battery button on some models."},
        {"q": "What is the lifespan of DJI drone batteries in years?", "a": "With moderate use (50-100 flights per year) and proper storage, DJI drone batteries typically last 3-5 years before they degrade to 80% capacity or less. With heavy use (200+ flights per year), they may only last 1-2 years. With light use and excellent care, they can last 5-7 years or more. Note that lithium batteries degrade over time even if unused — a battery that sits on a shelf for 5 years will still have reduced capacity even with zero cycles. Calendar aging is unavoidable but can be slowed with proper storage."},
        {"q": "Is it bad to leave DJI batteries fully charged?", "a": "Yes — leaving LiPo batteries fully charged for extended periods (days to weeks) causes accelerated degradation. DJI Intelligent Batteries help mitigate this by automatically self-discharging to ~60% after 10 days of inactivity (adjustable). However, it is still better to manually discharge or use the battery if you know you will not fly for a while. For storage longer than a week, aim for 40-60% charge. Storing fully charged for months can permanently reduce capacity by 10-30% or more."},
        {"q": "Can DJI batteries be replaced?", "a": "Yes — DJI sells replacement batteries for all their consumer drone models. Prices range from $55 for Mini series batteries up to $200+ for Mavic 3 Pro batteries. You can also find third-party batteries from other brands at lower prices, but we recommend genuine DJI batteries for safety and reliability. The built-in BMS in DJI batteries is specifically designed for their drones, and third-party batteries may have compatibility issues or safety concerns."},
        {"q": "What temperature is bad for drone batteries?", "a": "Heat is the biggest enemy. Temperatures above 35°C (95°F) cause accelerated degradation, and temperatures above 50-60°C (122-140°F) can cause permanent damage or even thermal runaway. Never leave batteries in a hot car in direct sun — interior temperatures can reach 60-70°C in under an hour. Cold temperatures (below 0°C / 32°F) temporarily reduce performance and capacity but generally do not cause permanent damage unless the battery is frozen or charged while freezing cold."},
        {"q": "Should I discharge my drone battery after flying?", "a": "It depends on when you will fly next. If you will fly again within 1-3 days, it is fine to leave the battery at whatever charge level it is at. If you will not fly for a week or more, it is better to discharge (or charge) to about 50% for storage. DJI batteries auto-discharge to ~60% after 10 days, so you do not have to do anything if you can wait that long. For long-term storage (1+ month), definitely bring it to 40-60% charge."},
        {"q": "How do I properly dispose of DJI drone batteries?", "a": "Never throw LiPo batteries in the trash — they are hazardous waste and can cause fires. Take them to: a battery recycling center, Home Depot or Lowes (they have battery recycling bins), Best Buy (electronics recycling), or your local household hazardous waste facility. Completely discharge the battery first if possible (to 0% or near 0%), and put it in a LiPo bag for transport. Swollen or damaged batteries should be handled extra carefully — store them in a fire-safe container and take them to a hazardous waste facility."},
        {"q": "Are swollen drone batteries dangerous?", "a": "Yes — swollen or puffy LiPo batteries are a safety concern. Swelling is caused by gas buildup inside the cells from electrolyte breakdown. A swollen battery is at higher risk of thermal runaway (fire) if it is charged, punctured, or further damaged. If your battery is swollen: stop using it immediately, do not charge it, do not puncture it, store it in a fire-safe container away from flammable materials, and dispose of it properly at a battery recycling center. It is not worth the risk — just replace it."},
        {"q": "Do more expensive batteries last longer?", "a": "Generally, yes — higher-end DJI drone batteries tend to last slightly longer in terms of cycle count. Mavic 3 and Inspire batteries (rated 300-400+ cycles) usually outlast Mini series batteries (rated 200-300 cycles). This is because they use higher-quality cells, have better thermal management, and have more sophisticated BMS. However, care and storage habits matter much more than the battery's initial quality. A well-cared-for Mini battery can easily outlast a poorly cared-for Mavic battery."},
    ],
    "related": drone_related(),
}

# =================== PAGE 14: RAIN / WATER RESISTANCE ===================

page14 = {
    "filename": "can-you-fly-dji-drone-in-rain.html",
    "title": "Can You Fly a DJI Drone in the Rain? Water Resistance Guide (2026)",
    "headline": "Can You Fly a DJI Drone in the Rain? Water Resistance Guide (2026)",
    "meta_desc": "Can you fly a DJI drone in the rain? Complete water resistance guide covering IP ratings of DJI drones, which models are water-resistant, rain risks, what to do if your drone gets wet, and rainy day alternatives.",
    "category": "Drones",
    "category_link": "drones.html",
    "breadcrumb_title": "Rain & Water Resistance",
    "hero_blur": "bg-blue-500/5",
    "hero_badges": '''<div class="px-3 py-1.5 bg-blue-500/20 text-blue-400 font-mono font-bold text-sm rounded-md border border-blue-500/30">WATER&nbsp;RESISTANCE</div>
        <span class="badge badge-info"><i data-lucide="droplets" style="width:0.75rem;height:0.75rem"></i>IP Ratings</span>
        <span class="badge badge-info"><i data-lucide="cloud-rain" style="width:0.75rem;height:0.75rem"></i>Rain Safety</span>''',
    "h1": 'Can You Fly a DJI Drone in the Rain? &mdash; <span class="gradient-text">Water Resistance Guide 2026</span>',
    "hero_desc": "Flying in the rain is tempting for moody cinematic shots, but is it safe? Most DJI consumer drones are not designed for rain — water can damage the electronics, motors, gimbal, and camera. However, some newer and higher-end models have improved water resistance. In this guide, we cover IP ratings of DJI drones, which models can handle moisture, the risks of rain flying, what to do if your drone gets wet, drying tips, and alternatives for rainy days.",
    "hero_stats": f'''<div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="shield" style="width:0.9rem;height:0.9rem"></i>Mavic 3 Series</div>
          <div class="font-mono font-bold text-xl text-blue-400">IP42 rated</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="shield-off" style="width:0.9rem;height:0.9rem"></i>Mini Series</div>
          <div class="font-bold text-xl text-red-400">Not rated</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="cloud-rain" style="width:0.9rem;height:0.9rem"></i>Light Drizzle</div>
          <div class="font-mono font-bold text-xl text-yellow-400">Maybe (risky)</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="cloud-lightning" style="width:0.9rem;height:0.9rem"></i>Heavy Rain</div>
          <div class="font-bold text-xl text-red-400">Never</div>
        </div>''',
    "qa_gradient": "from-blue-950/20 to-navy-900 border-blue-500/20",
    "qa_icon_color": "#60a5fa",
    "qa_title": "Can You Fly DJI Drones in Rain?",
    "qa_text": '<strong class="text-white">Most DJI consumer drones (Mini, Air, Avata) are NOT waterproof or water-resistant — flying in any rain can damage them and void your warranty. Only certain models (Mavic 3 series, some industrial drones) have limited IP42 water resistance, which means they can handle light drizzle and splashes but not heavy rain.</strong> If you fly a non-water-resistant drone in the rain, water can seep into the electronics, motor windings, gimbal, and camera, causing short circuits, corrosion, and permanent damage. Even a light drizzle can be enough to cause problems, especially if water gets into the battery compartment or on exposed circuit boards. The gimbal camera is particularly vulnerable because it has exposed motors and delicate electronics. For the best results, wait for dry weather or use a drone specifically designed for wet conditions.',
    "qa_extra": f'''<div class="grid md:grid-cols-2 gap-3 mt-4">
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-green-400 font-semibold mb-1">Water-Resistant Models</div>
          <p class="text-sm text-gray-300">Mavic 3, Mavic 3 Classic, Mavic 3 Pro, Mavic 3E/T (enterprise), Matrice series</p>
        </div>
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-red-400 font-semibold mb-1">NOT Water-Resistant</div>
          <p class="text-sm text-gray-300">All Mini models, Air 2/2S, Air 3, Avata, FPV, Spark, Mavic Mini, Mavic 2</p>
        </div>
      </div>''',
    "sections": [
        {
            "id": "ip-ratings",
            "title": "IP Ratings Explained",
            "content": p("IP (Ingress Protection) ratings tell you how well a device is protected against dust and water. The first number is dust protection (0-6), the second is water protection (0-9). Here is what the ratings mean:") +
            specs_table(
                ["IP Rating", "Dust Protection", "Water Protection", "What It Means for Drones"],
                [
                    ["<strong>No rating</strong>", "No protection", "No protection", "Keep dry — any moisture is risky"],
                    ["<strong>IPX1</strong>", "—", "Dripping water (10 min)", "Protected against light drizzle only briefly"],
                    ["<strong>IPX2</strong>", "—", "Dripping water tilted 15°", "Can handle light drizzle from any angle briefly"],
                    ["<strong>IP42</strong>", "Solid objects >1mm", "Dripping water tilted 15°", "Dust-protected, light splash/drizzle resistant"],
                    ["<strong>IPX4</strong>", "—", "Splashing water (any direction)", "Can handle rain from any direction briefly"],
                    ["<strong>IP54</strong>", "Dust-protected", "Splashing water", "Industrial drones often have this"],
                    ["<strong>IP55</strong>", "Dust-protected", "Water jets", "Heavy rain resistant, but not submersible"],
                    ["<strong>IP67</strong>", "Dust-tight", "Immersion up to 1m", "Fully waterproof, can be submerged briefly"],
                ]
            ) +
            p("Important: most DJI consumer drones have NO official IP rating. DJI does not publish IP ratings for Mini series, Air series, or Avata drones — which means they are not designed for any exposure to water. Only Mavic 3 series (consumer and enterprise) and some Matrice/Inspire industrial drones have published water resistance ratings.") +
            alert("warning", "alert-triangle", "IP rating vs warranty", "Even if a drone has an IP rating, water damage may not be covered under warranty unless it is explicitly stated. DJI's standard warranty does not cover water damage, even on IP-rated models, if you use it beyond the specified conditions. Always read the fine print. IP ratings are tested under controlled laboratory conditions — real-world conditions (salt water, dirty water, high pressure) can be different.")
        },
        {
            "id": "water-resistant-models",
            "title": "DJI Drone Water Resistance by Model",
            "content": p("Here is the water resistance status of current popular DJI drone models:") +
            specs_table(
                ["Drone Model", "Water Resistance Rating", "Can Fly in Rain?", "Warranty Covers Water?"],
                [
                    ["<strong>DJI Mini 2 / SE / 3 / 4 / 5 Pro</strong>", "None — not rated", "No — any rain risks damage", "No — water damage not covered"],
                    ["<strong>DJI Air 2 / 2S</strong>", "None — not rated", "No — avoid moisture", "No — water damage not covered"],
                    ["<strong>DJI Air 3</strong>", "None — not officially rated", "No — avoid rain", "No — water damage not covered"],
                    ["<strong>DJI Mavic 3 / Classic</strong>", "IP42 (light drizzle)", "Light drizzle — yes, heavy rain — no", "Limited — depends on cause"],
                    ["<strong>DJI Mavic 3 Pro</strong>", "IP42 (light drizzle)", "Light drizzle — yes, heavy rain — no", "Limited — depends on cause"],
                    ["<strong>DJI Avata</strong>", "None — not rated", "No — avoid water", "No — water damage not covered"],
                    ["<strong>DJI FPV</strong>", "None — not rated", "No — avoid water", "No — water damage not covered"],
                    ["<strong>DJI Mavic 3 Enterprise (E/T)</strong>", "IP54", "Can handle moderate rain", "Better but still limited"],
                    ["<strong>DJI Matrice 30 / 300 RTK</strong>", "IP55", "Can handle heavy rain", "Enterprise warranty"],
                ]
            ) +
            grid_cards([
                {"title": "Mavic 3 Series IP42 — What It Means", "color": "text-blue-400", "desc": "The Mavic 3 series has IP42 water resistance, which means: protected against solid objects larger than 1mm (so dust is mostly kept out), and protected against dripping water when tilted up to 15 degrees. In practice, this means the Mavic 3 can handle light drizzle and a few raindrops without damage. But it is NOT designed for steady rain, heavy rain, or being submerged. DJI still recommends not flying in rain if you can avoid it."},
                {"title": "Enterprise Drones — IP54/IP55", "color": "text-green-400", "desc": "DJI's enterprise and industrial drones (Mavic 3 Enterprise, Matrice 30, Matrice 300 RTK) have higher IP ratings (IP54 or IP55) because they are designed for work in all weather conditions — public safety, inspection, surveying, etc. These can genuinely handle moderate to heavy rain. However, they are also much more expensive ($3,000-$20,000+) and are not typical consumer drones."},
            ], 2)
        },
        {
            "id": "rain-risks",
            "title": "Risks of Flying in the Rain",
            "content": p("Even if your drone can technically survive a little rain, there are good reasons to avoid it:") +
            step_grid([
                {"title": "Electrical Short Circuits", "desc": "Water conducts electricity. If water gets inside the drone body and onto circuit boards, it can cause short circuits that damage electronics instantly. This can cause the drone to crash mid-flight, or damage the battery, flight controller, camera, or other components. Short circuits from water are one of the most common causes of drone water damage."},
                {"title": "Motor Damage", "desc": "Drone motors are brushless and have exposed windings. Water in the motors can cause corrosion over time, even if the drone seems fine after drying. Water can also wash out the lubrication from motor bearings, causing them to wear out faster and potentially fail mid-flight. Motors are expensive to replace — often $50-$100 each."},
                {"title": "Gimbal & Camera Damage", "desc": "The gimbal and camera are the most delicate parts of the drone. They have tiny motors, sensors, and ribbon cables that are very sensitive to water. Water can fog the lens from the inside, damage the image sensor, corrode gimbal motor windings, or cause the gimbal to malfunction. Gimbal repairs are expensive — often $200-$500, or it may be cheaper to replace the whole camera/gimbal assembly."},
                {"title": "Battery Damage", "desc": "Water in the battery compartment can cause corrosion on the battery contacts and the drone's power terminals. If water gets inside the battery itself (which it can if the seals are compromised), it can cause a short circuit inside the battery — potentially leading to swelling or even a fire. Always inspect battery contacts after exposure to moisture."},
                {"title": "Corrosion (Hidden Damage)", "desc": "Even if the drone seems fine after getting wet, water can cause corrosion that shows up weeks or months later. This is especially true with salt water or dirty water. Corrosion slowly eats away at metal contacts, circuit board traces, and motor windings. A drone that survived a rain flight might mysteriously fail months later due to hidden corrosion."},
                {"title": "Reduced Performance", "desc": "Water on the propellers and body can affect aerodynamics and flight performance. Rain can interfere with the camera image — raindrops on the lens ruin photos and video. Moisture can also fog the lens from the inside due to temperature differences. Heavy rain can even weigh the drone down slightly and reduce flight time."},
                {"title": "Warranty Void", "desc": "Water damage is almost always excluded from DJI's standard warranty. If your drone breaks from water damage and you send it in for repair, DJI will likely charge you for the repair even if the drone is still under warranty. DJI Care Refresh covers accidental damage including water damage on most plans — but only if you have the coverage and it was truly an accident."},
            ], "red") +
            alert("critical", "waves", "Salt water is especially dangerous", "Flying near the ocean? Salt water is far more corrosive and conductive than fresh water. Even a few drops of salt spray can cause serious corrosion damage over time. If your drone gets anywhere near salt water, rinse it with fresh water (distilled or deionized water, carefully) and dry it thoroughly as soon as possible. Saltwater damage can destroy a drone in days or weeks if not cleaned properly.")
        },
        {
            "id": "if-gets-wet",
            "title": "What to Do If Your Drone Gets Wet",
            "content": p("If your drone gets caught in unexpected rain or lands in water, follow these steps immediately:") +
            step_grid([
                {"title": "Step 1: Power Off Immediately", "desc": "As soon as the drone is back in your hands, turn it off. Press and hold the power button until it shuts down. If it is already off (crashed in water), do NOT turn it on to test it. Turning on a wet drone is the #1 way to cause permanent damage from short circuits. The battery is the most dangerous part — remove it carefully if you can do so safely."},
                {"title": "Step 2: Remove the Battery", "desc": "Take the battery out right away. This cuts power to everything and prevents further short circuit damage. Be careful not to press any buttons — just eject the battery. Set the battery aside in a safe place (on a non-flammable surface, away from anything flammable) and inspect it later for damage or swelling."},
                {"title": "Step 3: Shake Off Excess Water", "desc": "Gently shake the drone to get as much water out as possible. Pay special attention to the motors, gimbal area, battery compartment, and any openings. Do not shake so hard that you damage the gimbal or other delicate parts — be firm but gentle. Wipe the outside dry with a soft, clean cloth."},
                {"title": "Step 4: Dry It Thoroughly", "desc": "Now you need to dry the drone completely. Options include: rice (fill a container with uncooked rice, bury the drone, leave 24-48 hours — somewhat effective but dusty), silica gel packets (better — use lots of them in a sealed container), or just air drying in a warm (not hot), dry place with good airflow. Do NOT use a hair dryer or oven — too much heat can damage plastic and electronics. 48-72 hours of drying is the minimum for water exposure."},
                {"title": "Step 5: Inspect Carefully Before Testing", "desc": "After drying, inspect the drone thoroughly before even thinking about turning it on. Look for: water droplets inside the lens, corrosion on contacts, residue or dirt inside, gimbal stiffness, motor grinding. Check the battery too — if it is swollen or damaged, do not use it. If everything looks clean and dry, you can try a quick test."},
                {"title": "Step 6: Test Cautiously", "desc": "Insert the battery, turn the drone on, and check for error messages. Check the camera, gimbal, and all controls. Do a quick hover test at low altitude in an open area — do not fly far or high on the first test flight. If anything seems off (weird noises, error messages, unstable flight), land immediately and get it checked out. When in doubt, send it to DJI for inspection."},
            ], "yellow") +
            alert("warning", "droplets", "Fogging inside the lens?", "If you see condensation or fogging inside the camera lens, do not panic — it usually goes away as the drone dries out. Put the drone in a sealed container with silica gel packets for 1-3 days. The moisture will gradually evaporate and be absorbed by the silica. Do not use the camera until the fog is completely gone — moisture on the sensor can cause spots or damage. If fog persists for more than a week, you may need professional service.")
        },
        {
            "id": "drying-tips",
            "title": "Drying Tips & Techniques",
            "content": p("How you dry your drone matters. Here are the best methods:") +
            specs_table(
                ["Drying Method", "Effectiveness", "Time", "Risks", "Notes"],
                [
                    ["<strong>Silica gel</strong>", "Excellent", "24-72 hours", "Low", "Best method — use lots of packets"],
                    ["<strong>Uncooked rice</strong>", "Moderate", "48-72 hours", "Low", "Common but less effective, gets dusty"],
                    ["<strong>Air drying (room temp)</strong>", "Good", "3-7 days", "Low", "Slow but safe — good airflow helps"],
                    ["<strong>Fan / forced air</strong>", "Good", "24-48 hours", "Low", "Speed up drying with gentle airflow"],
                    ["<strong>Hair dryer (cool setting)</strong>", "Fair", "Hours", "Medium", "Use only cool setting, keep distance"],
                    ["<strong>Hair dryer (hot)</strong>", "Terrible", "—", "High", "Never — heat melts plastic, damages electronics"],
                    ["<strong>Oven / microwave</strong>", "Terrible", "—", "Very High", "Never — will destroy the drone"],
                ]
            ) +
            step_grid([
                {"title": "Pro Drying Tips", "desc": "1) Use lots of silica gel — more is better. You can buy big boxes of silica gel packets cheaply online. 2) Use a sealed container (plastic bin, ziplock bag) to keep the silica gel working efficiently. 3) Put the drone on its side or upside down to let water drain out of crevices. 4) Open all ports and covers (battery door, SD card slot, USB port) to let air circulate. 5) Be patient — 48 hours minimum, 72 hours is better. Turning it on too early is the #1 mistake people make."},
            ], "green") +
            alert("info", "flask-conical", "Distilled water rinse for saltwater", "If your drone was exposed to salt water, you need to rinse off the salt before drying. Use distilled or deionized water (not tap water, which has minerals) to gently rinse the affected areas. Salt crystals left behind will corrode everything they touch. After rinsing, dry thoroughly as described above. This feels counterintuitive (putting more water on a wet drone), but it is necessary for salt water exposure and can save your drone from slow corrosion death.")
        },
        {
            "id": "fogging",
            "title": "Fogging & Condensation Issues",
            "content": p("Even if you do not fly in the rain, you might encounter fogging or condensation inside the camera lens or drone body when flying in humid conditions or moving between temperature extremes.") +
            step_grid([
                {"title": "What Causes Fogging?", "desc": "Condensation happens when warm, moist air hits a cold surface. If you take a cold drone from an air-conditioned house or car out into warm, humid air, moisture from the air can condense on the cold electronics and inside the camera lens. The same thing happens in reverse: a warm drone going into a cold environment. Fogging is basically tiny water droplets forming on surfaces inside the drone."},
                {"title": "Is Fogging Dangerous?", "desc": "Minor fogging that goes away quickly is usually not dangerous — it is just surface moisture that will evaporate. But heavy or persistent condensation can be a problem: it can cause short circuits if enough water accumulates, it can cause corrosion over time, and it ruins photos and video. If you see heavy condensation inside the camera body or drone, stop flying and let it dry out."},
                {"title": "How to Prevent Fogging", "desc": "1) Acclimate the drone gradually — let it warm up or cool down to the ambient temperature in its case before taking it out. 2) Use silica gel packets in your drone case to absorb moisture. 3) Keep the drone in its case when moving between temperature extremes. 4) In very humid conditions, power on the drone and let it run for a few minutes before takeoff — the heat from electronics helps evaporate moisture. 5) Consider anti-fog inserts for the camera if you frequently fly in humid conditions."},
                {"title": "How to Fix Fogged Lens", "desc": "If the lens fogs up mid-flight, the best thing to do is land and wait. Usually, the warmth from the drone's electronics will clear it within a few minutes. You can also: point the camera toward the sun (carefully — do not look at the sun through the camera), gently warm the camera with your hand, or use a lens cloth on the outside (only the outside — never try to clean the inside of the lens). If fogging is severe, land and let the drone acclimate."},
            ], "blue")
        },
        {
            "id": "rainy-day-alternatives",
            "title": "Rainy Day Alternatives",
            "content": p("If it is raining and you cannot fly, here are some productive things to do instead:") +
            grid_cards([
                {"title": "Edit Your Footage", "color": "text-purple-400", "desc": "Rainy days are perfect for editing. Go through your past flights, organize your footage, and edit that video you have been putting off. Use software like Adobe Premiere Pro, Final Cut Pro, DaVinci Resolve (free!), or CapCut. You can also organize your photo library, tag your best shots, and back everything up."},
                {"title": "Plan Your Next Flight", "color": "text-blue-400", "desc": "Plan where you want to fly next. Use Google Earth to scout locations, check out photo spots, and plan flight routes. Research the local drone laws for new areas. Check weather forecasts for the coming week. Join drone forums and see what other pilots are sharing. Learn about new flying techniques."},
                {"title": "Maintain Your Drone", "color": "text-green-400", "desc": "Rainy days are great for drone maintenance. Clean your drone — wipe down the body, clean the lens, check motors for debris, inspect propellers for nicks and cracks. Update firmware on the drone, controller, and batteries. Calibrate the compass and IMU. Check battery health. Organize your gear. Back up your SD card."},
                {"title": "Learn New Skills", "color": "text-yellow-400", "desc": "Watch tutorials on YouTube. Learn about cinematic flying techniques, photography composition, video editing, color grading. Practice on a drone simulator (many great simulators are available). Read the drone manual — you will probably learn something you did not know. Study local drone regulations and airspace rules."},
                {"title": "Indoor Flying (Carefully)", "color": "text-pink-400", "desc": "If you have a small, lightweight drone (like a Mini or an indoor FPV drone), you can fly carefully indoors on rainy days. Make sure you have enough space, no fragile objects around, and you are comfortable flying in tight spaces. Indoor flying is great practice for precise maneuvers. Start slow and stay low. A small crash inside is much better than a crash in the rain."},
                {"title": "Work on Your Setup", "color": "text-orange-400", "desc": "Tinker with your gear: organize your drone bag, install new accessories, test out filters, adjust controller settings, set up your photo and video presets. Experiment with different camera settings to see what you like. Make a checklist for your pre-flight routine. Upgrade your editing workstation. The possibilities are endless."},
            ], 2) +
            alert("success", "umbrella", "Patience is a virtue", "It can be frustrating to wake up to rain when you were excited to fly. But remember: pushing your luck in bad weather is how drones get damaged or lost. The rain will pass, and your drone will be ready to fly when the sun comes out. Use the rainy day productively and you will come out ahead. Plus, the light after rain can be amazing for photos — wait for the rain to stop and you might get incredible shots."),
        },
    ],
    "faqs": [
        {"q": "Can I fly my DJI Mini in the rain?", "a": "No — DJI Mini drones (all models: Mini 2, Mini SE, Mini 3, Mini 4 Pro, Mini 5 Pro) have NO official water resistance rating. Flying in any rain, even light drizzle, risks damaging the electronics, gimbal, camera, and motors. Water damage is not covered under warranty. If you get caught in unexpected rain, land immediately, turn off the drone, remove the battery, and dry it thoroughly for at least 48-72 hours before testing it again."},
        {"q": "Which DJI drones are waterproof?", "a": "No DJI consumer drones are fully waterproof (IP67 or submersible). The most water-resistant consumer DJI drone is the Mavic 3 series (Mavic 3, Mavic 3 Classic, Mavic 3 Pro), which has an IP42 rating — meaning it can handle light drizzle and splashes but not heavy rain or submersion. DJI's enterprise and industrial drones (Mavic 3 Enterprise, Matrice 30, Matrice 300 RTK) have higher ratings (IP54 or IP55) and can handle moderate to heavy rain. No Mini, Air, Avata, or FPV model is water-resistant."},
        {"q": "What does IP42 mean?", "a": "IP42 is an Ingress Protection rating. The '4' means the drone is protected against solid objects larger than 1mm (basic dust protection). The '2' means it is protected against dripping water when the device is tilted up to 15 degrees. In practical terms for a drone, IP42 means it can handle light drizzle and a few raindrops without damage, but it is NOT designed for steady rain, heavy rain, or being submerged. DJI still recommends avoiding rain even with IP42-rated drones."},
        {"q": "What should I do if my drone gets wet?", "a": "If your drone gets caught in rain or lands in water: 1) Power off immediately (do NOT turn it on to test). 2) Remove the battery right away. 3) Gently shake off excess water. 4) Dry the drone completely for 48-72 hours using silica gel packets (best), uncooked rice, or just air drying in a warm dry place. 5) Inspect carefully for damage or corrosion before testing. 6) Test cautiously with a short hover at low altitude. If anything seems wrong, do not fly — get it serviced. The most common mistake is turning it on too early — be patient and let it dry completely."},
        {"q": "Is it safe to fly in light drizzle?", "a": "It depends on the drone. For non-water-resistant drones (all Mini, Air, Avata, FPV models): no — even light drizzle can cause damage over time, and a sudden heavier rain could be disastrous. For IP42-rated drones (Mavic 3 series): light drizzle is probably fine, but it is still risky. You never know when drizzle will turn into real rain. If you can avoid it, wait for better weather. If you must fly in drizzle with a water-resistant drone, keep flights short and stay close to home so you can land quickly if it gets worse."},
        {"q": "Will DJI warranty cover water damage?", "a": "Generally, no — standard DJI warranty does not cover water damage, even on IP-rated models. The warranty covers manufacturing defects, not accidental damage from weather or pilot error. However, DJI Care Refresh (DJI's optional accident protection plan) does cover water damage on most drones, as long as it is accidental and you pay the replacement fee. Always check the details of your specific plan. If you fly near water or in variable weather, DJI Care Refresh is usually worth it."},
        {"q": "Can I fly right after it rains?", "a": "Yes — flying after rain is fine as long as it is no longer actively raining and the drone stays dry. However, be aware of: wet ground (can dirty the camera if you take off from muddy ground), fogging/condensation (if the drone was in a warm house and you take it into cool humid air), wind (storms often leave gusty winds), and puddles (avoid low-altitude flying over puddles — water spray from prop wash could get on the drone)."},
        {"q": "How do I dry out a wet drone?", "a": "The best way is with silica gel packets: put the drone (and battery, separately) in a sealed container with lots of silica gel packets and leave it for 48-72 hours. Silica gel absorbs moisture from the air. Uncooked rice works in a pinch but is less effective and leaves dust. Air drying in a warm (not hot), dry place with good airflow also works but takes longer (3-7 days). Never use a hair dryer on hot, oven, or microwave — heat damages plastic and electronics. The key is patience — do not turn it on until it is completely dry."},
        {"q": "What if there is fog inside the camera lens?", "a": "Fogging inside the lens is caused by condensation — moisture in the air condensing on cold surfaces. It is usually not permanent. To fix it: put the drone in a sealed container with silica gel packets for 1-3 days. The silica gel will absorb the moisture. You can also try turning the drone on and letting it run — the warmth from the electronics helps evaporate moisture. Wipe the outside of the lens with a microfiber cloth, but never try to clean the inside. If fogging persists for more than a week, the seal may be compromised and you should get it serviced."},
        {"q": "Can I fly my Mavic 3 in the rain?", "a": "The Mavic 3 has an IP42 rating, which means it can handle light drizzle and splashes. DJI says it is tested to withstand dripping water and light rain. However, DJI still recommends not flying in rain if you can avoid it, and water damage may not be covered under warranty. If you do fly your Mavic 3 in light rain: keep flights short, stay close to home, be ready to land immediately if it gets heavier, and dry the drone thoroughly afterward. Heavy rain, storms, or flying near water (ocean spray, etc.) are still risky even with IP42."},
    ],
    "related": drone_related(),
}

PAGES = [page13, page14]

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
