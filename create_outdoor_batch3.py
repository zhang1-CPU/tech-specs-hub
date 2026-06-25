#!/usr/bin/env python3
"""Generate batch 3: Outdoor Power pages 5-7."""

import os, json, html, re
from typing import List, Dict, Any

OUTPUT_DIR = "/workspace/pages/specs"
BASE_URL = "https://powerspecshub.com/pages/specs"
SITE_NAME = "TechSpecsHub"
UPDATED_DATE = "2026-06-25"

color_map = {"green": "4ade80", "red": "f87171", "yellow": "facc15", "blue": "60a5fa", "purple": "a78bfa", "electric": "22d3ee", "orange": "fb923c"}

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

# =================== PAGE 5: TAILGATING ===================

page5 = {
    "filename": "portable-power-station-for-tailgating.html",
    "title": "Best Portable Power Station for Tailgating & Outdoor Events (2026)",
    "headline": "Best Portable Power Station for Tailgating & Outdoor Events (2026)",
    "meta_desc": "Best portable power stations for tailgating, parties, and outdoor events. Power TVs, speakers, grills, and more — top picks, device power draw, setup tips, and solar for all-day events.",
    "category": "Outdoor Power",
    "category_link": "outdoor-power.html",
    "breadcrumb_title": "Tailgating Power Guide",
    "hero_blur": "bg-purple-500/5",
    "hero_badges": '''<div class="px-3 py-1.5 bg-purple-500/20 text-purple-400 font-mono font-bold text-sm rounded-md border border-purple-500/30">TAILGATING</div>
        <span class="badge badge-info"><i data-lucide="party-popper" style="width:0.75rem;height:0.75rem"></i>Outdoor Events</span>
        <span class="badge badge-info"><i data-lucide="tv" style="width:0.75rem;height:0.75rem"></i>TV &amp; Audio</span>''',
    "h1": 'Best Portable Power Station for Tailgating &amp; Outdoor Events &mdash; <span class="gradient-text">2026 Guide</span>',
    "hero_desc": "A portable power station turns your tailgate from basic to legendary. Power a big-screen TV, blast music from speakers, keep drinks cold with a portable fridge, charge everyone's phones, and even run an electric grill or hot plate. No more hunting for an outlet at the stadium, no more noisy generators ruining the vibe. This guide covers everything you need: how much power you actually need, what devices draw, our top picks for different group sizes, and pro setup tips for the ultimate tailgate setup.",
    "hero_stats": f'''<div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="users" style="width:0.9rem;height:0.9rem"></i>Small Group</div>
          <div class="font-mono font-bold text-xl text-electric-400">500&ndash;1000Wh</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="users" style="width:0.9rem;height:0.9rem"></i>Medium Group</div>
          <div class="font-bold text-xl text-green-400">1,000&ndash;2,000Wh</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="users" style="width:0.9rem;height:0.9rem"></i>Big Party</div>
          <div class="font-bold text-xl text-yellow-400">2,000Wh+</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="volume-2" style="width:0.9rem;height:0.9rem"></i>Quiet?</div>
          <div class="font-mono font-bold text-xl text-white">100% Silent</div>
        </div>''',
    "qa_gradient": "from-purple-950/20 to-navy-900 border-purple-500/20",
    "qa_icon_color": "#a78bfa",
    "qa_title": "Best Power Station for Tailgating",
    "qa_text": '<strong class="text-white">For most tailgates, a 1,000-2,000Wh portable power station with 1,500-2,400W output is the perfect sweet spot — it powers a TV, speaker, phone chargers, and a mini fridge for 6+ hours.</strong> For small groups (2-4 people), a 500-1,000Wh station handles speakers, phones, and a small TV. For big parties with multiple TVs, full-size fridges, and electric grills, go with 2,000Wh+ and 2,000W+ output. The biggest advantage over generators? Zero noise, zero fumes, and zero fuel hassle — you can have conversations and enjoy music without generator roar.',
    "qa_extra": f'''<div class="grid md:grid-cols-2 gap-3 mt-4">
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-green-400 font-semibold mb-1 flex items-center gap-2"><i data-lucide="check-circle" style="width:1rem;height:1rem"></i>Power station vs generator</div>
          <p class="text-sm text-gray-300">Silent, no fumes, no fuel needed, less maintenance, indoor-safe, instant power. Generator wins for all-day high-power use.</p>
        </div>
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-purple-400 font-semibold mb-1 flex items-center gap-2"><i data-lucide="sun" style="width:1rem;height:1rem"></i>All-day tailgating</div>
          <p class="text-sm text-gray-300">Pair your power station with 200-400W of portable solar panels to recharge during the day and keep the party going indefinitely.</p>
        </div>
      </div>''',
    "sections": [
        {
            "id": "tailgating-power-needs",
            "title": "Tailgating Power Needs — What Devices Draw",
            "content": p("The first step in choosing a tailgating power station is figuring out what you want to power and how much electricity each device uses. Here are the most common tailgating devices and their power draw:") +
            specs_table(
                ["Device", "Running Watts", "Surge Watts", "Per Hour (Wh)"],
                [
                    ["<strong>50\" LED TV</strong>", "60–100W", "150–200W", "60–100 Wh"],
                    ["<strong>65\" LED TV</strong>", "80–150W", "200–300W", "80–150 Wh"],
                    ["<strong>Bluetooth Speaker (large)</strong>", "20–80W", "—", "20–80 Wh"],
                    ["<strong>Home Stereo / Receiver</strong>", "100–300W", "300–500W", "100–300 Wh"],
                    ["<strong>Portable Fridge (12V)</strong>", "40–80W", "100–150W", "400–800 Wh/day"],
                    ["<strong>Electric Grill</strong>", "1,200–1,800W", "—", "1,200–1,800 Wh/hr"],
                    ["<strong>Electric Hot Plate</strong>", "1,000–1,500W", "—", "1,000–1,500 Wh/hr"],
                    ["<strong>Microwave (700W)</strong>", "800–1,100W", "1,500–2,000W", "Varies by use"],
                    ["<strong>Phone Charger (per phone)</strong>", "5–15W", "—", "5–15 Wh"],
                    ["<strong>Laptop Charger</strong>", "45–100W", "—", "45–100 Wh"],
                    ["<strong>String Lights (LED)</strong>", "10–30W", "—", "10–30 Wh"],
                    ["<strong>Crockpot / Slow Cooker</strong>", "150–250W", "—", "150–250 Wh/hr"],
                ]
            ) +
            p("As a general rule of thumb for a typical 4-6 hour tailgate:") +
            '<ul class="space-y-2 text-sm text-gray-300 mb-4">' +
            '<li>• <strong class="text-white">Basic setup:</strong> Speaker + phones + string lights = ~100-200W total, ~500-1,000Wh for 6 hours</li>' +
            '<li>• <strong class="text-white">Standard setup:</strong> 55" TV + speaker + phones + fridge = ~200-350W, ~1,200-2,000Wh for 6 hours</li>' +
            '<li>• <strong class="text-white">Premium setup:</strong> 65" TV + sound system + 2 fridges + electric grill = ~600-1,000W average, ~3,000-6,000Wh for 6 hours</li>' +
            '</ul>' +
            p("Remember: the fridge is usually the biggest power consumer because it runs all day. If you can use a regular cooler with ice instead of an electric fridge, you slash your power needs dramatically. Electric grills are also huge power hogs — charcoal or propane grills are more tailgate-friendly for a reason.") +
            alert("info", "lightbulb", "Pro tip for sizing", "Size your power station for 1.5x what you think you need. It is better to have extra capacity than to run out of power before kickoff. Also, people always want to charge their phones — you would not believe how many random people will ask to plug in. More capacity = more popular tailgate.")
        },
        {
            "id": "top-picks-tailgating",
            "title": "Top Picks by Group Size",
            "content": p("Here are our recommended power stations for different tailgate sizes in 2026:") +
            '<div class="space-y-6 mb-6">' +
            '<div class="bg-navy-900/80 border border-white/10 rounded-xl p-6">' +
            '<div class="flex items-center gap-3 mb-4"><div class="px-3 py-1 bg-electric-500/20 text-electric-400 font-mono font-bold text-sm rounded-md border border-electric-500/30">SMALL&nbsp;GROUPS</div><span class="text-gray-400 text-sm">2–4 people</span></div>' +
            '<h3 class="font-bold text-2xl mb-3 text-white">Best for Small Tailgates &amp; Pregames</h3>' +
            p("<strong>Top Pick: Jackery Explorer 500 (518Wh)</strong> — The classic tailgate workhorse for small groups. 500W output handles a TV, speaker, and phone chargers easily. Lightweight (13 lbs), easy to carry, reliable brand. Includes car charging cable so you can top it up on the drive to the game. Not enough for a fridge or electric grill, but perfect for the essentials.") +
            p("<strong>Runner-up: Anker 521 PowerHouse (256Wh)</strong> — Ultra-compact and lightweight (9 lbs). Perfect if you just need speakers, phone charging, and maybe a small 32\" TV. The 200W output is limiting but enough for basic tailgating. 5-year warranty is a big plus.") +
            p("<strong>Upgrade Pick: EcoFlow River 2 Pro (768Wh)</strong> — 800W output (1,600W surge) gives you more headroom. Can run a small fridge if you want. Very fast charging (70 minutes 0-100%). Lightweight and portable. Great all-around small tailgate station.") +
            "</div>" +
            '<div class="bg-navy-900/80 border border-white/10 rounded-xl p-6">' +
            '<div class="flex items-center gap-3 mb-4"><div class="px-3 py-1 bg-green-500/20 text-green-400 font-mono font-bold text-sm rounded-md border border-green-500/30">MEDIUM&nbsp;GROUPS</div><span class="text-gray-400 text-sm">4–10 people</span></div>' +
            '<h3 class="font-bold text-2xl mb-3 text-white">Best for the Standard Tailgate</h3>' +
            p("<strong>Top Pick: Bluetti AC180 (1,152Wh)</strong> — The sweet spot for most tailgaters. 1,800W output handles almost anything except full-size electric grills. Powers a 65\" TV, big speaker, portable fridge, and 10+ phone chargers simultaneously. 1,152Wh capacity gives you 6+ hours of tailgating. Very well-built, tons of ports.") +
            p("<strong>Runner-up: EcoFlow Delta 2 (1,024Wh)</strong> — 1,800W output (2,700W surge), expandable to 3kWh. Faster charging than the Bluetti (80% in 50 minutes). Great app for monitoring. Slightly less capacity than AC180 but more features. Expandable if you later need more power.") +
            p("<strong>Value Pick: Jackery Explorer 1000 v2 (1,024Wh)</strong> — Reliable, simple, no app needed (great for people who hate apps). 1,500W continuous output. Proven design. Excellent customer support. You pay a bit of a premium for the Jackery name, but you get peace of mind.") +
            "</div>" +
            '<div class="bg-navy-900/80 border border-white/10 rounded-xl p-6">' +
            '<div class="flex items-center gap-3 mb-4"><div class="px-3 py-1 bg-purple-500/20 text-purple-400 font-mono font-bold text-sm rounded-md border border-purple-500/30">BIG&nbsp;PARTIES</div><span class="text-gray-400 text-sm">10+ people / all-day</span></div>' +
            '<h3 class="font-bold text-2xl mb-3 text-white">Best for Big Tailgates &amp; All-Day Parties</h3>' +
            p("<strong>Top Pick: EcoFlow Delta Pro 3 (4,096Wh)</strong> — The ultimate tailgate machine. 4,000W continuous output handles multiple TVs, full sound systems, multiple fridges, even an electric grill occasionally. 4kWh capacity means all-day power without worrying. Add solar panels for indefinite partying. Heavy (93 lbs) but has wheels. This is the power station that makes you the most popular tailgate in the lot.") +
            p("<strong>Runner-up: Jackery Explorer 2000 Plus (2,042Wh)</strong> — 2,200W output, expandable to 8kWh with extra battery packs. 2kWh is enough for most all-day tailgates with a TV, sound system, and fridge. Expandable if you need more later. Reliable Jackery quality.") +
            p("<strong>Budget Big Pick: Bluetti AC200P (2,000Wh)</strong> — Great value for the capacity. 2,000W output, 700W solar input. Not as many smart features as EcoFlow, but solid build quality and good value. Heavier than competitors but you get a lot of watt-hours per dollar.") +
            "</div>" +
            "</div>"
        },
        {
            "id": "tv-speaker-power",
            "title": "TV &amp; Speaker Setup for Tailgating",
            "content": p("The centerpiece of any great tailgate is the TV and sound system. Here is what you need to know about powering them:") +
            '<div class="grid md:grid-cols-2 gap-6 mb-6">' +
            '<div>' +
            '<h3 class="font-bold text-xl mb-4 text-electric-400">TV Considerations</h3>' +
            '<ul class="space-y-3 text-sm text-gray-300">' +
            '<li><strong class="text-white">Size:</strong> 50-55" is the sweet spot for most tailgates. Big enough to see, small enough to transport. 65" is great if you have the space and power.</li>' +
            '<li><strong class="text-white">LED vs OLED:</strong> LED is better for tailgating — brighter, cheaper, less fragile, and uses less power. OLED looks amazing but is hard to see in sunlight, uses more power, and is easily damaged.</li>' +
            '<li><strong class="text-white">Mounting:</strong> A portable TV stand or mount makes setup easy. Some people use hitch-mounted TV stands that attach to their truck or SUV.</li>' +
            '<li><strong class="text-white">Sunlight:</strong> TVs are hard to see in direct sun. Position your setup in shade if possible. Anti-glare screen protectors help. QLED or mini-LED TVs are brighter and better for outdoor use.</li>' +
            '<li><strong class="text-white">Streaming:</strong> You need internet to stream games. Options: hotspot from your phone (best), portable Wi-Fi device, or satellite dish (rare at tailgates due to setup time).</li>' +
            '</ul></div>' +
            '<div>' +
            '<h3 class="font-bold text-xl mb-4 text-purple-400">Audio Setup Options</h3>' +
            '<ul class="space-y-3 text-sm text-gray-300">' +
            '<li><strong class="text-white">Portable Bluetooth speaker:</strong> Simplest option. A large party speaker (JBL PartyBox, Sony SRS-XP) uses 20-50W and sounds great for most groups.</li>' +
            '<li><strong class="text-white">Soundbar:</strong> Good if you want better TV audio. Uses 30-100W. Simple setup, just one cable to the TV.</li>' +
            '<li><strong class="text-white">Full stereo system:</strong> For serious audio, a receiver + bookshelf speakers or PA system uses 100-300W. Sounds amazing but is more to haul and set up.</li>' +
            '<li><strong class="text-white">Pro tip:</strong> Always test your speaker volume before the tailgate. Stadium lots can be loud — what sounds loud in your living room might be too quiet at the game.</li>' +
            '<li><strong class="text-white">Battery-powered speakers:</strong> Some party speakers have built-in batteries that last 8-20 hours. This saves your power station for the TV and other devices.</li>' +
            '</ul></div></div>' +
            p("Typical power draw for a complete A/V setup: 55\" TV (80W) + large Bluetooth speaker (50W) + streaming stick (5W) = ~135W total. On a 1,000Wh power station, that is about 7+ hours of runtime. Plenty for a full pregame + postgame.") +
            alert("info", "tv", "Pro TV tip", "Most TVs have a 'Power Saving' or 'Eco' mode that reduces brightness and power use. Turn this down a bit and you can extend TV runtime by 20-30%. You probably do not need full brightness anyway if it is not in direct sun.")
        },
        {
            "id": "setup-tips",
            "title": "Tailgate Setup Tips &amp; Tricks",
            "content": p("A great tailgate power setup is about more than just the power station. Here are pro tips from seasoned tailgaters:") +
            step_grid([
                {"title": "Charge Everything Before You Leave", "desc": "This sounds obvious but people forget. Charge your power station fully the night before. Charge your phones and Bluetooth speaker too. The power station is for extending the party, not for starting from zero. If you have a car charger, top up the station on the drive to the stadium."},
                {"title": "Test Your Setup at Home First", "desc": "Do a full test run in your driveway or backyard. Set up the TV, speaker, and everything else. Run it for a few hours. See if anything does not work, what the actual power draw is, and how long the battery lasts. You do not want to troubleshoot in the stadium parking lot before kickoff."},
                {"title": "Use Short, Thick Cables", "desc": "Long extension cables waste power through voltage drop. Keep cables as short as possible. Use 14-gauge or thicker extension cords for high-power devices. Do not daisy-chain power strips — plug directly into the station or use a single high-quality surge protector."},
                {"title": "Centralize Your Power Station", "desc": "Put the power station in a central location where everyone can reach it. On a table, under the canopy, or on the tailgate of your truck. Make sure it is visible so people know they can charge their phones. But keep it off the ground and protected from rain/spills."},
                {"title": "Label Cables and Devices", "desc": "When you have 10+ cables running everywhere, it gets confusing. Label what each cable powers. Use colored tape to distinguish TV, speaker, fridge, etc. This makes troubleshooting and teardown much faster."},
                {"title": "Have a Rain Plan", "desc": "Most power stations are not waterproof. If there is a chance of rain, bring a clear plastic bin to cover the station (leave ventilation gaps — do not seal it airtight). Or position it under the canopy where it stays dry. Never use a power station in heavy rain or standing water."},
            ], "purple") +
            p("One underrated tip: bring a power strip with multiple USB ports. Instead of everyone crowding the power station's USB ports, plug one multi-port USB charger into an AC outlet and put it on the table. This frees up the station's ports for high-power devices and makes phone charging more convenient for everyone.") +
            alert("warning", "umbrella", "Weather safety note", "Never use a portable power station in heavy rain or when it is submerged in water. Most are splash-resistant at best. If lightning is in the area, unplug everything and get inside your vehicle. Power stations attract electricity just like any other metal object.")
        },
        {
            "id": "solar-all-day",
            "title": "Solar for All-Day Tailgates",
            "content": p("If your tailgate starts early and goes late (or goes all weekend), pairing your power station with portable solar panels means you never run out of power. Here is what you need:") +
            specs_table(
                ["Solar Setup", "Typical Production", "What It Powers"],
                [
                    ["<strong>100W panel</strong>", "300–500 Wh/day", "Keeps up with phones, speaker, small TV"],
                    ["<strong>200W panel</strong>", "600–1,000 Wh/day", "TV + speaker + phones + partial fridge"],
                    ["<strong>400W panel(s)</strong>", "1,200–2,000 Wh/day", "Full setup indefinitely (sunny day)"],
                    ["<strong>600W+ panels</strong>", "1,800–3,000 Wh/day", "Big party setup, multiple fridges"],
                ]
            ) +
            p("The best part about solar for tailgating: you set up the panels first thing in the morning, and while you are hanging out, eating, and playing games, the sun is charging your battery. By game time, your station is full or close to it. Then during the game, you are running purely from battery (or solar + battery if you have enough panels).") +
            step_grid([
                {"title": "Portable vs. Fixed Panels", "desc": "Portable folding solar panels are the most popular for tailgating — they fold up like a suitcase, are easy to transport, and you can angle them toward the sun. Rigid panels are more efficient and durable but bulkier. For most tailgaters, 100W or 200W portable folding panels are the sweet spot."},
                {"title": "Panel Placement Tips", "desc": "Set up your panels where they get the most direct sun. Angle them toward the sun (not flat on the ground). Keep them away from shadows from trees, vehicles, or buildings. Even partial shading can cut output dramatically. If you have multiple panels, they can be in different positions as long as they connect to the same station."},
                {"title": "MPPT vs PWM", "desc": "All modern power stations use MPPT (Maximum Power Point Tracking) charge controllers, which are 20-30% more efficient than the old PWM technology. This matters for tailgating because solar conditions are variable — clouds, shadows from passing cars, changing sun angle. MPPT squeezes more power out of whatever sunlight is available."},
            ], "yellow") +
            alert("info", "sun", "Solar math example", "A 200W solar panel in full sun produces about 150W (real-world). Over 5 hours of good sun, that is 750Wh added back to your battery. If you are using 150W (TV + speaker), you are essentially breaking even — your battery stays at the same level all day. With 400W of solar, you are charging faster than you are using — battery actually goes up during the day.")
        },
        {
            "id": "common-mistakes-tailgate",
            "title": "Common Tailgating Power Mistakes",
            "content": p("After talking to many regular tailgaters, these are the most common mistakes people make with their first power station setup:") +
            '<div class="space-y-4">' +
            step_grid([
                {"title": "Buying Too Small", "desc": "The #1 mistake. 'I just need to charge phones and run a speaker' quickly becomes 'let's bring the TV and the fridge and the blender.' People underestimate how much they will want to plug in. Buy bigger than you think you need — you will use it. A 1,000Wh station is the minimum we recommend for any serious tailgate."},
                {"title": "Not Testing Before the Game", "desc": "You would not believe how many people buy a power station, throw it in their truck, and try to set it up for the first time at the stadium. Then they cannot figure out why the TV will not turn on, or the speaker is not connecting, or the solar panels are not charging. Always do a full test run at home first."},
                {"title": "Forgetting Cables and Adapters", "desc": "You have your power station, your TV, your speaker — and no HDMI cable. Or you forgot the power cable for the TV. Or you need a longer extension cord. Make a checklist. Pack everything the night before. Spare cables are cheap — bring extras."},
                {"title": "Running Everything at Once", "desc": "It is tempting to turn on the TV, the speaker, the lights, the fridge, and the crockpot all at once. But that might overload your inverter or drain the battery fast. Prioritize. Do you really need the lights on during the day? Can you run the grill before the TV goes on? Stagger high-power usage."},
                {"title": "No Backup Plan", "desc": "What if the power station dies? What if it rains? What if the stadium has weird rules? Always have a Plan B. A backup portable charger for phones. A generator for all-day events. Knowing where the nearest electrical outlet is. Hope for the best, plan for the worst."},
                {"title": "Ignoring Security", "desc": "Power stations are expensive and easy to steal. Never leave your setup unattended, especially in a stadium parking lot. If you need to go inside the game, either bring the station with you or have someone stay back to watch the gear. Cable locks can deter casual theft but will not stop a determined thief."},
            ], "red") + "</div>"
        },
    ],
    "faqs": [
        {"q": "What size portable power station do I need for tailgating?", "a": "For small groups (2-4 people) with just a speaker and phone chargers: 500-1,000Wh. For medium groups (4-10 people) with a TV, speaker, and fridge: 1,000-2,000Wh. For big parties, all-day events, or multiple high-power devices: 2,000Wh+. As a rule of thumb, size bigger than you think — people always want to charge their phones and plug in extra devices. The most popular size is 1,000-2,000Wh."},
        {"q": "Can a portable power station run a TV for tailgating?", "a": "Absolutely. A typical 55\" LED TV uses 60-100W, and a 65\" uses 80-150W. A 1,000Wh power station can run a 55\" TV for 8-12 hours — more than enough for pregame, the game, and postgame. Pair it with a speaker and you have a complete viewing setup. Just make sure you have a way to stream the game (hotspot, portable Wi-Fi, etc.)."},
        {"q": "How long will a power station last at a tailgate?", "a": "It depends on what you are powering. A 1,000Wh station powering just speakers and phone chargers might last 12-20+ hours. Add a 55\" TV and it drops to 6-10 hours. Add a portable fridge and it might be 3-5 hours. The fridge is usually the biggest drain. Use a cooler with ice instead if you want to maximize runtime. With solar panels, you can extend this indefinitely on sunny days."},
        {"q": "Are portable power stations allowed in stadium parking lots?", "a": "Most stadiums allow portable power stations in tailgate lots — they are much safer and quieter than generators. However, rules vary by stadium and event. Some ban generators but explicitly allow battery power stations. A few ban all external power sources. Always check the stadium's tailgating rules before you go. If in doubt, call the stadium guest services."},
        {"q": "Can I bring a power station inside the stadium?", "a": "Almost never. Most stadiums ban portable power stations and large battery packs from inside the stadium — they are considered potential hazards. The standard rule is: power stations stay in the parking lot for tailgating, bring only small portable chargers (under 20,000mAh) inside. Always check the specific stadium's bag policy before you go."},
        {"q": "What is better for tailgating: generator or power station?", "a": "For most tailgates, a power station is better — it is silent, produces no fumes, requires no fuel, and you can have conversations without shouting over generator noise. The only advantage of a generator is unlimited runtime (as long as you have fuel) and higher power output for very large setups. Many serious tailgaters use both: power station for the main party, generator as backup or for high-power devices like electric grills."},
        {"q": "Can I charge the power station while driving to the game?", "a": "Yes! Most portable power stations come with a car charging cable or offer one as an accessory. Charging from your car's 12V outlet while driving is a great way to top up the battery on the way to the stadium. Charge rate is usually 80-150W from a car, so you can add a few hundred watt-hours during a 1-2 hour drive. It is basically free power that you do not have to think about."},
        {"q": "How do I watch TV at a tailgate?", "a": "You need three things: a TV (50-65\" LED recommended), a power source (your portable power station), and a way to get the game signal. For streaming, most people use their phone's hotspot to connect a streaming stick (Roku, Fire TV, Chromecast) or smart TV. You need good cell service at the stadium for this to work. Some people use satellite dishes, but setup is more complex. Over-the-air antenna works if the stadium is close enough to broadcast towers."},
        {"q": "Can a portable power station run a mini fridge?", "a": "Yes, most portable power stations can run a 12V portable fridge or cooler. A typical 40L portable fridge draws 40-80W while running, but cycles on and off like a regular fridge — average draw is 20-40W. A 1,000Wh station can run a portable fridge for 20-40 hours (1-2 days). For tailgating, this means your drinks stay cold all day without using ice. 12V fridges are more efficient than running a mini-fridge on AC."},
        {"q": "Are power stations safe to use around food and drinks?", "a": "Yes, perfectly safe. Unlike generators, which produce deadly carbon monoxide fumes, portable power stations produce no exhaust. They are completely safe to use in enclosed spaces, near food, and around people. The only safety concerns are: don't get them wet, don't block the ventilation vents, and don't overload them. Follow the manufacturer's instructions and you have nothing to worry about."},
    ],
    "related": [
        {"href": "best-portable-power-station-under-500.html", "badge": "BUDGET", "badge_class": "bg-green-500/20 text-green-400", "border_class": "border-green-500/30", "badge2": "Under $500", "title": "Best Under $500", "desc": "Top budget portable power stations under $500 — what you get, limitations, best value brands, and used options."},
        {"href": "can-i-use-extension-cord-with-power-station.html", "badge": "EXTENSION&nbsp;CORDS", "badge_class": "bg-blue-500/20 text-blue-400", "border_class": "border-blue-500/30", "badge2": "Safety Guide", "title": "Extension Cord Guide", "desc": "Can you use an extension cord? Safety, gauge vs length, voltage drop, recommended sizes by wattage."},
        {"href": "how-to-charge-power-station-without-electricity.html", "badge": "OFF-GRID", "badge_class": "bg-yellow-500/20 text-yellow-400", "border_class": "border-yellow-500/30", "badge2": "Charging", "title": "Charging Without Electricity", "desc": "Solar, car, generator, wind, hand crank — all the ways to charge a power station when you are off-grid."},
        {"href": "best-portable-power-station-for-rv.html", "badge": "RV&nbsp;POWER", "badge_class": "bg-purple-500/20 text-purple-400", "border_class": "border-purple-500/30", "badge2": "Boondocking", "title": "Best for RV", "desc": "Best power stations for RV and boondocking — sizing, solar, TT-30 explained, top picks by RV size."},
        {"href": "jackery-explorer-2000-plus.html", "badge": "SPEC&nbsp;SHEET", "badge_class": "bg-yellow-500/20 text-yellow-400", "border_class": "border-yellow-500/30", "badge2": "Jackery", "title": "Jackery Explorer 2000 Plus", "desc": "Full specs for the Jackery Explorer 2000 Plus — 2,042Wh LFP, 2,200W output, expandable to 8kWh."},
        {"href": "outdoor-power.html", "badge": "ALL&nbsp;MODELS", "badge_class": "bg-electric-500/20 text-electric-400", "border_class": "border-electric-500/30", "badge2": "Category", "title": "Outdoor Power Hub", "desc": "Browse all portable power station guides, comparisons, specs, and troubleshooting resources in one place."},
    ],
}

PAGES = [page5]

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
