#!/usr/bin/env python3
"""Generate batch 2: remaining 7 Outdoor Power pages."""

import os
import json
import html
import re
from typing import List, Dict, Any

OUTPUT_DIR = "/workspace/pages/specs"
BASE_URL = "https://powerspecshub.com/pages/specs"
SITE_NAME = "TechSpecsHub"
UPDATED_DATE = "2026-06-25"
UPDATED_DATE_TEXT = "June 25, 2026"

# Helper functions (same as before)
def p(text: str) -> str:
    return f'<p class="text-gray-300 leading-relaxed mb-4">{text}</p>'

def ul(items: List[str], icon: str = "check", color: str = "green") -> str:
    lis = "".join(f'<li class="flex items-start gap-2"><i data-lucide="{icon}" style="width:1rem;height:1rem;color:#{color_map[color]};flex-shrink:0;margin-top:0.1rem"></i><span>{item}</span></li>' for item in items)
    return f'<ul class="space-y-3 text-sm text-gray-300">{lis}</ul>'

color_map = {"green": "4ade80", "red": "f87171", "yellow": "facc15", "blue": "60a5fa", "purple": "a78bfa", "electric": "22d3ee"}

def alert(alert_type: str, icon: str, title: str, text: str) -> str:
    return f'''<div class="alert alert-{alert_type}">
  <i data-lucide="{icon}" style="width:1rem;height:1rem;flex-shrink:0;margin-top:0.1rem"></i>
  <p class="text-sm"><strong>{title}:</strong> {text}</p>
</div>'''

def specs_table(headers: List[str], rows: List[List[str]]) -> str:
    thead = "".join(f"<th>{h}</th>" for h in headers)
    tbody = ""
    for row in rows:
        tbody += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
    return f'''<div class="overflow-x-auto mb-6">
  <table class="specs-table w-full text-sm">
    <thead><tr>{thead}</tr></thead>
    <tbody>{tbody}</tbody>
  </table>
</div>'''

def step_grid(steps: List[Dict[str, str]], color: str = "green") -> str:
    html_str = '<div class="space-y-4">'
    for i, step in enumerate(steps, 1):
        html_str += f'''        <div class="flex items-start gap-3">
          <div class="w-10 h-10 bg-{color}-500/20 rounded-full flex items-center justify-center flex-shrink-0">
            <span class="font-mono font-bold text-{color}-400">{i}</span>
          </div>
          <div>
            <h4 class="font-semibold text-white">{step["title"]}</h4>
            <p class="text-sm text-gray-400">{step["desc"]}</p>
          </div>
        </div>'''
    html_str += "</div>"
    return html_str

def grid_cards(cards: List[Dict[str, str]], cols: int = 2) -> str:
    html_str = f'<div class="grid md:grid-cols-{cols} gap-4">'
    for card in cards:
        html_str += f'''      <div class="bg-navy-900/80 border border-white/10 rounded-xl p-5">
        <h4 class="font-semibold {card.get("color", "text-electric-400")} mb-2">{card["title"]}</h4>
        <p class="text-sm text-gray-300">{card["desc"]}</p>
      </div>'''
    html_str += "</div>"
    return html_str

def section(sid: str, title: str, content: str) -> str:
    return f'''  <section id="{sid}" class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <h2 class="font-bold text-3xl mb-5">{title}</h2>
    <div class="glass-card p-6 md:p-8">
{content}
    </div>
  </section>'''

# Import the build functions from the main structure
def build_header(title: str, meta_desc: str, canonical: str, article_json: dict, faq_json: dict, breadcrumb_json: dict) -> str:
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

BODY_HEADER = open("/workspace/pages/specs/portable-power-station-eco-mode.html").read().split('''<body class="bg-navy-950 text-white min-h-screen font-display">''')[1].split('''  <!-- BREADCRUMB -->''')[0]

FOOTER = '''  <!-- FOOTER -->
  <footer class="border-t border-white/5 mt-12">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <hr class="border-white/10 my-8">
      <div class="flex flex-col sm:flex-row justify-between items-center gap-4 text-sm text-gray-500">
        <div>&copy; <span id="current-year">2026</span> TechSpecsHub. All rights reserved.</div>
        <div class="flex items-center gap-1">
          <i data-lucide="shield-check" style="width:0.875rem;height:0.875rem;color:#6b7280"></i>
          <span>Data updated: June 2026</span>
        </div>
      </div>
    </div>
  </footer>

  <script src="../../assets/js/main.js" defer></script>

</body>
</html>'''

