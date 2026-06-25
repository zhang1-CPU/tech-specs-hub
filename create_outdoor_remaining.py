#!/usr/bin/env python3
"""Generate remaining 2 Outdoor Power pages: under $500 and UPS mode."""

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

# =================== PAGE 9: BEST UNDER $500 ===================

page9 = {
    "filename": "best-portable-power-station-under-500.html",
    "title": "Best Portable Power Station Under $500 (2026 Budget Guide)",
    "headline": "Best Portable Power Station Under $500 (2026 Budget Guide)",
    "meta_desc": "Best portable power station under $500 in 2026. Top budget picks from Jackery, Bluetti, EcoFlow, Anker, and more. What you get for $500, limitations, best value brands, and buying advice.",
    "category": "Outdoor Power",
    "category_link": "outdoor-power.html",
    "breadcrumb_title": "Best Under $500",
    "hero_blur": "bg-green-500/5",
    "hero_badges": '''<div class="px-3 py-1.5 bg-green-500/20 text-green-400 font-mono font-bold text-sm rounded-md border border-green-500/30">BUDGET&nbsp;PICKS</div>
        <span class="badge badge-info"><i data-lucide="dollar-sign" style="width:0.75rem;height:0.75rem"></i>Under $500</span>
        <span class="badge badge-info"><i data-lucide="award" style="width:0.75rem;height:0.75rem"></i>Top Picks 2026</span>''',
    "h1": 'Best Portable Power Station Under $500 &mdash; <span class="gradient-text">2026 Budget Guide</span>',
    "hero_desc": "You can get a surprisingly capable portable power station for under $500. Budget stations in this price range typically offer 300-600Wh of capacity, 300-800W of AC output, multiple ports, solar charging support, and even features like UPS mode or pass-through charging. They are perfect for camping, tailgating, emergency backup, and powering electronics on the go. In this guide, we cover the top picks, what to expect, what compromises exist, and how to choose the best value.",
    "hero_stats": f'''<div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="battery-medium" style="width:0.9rem;height:0.9rem"></i>Capacity</div>
          <div class="font-mono font-bold text-xl text-green-400">200-600Wh</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="zap" style="width:0.9rem;height:0.9rem"></i>AC Output</div>
          <div class="font-bold text-xl text-yellow-400">300-800W</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="sun" style="width:0.9rem;height:0.9rem"></i>Solar Input</div>
          <div class="font-mono font-bold text-xl text-blue-400">60-200W</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="dollar-sign" style="width:0.9rem;height:0.9rem"></i>Price Range</div>
          <div class="font-bold text-xl text-purple-400">$199-$499</div>
        </div>''',
    "qa_gradient": "from-green-950/20 to-navy-900 border-green-500/20",
    "qa_icon_color": "#4ade80",
    "qa_title": "Best Budget Power Station Overall",
    "qa_text": '<strong class="text-white">The best portable power station under $500 for most people is the Jackery Explorer 300 Plus or the Bluetti EB55.</strong> The Jackery Explorer 300 Plus (around $299) offers 288Wh capacity, 300W AC output, fast charging, and excellent port selection in a lightweight package. The Bluetti EB55 (around $399) steps up to 537Wh capacity and 700W output with LiFePO4 chemistry for longer cycle life. Both are reliable, well-built, and backed by established brands with good customer support. For $500 or less, you can get a station that powers phones, laptops, cameras, small appliances, and lights for weekend trips or emergency backup.',
    "qa_extra": f'''<div class="grid md:grid-cols-3 gap-3 mt-4">
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-green-400 font-semibold mb-1 text-sm">Best Overall</div>
          <div class="font-bold text-white">Jackery Explorer 300+</div>
          <div class="text-xs text-gray-400 mt-1">~$299 · 288Wh · 300W</div>
        </div>
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-blue-400 font-semibold mb-1 text-sm">Best Value</div>
          <div class="font-bold text-white">Bluetti EB55</div>
          <div class="text-xs text-gray-400 mt-1">~$399 · 537Wh · 700W</div>
        </div>
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-yellow-400 font-semibold mb-1 text-sm">Best Compact</div>
          <div class="font-bold text-white">Anker 521 PowerHouse</div>
          <div class="text-xs text-gray-400 mt-1">~$249 · 256Wh · 200W</div>
        </div>
      </div>''',
    "sections": [
        {
            "id": "top-picks",
            "title": "Top Picks: Best Budget Power Stations",
            "content": p("Here are our top picks for the best portable power stations under $500 in 2026, organized by use case. All of these offer good build quality, reliable performance, and decent value for the price.") +
            specs_table(
                ["Model", "Capacity", "AC Output", "Weight", "Price", "Best For"],
                [
                    ["<strong>Jackery Explorer 300 Plus</strong>", "288Wh", "300W", "3.5 kg", "~$299", "Best overall compact pick"],
                    ["<strong>Bluetti EB55</strong>", "537Wh", "700W", "6.5 kg", "~$399", "Best value, LiFePO4"],
                    ["<strong>EcoFlow River 2</strong>", "256Wh", "300W", "3.5 kg", "~$239", "Fastest charging"],
                    ["<strong>Anker 521 PowerHouse</strong>", "256Wh", "200W", "2.9 kg", "~$249", "Most compact, premium build"],
                    ["<strong>Jackery Explorer 500</strong>", "518Wh", "500W", "6.4 kg", "~$499", "Best mid-size from Jackery"],
                    ["<strong>OUPES 600W</strong>", "595Wh", "600W", "5.2 kg", "~$399", "Best budget LiFePO4"],
                    ["<strong>FlashFish 300W</strong>", "280Wh", "300W", "3.3 kg", "~$179", "Cheapest decent option"],
                ]
            ) +
            p("Prices and specs are approximate as of mid-2026 and may vary by retailer, sales, and promotions. Always check current prices before buying, as there are frequent sales that can bring premium models into the under-$500 range.")
        },
        {
            "id": "what-you-get",
            "title": "What You Get for Under $500",
            "content": p("Under $500, you can get a perfectly functional portable power station for many use cases. Here is what to expect in this price range:") +
            '<div class="grid md:grid-cols-2 gap-6 mb-6">' +
            '<div>' +
            '<h3 class="font-bold text-xl mb-4 text-green-400">What You Will Get</h3>' +
            '<ul class="space-y-3 text-sm text-gray-300">' +
            '<li>• <strong class="text-white">200-600Wh capacity</strong> — enough for phones, laptops, camera gear, small appliances</li>' +
            '<li>• <strong class="text-white">200-800W AC output</strong> — powers most electronics and many small appliances</li>' +
            '<li>• <strong class="text-white">Multiple ports</strong> — USB-A, USB-C, DC, car port, 1-2 AC outlets</li>' +
            '<li>• <strong class="text-white">Solar charging support</strong> — most support 60-200W solar input</li>' +
            '<li>• <strong class="text-white">LCD display</strong> — shows battery level, input/output wattage</li>' +
            '<li>• <strong class="text-white">LED flashlight</strong> — useful for camping and emergencies</li>' +
            '<li>• <strong class="text-white">Lightweight &amp; portable</strong> — 3-7 kg, easy to carry</li>' +
            '<li>• <strong class="text-white">1-2 year warranty</strong> — decent coverage from reputable brands</li>' +
            '</ul></div>' +
            '<div>' +
            '<h3 class="font-bold text-xl mb-4 text-red-400">What You Will NOT Get</h3>' +
            '<ul class="space-y-3 text-sm text-gray-300">' +
            '<li>• <strong class="text-white">High capacity (1,000Wh+)</strong> — that is the $700-1,500+ range</li>' +
            '<li>• <strong class="text-white">High output (1,500W+)</strong> — no running AC units or large appliances</li>' +
            '<li>• <strong class="text-white">Expandable battery</strong> — most budget models are fixed capacity</li>' +
            '<li>• <strong class="text-white">LiFePO4 (always)</strong> — some budget models still use NMC lithium-ion</li>' +
            '<li>• <strong class="text-white">UPS mode (all models)</strong> — some have it, some do not</li>' +
            '<li>• <strong class="text-white">Fast charging (all models)</strong> — budget stations may charge slowly</li>' +
            '<li>• <strong class="text-white">Premium build quality</strong> — mostly plastic, may feel less substantial</li>' +
            '<li>• <strong class="text-white">5-year warranty</strong> — budget warranties are usually 1-2 years</li>' +
            '</ul></div></div>' +
            p("The key is to manage expectations. A $300 power station will not power a microwave or air conditioner, but it will easily charge your phone 20+ times, run your laptop for 10+ hours, power LED lights all night, and run a small fridge or CPAP machine for 8+ hours. For camping, tailgating, or emergency backup during short outages, that is plenty.")
        },
        {
            "id": "limitations",
            "title": "Limitations of Budget Power Stations",
            "content": p("Budget power stations have real limitations you should be aware of before buying. Understanding these helps you choose the right model and avoid disappointment.") +
            grid_cards([
                {"title": "Lower Capacity", "color": "text-yellow-400", "desc": "Budget stations top out around 500-600Wh. That is enough for weekend camping but not for multi-day off-grid use without solar. If you need to power high-draw devices or need multi-day runtime, you will either need solar charging or a larger (more expensive) station."},
                {"title": "Lower AC Output", "color": "text-orange-400", "desc": "Most budget stations offer 200-500W of AC output, with a few reaching 700-800W. That means no microwaves, electric kettles, space heaters, or air conditioners. Check the wattage of devices you want to power before buying. Surge watts matter too — devices with motors need extra power to start."},
                {"title": "Slower Charging", "color": "text-blue-400", "desc": "Budget power stations often charge slower than premium models. AC charging might take 5-8 hours instead of 1-2 hours. Solar charging efficiency can be lower too. If fast charging is important to you, look specifically for models that advertise fast recharge times."},
                {"title": "Shorter Cycle Life", "color": "text-purple-400", "desc": "Many budget power stations use NMC lithium-ion batteries rated for 500-1,000 cycles (to 80% capacity). More expensive models with LiFePO4 batteries offer 2,000-6,000+ cycles. If you will use your station daily or weekly, LiFePO4 is worth paying extra for. For occasional use, NMC is fine."},
                {"title": "Fewer Features", "color": "text-green-400", "desc": "Budget models may skip features like UPS mode, app control, Bluetooth, expandable capacity, wireless charging, multiple AC outlets, or advanced MPPT solar charging. Decide which features are must-haves vs nice-to-haves before shopping."},
                {"title": "Build Quality & Reliability", "color": "text-red-400", "desc": "Cheaper brands may cut corners on components, build quality, and quality control. Stick with reputable brands even in the budget range — Jackery, Bluetti, EcoFlow, Anker, and Goal Zero all have budget offerings that are more reliable than no-name brands from Amazon."},
            ], 2) +
            alert("info", "lightbulb", "When to splurge vs save", "If you will use your power station more than 5-10 times per year, or for critical applications (medical devices, home backup), consider spending more for LiFePO4 chemistry, higher output, and better warranty. If you only need it for occasional camping trips or rare emergencies, a budget model will serve you fine and save you money.")
        },
        {
            "id": "best-value-brands",
            "title": "Best Value Brands in 2026",
            "content": p("Not all budget power stations are created equal. Some brands offer much better value, build quality, and support than others. Here are the best value brands to consider:") +
            specs_table(
                ["Brand", "Price Range", "Strengths", "Weaknesses", "Best Budget Model"],
                [
                    ["<strong>Jackery</strong>", "$200-$1,500+", "Widely available, great support, reliable, lightweight", "Premium pricing, NMC batteries, slower charging", "Explorer 300 Plus (~$299)"],
                    ["<strong>Bluetti</strong>", "$250-$3,000+", "Great value, LiFePO4 on many models, lots of features", "Heavier than some, mixed app experience", "EB55 (~$399)"],
                    ["<strong>EcoFlow</strong>", "$200-$3,000+", "Fast charging, good app, innovative features", "Some quality control issues reported", "River 2 (~$239)"],
                    ["<strong>Anker</strong>", "$200-$1,500", "Premium build, great customer support, compact", "Higher price for capacity, lower output", "521 PowerHouse (~$249)"],
                    ["<strong>OUPES</strong>", "$200-$1,000+", "Excellent value, LiFePO4, good solar input", "Less well-known, limited retail presence", "600W (~$399)"],
                    ["<strong>Goal Zero</strong>", "$250-$2,000+", "Premium brand, great quality, solar ecosystem", "Expensive for what you get", "Yeti 200X (~$299)"],
                ]
            ) +
            p("Our advice: start with Bluetti, OUPES, or EcoFlow if you want the most features and capacity for your money. Jackery and Anker cost a bit more but offer better brand recognition, support, and reliability. No-name brands from Amazon can be tempting due to low prices, but they often have shorter lifespans, worse performance, and little to no customer support.")
        },
        {
            "id": "used-refurbished",
            "title": "Used &amp; Refurbished Options",
            "content": p("You can often get a significantly better power station for your $500 budget by buying used, open-box, or refurbished. Here is what to know:") +
            '<div class="grid md:grid-cols-2 gap-6 mb-6">' +
            '<div>' +
            '<h3 class="font-bold text-xl mb-4 text-green-400">Where to Look</h3>' +
            '<ul class="space-y-3 text-sm text-gray-300">' +
            '<li>• <strong class="text-white">Brand refurbished</strong> — Jackery, Bluetti, EcoFlow all sell certified refurbished units on their websites, usually with 90-day to 1-year warranty</li>' +
            '<li>• <strong class="text-white">Amazon Renewed</strong> — Amazon\'s certified refurbished program with 90-day return policy</li>' +
            '<li>• <strong class="text-white">eBay</strong> — great for used units, check seller ratings and return policy</li>' +
            '<li>• <strong class="text-white">Facebook Marketplace / Craigslist</strong> — local deals, but inspect in person</li>' +
            '<li>• <strong class="text-white">REI Garage / Outlet</strong> — open-box and clearance items from a reputable retailer</li>' +
            '<li>• <strong class="text-white">Brand sales</strong> — holiday sales (Black Friday, Prime Day) can bring new units way down in price</li>' +
            '</ul></div>' +
            '<div>' +
            '<h3 class="font-bold text-xl mb-4 text-red-400">What to Check</h3>' +
            '<ul class="space-y-3 text-sm text-gray-300">' +
            '<li>• <strong class="text-white">Cycle count / battery health</strong> — ask how many times it has been charged. Lithium batteries degrade over time</li>' +
            '<li>• <strong class="text-white">Physical damage</strong> — look for dents, cracks, water damage, or signs of dropping</li>' +
            '<li>• <strong class="text-white">Functionality</strong> — test all ports and outlets if possible. Bring a device to plug in</li>' +
            '<li>• <strong class="text-white">Warranty</strong> — is the original warranty transferable? Does the seller offer any guarantee?</li>' +
            '<li>• <strong class="text-white">Age</strong> — lithium batteries degrade even when unused. Try to find units under 2-3 years old</li>' +
            '<li>• <strong class="text-white">Return policy</strong> — can you return it if it is not as described?</li>' +
            '</ul></div></div>' +
            alert("warning", "alert-triangle", "Battery health is everything", "The battery is the most expensive part of a power station. A used unit with a degraded battery might seem like a bargain but could have 50% or less of its original capacity. Always test capacity if you can (charge it fully, then discharge at a known wattage and time it). For used LiFePO4 units, degradation is slower — they are a safer bet used than NMC.") +
            p("As a rough guide, expect to pay 50-70% of retail for a good condition used unit, and 70-85% for certified refurbished. If a deal seems too good to be true (e.g., a $1,000 unit for $200), it probably is — the battery is likely shot, or it is stolen/counterfeit.")
        },
        {
            "id": "what-to-compromise",
            "title": "What to Compromise On",
            "content": p("On a $500 budget, you cannot have everything. Here is what matters most and what you can safely compromise on:") +
            specs_table(
                ["Factor", "Importance", "Notes", "Can You Compromise?"],
                [
                    ["<strong>Capacity (Wh)</strong>", "Very High", "Determines how long devices run. Get as much as you can afford.", "Only if you have solar or rarely use it"],
                    ["<strong>AC Output (W)</strong>", "Very High", "Determines what you can power. Check device wattages.", "Not if you need specific high-wattage devices"],
                    ["<strong>Battery Chemistry (LFP vs NMC)</strong>", "Medium-High", "LiFePO4 = 3-6x longer cycle life, safer.", "Yes if you use it <10x/year, NMC is fine"],
                    ["<strong>Number of Ports</strong>", "Medium", "More ports = more convenience, but you can use power strips.", "Easy to compromise, use power strips"],
                    ["<strong>Charging Speed</strong>", "Medium", "Fast charging is nice but not essential for everyone.", "Yes if you charge overnight or use solar"],
                    ["<strong>Weight & Size</strong>", "Medium", "Lighter is better for carrying, heavier usually = more capacity.", "Depends on your use case"],
                    ["<strong>Brand Reputation</strong>", "Medium-High", "Better brands = better support, reliability, warranty.", "Somewhat, but avoid no-name brands"],
                    ["<strong>Warranty Length</strong>", "Medium", "Longer warranty = more peace of mind.", "Can compromise for good value on budget"],
                    ["<strong>UPS Mode</strong>", "Low-Medium", "Only matters if you need uninterruptible power.", "Most people can skip this"],
                    ["<strong>App / Smart Features</strong>", "Low", "Convenient but not essential. You can use the display.", "Easy to compromise on budget"],
                ]
            ) +
            step_grid([
                {"title": "How to Prioritize", "desc": "1) First make sure the AC output is high enough for your devices. 2) Then get as much capacity as you can afford. 3) Choose LiFePO4 if you can find it in your budget and you will use it regularly. 4) Pick a reputable brand. 5) Everything else is secondary. These five factors will determine 90% of your satisfaction with the purchase."},
                {"title": "Budget Tiers", "desc": "Under $200: Very basic, low capacity (150-300Wh), 200W output, no-name brands risky. $200-$300: Good entry level, reputable brands available, 250-300Wh, 300W output. $300-$400: Sweet spot for value, 500-600Wh possible, 500-700W output, LiFePO4 available. $400-$500: Near-premium features, 500Wh+, 500-1000W output, better build quality. We recommend the $300-$400 range for most people — the best balance of price and capability."},
            ], "green")
        },
        {
            "id": "buying-tips",
            "title": "Buying Tips &amp; How to Get the Best Deal",
            "content": p("Follow these tips to get the most value for your $500 budget:") +
            step_grid([
                {"title": "Wait for Sales", "desc": "Power stations go on sale frequently. The best deals are usually during: Black Friday / Cyber Monday (November), Amazon Prime Day (July), holiday sales (December), back-to-school (August), and brand anniversary sales. You can often save 20-40% during these events. If you can wait for a sale, you will get much more for your $500."},
                {"title": "Check Multiple Retailers", "desc": "Prices vary between Amazon, brand websites, Home Depot, Lowes, REI, and Best Buy. Use price comparison tools like CamelCamelCamel for Amazon to see historical prices. Sometimes brand websites offer bundle deals (power station + solar panel) that save you money compared to buying separately."},
                {"title": "Consider Bundles", "desc": "Many brands sell power station + solar panel bundles at a discount. If you think you might want solar later, buying the bundle can save $50-150 compared to buying separately. Just make sure the solar panel size and connector type are compatible with the station."},
                {"title": "Look for Open-Box / Refurbished", "desc": "Open-box and certified refurbished units from reputable sellers can be 20-30% cheaper than new, often with the same warranty. Check the brand\'s official refurbished store first, then Amazon Renewed, then REI Garage for the best options with return policies."},
                {"title": "Read Recent Reviews", "desc": "Read reviews from the last 2-3 months — older reviews may not reflect current quality. Look for patterns: if multiple recent reviews mention DOA units or battery issues, consider a different model. YouTube reviews from independent creators can give you real-world performance data."},
                {"title": "Check Return Policy", "desc": "Make sure you can return the unit if it arrives damaged or does not meet your needs. Amazon has the best return policy (30 days, usually free returns). Brand websites vary — check the fine print. For used units, returns are usually not available, so inspect carefully."},
            ], "yellow") +
            alert("info", "shield", "Warranty matters more on budget units", "With budget electronics, the warranty is even more important because the risk of early failure is higher. Look for at least a 1-year warranty. Brands like Jackery, Anker, and Bluetti have better warranty support than no-name brands. Register your product after purchase to activate the warranty — many brands require this."),
        },
    ],
    "faqs": [
        {"q": "What is the best portable power station under $500?", "a": "The best portable power station under $500 depends on your needs, but our top picks are: Jackery Explorer 300 Plus (best overall compact, ~$299), Bluetti EB55 (best value with LiFePO4, ~$399), and EcoFlow River 2 (fastest charging, ~$239). For maximum capacity under $500, look for 500-600Wh models from Bluetti or OUPES, which often go on sale for under $400."},
        {"q": "How long will a 500Wh power station last?", "a": "It depends on what you are powering. A 500Wh power station can charge a phone (~20Wh) about 20-25 times, run a laptop (~50W) for 8-10 hours, power a 32-inch TV (~80W) for 5-6 hours, run a small car fridge (~40W average) for 10-12 hours, or power a CPAP machine (~40W) for 10-12 hours. High-wattage devices like microwaves or space heaters will drain it in 30 minutes or less."},
        {"q": "Is LiFePO4 worth it on a budget?", "a": "LiFePO4 batteries are worth paying extra for if you will use your power station regularly (weekly or daily) and want it to last 5+ years. LiFePO4 batteries typically last 3-6 times longer than NMC lithium-ion (2,000-6,000 cycles vs 500-1,000). If you will only use your station a few times per year for camping or emergencies, NMC is fine and saves you money. Many budget models under $500 now use LiFePO4, so it is worth looking for."},
        {"q": "Can a $300 power station run a fridge?", "a": "A small 12V car fridge or portable cooler (30-50W average) can run for 8-15 hours on a 300Wh budget power station. A full-size household refrigerator (100-200W average, with compressor surges up to 500-1,000W) would need a larger station with higher output — budget stations usually do not have enough surge wattage for the compressor startup. Check the surge/peak wattage rating, not just the continuous output."},
        {"q": "Are cheap no-name power stations from Amazon safe?", "a": "Generally, no — we recommend sticking with reputable brands even on a budget. No-name brands often cut corners on battery quality, BMS (battery management system), and safety features. There have been reports of swelling batteries, overheating, and even fires from cheap power stations. The $50-100 you save is not worth the safety risk. Jackery, Bluetti, EcoFlow, and Anker all have budget models that are much safer."},
        {"q": "What size solar panel do I need for a budget power station?", "a": "Most budget power stations support 60-200W of solar input. Match your panel to the station's maximum input rating — using a larger panel than supported will not charge faster. For a 300Wh station, a 60-100W panel is ideal and will fully recharge in 4-8 hours of good sun. For a 500Wh station, 100-150W is better. Portable folding solar panels in the 100W range cost $100-200."},
        {"q": "Can I use a budget power station for home backup?", "a": "A budget power station (under $500) is good for limited emergency backup — charging phones, powering lights, running a radio or small TV, and maybe a small fridge or CPAP machine during a short outage. It will not power your whole house, run large appliances, or last multiple days without solar. For whole-home backup, you need a much larger system (2,000Wh+) which costs $1,500-5,000+."},
        {"q": "How long do budget power stations last?", "a": "Budget power stations with NMC lithium-ion batteries typically last 500-1,000 charge cycles before dropping to 80% capacity. With occasional use (once or twice a month), that translates to 5-10 years of usable life. Budget LiFePO4 models last 2,000-4,000 cycles — 3-4x longer. Proper storage (around 50% charge, cool temperatures) extends lifespan significantly."},
        {"q": "What size power station do I need for camping?", "a": "For weekend camping with basic electronics (phones, camera, LED lights, speaker), a 200-300Wh station is plenty. If you also want to run a small fridge, laptop, or other mid-power devices, go for 500Wh+. If you want solar charging to extend your trip, pair a 300-500Wh station with a 60-100W solar panel. Most people are happy with 300-500Wh for 2-3 day camping trips."},
        {"q": "Is it better to buy used or new budget power station?", "a": "For $500, you can get a very capable new power station (500Wh+, 500W+), so we usually recommend buying new for the warranty and peace of mind. However, buying used or refurbished can get you a $800-$1,000 model for $500 if you are lucky — just make sure to check battery health and condition carefully. Certified refurbished from the brand is the safest way to go used, as it usually includes a warranty."},
    ],
    "related": std_related(),
}