def faq_details(faqs: List[Dict[str, str]]) -> str:
    html_str = '''  <section id="faq" class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="text-center mb-10">
      <h2 class="font-bold text-3xl md:text-4xl mb-4">Frequently Asked Questions</h2>
      <p class="text-gray-400">Common questions answered by our experts.</p>
    </div>
    <div class="space-y-3">'''
    for q in faqs:
        html_str += f'''      <details class="glass-card p-5 group">
        <summary class="cursor-pointer font-semibold flex items-center justify-between gap-4">
          <span>{q["q"]}</span>
          <i data-lucide="chevron-down" style="width:1rem;height:1rem" class="text-gray-500 group-open:rotate-180 transition-transform flex-shrink-0"></i>
        </summary>
        <p class="mt-3 text-gray-400 text-sm leading-relaxed">{q["a"]}</p>
      </details>'''
    html_str += '''    </div>
  </section>'''
    return html_str

def related_guides(cards: List[Dict[str, str]]) -> str:
    html_str = '''  <section id="related" class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h2 class="font-bold text-3xl mb-5">Related Guides &amp; Resources</h2>
    <div class="grid md:grid-cols-3 gap-4">'''
    for card in cards:
        html_str += f'''      <a href="{card["href"]}" class="glass-card p-6 block hover:border-electric-400/50 transition-all group">
        <div class="flex items-start gap-3 mb-3">
          <div class="px-2.5 py-1 {card["badge_class"]} font-mono font-semibold text-sm rounded-md border {card["border_class"]}">{card["badge"]}</div>
          <span class="badge badge-info">{card["badge2"]}</span>
        </div>
        <h3 class="font-bold text-lg mb-2 group-hover:text-electric-400 transition-colors">{card["title"]}</h3>
        <p class="text-sm text-gray-400">{card["desc"]}</p>
      </a>'''
    html_str += '''    </div>
  </section>'''
    return html_str

def build_page(page_data: dict) -> str:
    canonical = f"{BASE_URL}/{page_data['filename']}"
    
    article_json = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": page_data["headline"],
        "description": page_data["meta_desc"],
        "url": canonical,
        "datePublished": UPDATED_DATE,
        "dateModified": UPDATED_DATE,
        "author": {"@type": "Organization", "name": SITE_NAME},
        "publisher": {"@type": "Organization", "name": SITE_NAME, "url": "https://powerspecshub.com/"},
        "image": {"@type": "ImageObject", "url": "https://powerspecshub.com/assets/images/og-default.png"}
    }
    
    faq_json = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}}
            for q in page_data["faqs"]
        ]
    }
    
    breadcrumb_json = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://powerspecshub.com/"},
            {"@type": "ListItem", "position": 2, "name": page_data["category"], "item": f"https://powerspecshub.com/pages/specs/{page_data['category_link']}"},
            {"@type": "ListItem", "position": 3, "name": page_data["breadcrumb_title"]}
        ]
    }
    
    head = build_header(page_data["title"], page_data["meta_desc"], canonical, article_json, faq_json, breadcrumb_json)
    
    # Breadcrumb
    breadcrumb_html = f'''  <!-- BREADCRUMB -->
  <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 pb-4">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="../../index.html">Home</a>
      <span class="breadcrumb-sep">/</span>
      <a href="{page_data["category_link"]}">{page_data["category"]}</a>
      <span class="breadcrumb-sep">/</span>
      <span class="breadcrumb-current">{page_data["breadcrumb_title"]}</span>
    </nav>
  </div>'''
    
    # Hero
    hero_html = f'''  <!-- HERO -->
  <section class="relative max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-4 pb-6">
    <div class="glass-card p-8 md:p-10 overflow-hidden relative">
      <div class="absolute top-0 right-0 w-[420px] h-[420px] {page_data["hero_blur"]} rounded-full blur-3xl pointer-events-none"></div>

      <div class="relative flex flex-wrap items-center gap-3 mb-5">
        {page_data["hero_badges"]}
      </div>

      <h1 class="font-bold text-4xl md:text-5xl mb-4 leading-tight">
        {page_data["h1"]}
      </h1>

      <p class="text-gray-400 text-lg leading-relaxed mb-6 max-w-3xl">
        {page_data["hero_desc"]}
      </p>

      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8">
        {page_data["hero_stats"]}
      </div>
    </div>
  </section>'''
    
    # Quick Answer
    quick_answer_html = f'''  <!-- QUICK ANSWER -->
  <section class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div class="glass-card p-6 md:p-8 bg-gradient-to-br {page_data["qa_gradient"]}">
      <h2 class="font-bold text-2xl mb-4 flex items-center gap-2"><i data-lucide="zap" style="width:1.25rem;height:1.25rem;color:{page_data["qa_icon_color"]}"></i>Quick Answer: {page_data["qa_title"]}</h2>
      <p class="text-gray-300 leading-relaxed mb-4">
        {page_data["qa_text"]}
      </p>
      {page_data["qa_extra"]}
    </div>
  </section>'''
    
    # TOC
    toc_items = "".join(
        f'<a href="#{s["id"]}" class="flex items-center gap-2 p-2 rounded-lg hover:bg-white/5 text-gray-300 hover:text-white transition-all"><span class="text-electric-400 font-mono">{i:02d}</span>{s["title"]}</a>'
        for i, s in enumerate(page_data["sections"], 1)
    )
    toc_html = f'''  <!-- TABLE OF CONTENTS -->
  <section class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div class="glass-card p-6 md:p-8">
      <h2 class="font-bold text-2xl mb-4 flex items-center gap-2"><i data-lucide="list" style="width:1.25rem;height:1.25rem;color:#22d3ee"></i>Table of Contents</h2>
      <div class="grid md:grid-cols-2 gap-2 text-sm">
        {toc_items}
        <a href="#faq" class="flex items-center gap-2 p-2 rounded-lg hover:bg-white/5 text-gray-300 hover:text-white transition-all"><span class="text-electric-400 font-mono">{len(page_data["sections"])+1:02d}</span>Frequently Asked Questions</a>
        <a href="#related" class="flex items-center gap-2 p-2 rounded-lg hover:bg-white/5 text-gray-300 hover:text-white transition-all"><span class="text-electric-400 font-mono">{len(page_data["sections"])+2:02d}</span>Related Guides</a>
      </div>
    </div>
  </section>'''
    
    # Content sections
    sections_html = "\n".join(section(s["id"], s["title"], s["content"]) for s in page_data["sections"])
    
    # FAQ
    faq_html = faq_details(page_data["faqs"])
    
    # Related
    related_html = related_guides(page_data["related"])
    
    return head + BODY_HEADER + breadcrumb_html + hero_html + quick_answer_html + toc_html + sections_html + faq_html + related_html + FOOTER