# =================== PAGE 10: UPS MODE ===================

page10 = {
    "filename": "portable-power-station-ups-mode-explained.html",
    "title": "Portable Power Station UPS Mode Explained: How It Works (2026)",
    "headline": "Portable Power Station UPS Mode Explained: How It Works (2026)",
    "meta_desc": "What is UPS mode on a portable power station? Complete guide covering how it works, switchover speed, which brands support it, UPS vs pass-through charging, use cases, limitations, and testing tips.",
    "category": "Outdoor Power",
    "category_link": "outdoor-power.html",
    "breadcrumb_title": "UPS Mode Guide",
    "hero_blur": "bg-purple-500/5",
    "hero_badges": '''<div class="px-3 py-1.5 bg-purple-500/20 text-purple-400 font-mono font-bold text-sm rounded-md border border-purple-500/30">UPS&nbsp;MODE</div>
        <span class="badge badge-info"><i data-lucide="battery-charging" style="width:0.75rem;height:0.75rem"></i>Uninterruptible</span>
        <span class="badge badge-info"><i data-lucide="plug" style="width:0.75rem;height:0.75rem"></i>Backup Power</span>''',
    "h1": 'Portable Power Station UPS Mode Explained &mdash; <span class="gradient-text">How It Works (2026)</span>',
    "hero_desc": "UPS mode (Uninterruptible Power Supply) is a feature that lets a portable power station automatically switch to battery power when the grid goes down — fast enough that your devices do not turn off. This is incredibly useful for computers, networking equipment, security cameras, medical devices, and anything else that needs uninterrupted power. But not all power stations have UPS mode, and the speed of the switchover varies a lot between brands. In this guide, we cover everything you need to know about UPS mode.",
    "hero_stats": f'''<div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="zap" style="width:0.9rem;height:0.9rem"></i>Switchover</div>
          <div class="font-mono font-bold text-xl text-green-400">&lt;10-50ms</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="battery" style="width:0.9rem;height:0.9rem"></i>Backup Time</div>
          <div class="font-bold text-xl text-yellow-400">Hours to days</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="plug" style="width:0.9rem;height:0.9rem"></i>Charging + Output</div>
          <div class="font-mono font-bold text-xl text-blue-400">Simultaneous</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="shield" style="width:0.9rem;height:0.9rem"></i>Protection</div>
          <div class="font-bold text-xl text-purple-400">Surge + Brownout</div>
        </div>''',
    "qa_gradient": "from-purple-950/20 to-navy-900 border-purple-500/20",
    "qa_icon_color": "#c084fc",
    "qa_title": "What Is UPS Mode?",
    "qa_text": '<strong class="text-white">UPS mode (Uninterruptible Power Supply) is a feature that allows a portable power station to instantly switch from grid/AC charging to battery power when the electricity goes out — so quickly that your connected devices do not shut down or restart.</strong> Without UPS mode, when the power goes out you would need to manually turn on the power station\'s AC output, and there would be a gap of several seconds or minutes where your devices lose power. With UPS mode, the switchover happens automatically in 10-50 milliseconds (depending on the model), which is fast enough that computers, routers, and most electronics do not even notice the interruption. This makes portable power stations with UPS mode useful as affordable battery backups for home office equipment, networking gear, and even some medical devices.',
    "qa_extra": f'''<div class="grid md:grid-cols-2 gap-3 mt-4">
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-green-400 font-semibold mb-1 flex items-center gap-2"><i data-lucide="check" style="width:1rem;height:1rem"></i>Supported by</div>
          <p class="text-sm text-gray-300">EcoFlow, Bluetti, Anker, Goal Zero, some Jackery models</p>
        </div>
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-red-400 font-semibold mb-1 flex items-center gap-2"><i data-lucide="x" style="width:1rem;height:1rem"></i>Not supported by</div>
          <p class="text-sm text-gray-300">Many budget models, some older Jackery units, no-name brands</p>
        </div>
      </div>''',
    "sections": [
        {
            "id": "how-ups-works",
            "title": "How UPS Mode Works",
            "content": p("UPS mode on a portable power station works by keeping the AC inverter on and active while the station is plugged in and charging. The power station passes grid power through to your devices while simultaneously charging its own battery. When the power cuts out, the station immediately switches over to battery power without dropping the output.") +
            step_grid([
                {"title": "Step 1: Normal Operation (Grid Power)", "desc": "When everything is working normally, your power station is plugged into the wall. The AC output is on. Grid power flows through the station to your connected devices. At the same time, the battery is charging (if it is not full). The power station is essentially acting as a pass-through + charger."},
                {"title": "Step 2: Power Failure Detected", "desc": "The power station continuously monitors the input AC voltage and frequency. When the grid voltage drops below a certain threshold (or disappears entirely), the BMS and inverter control system detects the failure within milliseconds."},
                {"title": "Step 3: Switch to Battery Power", "desc": "The system immediately switches from pass-through mode to battery inverter mode. Instead of passing grid power through, the inverter starts drawing DC power from the battery and converting it to AC for your devices. This happens in 10-50 milliseconds on most good UPS-equipped stations."},
                {"title": "Step 4: Running on Battery", "desc": "Your devices continue running on battery power without interruption. The power station provides power for as long as the battery lasts — anywhere from a few minutes to many hours depending on the load and battery size."},
                {"title": "Step 5: Power Restoration", "desc": "When grid power comes back, the station detects the restored voltage and switches back to pass-through mode. It resumes charging the battery and powering devices from the grid. Again, this transition is usually seamless."},
            ], "purple") +
            specs_table(
                ["Component", "Function"],
                [
                    ["<strong>AC Input / Charger</strong>", "Receives grid power, charges the battery"],
                    ["<strong>Battery Pack</strong>", "Stores energy for backup use"],
                    ["<strong>BMS (Battery Management System)</strong>", "Monitors battery health, safety, and state of charge"],
                    ["<strong>Inverter</strong>", "Converts DC battery power to AC output power"],
                    ["<strong>UPS Control Circuit</strong>", "Monitors grid power, manages switchover"],
                    ["<strong>AC Output / Sockets</strong>", "Provides power to your devices"],
                    ["<strong>Display / Controls</strong>", "Shows status, lets you configure UPS settings"],
                ]
            ) +
            p("The key difference between a regular power station and one with UPS mode is that the inverter stays on all the time while plugged in. On power stations without UPS mode, you have to manually turn on the AC output, and it turns off when there is no input power — or it charges but does not provide output while charging.")
        },
        {
            "id": "switchover-speed",
            "title": "How Fast Is the Switchover?",
            "content": p("Switchover speed is the most important spec for UPS mode. It determines whether your devices will stay on during the transition. Here is how different speeds compare:") +
            specs_table(
                ["Switchover Time", "Rating", "What Survives", "What Does Not"],
                [
                    ["<strong>0ms (online UPS)</strong>", "Best", "Everything — all devices, including the most sensitive", "Nothing — completely seamless"],
                    ["<strong>2-10ms</strong>", "Excellent", "Computers, routers, monitors, most electronics", "Almost nothing drops out"],
                    ["<strong>10-20ms</strong>", "Very Good", "Most electronics, desktop PCs, networking gear", "Very sensitive equipment rarely"],
                    ["<strong>20-50ms</strong>", "Good", "Most consumer electronics, laptops with battery", "Some very sensitive devices, old PCs"],
                    ["<strong>50-100ms</strong>", "Marginal", "Laptops (with internal battery), lights, simple devices", "Desktop PCs, some networking gear may restart"],
                    ["<strong>100ms+</strong>", "Poor / Not UPS", "Only devices with internal batteries", "Most electronics will reset or power off"],
                ]
            ) +
            p("Most portable power stations with UPS mode claim switchover times under 20-50ms. In real-world testing, many are in the 10-30ms range, which is fast enough for most consumer electronics. However, claimed switchover times are not always accurate — we recommend testing with your actual devices before relying on it for critical applications.") +
            alert("info", "cpu", "Why switchover speed matters for computers", "A desktop PC without a UPS will instantly power off when electricity cuts out, potentially losing unsaved work and damaging the filesystem. Laptops are more forgiving because they have internal batteries — even if the power station takes a second to switch over, the laptop\'s battery bridges the gap. For desktop computers, aim for 20ms or faster switchover to be safe."),
        },
        {
            "id": "brands-with-ups",
            "title": "Which Brands &amp; Models Support UPS Mode?",
            "content": p("Not all portable power stations have UPS mode. Here is a breakdown of which brands offer it and on which models:") +
            specs_table(
                ["Brand", "UPS Support", "Switchover Speed", "Notable Models"],
                [
                    ["<strong>EcoFlow</strong>", "Most models", "~10-20ms (X-Boost/UPS)", "River 2, River 2 Pro, Delta 2, Delta Pro"],
                    ["<strong>Bluetti</strong>", "Most models", "~10-20ms (UPS mode)", "EB3A, EB55, AC70, AC180, AC200Max"],
                    ["<strong>Jackery</strong>", "Some newer models", "~20-50ms", "Explorer 1000 Plus, Explorer 2000 Plus (check specs)"],
                    ["<strong>Anker</strong>", "Many models", "~20ms", "521, 535, 555, 757 PowerHouse"],
                    ["<strong>Goal Zero</strong>", "Yeti X/Pro series", "~20ms", "Yeti 500X, Yeti 1000X, Yeti 1500X"],
                    ["<strong>OUPES</strong>", "Some models", "~10-30ms", "600W, 1200W, 2400W"],
                    ["<strong>No-name / generic</strong>", "Rarely", "Often poor/slow", "Hit or miss — many do not have true UPS"],
                ]
            ) +
            alert("warning", "alert-triangle", "Always verify UPS support before buying", "Brands sometimes add or remove UPS features from newer models without much fanfare. Do not assume a model has UPS just because an older version from the same brand did. Check the product page, manual, or contact support to confirm. Look for terms like 'UPS mode', 'uninterruptible power supply', 'backup power', or 'EPS' (Emergency Power Supply).") +
            p("If UPS functionality is important to you, make sure to: 1) Check the product specifications for 'UPS' or 'uninterruptible' explicitly, 2) Look for switchover time specs (under 20ms is excellent), 3) Read user reviews and YouTube tests that specifically test the UPS feature, 4) Buy from a brand with good return policy in case it does not work as expected.")
        },
        {
            "id": "ups-vs-passthrough",
            "title": "UPS Mode vs Pass-Through Charging",
            "content": p("UPS mode and pass-through charging are related but different features. They are often confused. Here is how they compare:") +
            '<div class="grid md:grid-cols-2 gap-6 mb-6">' +
            '<div class="bg-navy-900/80 border border-electric-500/30 rounded-xl p-6">' +
            '<h3 class="font-bold text-xl mb-4 text-electric-400">Pass-Through Charging</h3>' +
            '<ul class="space-y-3 text-sm text-gray-300">' +
            '<li>• <strong class="text-white">What it does:</strong> Lets you charge the battery and use AC output at the same time</li>' +
            '<li>• <strong class="text-white">Automatic switch on power loss:</strong> No — you have to manually turn on output or there may be a delay</li>' +
            '<li>• <strong class="text-white">Seamless transition:</strong> Not guaranteed — might be seconds of dead air</li>' +
            '<li>• <strong class="text-white">Inverter always on:</strong> Not necessarily — may turn on/off</li>' +
            '<li>• <strong class="text-white">Good for:</strong> Charging and using simultaneously without needing uninterruptible power</li>' +
            '<li>• <strong class="text-white">Common on:</strong> Many power stations, even budget ones</li>' +
            '<li>• <strong class="text-white">Does not equal UPS:</strong> Having pass-through does not mean you have UPS mode</li>' +
            '</ul></div>' +
            '<div class="bg-navy-900/80 border border-purple-500/30 rounded-xl p-6">' +
            '<h3 class="font-bold text-xl mb-4 text-purple-400">UPS Mode</h3>' +
            '<ul class="space-y-3 text-sm text-gray-300">' +
            '<li>• <strong class="text-white">What it does:</strong> Automatically switches to battery power when grid fails — fast enough for no interruption</li>' +
            '<li>• <strong class="text-white">Includes pass-through:</strong> Yes — always, because it needs to be plugged in and providing power</li>' +
            '<li>• <strong class="text-white">Seamless transition:</strong> Yes — 10-50ms switchover</li>' +
            '<li>• <strong class="text-white">Inverter always on:</strong> Yes — stays active to enable fast switching</li>' +
            '<li>• <strong class="text-white">Good for:</strong> Uninterruptible backup for computers, routers, medical devices</li>' +
            '<li>• <strong class="text-white">Common on:</strong> Mid-range to premium power stations</li>' +
            '<li>• <strong class="text-white">Always includes pass-through:</strong> Yes — UPS is a superset of pass-through</li>' +
            '</ul></div></div>' +
            p("The key takeaway: UPS mode always includes pass-through charging, but pass-through charging does NOT equal UPS mode. Many budget power stations have pass-through charging (you can charge and discharge at the same time) but do not have true UPS mode because the switchover is not fast enough or not automatic. If you need uninterruptible power, make sure the product specifically advertises UPS functionality.") +
            alert("info", "lightbulb", "How to tell the difference", "If the product page only mentions 'pass-through charging' or 'charge while using', it probably does not have true UPS mode. Look for explicit mentions of 'UPS', 'uninterruptible power supply', 'backup power with zero downtime', or 'EPS (Emergency Power Supply) mode'. If in doubt, email the manufacturer and ask for the switchover time in milliseconds.")
        },
        {
            "id": "use-cases",
            "title": "Use Cases for UPS Mode",
            "content": p("UPS mode is useful in many scenarios. Here are the most common use cases:") +
            grid_cards([
                {"title": "Home Office / Desktop PC", "color": "text-blue-400", "desc": "A power outage in the middle of work can cost you hours of progress or even corrupt files. UPS mode gives you time to save your work and shut down properly, or keep working if the outage is short. A 500Wh station can keep a desktop PC + monitor running for 1-3 hours, depending on usage."},
                {"title": "Internet & Networking", "color": "text-green-400", "desc": "Keeping your router and modem online during a power outage means you still have internet access for work, emergency communication, and information. A small 200-300Wh power station can run a router + modem for 8-20+ hours — long enough for most outages."},
                {"title": "Security Cameras & NVR", "color": "text-yellow-400", "desc": "Power outages are when security cameras are most needed. UPS mode keeps your security system running without interruption. Most NVRs and cameras use very little power (10-50W), so even a small power station can keep them going for many hours or days."},
                {"title": "Medical Devices (CPAP, etc.)", "color": "text-red-400", "desc": "For people who rely on CPAP machines, oxygen concentrators, or other medical devices, power outages can be life-threatening. UPS mode ensures no interruption in power. Note: for critical medical use, always have a backup plan and consult your doctor — do not rely solely on a consumer power station."},
                {"title": "Gaming Consoles & PC", "color": "text-purple-400", "desc": "Losing power mid-game can mean losing progress, getting banned from online matches, or even damaging game saves. UPS mode gives you time to save and exit properly, or keep gaming through short outages. Great for dedicated gamers and streamers."},
                {"title": "Refrigerator / Freezer", "color": "text-electric-400", "desc": "During extended outages, a power station with UPS mode can keep your fridge or freezer running to prevent food from spoiling. Note: fridges draw a lot of power (100-200W average, 500-1000W surge), so you need a larger station (1,000Wh+) for this to be practical for more than a few hours."},
            ], 2) +
            p("The beauty of using a portable power station as a UPS is that it serves double duty: it is a UPS for your home office/equipment when you are at home, and a portable power source for camping, tailgating, and travel when you need it. Traditional UPS units (like APC or CyberPower) are cheaper per watt and have faster switchover, but they only work as UPS — they are not portable and cannot be used off-grid."),
        },
        {
            "id": "limitations",
            "title": "Limitations &amp; Things to Know",
            "content": p("UPS mode on portable power stations is great, but it has limitations you should be aware of:") +
            step_grid([
                {"title": "Not True 'Online' UPS", "desc": "Traditional enterprise UPS units are 'online' double-conversion — they always run from the battery/inverter, and the grid only charges the battery. This means zero switchover time. Portable power stations are typically 'line-interactive' or 'standby' UPS — they pass through grid power normally and switch to battery on failure. Switchover is fast (10-50ms) but not instantaneous. For 99% of consumer use, this is fine."},
                {"title": "Idle Power Draw", "desc": "Keeping the inverter on 24/7 for UPS mode uses some power even when nothing is plugged in. This idle draw is usually 5-20W, which adds up over time. If the power station is plugged in, this is not an issue — the grid supplies the idle power. But if you are running off battery, the idle draw slowly drains the battery even with no load."},
                {"title": "Limited Backup Time vs Traditional UPS", "desc": "Traditional UPS units for computers usually have 5-15 minutes of runtime — just enough to save work and shut down. Portable power stations have much more capacity (hours of runtime), which is great but also makes them bigger and heavier. If you only need 5 minutes of backup, a small $50 UPS might be more efficient. If you want hours of backup plus portability, a power station is better."},
                {"title": "Warranty & Lifespan Considerations", "desc": "Using your power station as a 24/7 UPS means the battery is always cycling (slightly) and the inverter is always on. This may reduce the lifespan compared to occasional use. However, LiFePO4 batteries handle partial cycling very well — it should not be a major concern. Check the manufacturer's policy on UPS use, as some warranties may not cover continuous UPS use."},
                {"title": "Output Limitations Apply", "desc": "The AC output wattage limit still applies in UPS mode. If your devices draw more than the station's rated output, it will shut down — even if the battery is full. Make sure your total load is well under the rated output (aim for 60-80% max for reliability). Surge/peak wattage also matters for devices with motors."},
                {"title": "Grid Voltage Sensitivity", "desc": "Some power stations are too sensitive or not sensitive enough to grid fluctuations. If the station switches to battery too easily (during minor voltage sags), it might discharge when you do not want it to. If it does not switch fast enough or at too low a voltage, it defeats the purpose. Ideally, you can adjust the UPS sensitivity threshold in settings."},
            ], "orange") +
            alert("critical", "flame", "Do not use for life-support devices without backup", "Never rely solely on a consumer portable power station for life-support or critical medical equipment. Always have a backup plan — a second power station, a generator, or a proper medical-grade UPS. Consumer power stations are not certified as medical devices and could fail. Consult your doctor or equipment provider for medical-grade backup solutions.")
        },
        {
            "id": "testing-ups",
            "title": "How to Test UPS Function",
            "content": p("If you have a power station with UPS mode, you should test it to make sure it works as expected before you actually need it. Here is how:") +
            step_grid([
                {"title": "Step-by-Step UPS Test", "desc": "1) Fully charge your power station. 2) Plug the station into wall power. 3) Plug a device into the station's AC output — something with a display and that you do not mind restarting, like a lamp or old laptop. 4) Make sure the station's AC output is turned on (some require you to enable UPS mode in settings). 5) While the device is running, simply unplug the power station from the wall. 6) Observe whether the device stays on or turns off. 7) Time how long the switchover takes if you have the right equipment (oscilloscope, or a computer with a clock that shows milliseconds). 8) Plug the station back in and verify it switches back to charging mode properly."},
                {"title": "What to Test Specifically", "desc": "Test with your actual devices — a desktop PC if that is what you will use it for, your router, etc. Different devices have different sensitivity. Test with your maximum expected load — does UPS mode work when you are pulling 80% of rated output? Test brownouts too (if you have a variac) — does the station switch over when voltage drops but does not go completely out? Test the restoration — when power comes back, is the transition smooth? Test battery level — does UPS still work when the battery is at 50%? 20%?"},
            ], "yellow") +
            alert("info", "wrench", "Tip: Use a lamp for quick testing", "A simple incandescent or LED lamp is a great quick test. Unplug the power station from the wall while the lamp is on. If the lamp flickers off then on, the switchover is too slow (or the station does not have true UPS). If the lamp stays on without any visible flicker, the switchover is fast — at least under 50ms or so. For a more precise test, use a desktop PC and see if it stays running."),
        },
    ],
    "faqs": [
        {"q": "What is UPS mode on a portable power station?", "a": "UPS mode (Uninterruptible Power Supply) is a feature that lets a portable power station automatically switch from grid/charging power to battery power when the electricity goes out — fast enough that your connected devices do not turn off or restart. The switchover typically happens in 10-50 milliseconds, which is seamless for most consumer electronics like computers, routers, and monitors."},
        {"q": "Do all portable power stations have UPS mode?", "a": "No — not all power stations have UPS mode. Many budget models and some older models do not support it. Having 'pass-through charging' (ability to charge and discharge at the same time) is not the same as UPS mode. For true UPS functionality, look for explicit mentions of 'UPS mode', 'uninterruptible power supply', or 'EPS' in the product specifications. Brands like EcoFlow, Bluetti, Anker, and Goal Zero offer UPS on many of their models."},
        {"q": "How fast is the switchover in UPS mode?", "a": "Switchover times vary by model. Good power stations with UPS mode typically switch in 10-20 milliseconds, which is fast enough that you will not notice and most electronics stay on. Some budget models with UPS claims may take 50-100ms or more, which can cause desktop PCs to shut down. For comparison, a traditional UPS usually switches in 2-10ms, and online double-conversion UPS has zero switchover time."},
        {"q": "Can I use a portable power station as a UPS for my computer?", "a": "Yes — a portable power station with UPS mode works well as a battery backup for a desktop computer. It gives you time to save your work and shut down properly during a power outage, or keep working through short outages. A 500Wh power station can typically run a desktop PC + monitor for 1-3 hours. Make sure the switchover time is under 20-30ms for reliable use with desktop PCs."},
        {"q": "What is the difference between UPS mode and pass-through charging?", "a": "Pass-through charging means you can charge the battery and use the AC output at the same time. UPS mode goes further: it includes pass-through charging, plus automatic and near-instantaneous switching to battery power when the grid fails. UPS mode always includes pass-through, but pass-through does not guarantee UPS functionality. Many budget stations have pass-through but not true UPS mode."},
        {"q": "Does UPS mode use more battery? (idle draw)", "a": "Yes, keeping the inverter on for UPS mode uses a small amount of power even when no devices are plugged in — typically 5-20W of idle draw. When the station is plugged in, this power comes from the grid so the battery does not drain. When running on battery, the idle draw slowly consumes capacity. For most UPS use cases (station plugged in at all times), this is not a concern."},
        {"q": "Can a portable power station replace a traditional UPS?", "a": "For most home and small office use, yes — a portable power station with UPS mode can replace a traditional UPS. The advantages are: much more capacity (hours vs minutes of runtime), portability (you can take it camping or to other locations), and multiple uses. The disadvantages are: higher cost per watt, slightly slower switchover (still fast enough for most uses), and larger/heavier form factor. For server rooms or critical equipment, a traditional enterprise UPS is still better."},
        {"q": "What size power station do I need for UPS?", "a": "It depends on what you want to power and for how long. For just a router + modem (20-30W), a small 200-300Wh station gives 6-15 hours of backup. For a desktop PC + monitor (150-250W), you want at least 500Wh for 2-4 hours of runtime. For a fridge, you need 1,000Wh+ for 5-10 hours. Calculate your total wattage and multiply by desired runtime hours, then add 20-30% for inverter efficiency and safety margin."},
        {"q": "Do Jackery power stations have UPS mode?", "a": "Most older Jackery models do not have true UPS mode — they have pass-through charging, but the switchover is not fast enough to be considered UPS. However, some newer Jackery models (like the Explorer 1000 Plus and 2000 Plus series) do support UPS functionality. Always check the specific model's product page or manual to confirm. Jackery has been adding UPS to more of their newer lineup."},
        {"q": "Is it safe to leave a power station plugged in all the time (UPS mode)?", "a": "Yes, it is generally safe to leave a good quality power station plugged in 24/7 for UPS use. The BMS (Battery Management System) manages charging, and once the battery is full, it stops charging and runs in pass-through mode. LiFePO4 batteries handle float/standby very well. However, there is always a small risk with any lithium battery — do not leave it unattended for weeks on end without checking, and make sure it has proper ventilation."},
    ],
    "related": std_related(),
}

PAGES = [page9, page10]

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