# ===================== PAGE 4: DISPOSAL =====================

page4 = {
    "filename": "how-to-dispose-of-portable-power-station.html",
    "title": "How to Dispose of a Portable Power Station (Battery Recycling 2026)",
    "headline": "How to Dispose of a Portable Power Station (Battery Recycling 2026)",
    "meta_desc": "How to properly dispose of a portable power station. Complete guide to battery recycling, hazardous waste rules, donation options, repair before replace, and state-by-state legal requirements.",
    "category": "Outdoor Power",
    "category_link": "outdoor-power.html",
    "breadcrumb_title": "Disposal & Recycling",
    "hero_blur": "bg-green-500/5",
    "hero_badges": '''<div class="px-3 py-1.5 bg-green-500/20 text-green-400 font-mono font-bold text-sm rounded-md border border-green-500/30">DISPOSAL</div>
        <span class="badge badge-info"><i data-lucide="recycle" style="width:0.75rem;height:0.75rem"></i>Recycling</span>
        <span class="badge badge-info"><i data-lucide="shield" style="width:0.75rem;height:0.75rem"></i>Safety</span>''',
    "h1": 'How to Dispose of a Portable Power Station &mdash; <span class="gradient-text">Battery Recycling Guide 2026</span>',
    "hero_desc": "When a portable power station reaches the end of its life, you cannot just throw it in the trash. Lithium batteries are classified as hazardous waste in most jurisdictions and require special handling. Improper disposal causes environmental harm, fires at waste facilities, and can result in significant fines. This guide covers the proper ways to dispose of or recycle your power station, donation options, repair vs. replacement, and the legal requirements in each state.",
    "hero_stats": '''<div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="recycle" style="width:0.9rem;height:0.9rem"></i>Recyclable</div>
          <div class="font-mono font-bold text-xl text-green-400">95%+ Metals</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="alert-triangle" style="width:0.9rem;height:0.9rem"></i>Hazardous?</div>
          <div class="font-bold text-xl text-yellow-400">Yes (Li-ion)</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="landmark" style="width:0.9rem;height:0.9rem"></i>Fines</div>
          <div class="font-mono font-bold text-xl text-red-400">$100&ndash;$50k</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="heart" style="width:0.9rem;height:0.9rem"></i>Donate?</div>
          <div class="font-bold text-xl text-blue-400">Often Yes</div>
        </div>''',
    "qa_gradient": "from-green-950/20 to-navy-900 border-green-500/20",
    "qa_icon_color": "#4ade80",
    "qa_title": "How to Dispose of a Portable Power Station",
    "qa_text": '<strong class="text-white">The best way to dispose of a portable power station is to take it to a certified lithium-ion battery recycling center, a household hazardous waste facility, or participate in a manufacturer take-back program.</strong> Never throw lithium batteries in the regular trash or recycling bin — they can cause fires in garbage trucks and at recycling facilities. Most cities have free or low-cost battery recycling through their hazardous waste departments. Many retailers like Home Depot, Lowe\'s, and Best Buy also accept rechargeable batteries for recycling.',
    "qa_extra": '''<div class="grid md:grid-cols-2 gap-3 mt-4">
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-green-400 font-semibold mb-1 flex items-center gap-2"><i data-lucide="check" style="width:1rem;height:1rem"></i>Best disposal methods</div>
          <p class="text-sm text-gray-300">Household hazardous waste, certified battery recycler, manufacturer take-back, retail drop-off</p>
        </div>
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-red-400 font-semibold mb-1 flex items-center gap-2"><i data-lucide="x" style="width:1rem;height:1rem"></i>Never do this</div>
          <p class="text-sm text-gray-300">Throw in trash, put in curbside recycling, burn, puncture, disassemble at home</p>
        </div>
      </div>''',
    "sections": [
        {
            "id": "proper-disposal-methods",
            "title": "Proper Disposal Methods",
            "content": p("There are several safe and legal ways to dispose of a portable power station. Here are the best options, ranked from most convenient to most specialized:") +
            step_grid([
                {"title": "Household Hazardous Waste (HHW) Facilities", "desc": "Most cities and counties operate household hazardous waste collection facilities or host periodic collection events. These accept lithium batteries for free or a small fee ($5-$20 per item). This is usually the easiest and cheapest option for most people. Search '[your county] household hazardous waste' to find locations near you."},
                {"title": "Retail Drop-Off Programs", "desc": "Many national retailers accept rechargeable batteries for recycling at no cost. Home Depot, Lowe's, Best Buy, Staples, and Batteries Plus Bulbs all have in-store recycling bins for rechargeable batteries. Some may not accept large power stations — call ahead to confirm. Smaller units can usually go in their standard battery bins."},
                {"title": "Manufacturer Take-Back Programs", "desc": "Some power station manufacturers offer take-back or recycling programs for their products. EcoFlow, Jackery, Bluetti, Goal Zero, and Anker all have some form of recycling program. Contact their customer support to inquire. In some cases, they may even cover shipping costs for returning old units."},
                {"title": "Certified Battery Recyclers", "desc": "For large or multiple units, a specialized lithium battery recycling company is the best option. Companies like Call2Recycle, Battery Solutions, and Redwood Materials process lithium batteries and recover valuable materials. They can handle everything from small power stations to large battery banks. Some charge a fee, others are free."},
                {"title": "Electronics Recycling Events", "desc": "Many communities host free electronics recycling events a few times per year. These usually accept lithium batteries along with other electronics. Check your local government website or search for 'electronics recycling near me' to find upcoming events. Be aware that some events only accept certain items."},
                {"title": "Scrap Metal Yards (Sometimes)", "desc": "Some scrap yards accept lithium batteries, but many do not. Call ahead to ask. If they do accept them, you may even get a small amount of money for the metal content. However, this is not the most environmentally friendly option since many scrap yards do not properly process the battery cells."},
            ], "green") +
            alert("info", "lightbulb", "Pro tip", "Call2Recycle (call2recycle.org) is a free national program that helps you find battery recycling locations near you. They have a location finder on their website and partner with thousands of retail locations across the US.")
        },
        {
            "id": "battery-types",
            "title": "Battery Types & Why They Matter for Disposal",
            "content": p("Portable power stations use different battery chemistries, and the disposal requirements can vary. Here are the most common types:") +
            specs_table(
                ["Battery Type", "Chemistry", "Hazard Level", "Recyclability"],
                [
                    ["<strong>LiFePO4 (LFP)</strong>", "Lithium Iron Phosphate", "Moderate", "High (iron, phosphate, lithium)"],
                    ["<strong>NMC</strong>", "Lithium Nickel Manganese Cobalt", "High (cobalt, nickel)", "Very high (valuable metals)"],
                    ["<strong>NCA</strong>", "Lithium Nickel Cobalt Aluminum", "High (cobalt, nickel)", "Very high"],
                    ["<strong>Lead-Acid (rare in portables)</strong>", "Lead Acid", "High (lead)", "Very high (lead is 99% recycled)"],
                ]
            ) +
            p("All lithium-ion batteries are considered hazardous waste under federal and most state regulations. This is because they contain toxic metals (cobalt, nickel, lithium) and can catch fire if damaged or improperly handled. LFP batteries are generally considered safer and less toxic than NMC/NCA, but they still require special disposal.") +
            p("The good news is that lithium batteries are highly recyclable. Modern recycling facilities can recover 95%+ of the valuable metals — lithium, cobalt, nickel, copper, aluminum — and reuse them in new batteries. Recycling keeps these finite resources in circulation and prevents them from leaching into landfills.") +
            alert("warning", "flame", "Fire risk", "The biggest danger from improper lithium battery disposal is fire. Damaged or punctured lithium batteries can experience thermal runaway — a self-sustaining chemical reaction that produces extreme heat and fire. This is why garbage trucks and recycling facilities catch fire so often from improperly discarded batteries. A single lithium battery in a trash compactor can ignite an entire truckload.")
        },
        {
            "id": "hazardous-waste",
            "title": "Hazardous Waste Concerns",
            "content": p("Lithium batteries pose several environmental and safety hazards when not disposed of properly:") +
            '<div class="grid md:grid-cols-2 gap-6">' +
            '<div>' +
            '<h3 class="font-bold text-xl mb-4 text-red-400 flex items-center gap-2"><i data-lucide="flame" style="width:1.25rem;height:1.25rem"></i>Fire &amp; Explosion Risk</h3>' +
            ul([
                "Batteries can be punctured during trash collection and transport",
                "Compaction in garbage trucks can cause internal short circuits",
                "Thermal runaway can ignite entire truckloads of garbage",
                "Fires at landfills and recycling facilities are costly and dangerous",
                "First responders are put at risk responding to these fires",
            ], "alert-triangle", "red") +
            '</div><div>' +
            '<h3 class="font-bold text-xl mb-4 text-yellow-400 flex items-center gap-2"><i data-lucide="droplets" style="width:1.25rem;height:1.25rem"></i>Environmental Contamination</h3>' +
            ul([
                "Toxic metals (cobalt, nickel, lead) can leach into soil and groundwater",
                "Lithium itself is toxic to aquatic life in high concentrations",
                "Electrolyte solutions are corrosive and flammable",
                "Landfill liners can eventually fail, releasing contaminants",
                "Improper disposal in developing countries causes severe health issues",
            ], "alert-triangle", "yellow") +
            "</div></div>" +
            p("Beyond the direct hazards, there is also the issue of resource waste. Lithium batteries contain valuable, finite resources that require significant energy and environmental impact to mine. Recycling these metals reduces the need for new mining and lowers the overall environmental footprint of battery technology.") +
            alert("critical", "alert-octagon", "Severe consequences", "In 2024, a waste management facility in Florida burned for 3 days because of a single lithium battery that caught fire in a garbage truck. The fire destroyed 200+ tons of recyclables and caused $2 million in damage. This is not an isolated incident — the EPA reports hundreds of lithium battery fires at waste facilities every year in the US.")
        },
        {
            "id": "donation-options",
            "title": "Donation Options (Before You Dispose)",
            "content": p("If your power station still works but you no longer need it, consider donating it instead of recycling. Many organizations would be thrilled to have a working portable power station. Here are some ideas:") +
            specs_table(
                ["Organization", "What They Accept", "How to Donate"],
                [
                    ["<strong>Local community centers</strong>", "Working power stations, any condition", "Drop off or call ahead"],
                    ["<strong>Emergency shelters</strong>", "Working units for backup power", "Contact local Red Cross or shelter"],
                    ["<strong>Schools / STEM programs</strong>", "Working or for parts", "Contact local schools or colleges"],
                    ["<strong>Habitat for Humanity ReStores</strong>", "Working condition", "Drop off at ReStore locations"],
                    ["<strong>Freecycle / Craigslist Free</strong>", "Anything (working or not)", "Post online, someone picks up"],
                    ["<strong>Local ham radio clubs</strong>", "Working units for emergency comms", "Find a club near you"],
                    ["<strong>Community gardens</strong>", "Working units for tools/lighting", "Contact local gardens"],
                    ["<strong>Theater / film groups</strong>", "Working units for location power", "Contact local production companies"],
                ]
            ) +
            p("Even if the battery is degraded (50-70% capacity), it can still be useful for applications where capacity is not critical — like powering LED lights, charging phones, or running small devices. A power station with half its original capacity is still better than no power station at all for many organizations.") +
            p("If the unit does not work at all, some hobbyists and tinkerers might want it for parts or to try repairing. Posting on local Facebook groups, Freecycle, or Craigslist in the free section usually results in someone coming to pick it up within a day or two.") +
            alert("info", "heart", "Good to know", "Some charities will even provide a tax donation receipt for working electronics. The value is usually based on the fair market value of the item. Check with the specific organization about their donation receipt policies.")
        },
        {
            "id": "repair-before-replace",
            "title": "Repair Before You Replace",
            "content": p("Before disposing of a power station, consider whether it can be repaired. Many power stations that seem dead have simple, fixable issues. Here is what to check:") +
            step_grid([
                {"title": "Check the Obvious Stuff First", "desc": "Is it actually turned on? Is the display just dim? Is the battery completely dead? Try charging it for 24+ hours with a known-good charger. Sometimes deeply discharged batteries need a long time to wake up. Try different cables and chargers. Check if a circuit breaker tripped (some models have a reset button)." },
                {"title": "Common Fixable Issues", "desc": "Many power station problems are not the battery itself: blown fuses, loose internal connections, faulty display, broken charging port, BMS software glitches, or inverter failures. If the battery still holds a charge but the output does not work, the battery pack is probably fine and only the inverter needs repair or replacement."},
                {"title": "Warranty Check", "desc": "If your unit is less than 2-5 years old, it might still be under warranty. Contact the manufacturer. Even if you are past the warranty period, some manufacturers offer flat-rate repair services that are cheaper than buying new. Always check before giving up on a unit."},
                {"title": "Third-Party Repair Shops", "desc": "There are increasing numbers of electronics repair shops that work on portable power stations. Search for 'battery repair near me' or 'portable power station repair.' Independent repair technicians can often fix issues for a fraction of the cost of replacement. Right-to-repair laws are making this easier every year."},
                {"title": "DIY Repair (If You Know What You Are Doing)", "desc": "If you have electronics experience, many issues are fixable at home. Blown fuses, loose wires, bad connectors, and some BMS issues are repairable. However, be extremely careful — lithium batteries can be dangerous if mishandled. Always work in a safe area with proper safety equipment."},
            ], "blue") +
            specs_table(
                ["Issue", "Repairable?", "Typical Repair Cost", "Worth Fixing?"],
                [
                    ["Blown fuse / tripped breaker", "Yes", "$0–$20", "Absolutely"],
                    ["Loose internal connection", "Yes", "$20–$100", "Yes"],
                    ["Faulty charging port", "Yes", "$30–$100", "Yes"],
                    ["Display not working", "Yes", "$50–$150", "Usually"],
                    ["Inverter failure", "Sometimes", "$100–$400", "Depends on unit value"],
                    ["Battery degradation (70%+)", "Yes (replace cells)", "$200–$1,000", "Depends on unit"],
                    ["Swollen / damaged battery", "No (dangerous)", "N/A", "No — recycle safely"],
                ]
            )
        },
        {
            "id": "state-laws",
            "title": "Legal Requirements by State",
            "content": p("Laws regarding lithium battery disposal vary by state and locality. Here is a summary of the general legal landscape in 2026:") +
            p('<strong class="text-white">Federal level:</strong> The EPA classifies lithium-ion batteries as hazardous waste under the Resource Conservation and Recovery Act (RCRA) when discarded. However, there is an exemption for household hazardous waste — individual households are not subject to the same strict rules as businesses. That said, it is still illegal in most places to put lithium batteries in the regular trash.') +
            '<div class="grid md:grid-cols-2 gap-4">' +
            grid_cards([
                {"title": "California", "color": "text-red-400", "desc": "Strictest regulations. Illegal to throw lithium batteries in trash. Mandatory recycling. Many cities require battery recycling at HHW facilities. Extended Producer Responsibility (EPR) laws make manufacturers responsible for end-of-life management. Fines can be substantial."},
                {"title": "New York", "color": "text-orange-400", "desc": "Lithium batteries cannot go in trash or curbside recycling. NYC has fines starting at $100 for improper disposal. NY has EPR laws for electronics that cover batteries. Many free HHW collection options available."},
                {"title": "Washington / Oregon", "color": "text-yellow-400", "desc": "Both states have strong recycling laws. EPR programs for electronics cover batteries. Most cities have curbside battery recycling programs or regular HHW collection events. Seattle has strict requirements."},
                {"title": "Texas / Florida", "color": "text-green-400", "desc": "Regulations vary by county. Some counties have strict rules, others are more relaxed. Check your local county waste management guidelines. Most large cities operate HHW facilities. State-level EPR laws are being considered."},
                {"title": "Midwest States", "color": "text-blue-400", "desc": "Regulations vary widely. Illinois, Michigan, and Minnesota have fairly comprehensive recycling programs. Rural areas may have fewer options. Check with your county or city waste management department."},
                {"title": "Rural / Less Populated States", "color": "text-purple-400", "desc": "Options may be limited. Look for periodic HHW collection events (often quarterly or annually). Some retailers accept batteries for recycling. Mail-in recycling programs are another option for rural areas."},
            ], 2) +
            "</div>" +
            p("When in doubt, contact your local waste management department or environmental health agency. They can tell you the specific rules for your area and direct you to the nearest disposal location.") +
            alert("warning", "scale", "Business vs. residential", "If you are disposing of power stations as a business (not a household), the rules are much stricter. Businesses must follow full RCRA hazardous waste regulations, which include proper labeling, manifest tracking, and using licensed hazardous waste haulers. Fines for improper business disposal can be tens of thousands of dollars.")
        },
        {
            "id": "safe-transport-storage",
            "title": "Safe Transport & Storage Before Disposal",
            "content": p("If you need to store or transport a power station before disposing of it, follow these safety guidelines:") +
            step_grid([
                {"title": "Discharge to 30-50% First", "desc": "If the battery is fully charged, discharge it to about 30-50% before storage or transport. A partially discharged battery is safer than a fully charged one — there is less energy available if something goes wrong. Use the power station to run a load (light, fan) to discharge it."},
                {"title": "Store in a Cool, Dry Place", "desc": "Keep the power station in a cool, dry area away from direct sunlight and heat sources. Room temperature (15-25°C / 59-77°F) is ideal. Do not store it in a hot attic, garage in summer, or near furnaces/water heaters. Heat accelerates degradation and increases fire risk."},
                {"title": "Insulate Terminals", "desc": "If you are transporting multiple batteries or loose battery cells, make sure the terminals cannot short circuit against metal objects. Tape over the terminals with electrical tape or put each battery in its own plastic bag. Short circuits can cause fires."},
                {"title": "Use Fire-Safe Containers for Damaged Batteries", "desc": "If the battery is swollen, damaged, or has been dropped, transport it in a fire-safe container. A metal ammo can, ceramic pot with lid, or sand-filled bucket works. Never put a damaged battery in your car's trunk or passenger compartment for a long drive."},
                {"title": "Never Disassemble Before Disposal", "desc": "Do not try to take apart the power station or remove individual battery cells before disposal. The recycling facility has the proper equipment and training to safely dismantle batteries. Disassembling at home is dangerous and can cause fires or chemical exposure."},
                {"title": "Keep Away from Children and Pets", "desc": "While waiting for disposal, keep the power station somewhere children and pets cannot reach. Curious kids or animals might damage it or try to open it. A high shelf or locked cabinet is best."},
            ], "orange") +
            alert("critical", "flame", "Damaged/ swollen batteries", "If your power station battery is swollen, bulging, leaking, or has been in a fire — treat it as extremely dangerous. Do NOT charge it. Do NOT put it in your car. Contact your local fire department or hazardous waste facility for guidance on safe transport. Some fire departments will come to pick up dangerous batteries.")
        },
    ],
    "faqs": [
        {"q": "How do I properly dispose of a portable power station?", "a": "The best ways to dispose of a portable power station are: take it to a household hazardous waste (HHW) facility, drop it off at a retail battery recycling program (Home Depot, Best Buy, etc.), use a manufacturer take-back program, or bring it to a certified lithium battery recycler. Never throw lithium batteries in the regular trash or curbside recycling — they are fire hazards. Search for '[your city] household hazardous waste' to find locations near you."},
        {"q": "Can I throw a portable power station in the trash?", "a": "No — it is illegal in most jurisdictions and extremely dangerous. Lithium-ion batteries can cause fires in garbage trucks, at transfer stations, and in landfills. The EPA classifies lithium batteries as hazardous waste. Fines for improper disposal range from $100 to thousands of dollars depending on location and circumstances. Always use proper battery recycling channels."},
        {"q": "Does Home Depot or Best Buy recycle power stations?", "a": "Home Depot, Lowe's, Best Buy, and many other retailers have battery recycling programs that accept rechargeable batteries. However, their ability to accept large portable power stations varies by location. Some stores only accept smaller batteries (AA, AAA, cell phone batteries). Call your local store ahead of time to confirm whether they accept larger power stations, and what their policies are."},
        {"q": "How much does it cost to recycle a power station?", "a": "Cost varies by location and method. Household hazardous waste facilities often accept batteries for free or a small fee ($5-$20). Many retail drop-off programs are free for consumers. Specialized battery recyclers may charge $20-$100 depending on the size and weight. Manufacturer take-back programs are sometimes free, especially if you are buying a new unit from them. Mail-in recycling programs typically cost $10-$30 for shipping."},
        {"q": "Can I donate a working portable power station?", "a": "Yes! Many organizations happily accept working portable power stations: community centers, emergency shelters, schools, Habitat for Humanity ReStores, ham radio clubs, community gardens, and theater groups. Even units with degraded batteries are useful for low-power applications. Post on Freecycle, Craigslist Free, or local Facebook groups if you want someone to pick it up for free."},
        {"q": "What should I do with a swollen battery?", "a": "A swollen (bulging) battery is a fire hazard. Stop using it immediately. Do not charge it, do not discharge it hard, and do not try to open or puncture it. Store it in a cool, safe place away from flammable materials (ideally in a fire-safe container). Contact your local household hazardous waste facility or fire department for guidance on safe disposal. Handle it as little as possible."},
        {"q": "Are lithium batteries really that dangerous in landfills?", "a": "Yes. When lithium batteries are crushed or punctured in garbage trucks or landfill compaction, they can short circuit and ignite — causing fires that are difficult to put out. The EPA reports hundreds of lithium battery fires at US waste facilities every year. These fires destroy equipment, release toxic fumes, and endanger workers. The valuable metals in batteries also leach into the environment over time."},
        {"q": "What metals can be recovered from recycled lithium batteries?", "a": "Modern recycling facilities can recover 95%+ of the valuable metals from lithium batteries, including: lithium, cobalt, nickel, copper, aluminum, iron, and sometimes manganese. These metals can be refined and reused in new batteries, creating a circular economy. Recycling reduces the need for new mining, which has significant environmental and social impacts."},
        {"q": "Is it legal to throw batteries in the trash?", "a": "It is illegal in most US states and municipalities to throw lithium batteries in the regular trash. Laws vary by location, but most classify lithium batteries as household hazardous waste that requires special disposal. Fines range from $100 to $50,000+ depending on jurisdiction and whether it is a first offense or a business violation. Always check your local waste management rules."},
        {"q": "How do I prepare a power station for disposal?", "a": "For safe disposal: discharge the battery to 30-50% if possible (use it to power a light or fan), do not disassemble it, tape over any exposed terminals if the unit is open, place it in a plastic bag to prevent short circuits, and transport it in a cool part of your vehicle (not a hot trunk). For damaged/swollen batteries, use a fire-safe container and contact the facility ahead of time. Never throw it in the regular trash."},
    ],
    "related": [
        {"href": "portable-power-station-battery-replacement-cost.html", "badge": "REPLACEMENT", "badge_class": "bg-yellow-500/20 text-yellow-400", "border_class": "border-yellow-500/30", "badge2": "Cost Guide", "title": "Battery Replacement Cost", "desc": "How much battery replacement costs by brand, DIY vs professional, warranty coverage, and whether it is worth it."},
        {"href": "how-to-store-portable-power-station.html", "badge": "STORAGE", "badge_class": "bg-green-500/20 text-green-400", "border_class": "border-green-500/30", "badge2": "Guide", "title": "Storage Guide", "desc": "How to store a portable power station long-term — ideal charge level, temperature, cycling schedule, and prep steps."},
        {"href": "portable-power-station-overheating-hot.html", "badge": "HEAT", "badge_class": "bg-orange-500/20 text-orange-400", "border_class": "border-orange-500/30", "badge2": "Safety", "title": "Overheating Guide", "desc": "Why power stations overheat, normal operating temperatures, cooling issues, and how to prevent overheating."},
        {"href": "portable-power-station-not-charging.html", "badge": "CHARGING", "badge_class": "bg-yellow-500/20 text-yellow-400", "border_class": "border-yellow-500/30", "badge2": "Troubleshooting", "title": "Not Charging", "desc": "Troubleshoot why your power station is not charging — common causes for AC, solar, and DC charging issues."},
        {"href": "portable-power-station-wont-turn-on.html", "badge": "POWER&nbsp;ON", "badge_class": "bg-red-500/20 text-red-400", "border_class": "border-red-500/30", "badge2": "Troubleshooting", "title": "Won't Turn On", "desc": "What to do when your portable power station will not turn on — step-by-step troubleshooting for all brands."},
        {"href": "outdoor-power.html", "badge": "ALL&nbsp;MODELS", "badge_class": "bg-electric-500/20 text-electric-400", "border_class": "border-electric-500/30", "badge2": "Category", "title": "Outdoor Power Hub", "desc": "Browse all portable power station guides, comparisons, specs, and troubleshooting resources in one place."},
    ],
}

PAGES = [page4]

# Generate pages
os.makedirs(OUTPUT_DIR, exist_ok=True)

for page in PAGES:
    filepath = os.path.join(OUTPUT_DIR, page["filename"])
    html_content = build_page(page)
    with open(filepath, "w") as f:
        f.write(html_content)
    text = re.sub(r'<[^>]+>', ' ', html_content)
    words = text.split()
    print(f"  Created: {page['filename']}  ({len(words)} words)")

print(f"\nTotal pages created: {len(PAGES)}")
