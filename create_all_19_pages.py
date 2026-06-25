#!/usr/bin/env python3
"""Generate all 19 missing SEO pages for TechSpecsHub."""

import os
import json
import html
from typing import List, Dict, Any

OUTPUT_DIR = "/workspace/pages/specs"
BASE_URL = "https://powerspecshub.com/pages/specs"
SITE_NAME = "TechSpecsHub"
UPDATED_DATE = "2026-06-25"
UPDATED_DATE_TEXT = "June 25, 2026"

def p(text: str) -> str:
    return f'<p class="text-gray-300 leading-relaxed mb-4">{text}</p>'

def ul(items: List[str]) -> str:
    lis = "".join(f'<li class="flex items-start gap-2"><i data-lucide="check" style="width:1rem;height:1rem;color:#4ade80;flex-shrink:0;margin-top:0.1rem"></i><span>{item}</span></li>' for item in items)
    return f'<ul class="space-y-3 text-sm text-gray-300">{lis}</ul>'

def ul_x(items: List[str]) -> str:
    lis = "".join(f'<li class="flex items-start gap-2"><i data-lucide="x" style="width:1rem;height:1rem;color:#f87171;flex-shrink:0;margin-top:0.1rem"></i><span>{item}</span></li>' for item in items)
    return f'<ul class="space-y-3 text-sm text-gray-300">{lis}</ul>'

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

BODY_HEADER = '''<body class="bg-navy-950 text-white min-h-screen font-display">

  <header>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16 gap-4">
        <a href="../../index.html" class="flex items-center gap-2.5 flex-shrink-0">
          <div class="w-9 h-9 bg-gradient-to-br from-electric-400 to-electric-600 rounded-lg flex items-center justify-center shadow-lg shadow-electric-500/20">
            <i data-lucide="cpu" style="width:1.25rem;height:1.25rem;color:#0a1628"></i>
          </div>
          <span class="font-bold text-lg tracking-tight">TechSpecs<span class="gradient-text">Hub</span></span>
        </a>

        <nav class="hidden lg:flex items-center gap-1 text-sm font-medium">
          <div class="nav-dropdown-trigger">
            <button class="flex items-center gap-1.5 px-3 py-2 text-gray-300 hover:text-white rounded-lg hover:bg-white/5 transition-all">
              Categories <i data-lucide="chevron-down" style="width:0.875rem;height:0.875rem"></i>
            </button>
            <div class="nav-dropdown">
              <p class="nav-dropdown-section-label">Device Categories</p>
              <a href="outdoor-power.html"><i data-lucide="battery-charging" style="width:1rem;height:1rem;color:#22d3ee;flex-shrink:0"></i>Outdoor Power Stations</a>
              <a href="hybrid-cars.html"><i data-lucide="car" style="width:1rem;height:1rem;color:#22d3ee;flex-shrink:0"></i>Hybrid &amp; EV Batteries</a>
              <a href="drones.html"><i data-lucide="plane" style="width:1rem;height:1rem;color:#22d3ee;flex-shrink:0"></i>Drones &amp; UAV</a>
              <a href="smart-home.html"><i data-lucide="home" style="width:1rem;height:1rem;color:#22d3ee;flex-shrink:0"></i>Smart Home Devices</a>
              <a href="ebike-micromobility.html"><i data-lucide="bike" style="width:1rem;height:1rem;color:#22d3ee;flex-shrink:0"></i>E-Bike &amp; Micromobility</a>
              <a href="3d-printers.html"><i data-lucide="box" style="width:1rem;height:1rem;color:#22d3ee;flex-shrink:0"></i>3D Printers</a>
              <a href="navigation.html"><i data-lucide="compass" style="width:1rem;height:1rem;color:#22d3ee;flex-shrink:0"></i>Navigation &amp; Marine</a>
            </div>
          </div>
          <div class="nav-dropdown-trigger">
            <button class="flex items-center gap-1.5 px-3 py-2 text-gray-300 hover:text-white rounded-lg hover:bg-white/5 transition-all">
              Tools &amp; Data <i data-lucide="chevron-down" style="width:0.875rem;height:0.875rem"></i>
            </button>
            <div class="nav-dropdown">
              <p class="nav-dropdown-section-label">Data Resources</p>
              <a href="../error-code-db.html"><i data-lucide="alert-circle" style="width:1rem;height:1rem;color:#f87171;flex-shrink:0"></i>Error Code Database</a>
              <a href="../master-specs.html"><i data-lucide="table-2" style="width:1rem;height:1rem;color:#22d3ee;flex-shrink:0"></i>Master Specs Comparison</a>
              <a href="../brand-index.html"><i data-lucide="building-2" style="width:1rem;height:1rem;color:#22d3ee;flex-shrink:0"></i>Brand Index A&ndash;Z</a>
              <hr class="my-2 border-white/10">
              <p class="nav-dropdown-section-label">Buyer's Guides</p>
              <a href="../tools/best-multimeters-2026.html"><i data-lucide="wrench" style="width:1rem;height:1rem;color:#fbbf24;flex-shrink:0"></i>Best Multimeters 2026</a>
            </div>
          </div>
          <a href="../about.html" class="px-3 py-2 text-gray-300 hover:text-white rounded-lg hover:bg-white/5 transition-all">About</a>
        </nav>

        <div class="flex items-center gap-2">
          <button id="search-btn" class="flex items-center gap-2 pl-3 pr-2 py-1.5 bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg transition-all text-sm text-gray-300 hover:text-white">
            <i data-lucide="search" style="width:0.9rem;height:0.9rem"></i>
            <span class="hidden sm:inline">Search</span>
            <kbd class="hidden md:inline-flex items-center gap-0.5 px-1.5 py-0.5 bg-white/10 rounded text-xs text-gray-400 font-mono ml-1">&crarr;K</kbd>
          </button>
          <button id="mobile-menu-btn" class="lg:hidden p-2 text-gray-400 hover:text-white rounded-lg hover:bg-white/5">
            <i data-lucide="menu" style="width:1.25rem;height:1.25rem"></i>
          </button>
        </div>
      </div>
    </div>

    <div id="mobile-menu" class="lg:hidden bg-navy-900 border-t border-white/5">
      <div class="max-w-7xl mx-auto px-4 py-3 space-y-1 text-sm">
        <p class="nav-dropdown-section-label">Categories</p>
        <a href="outdoor-power.html" class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-white/5 text-gray-300 hover:text-white transition-all"><i data-lucide="battery-charging" style="width:1rem;height:1rem;color:#22d3ee"></i>Outdoor Power Stations</a>
        <a href="hybrid-cars.html" class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-white/5 text-gray-300 hover:text-white transition-all"><i data-lucide="car" style="width:1rem;height:1rem;color:#22d3ee"></i>Hybrid &amp; EV Batteries</a>
        <a href="drones.html" class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-white/5 text-gray-300 hover:text-white transition-all"><i data-lucide="plane" style="width:1rem;height:1rem;color:#22d3ee"></i>Drones &amp; UAV</a>
        <a href="smart-home.html" class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-white/5 text-gray-300 hover:text-white transition-all"><i data-lucide="home" style="width:1rem;height:1rem;color:#22d3ee"></i>Smart Home Devices</a>
        <a href="ebike-micromobility.html" class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-white/5 text-gray-300 hover:text-white transition-all"><i data-lucide="bike" style="width:1rem;height:1rem;color:#22d3ee"></i>E-Bike &amp; Micromobility</a>
        <a href="3d-printers.html" class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-white/5 text-gray-300 hover:text-white transition-all"><i data-lucide="box" style="width:1rem;height:1rem;color:#22d3ee"></i>3D Printers</a>
        <a href="navigation.html" class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-white/5 text-gray-300 hover:text-white transition-all"><i data-lucide="compass" style="width:1rem;height:1rem;color:#22d3ee"></i>Navigation &amp; Marine</a>
        <hr class="border-white/10 my-2">
        <p class="nav-dropdown-section-label">Tools &amp; Data</p>
        <a href="../error-code-db.html" class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-white/5 text-gray-300 hover:text-white transition-all"><i data-lucide="alert-circle" style="width:1rem;height:1rem;color:#f87171"></i>Error Code Database</a>
        <a href="../master-specs.html" class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-white/5 text-gray-300 hover:text-white transition-all"><i data-lucide="table-2" style="width:1rem;height:1rem;color:#22d3ee"></i>Master Specs Comparison</a>
        <a href="../brand-index.html" class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-white/5 text-gray-300 hover:text-white transition-all"><i data-lucide="building-2" style="width:1rem;height:1rem;color:#22d3ee"></i>Brand Index A&ndash;Z</a>
        <a href="../tools/best-multimeters-2026.html" class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-white/5 text-gray-300 hover:text-white transition-all"><i data-lucide="wrench" style="width:1rem;height:1rem;color:#fbbf24"></i>Best Multimeters 2026</a>
        <hr class="border-white/10 my-2">
        <a href="../about.html" class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-white/5 text-gray-300 hover:text-white transition-all"><i data-lucide="info" style="width:1rem;height:1rem;color:#22d3ee"></i>About</a>
      </div>
    </div>
  </header>

  <div id="search-modal">
    <div id="search-backdrop"></div>
    <div class="modal-inner">
      <div class="modal-box">
        <div class="flex items-center gap-3 px-4 py-3.5 border-b border-white/10">
          <i data-lucide="search" style="width:1.1rem;height:1.1rem;color:#6b7280;flex-shrink:0"></i>
          <input id="search-input-field" type="text" placeholder="Search models, error codes, specs&hellip;" autocomplete="off" spellcheck="false">
          <button id="search-close-btn" class="p-1.5 text-gray-400 hover:text-white rounded transition-colors flex-shrink-0">
            <i data-lucide="x" style="width:1rem;height:1rem"></i>
          </button>
        </div>
        <div id="search-results-list"></div>
        <div class="border-t border-white/5 px-4 py-2.5 flex items-center justify-between text-xs text-gray-500">
          <span>Press <kbd class="bg-white/10 px-1.5 py-0.5 rounded font-mono text-gray-300">Enter</kbd> to search, <kbd class="bg-white/10 px-1.5 py-0.5 rounded font-mono text-gray-300">Esc</kbd> to close</span>
        </div>
      </div>
    </div>
  </div>
'''

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


# ===================== PAGE DATA =====================

PAGES = []

# ===== OUTDOOR POWER PAGE 2: Battery Replacement Cost =====

PAGES.append({
    "filename": "portable-power-station-battery-replacement-cost.html",
    "title": "Portable Power Station Battery Replacement Cost & Options (2026)",
    "headline": "Portable Power Station Battery Replacement Cost & Options (2026)",
    "meta_desc": "How much does it cost to replace a portable power station battery? Complete cost guide by brand, DIY vs professional, warranty coverage, and whether replacement is worth it.",
    "category": "Outdoor Power",
    "category_link": "outdoor-power.html",
    "breadcrumb_title": "Battery Replacement Cost",
    "hero_blur": "bg-yellow-500/5",
    "hero_badges": '''<div class="px-3 py-1.5 bg-yellow-500/20 text-yellow-400 font-mono font-bold text-sm rounded-md border border-yellow-500/30">REPLACEMENT&nbsp;COST</div>
        <span class="badge badge-info"><i data-lucide="dollar-sign" style="width:0.75rem;height:0.75rem"></i>Cost Guide</span>
        <span class="badge badge-info"><i data-lucide="wrench" style="width:0.75rem;height:0.75rem"></i>DIY &amp; Pro</span>''',
    "h1": 'Portable Power Station Battery Replacement Cost &mdash; <span class="gradient-text">Complete 2026 Guide</span>',
    "hero_desc": "Battery replacement is one of the most important cost considerations when buying a portable power station. Lithium batteries do not last forever — after 500-6000 cycles (depending on chemistry), capacity drops and performance degrades. This guide covers exactly how much replacement costs by brand, whether you should replace or buy new, DIY options, warranty coverage, and how to extend battery life to delay replacement as long as possible.",
    "hero_stats": '''<div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="dollar-sign" style="width:0.9rem;height:0.9rem"></i>Avg. Cost</div>
          <div class="font-mono font-bold text-xl text-white">$300&ndash;$1,500</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="battery" style="width:0.9rem;height:0.9rem"></i>LFP Cycles</div>
          <div class="font-mono font-bold text-xl text-green-400">3,000&ndash;6,000</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="battery" style="width:0.9rem;height:0.9rem"></i>NMC Cycles</div>
          <div class="font-bold text-xl text-yellow-400">500&ndash;1,000</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="shield" style="width:0.9rem;height:0.9rem"></i>Warranty</div>
          <div class="font-bold text-xl text-electric-400">2&ndash;5 yrs</div>
        </div>''',
    "qa_gradient": "from-yellow-950/20 to-navy-900 border-yellow-500/20",
    "qa_icon_color": "#facc15",
    "qa_title": "How Much Does Battery Replacement Cost?",
    "qa_text": '<strong class="text-white">Battery replacement for a portable power station costs $300 to $1,500 on average, depending on capacity and chemistry.</strong> A small 500Wh NMC battery might cost $200-$400 to replace, while a large 2,000Wh+ LFP battery can cost $800-$1,500. Some brands sell official replacement battery modules, while others require sending the unit in for service. In many cases, especially with budget stations, replacing the entire unit is more cost-effective than replacing just the battery.',
    "qa_extra": '''<div class="grid md:grid-cols-2 gap-3 mt-4">
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-green-400 font-semibold mb-1 flex items-center gap-2"><i data-lucide="thumbs-up" style="width:1rem;height:1rem"></i>Replace when&hellip;</div>
          <p class="text-sm text-gray-300">Unit is premium model, battery is 50-70% of new cost, unit works perfectly otherwise</p>
        </div>
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-red-400 font-semibold mb-1 flex items-center gap-2"><i data-lucide="thumbs-down" style="width:1rem;height:1rem"></i>Replace vs buy new when&hellip;</div>
          <p class="text-sm text-gray-300">Replacement is 70%+ of new cost, unit is older model, newer models have better features</p>
        </div>
      </div>''',
    "sections": [
        {
            "id": "cost-by-brand",
            "title": "Battery Replacement Cost by Brand",
            "content": p("The cost of replacing your power station battery varies dramatically by brand. Some brands sell user-replaceable battery modules, while others require you to send the entire unit to a service center. Here is what you can expect from each major brand in 2026:") +
            specs_table(
                ["Brand", "Battery Type", "Typical Replacement Cost", "User-Replaceable?", "Warranty Period"],
                [
                    ["<strong>EcoFlow</strong>", "LFP (most models)", "$500–$1,200", "Some models (Delta Pro)", "2–5 years"],
                    ["<strong>Jackery</strong>", "NMC / LFP", "$400–$1,000", "No (service center)", "2–3 years"],
                    ["<strong>Bluetti</strong>", "LFP", "$600–$1,400", "Some models (AC series)", "2–5 years"],
                    ["<strong>Anker</strong>", "LFP", "$350–$900", "No (service center)", "5 years (535/757)"],
                    ["<strong>Goal Zero</strong>", "LFP / NMC", "$500–$1,300", "No (service center)", "2 years"],
                    ["<strong>Budget brands</strong>", "NMC / generic LFP", "$200–$600", "Rarely", "1 year"],
                ]
            ) +
            p("Important note: Prices change frequently and vary by model. Always check the manufacturer's website or contact support for current pricing. Some brands do not publicly list replacement costs — you have to request a quote through their support portal.") +
            alert("info", "lightbulb", "Pro tip", "Before paying for replacement, check if your unit is still under warranty. Most brands cover defective batteries for 2-5 years. If your battery has lost significant capacity within the warranty period and you did not abuse it, you may qualify for a free replacement.")
        },
        {
            "id": "is-it-worth-it",
            "title": "Is Battery Replacement Worth It?",
            "content": p("Whether replacing the battery is worth it depends on several factors. Here is a framework to help you decide:") +
            '<div class="grid md:grid-cols-2 gap-6 mb-6">' +
            '<div><h3 class="font-bold text-xl mb-4 text-green-400 flex items-center gap-2"><i data-lucide="check-circle" style="width:1.25rem;height:1.25rem"></i>Replacement Is Worth It When&hellip;</h3>' +
            ul([
                "The replacement cost is less than 50% of a comparable new unit",
                "Your power station is a premium model with features you cannot get in cheaper new units",
                "The inverter, charge controller, and other components are in perfect working order",
                "Your model has expandable battery capacity you want to keep using",
                "You need the exact same form factor for your existing setup (van, RV, etc.)",
                "The brand offers a good warranty on the replacement battery"
            ]) +
            '</div><div><h3 class="font-bold text-xl mb-4 text-red-400 flex items-center gap-2"><i data-lucide="x-circle" style="width:1.25rem;height:1.25rem"></i>Buy New Instead When&hellip;</h3>' +
            ul_x([
                "Replacement costs 70% or more of a comparable new unit",
                "Your model is 5+ years old and newer models have much better efficiency and features",
                "The unit has other issues besides the battery (display problems, port failures)",
                "You can get a sale or refurbished unit at a good price",
                "The brand has poor customer support and you do not want to deal with them again",
                "You actually need more capacity than your current unit provides"
            ]) +
            "</div></div>" +
            p("As a general rule of thumb: if replacement costs more than 60% of what a comparable new unit costs, just buy new. You get a fresh warranty, latest technology, and the peace of mind that everything is new — not just the battery.") +
            alert("warning", "calculator", "Quick math", "If your station cost $1,000 new and replacement is $500, it is probably worth replacing (50% cost). If replacement is $700 (70%), buy new instead — especially if you can find a sale or refurbished unit.")
        },
        {
            "id": "diy-vs-pro",
            "title": "DIY Replacement vs Professional Service",
            "content": p("Some power stations are designed for user-replaceable batteries, while others are fully sealed and require professional service. Here are the pros and cons of each approach:") +
            specs_table(
                ["Factor", "DIY Replacement", "Professional Service"],
                [
                    ["<strong>Cost</strong>", "$200–$800 (parts only)", "$400–$1,500 (parts + labor)"],
                    ["<strong>Warranty</strong>", "Voids manufacturer warranty usually", "Preserves warranty"],
                    ["<strong>Safety</strong>", "Risk if you do not know what you are doing", "Certified technicians, safe"],
                    ["<strong>Time</strong>", "1–4 hours if you have skills", "1–4 weeks turnaround"],
                    ["<strong>Available for</strong>", "Only modular designs", "All brands/models"],
                    ["<strong>BMS compatibility</strong>", "May need to flash or match BMS", "Guaranteed compatible"],
                ]
            ) +
            p('<strong class="text-white">Safety warning:</strong> Working with lithium batteries is dangerous. Shorting a battery pack can cause fires, explosions, and serious injury. Only attempt DIY replacement if you have experience with high-voltage DC systems, proper tools, and safety equipment. Always work in a well-ventilated area away from flammable materials.') +
            alert("critical", "alert-octagon", "Important safety note", "Never open a swollen or damaged battery pack. Swollen batteries are at risk of thermal runaway. If your battery is swollen, do not attempt DIY replacement — contact a professional battery recycling service or the manufacturer for safe disposal and replacement options.")
        },
        {
            "id": "warranty-coverage",
            "title": "Warranty Coverage for Batteries",
            "content": p("Most portable power stations come with a warranty that covers the battery, but the terms vary significantly. Here is what you need to know:") +
            step_grid([
                {"title": "What the Warranty Usually Covers", "desc": "Manufacturing defects, premature capacity loss, BMS failures, and cells that fail under normal use. The standard warranty period is 2-5 years depending on the brand and model. Premium LFP models tend to have longer warranties."},
                {"title": "What the Warranty Does NOT Cover", "desc": "Normal wear and tear, capacity loss from normal cycling, physical damage, water damage, overcharging/discharging outside specs, freezing damage, DIY modifications, and use with incompatible accessories. Most warranties cover defects, not usage-based degradation."},
                {"title": "How to Make a Warranty Claim", "desc": "Contact customer support, provide your order number and serial number, describe the issue, run any diagnostic tests they ask for, and send photos/videos as evidence. If approved, they will either repair, replace, or refund — depending on the policy."},
                {"title": "Capacity Warranty Thresholds", "desc": "Many brands define 'battery failure' as dropping below 60-70% of original capacity within the warranty period. If your battery is at 75% capacity after 3 years, that is probably considered normal wear and not covered. Check the fine print for your specific model."},
            ], "electric") +
            p("Some premium brands like EcoFlow and Anker offer 5-year warranties on their higher-end models. Budget brands typically only offer 1-year warranties. Extended warranties are sometimes available at extra cost — evaluate whether they are worth it based on the price of the unit and replacement cost.")
        },
        {
            "id": "signs-of-failure",
            "title": "Signs Your Battery Needs Replacement",
            "content": p("How do you know when it is actually time to replace the battery? Watch for these common signs of battery degradation:") +
            '<div class="space-y-4 mb-6">' +
            step_grid([
                {"title": "Significantly Reduced Runtime", "desc": "The most obvious sign. If your station used to run your fridge for 24 hours and now only runs it for 8-10 hours, the battery has lost significant capacity. Test with a known load to confirm it is the battery, not just higher power draw from the device."},
                {"title": "Voltage Drops Rapidly Under Load", "desc": "If the battery percentage drops from 100% to 20% very quickly when you plug in a load, the battery's internal resistance has increased. This means less usable capacity and more heat generation during use."},
                {"title": "Charging Takes Much Longer", "desc": "If charging that used to take 2 hours now takes 5+ hours (with the same charger and conditions), the battery may have high internal resistance or some cells have failed. Rule out charger and cable issues first."},
                {"title": "Battery Swells or Bulges", "desc": "If the case is bulging, the battery is swollen. STOP USING IT IMMEDIATELY. A swollen battery is a fire hazard. Do not charge it, do not discharge it hard, and do not attempt to open it. Contact the manufacturer or a recycling center for safe disposal."},
                {"title": "BMS Errors or Fault Codes", "desc": "Frequent battery-related error codes, BMS (Battery Management System) errors, or the unit refusing to charge/discharge despite being plugged in. These can indicate battery health issues that the BMS is trying to protect you from."},
                {"title": "Excessive Heat During Use", "desc": "If the battery area gets much hotter than it used to during charging or discharging, it could be a sign of high internal resistance or failing cells. Some warmth is normal, but a noticeable increase is a red flag."},
            ], "orange") + "</div>" +
            alert("warning", "thermometer", "Temperature matters", "Battery performance drops in cold weather. If you notice reduced runtime only in cold temperatures, that is normal — lithium batteries have lower capacity when cold. The real test is performance at room temperature (20-25°C / 68-77°F).")
        },
        {
            "id": "extend-life",
            "title": "How to Extend Battery Life & Delay Replacement",
            "content": p("The best way to save money on battery replacement is to delay it for as long as possible. Here are proven ways to extend your power station's battery life:") +
            '<div class="grid md:grid-cols-2 gap-4">' +
            grid_cards([
                {"title": "Keep Charge Between 20-80%", "color": "text-green-400", "desc": "Avoiding full charges and full discharges reduces stress on the battery cells. If you do not need 100% capacity, set the charge limit to 80-90% in the app. Try not to discharge below 20% regularly."},
                {"title": "Store at 50-60% Charge", "color": "text-blue-400", "desc": "For long-term storage, charge to 50-60% and recharge to that level every 3-6 months. Storing at 100% or 0% causes accelerated degradation. Most brands recommend 50% for storage."},
                {"title": "Avoid Extreme Temperatures", "color": "text-red-400", "desc": "Heat is the #1 killer of lithium batteries. Do not leave your power station in a hot car, in direct sun, or near heat sources. Cold is also bad — avoid charging below freezing (0°C / 32°F)."},
                {"title": "Use Proper Charging Settings", "color": "text-yellow-400", "desc": "Fast charging generates more heat. If you are not in a hurry, use standard or silent charging mode instead of turbo/fast charging. Slower charging is gentler on the battery cells."},
                {"title": "Keep It Clean and Dry", "color": "text-purple-400", "desc": "Dust and moisture can cause corrosion on contacts and inside the unit. Keep the vents clear for proper cooling. Wipe the exterior with a dry cloth periodically. Do not use compressed air — it can push dust deeper."},
                {"title": "Update Firmware", "color": "text-electric-400", "desc": "Manufacturers often release firmware updates that improve BMS algorithms, charging profiles, and thermal management. Keeping firmware up to date ensures the battery is managed optimally."},
            ], 2) +
            "</div>" +
            p("Following these best practices can extend battery life by 30-50% compared to average use. For a typical LFP battery rated for 3,000 cycles, good care could push it to 4,000-5,000 cycles — potentially adding years of useful life before replacement is needed.") +
            alert("info", "calendar", "Real-world example", "A 1,000Wh LFP power station used daily (1 full cycle per day) with good care might last 8-10 years before reaching 70% capacity. With poor care (always 100-0%, stored in heat), it might only last 4-5 years. Good habits literally cut your long-term cost in half.")
        },
        {
            "id": "third-party-options",
            "title": "Third-Party Replacement Options",
            "content": p("If official replacement is too expensive or unavailable, there are third-party options. Be cautious — quality varies widely and using third-party batteries usually voids your warranty. Here is what to consider:") +
            specs_table(
                ["Option", "Pros", "Cons", "Cost Range"],
                [
                    ["<strong>Third-party battery kits</strong>", "Cheaper than official, sometimes better cells", "Quality varies, may not match BMS, voids warranty", "$200–$700"],
                    ["<strong>Local battery shop</strong>", "Professional installation, support", "Limited experience with power stations, variable quality", "$300–$900"],
                    ["<strong>Used batteries (eBay/Facebook)</strong>", "Very cheap", "Unknown condition, safety risk, no warranty", "$100–$500"],
                    ["<strong>Refurbished from manufacturer</strong>", "Tested, warranty, cheaper than new", "Not always available, may have cosmetic wear", "$300–$800"],
                    ["<strong>Battery rebuild service</strong>", "Reuses your case/BMS, custom cells", "Quality depends on the rebuilder", "$250–$600"],
                ]
            ) +
            alert("critical", "alert-triangle", "Safety warning about third-party batteries", "Poor-quality replacement batteries are a major fire risk. Cheap cells from unknown manufacturers may not have proper protections, can swell, and can cause thermal runaway. If you go third-party, use a reputable company with good reviews and a track record of safe installations. Never buy no-name battery packs from random sellers.")
        },
    ],
    "faqs": [
        {"q": "How much does it cost to replace a portable power station battery?", "a": "Battery replacement costs $300 to $1,500 on average, depending on capacity and chemistry. Small 500Wh NMC batteries cost $200-$400, while large 2,000Wh+ LFP batteries cost $800-$1,500. Some brands sell user-replaceable modules, while others require service center replacement. Labor adds $100-$300 if you use professional service."},
        {"q": "Is it worth replacing the battery in a portable power station?", "a": "Replacement is worth it if the cost is less than 50-60% of a comparable new unit and the rest of the station works perfectly. If replacement costs 70% or more of a new unit, you are usually better off buying new — especially since you get a full warranty and the latest features. Premium models with expandable capacity are more often worth repairing than budget models."},
        {"q": "How long do portable power station batteries last?", "a": "LiFePO4 (LFP) batteries last 3,000-6,000 cycles before dropping to 80% capacity, which is typically 5-10 years with regular use. NMC (lithium nickel manganese cobalt oxide) batteries last 500-1,000 cycles, or about 2-5 years. Actual lifespan depends on usage patterns, charging habits, temperature exposure, and storage practices."},
        {"q": "Does the warranty cover battery replacement?", "a": "Warranties cover manufacturing defects and premature failure, but not normal wear and tear from use. Most brands define failure as dropping below 60-70% of original capacity within the warranty period (2-5 years). If your battery degrades normally over time, that is usually not covered. Always check the specific warranty terms for your model."},
        {"q": "Can I replace the battery myself?", "a": "Some models have user-replaceable battery modules (certain EcoFlow, Bluetti, and Goal Zero models), but most require professional service or are not designed to be opened. DIY replacement is possible if you have electrical experience and the right tools, but it voids your warranty and carries safety risks. Always follow proper safety procedures when working with lithium batteries."},
        {"q": "What are the signs that my battery needs replacing?", "a": "Common signs include: significantly reduced runtime, rapid voltage drop under load, longer charging times, swelling or bulging of the case, frequent BMS error codes, and excessive heat during charging or discharging. Some warmth during use is normal, but a noticeable change in performance or temperature is a red flag."},
        {"q": "How do I extend my power station battery life?", "a": "The most effective ways to extend battery life are: keep charge between 20-80% for daily use, store at 50-60% charge long-term, avoid extreme temperatures (especially heat), use slower charging when possible, keep the unit clean and vents clear, and keep firmware updated for optimal BMS performance."},
        {"q": "Can I upgrade to a larger battery?", "a": "Some power stations support expandable battery packs (EcoFlow Delta series, Bluetti AC series, certain Jackery models) that let you add capacity by connecting extra battery modules. For non-expandable models, upgrading the internal battery is usually not practical or cost-effective — you would need to match the BMS, enclosure, and charging system, which often costs more than buying a larger unit."},
        {"q": "What happens to old power station batteries?", "a": "Old lithium batteries should be recycled at a certified battery recycling center, not thrown in the trash. Many cities have hazardous waste collection days for batteries. Some retailers and manufacturers offer take-back programs. The valuable metals (lithium, cobalt, nickel, copper) can be recovered and reused in new batteries."},
        {"q": "Are third-party replacement batteries safe?", "a": "Quality varies dramatically. Reputable third-party battery shops that use name-brand cells and properly match the BMS can be safe and cost-effective. However, cheap no-name battery packs from unknown sellers are a major fire hazard — they may lack proper cell matching, protection circuits, and quality control. Always verify the reputation of any third-party service before purchasing."},
    ],
    "related": [
        {"href": "lifepo4-vs-lithium-ion-power-station.html", "badge": "LFP&nbsp;vs&nbsp;NMC", "badge_class": "bg-purple-500/20 text-purple-400", "border_class": "border-purple-500/30", "badge2": "Comparison", "title": "LFP vs Lithium-Ion", "desc": "Complete comparison of LiFePO4 vs lithium-ion batteries — cycle life, safety, cost, density, and which is right for you."},
        {"href": "how-to-store-portable-power-station.html", "badge": "STORAGE", "badge_class": "bg-green-500/20 text-green-400", "border_class": "border-green-500/30", "badge2": "Guide", "title": "Storage Guide", "desc": "How to store a portable power station long-term — ideal charge level, temperature, cycling schedule, and prep steps."},
        {"href": "portable-power-station-eco-mode.html", "badge": "ECO&nbsp;MODE", "badge_class": "bg-green-500/20 text-green-400", "border_class": "border-green-500/30", "badge2": "All Brands", "title": "ECO Mode Guide", "desc": "What is ECO mode, how much battery it saves, how to disable it, and how to optimize for longer runtime."},
        {"href": "can-portable-power-station-charge-while-in-use.html", "badge": "PASS-THROUGH", "badge_class": "bg-blue-500/20 text-blue-400", "border_class": "border-blue-500/30", "badge2": "FAQ", "title": "Charging While Using", "desc": "Can you charge and discharge at the same time? How pass-through charging works, which brands support it, and safety."},
        {"href": "portable-power-station-overheating-hot.html", "badge": "HEAT", "badge_class": "bg-orange-500/20 text-orange-400", "border_class": "border-orange-500/30", "badge2": "Safety", "title": "Overheating Guide", "desc": "Why power stations overheat, normal operating temperatures, cooling system issues, and how to prevent overheating."},
        {"href": "outdoor-power.html", "badge": "ALL&nbsp;MODELS", "badge_class": "bg-electric-500/20 text-electric-400", "border_class": "border-electric-500/30", "badge2": "Category", "title": "Outdoor Power Hub", "desc": "Browse all portable power station guides, comparisons, specs, and troubleshooting resources in one place."},
    ],
})

# ===== OUTDOOR POWER PAGE 3: Best for RV =====

PAGES.append({
    "filename": "best-portable-power-station-for-rv.html",
    "title": "Best Portable Power Station for RV & Boondocking (2026)",
    "headline": "Best Portable Power Station for RV & Boondocking (2026)",
    "meta_desc": "Best portable power stations for RV use and boondocking. Complete guide to RV power needs, TT-30 30A hookups, solar for RVs, top picks by RV size, and installation tips.",
    "category": "Outdoor Power",
    "category_link": "outdoor-power.html",
    "breadcrumb_title": "Best for RV",
    "hero_blur": "bg-blue-500/5",
    "hero_badges": '''<div class="px-3 py-1.5 bg-blue-500/20 text-blue-400 font-mono font-bold text-sm rounded-md border border-blue-500/30">RV&nbsp;POWER</div>
        <span class="badge badge-info"><i data-lucide="home" style="width:0.75rem;height:0.75rem"></i>Boondocking</span>
        <span class="badge badge-info"><i data-lucide="sun" style="width:0.75rem;height:0.75rem"></i>Solar Ready</span>''',
    "h1": 'Best Portable Power Station for RV &amp; Boondocking &mdash; <span class="gradient-text">2026 Guide</span>',
    "hero_desc": "Finding the right portable power station for your RV can transform your camping experience. Whether you are boondocking off-grid for weeks at a time or just want backup power at campgrounds with unreliable hookups, a good power station keeps your fridge, AC, lights, and devices running. This guide covers exactly what you need, how much power you actually use, the TT-30 30A connection explained, and our top picks for different RV sizes and budgets.",
    "hero_stats": '''<div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="zap" style="width:0.9rem;height:0.9rem"></i>Small RV</div>
          <div class="font-mono font-bold text-xl text-electric-400">1,000&ndash;2,000Wh</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="zap" style="width:0.9rem;height:0.9rem"></i>Medium RV</div>
          <div class="font-bold text-xl text-green-400">2,000&ndash;4,000Wh</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="zap" style="width:0.9rem;height:0.9rem"></i>Large RV</div>
          <div class="font-bold text-xl text-yellow-400">4,000Wh+</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="sun" style="width:0.9rem;height:0.9rem"></i>Solar Input</div>
          <div class="font-mono font-bold text-xl text-white">400&ndash;1,600W</div>
        </div>''',
    "qa_gradient": "from-blue-950/20 to-navy-900 border-blue-500/20",
    "qa_icon_color": "#60a5fa",
    "qa_title": "What Is the Best Power Station for RVs?",
    "qa_text": '<strong class="text-white">The best portable power station for an RV depends on your RV size and power needs, but for most people, a 2,000-4,000Wh LFP power station with 2,000-3,600W output and 400-800W solar input is the sweet spot.</strong> For small campers and van lifers, 1,000-2,000Wh is usually enough. For large RVs running AC, microwaves, and multiple appliances, look at 4,000Wh+ models with expandable battery capacity. The EcoFlow Delta Pro 3, Bluetti AC300, and Jackery Explorer 2000 Plus are among the most popular RV choices in 2026.',
    "qa_extra": '''<div class="grid md:grid-cols-2 gap-3 mt-4">
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-green-400 font-semibold mb-1 flex items-center gap-2"><i data-lucide="check-circle" style="width:1rem;height:1rem"></i>Key RV features</div>
          <p class="text-sm text-gray-300">High AC output, RV plug compatibility, large solar input, expandable capacity, app monitoring, 30A support</p>
        </div>
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-yellow-400 font-semibold mb-1 flex items-center gap-2"><i data-lucide="sun" style="width:1rem;height:1rem"></i>Boondocking essential</div>
          <p class="text-sm text-gray-300">Solar input of at least 400W is critical for off-grid use — it lets you recharge during the day without a generator.</p>
        </div>
      </div>''',
    "sections": [
        {
            "id": "rv-power-needs",
            "title": "How Much Power Does an RV Actually Use?",
            "content": p("Before buying a power station, you need to understand how much power your RV actually consumes. This varies dramatically based on the size of your RV, what appliances you use, and whether you have air conditioning. Here are typical power draw numbers:") +
            specs_table(
                ["Appliance/Device", "Running Watts", "Surge Watts", "Daily kWh (est.)"],
                [
                    ["<strong>RV Air Conditioner (13,500 BTU)</strong>", "1,200–1,800W", "3,000–5,000W", "6–12 kWh"],
                    ["<strong>RV Refrigerator (compressor)</strong>", "100–300W", "400–600W", "1.5–3 kWh"],
                    ["<strong>Microwave (1,000W)</strong>", "1,000–1,200W", "1,500–2,000W", "0.1–0.5 kWh"],
                    ["<strong>LED Lights (10 bulbs)</strong>", "50–100W", "—", "0.3–1 kWh"],
                    ["<strong>Water Pump</strong>", "50–100W", "150–300W", "0.1–0.3 kWh"],
                    ["<strong>TV + Streaming</strong>", "80–150W", "—", "0.5–1.5 kWh"],
                    ["<strong>Laptop + Phones</strong>", "50–100W", "—", "0.2–0.5 kWh"],
                    ["<strong>Coffee Maker</strong>", "800–1,200W", "—", "0.1–0.2 kWh"],
                    ["<strong>Hair Dryer</strong>", "1,500–1,800W", "—", "0.1–0.2 kWh"],
                    ["<strong>Furnace Blower</strong>", "300–500W", "600–1,000W", "1–3 kWh (winter)"],
                ]
            ) +
            p("The biggest variable is air conditioning. If you want to run RV AC from a power station, your power needs jump dramatically. A single AC unit can use 6-12 kWh per day depending on outside temperature and how often it cycles. Without AC, most RVs use 2-5 kWh per day for lights, fridge, devices, and basic appliances.") +
            alert("info", "calculator", "Quick sizing rule", "For boondocking without AC: get a power station with 2-3x your daily usage. This gives you 2-3 days of autonomy without solar. With solar, you can size closer to your daily usage since the sun recharges you each day. For AC use, multiply by 2-4x and plan on significant solar or generator backup.")
        },
        {
            "id": "tt30-explained",
            "title": "TT-30 30A RV Plug Explained",
            "content": p("RV parks typically provide 30A or 50A electrical hookups. The 30A service uses a TT-30 plug, which is the most common type for smaller and medium RVs. Here is what you need to know:") +
            '<div class="grid md:grid-cols-2 gap-6 mb-6">' +
            '<div>' +
            '<h3 class="font-bold text-xl mb-4 text-electric-400 flex items-center gap-2"><i data-lucide="plug" style="width:1.25rem;height:1.25rem"></i>What Is TT-30?</h3>' +
            p("TT-30 (Travel Trailer 30 amp) is a 120V, 30-amp electrical connector standard for RVs. It has a distinctive L-shaped ground pin and two flat blades. The 'TT' stands for Travel Trailer. A 30A service provides up to 3,600 watts total (120V × 30A = 3,600W).") +
            p("Most Class B vans, Class C motorhomes, and travel trailers use 30A service. Larger Class A motorhomes and fifth wheels often use 50A service instead (which is actually 12,000W — two 50A legs at 120V each).") +
            '</div><div>' +
            '<h3 class="font-bold text-xl mb-4 text-green-400 flex items-center gap-2"><i data-lucide="arrow-left-right" style="width:1.25rem;height:1.25rem"></i>Power Station + RV Hookup</h3>' +
            p("When connecting a portable power station to your RV, you have several options: (1) use the power station's regular AC outlets for individual devices, (2) connect via a transfer switch or inverter charger setup, or (3) use a special RV plug adapter if the power station supports it.") +
            p("For the simplest setup, many RVers just plug their most important devices directly into the power station. For whole-RV power, you would typically wire an inverter/charger into your RV's electrical system — which is different from using a portable power station.") +
            "</div></div>" +
            specs_table(
                ["Setup Method", "Difficulty", "Cost", "What It Powers"],
                [
                    ["<strong>Plug devices directly</strong>", "Easy", "$0", "Individual devices (fridge, TV, chargers)"],
                    ["<strong>Transfer switch (manual)</strong>", "Medium", "$100–$300", "Whole RV (selected circuits)"],
                    ["<strong>RV inverter/charger</strong>", "Hard", "$500–$2,000", "Whole RV, auto-switching"],
                    ["<strong>Portable station + adapter</strong>", "Easy", "$20–$50", "Whole RV (within output limit)"],
                ]
            ) +
            alert("warning", "alert-triangle", "Electrical safety note", "RV electrical systems can be dangerous if wired incorrectly. If you are installing a transfer switch or hardwiring anything, hire a certified RV technician or electrician. Never backfeed power into a campground pedestal — that is illegal and can kill line workers.")
        },
        {
            "id": "top-picks",
            "title": "Top Picks by RV Size",
            "content": p("Here are our recommendations for different RV sizes and use cases in 2026. These are based on real-world RV owner feedback, reliability data, and feature sets:") +
            '<div class="space-y-6 mb-6">' +
            '<div class="bg-navy-900/80 border border-white/10 rounded-xl p-6">' +
            '<div class="flex items-center gap-3 mb-4"><div class="px-3 py-1 bg-electric-500/20 text-electric-400 font-mono font-bold text-sm rounded-md border border-electric-500/30">SMALL&nbsp;RV&nbsp;/&nbsp;VAN</div><span class="text-gray-400 text-sm">1,000–2,000Wh</span></div>' +
            '<h3 class="font-bold text-2xl mb-3 text-white">Best for Van Life &amp; Small Campers</h3>' +
            p("<strong>Top Pick: EcoFlow Delta 2 Max (2,048Wh)</strong> — Perfect for Class B vans and small travel trailers. 2,400W AC output handles most appliances except AC. 500W solar input for boondocking. Light enough to move around (50 lbs). Expandable to 6kWh with extra batteries. Great app for monitoring.") +
            p("<strong>Runner-up: Bluetti AC200P (2,000Wh)</strong> — Excellent value, 2,000W output, 700W solar input, tons of ports. Heavier than the EcoFlow but more solar input per dollar. Very popular with van lifers.") +
            p("<strong>Budget Pick: Anker 535 PowerHouse (512Wh)</strong> — If you have very modest needs (just lights, phones, laptop), the 535 is compact, efficient, and has a 5-year warranty. Can be paired with 200W of solar. Not enough for a fridge or microwave.") +
            "</div>" +
            '<div class="bg-navy-900/80 border border-white/10 rounded-xl p-6">' +
            '<div class="flex items-center gap-3 mb-4"><div class="px-3 py-1 bg-green-500/20 text-green-400 font-mono font-bold text-sm rounded-md border border-green-500/30">MEDIUM&nbsp;RV</div><span class="text-gray-400 text-sm">2,000–4,000Wh</span></div>' +
            '<h3 class="font-bold text-2xl mb-3 text-white">Best for Medium Travel Trailers &amp; Class C</h3>' +
            p("<strong>Top Pick: EcoFlow Delta Pro 3 (4,096Wh)</strong> — The gold standard for medium RVs in 2026. 4,000W continuous output, 8,000W surge — runs almost everything except roof AC (and with the RV adapter, some people run soft-start AC). 1,600W solar input charges extremely fast. Expandable to 16kWh. Smart Home Panel compatible for whole-house/RV integration.") +
            p("<strong>Runner-up: Bluetti AC300 + B300 (3,072Wh)</strong> — Modular design, 3,000W output, 2,400W solar input (2x MPPT). Can stack multiple battery modules. Very popular with full-time RVers. Slightly lower output than Delta Pro 3 but more solar input.") +
            p("<strong>Value Pick: Jackery Explorer 2000 Plus (2,042Wh)</strong> — 2,200W output, expandable to 8kWh, very reliable brand, excellent customer support. 1,000W solar input. Great all-around choice if you do not need the absolute maximum output.") +
            "</div>" +
            '<div class="bg-navy-900/80 border border-white/10 rounded-xl p-6">' +
            '<div class="flex items-center gap-3 mb-4"><div class="px-3 py-1 bg-yellow-500/20 text-yellow-400 font-mono font-bold text-sm rounded-md border border-yellow-500/30">LARGE&nbsp;RV&nbsp;/&nbsp;FULL-TIME</div><span class="text-gray-400 text-sm">4,000Wh+</span></div>' +
            '<h3 class="font-bold text-2xl mb-3 text-white">Best for Large RVs &amp; Full-Time Boondocking</h3>' +
            p("<strong>Top Pick: EcoFlow Delta Pro Ultra (7,200Wh)</strong> — The ultimate boondocking machine. 7,200Wh expandable to 72kWh (yes, really). 5,400W continuous output, 10,800W surge — will run almost any RV appliance including multiple AC units with soft start. 3,000W+ solar input capability. Whole home panel integration. This is a serious system for serious RVers.") +
            p("<strong>Runner-up: Bluetti AC500 + B300S (3,072Wh base)</strong> — 5,000W output, 2,400W solar input, expandable to 18,432Wh with 6 battery modules. Split phase 120V/240V available. Very popular with fifth wheel and Class A owners.") +
            p("<strong>Note on RV AC:</strong> Running roof AC from a portable power station is challenging. A typical 13,500 BTU AC draws 1,200-1,800W running but 3,000-5,000W surge. Installing a soft start kit can reduce surge to 1,500-2,000W, making it possible with larger stations. Expect 2-6 hours of AC runtime per 2kWh of battery depending on temperature.") +
            "</div>" +
            "</div>" +
            alert("info", "lightbulb", "Pro tip for sizing", "If you are unsure, size up. It is better to have too much capacity than too little. Many RVers start with 2kWh and end up adding more batteries within a year. With expandable models, you can start with one battery and add more later — which spreads out the cost.")
        },
        {
            "id": "solar-for-rv",
            "title": "Solar for RVs — How Much Do You Need?",
            "content": p("For boondocking, solar is essential. It lets you recharge your power station during the day, extending your off-grid time indefinitely (as long as the sun shines). Here is how to figure out how much solar you need:") +
            step_grid([
                {"title": "Calculate Your Daily Usage", "desc": "Add up all the watt-hours you use per day. For most RVers without AC, this is 2-5 kWh per day. With AC, it is 8-20+ kWh per day. You can measure this with a watt meter or by checking your battery discharge over a typical day."},
                {"title": "Account for Solar Efficiency", "desc": "Solar panels produce their rated wattage only in perfect conditions (full sun, panel pointed directly at the sun, cool temperature). In real RV use, expect 70-85% of rated output on average. A 400W panel system typically produces 1.6-2.6 kWh per day in good sun."},
                {"title": "Peak Sun Hours", "desc": "Most locations get 3-6 peak sun hours per day (the equivalent hours of full 1,000W/m² sunlight). Arizona and desert areas get 6+, the Pacific Northwest gets 2-4 in winter, most of the US gets 4-5 average. Use this to calculate total daily production."},
                {"title": "The 1:1 Rule for Quick Estimating", "desc": "As a quick rule of thumb: 100W of solar ≈ 0.3-0.5 kWh per day (in good conditions). So if you use 3 kWh/day, you need 600-1,000W of solar to fully recharge each day. For cloudy days, winter, or if you park in shade, double that."},
            ], "yellow") +
            specs_table(
                ["Solar Array Size", "Daily Production (good sun)", "What It Powers"],
                [
                    ["<strong>200W</strong>", "0.6–1.0 kWh/day", "Phones, laptops, LED lights, small devices"],
                    ["<strong>400W</strong>", "1.2–2.0 kWh/day", "Above + 12V fridge, water pump, TV"],
                    ["<strong>800W</strong>", "2.4–4.0 kWh/day", "Medium RV full-time boondocking (no AC)"],
                    ["<strong>1,200W</strong>", "3.6–6.0 kWh/day", "Comfortable boondocking, microwave, coffee maker"],
                    ["<strong>2,000W+</strong>", "6–10 kWh/day", "Large RV, some AC use, all appliances"],
                ]
            ) +
            p("Mounting options for RV solar: roof-mounted (permanent, best for full-timers), portable panels (cheaper, flexible, can be angled), or a mix. Roof-mounted is convenient but fixed angle — portable panels let you chase the sun and park in shade while the panels are in sun.") +
            alert("info", "sun", "Solar MPPT tip", "Make sure your power station has MPPT (Maximum Power Point Tracking) charge controllers — all modern ones do. MPPT is 20-30% more efficient than the old PWM technology. Some premium stations have dual MPPT, meaning you can point two arrays in different directions for better production."),
        },
        {
            "id": "hookups-vs-boondocking",
            "title": "Campground Hookups vs Boondocking",
            "content": p("Portable power stations serve different roles depending on whether you are at a campground with full hookups or boondocking off-grid. Here is how to think about each scenario:") +
            '<div class="grid md:grid-cols-2 gap-6">' +
            '<div class="bg-navy-900/80 border border-white/10 rounded-xl p-6">' +
            '<h3 class="font-bold text-2xl mb-4 text-green-400">At Campgrounds with Hookups</h3>' +
            p("When you have 30A or 50A service, a power station still adds value:") +
            '<ul class="space-y-2 text-sm text-gray-300">' +
            '<li>• <strong class="text-white">Power conditioning:</strong> Some campgrounds have dirty or fluctuating power — a power station with UPS mode protects your sensitive electronics.</li>' +
            '<li>• <strong class="text-white">Peak shaving:</strong> If the pedestal is old and trips easily, you can use the power station to supplement during high-demand moments (microwave + AC + hair dryer all at once).</li>' +
            '<li>• <strong class="text-white">Backup for outages:</strong> Campground power sometimes goes out. With a power station, you keep the fridge and lights on.</li>' +
            '<li>• <strong class="text-white">Quiet hours:</strong> Run essentials from battery during quiet hours without using the generator.</li>' +
            '</ul></div>' +
            '<div class="bg-navy-900/80 border border-white/10 rounded-xl p-6">' +
            '<h3 class="font-bold text-2xl mb-4 text-electric-400">Boondocking / Dry Camping</h3>' +
            p("Off-grid is where power stations truly shine. Here is what you need:") +
            '<ul class="space-y-2 text-sm text-gray-300">' +
            '<li>• <strong class="text-white">Enough capacity for 2-3 days:</strong> So you can survive cloudy days and not worry about solar.</li>' +
            '<li>• <strong class="text-white">Solar for indefinite stays:</strong> Match your solar to your daily usage for indefinite off-grid time.</li>' +
            '<li>• <strong class="text-white">Generator backup (optional):</strong> For extended cloudy periods, a small generator can top up the battery. Much more efficient than running the generator 24/7.</li>' +
            '<li>• <strong class="text-white">Conservation habits:</strong> LED lights, efficient fridge, gas for cooking, and awareness of what you plug in make a huge difference in how long you last.</li>' +
            '</ul></div></div>' +
            p("Many RVers use a hybrid approach: stay at campgrounds with hookups 50-70% of the time, boondock 30-50% of the time. A portable power station makes both experiences better — it is not just for off-grid use.") +
            alert("warning", "clock", "Generator + power station pairing", "If you have a generator, you do not need to run it all day. Run it for 1-2 hours at a time to fast-charge your power station, then turn it off and run everything from the battery. This is quieter, uses less fuel, and is easier on the generator than running it constantly at low load.")
        },
        {
            "id": "installation-tips",
            "title": "RV Installation &amp; Setup Tips",
            "content": p("Setting up a portable power station in your RV is usually straightforward, but there are some best practices to follow for safety and convenience:") +
            '<div class="space-y-4">' +
            step_grid([
                {"title": "Choose the Right Location", "desc": "Place the power station in a well-ventilated area, away from direct sunlight and heat sources. It should be level and secured so it does not slide around while driving. Good locations: under a dinette seat, in a storage bay with ventilation, or on the floor secured with bungee cords. Never block the air vents."},
                {"title": "Ventilation Is Critical", "desc": "Power stations produce heat during charging and high-output use. They need airflow to cool properly. Do not enclose them in a sealed cabinet. If you put one in a storage compartment, add vent fans or leave the door partially open during heavy use. Overheating reduces battery life and can trigger safety shutdowns."},
                {"title": "Use the Right Cables", "desc": "For AC connections, use heavy-duty extension cords rated for the wattage. 14-gauge for up to 15A, 12-gauge for up to 20A, 10-gauge for 30A. Keep cables as short as possible. For solar, use properly sized PV wire — voltage drop is less of an issue with higher voltage solar arrays, but current capacity still matters."},
                {"title": "Grounding and Safety", "desc": "Most portable power stations have a floating neutral, which is fine for most RV use. However, some RV appliances and surge protectors may complain about 'open ground' or 'reverse polarity.' You may need a ground-neutral bond plug for compatibility. Always have working smoke and carbon monoxide detectors in your RV."},
                {"title": "Monitoring and Alerts", "desc": "Install the manufacturer's app on your phone so you can monitor battery level, input/output, and receive alerts. This is especially useful at night — you can check the battery without getting out of bed. Set up low-battery alerts so you know when it is time to start the generator or reduce usage."},
                {"title": "Winter Considerations", "desc": "Lithium batteries lose capacity in cold weather and should not be charged below freezing. If you camp in winter, keep the power station inside the heated living space of the RV if possible. Some premium models have low-temperature charging protection that automatically stops charging when it is too cold."},
            ], "purple") + "</div>" +
            alert("critical", "alert-octagon", "Critical safety reminder", "Never run a generator inside your RV or in an enclosed space — carbon monoxide poisoning kills campers every year. Generators must be outside, at least 10 feet from the RV, with the exhaust pointed away. Same with propane heaters — use RV-rated devices and always have a working CO detector.")
        },
        {
            "id": "common-mistakes",
            "title": "Common RV Power Mistakes to Avoid",
            "content": p("After talking to hundreds of RVers, these are the most common mistakes people make with their first portable power station:") +
            '<div class="space-y-4">' +
            step_grid([
                {"title": "Buying Too Small", "desc": "The #1 mistake. People underestimate their power usage and end up disappointed. 'I just need to charge my phone and run a light' quickly becomes running the fridge, TV, microwave, and coffee maker. Size bigger than you think you need. You can always use less power, but you cannot create capacity you do not have."},
                {"title": "Ignoring Solar Needs", "desc": "Buying a big battery without enough solar is like buying a big water tank with no hose to refill it. For boondocking, solar is essential. Plan for at least 200W of solar per 1kWh of battery if you want to stay off-grid indefinitely. More is better."},
                {"title": "Running Too Many Things at Once", "desc": "It is easy to overload the inverter. The microwave + coffee maker + hair dryer + AC all at once will trip even large inverters. Be mindful of what is running. Stagger high-wattage usage. Most stations will just shut off on overload (no damage), but it is annoying and you lose power momentarily."},
                {"title": "Forgetting About Surge Watts", "desc": "Appliances with motors (fridge compressor, AC, furnace blower) draw 2-3x their running wattage when they start up. This is called surge or starting watts. Make sure your power station's surge rating is higher than the surge draw of all devices that might start at once. This is the #1 cause of 'why does my power station trip when the fridge starts?'"},
                {"title": "Poor Cable Management", "desc": "Long, thin extension cords cause voltage drop and reduce effective output. They can also be trip hazards. Use the shortest, thickest cords you can. Keep cable runs organized. Do not run cords under rugs or through door frames where they can get damaged."},
                {"title": "Not Testing Before the Trip", "desc": "Never show up to a campsite with a power station you have never tested. Do a full test run at home: charge it fully, plug in your devices, see how long it lasts, test the solar, learn the app. You do not want to figure out that something does not work when you are already off-grid."},
            ], "red") + "</div>"
        },
    ],
    "faqs": [
        {"q": "What size portable power station do I need for my RV?", "a": "For small vans and minimal use: 1,000-2,000Wh. For medium RVs with fridge, lights, devices, and occasional microwave: 2,000-4,000Wh. For large RVs, full-time boondocking, or running AC: 4,000Wh+ with expandable capacity. The most popular size for serious RVers is 2,000-4,000Wh with 400-800W of solar input. Always size bigger than you think you need."},
        {"q": "Can a portable power station run an RV air conditioner?", "a": "Larger power stations (3,000W+ output) can run RV AC, especially with a soft start kit installed on the AC unit. A 13,500 BTU AC draws 1,200-1,800W running but 3,000-5,000W surge — the surge is the hard part. Soft start kits reduce surge to 1,500-2,000W. Runtime depends on outside temperature: expect 2-6 hours of AC per 2kWh of battery. For all-day AC, you need significant solar or a generator."},
        {"q": "What is the difference between 30A and 50A RV service?", "a": "30A RV service is 120V on a single circuit, providing up to 3,600W total. 50A service has two separate 120V legs at 50A each, providing 12,000W total (6,000W per leg). Most small and medium RVs use 30A, while large Class A and fifth wheels use 50A. A portable power station supplements or replaces this service when boondocking."},
        {"q": "How much solar do I need for my RV?", "a": "As a rule of thumb: 200W for minimal device charging, 400W for basic off-grid living (lights, fridge, devices), 800-1,200W for comfortable boondocking with all appliances (no AC), and 2,000W+ for large RVs or partial AC use. Actual production depends on location, weather, panel angle, and shading. Expect 3-6 peak sun hours per day in most places."},
        {"q": "Which is better for RV: generator or power station?", "a": "It is not an either/or — many RVers use both. Power stations are quiet, produce no fumes, require no fuel, and need almost no maintenance. Generators can produce unlimited power (as long as you have fuel) but are noisy, smelly, require maintenance, and use gas. The best setup: power station as your primary power source, solar for daytime recharging, and a small generator as backup for cloudy days or high-demand periods."},
        {"q": "How do I connect a portable power station to my RV?", "a": "The simplest way: plug individual devices directly into the power station's AC outlets. For whole-RV power, you can use a transfer switch (manual or automatic) that switches between shore power and battery power. Some RVers use an inverter charger hardwired into the RV's electrical system, which is different from a portable station. Always hire a professional for electrical work."},
        {"q": "Can I charge my power station while driving?", "a": "Yes! Many RVers charge their portable power station from the vehicle's alternator while driving. You need a DC-DC charger or a 12V car charging cable that supports the right current. This is a great way to top up the battery while traveling between campsites. The charge rate depends on your alternator and the DC-DC charger — typically 10-50A at 12V."},
        {"q": "How long do RV power station batteries last?", "a": "LiFePO4 (LFP) power stations last 3,000-6,000 cycles, which is 5-10 years for typical RV use. If you cycle the battery once per day (full boondocking every day), expect 5-8 years. If you only use it on weekends, it could last 10+ years. Good care (avoiding extreme temperatures, not discharging fully, storing at 50%) extends life significantly."},
        {"q": "What is the best power station for van life?", "a": "For van life, the EcoFlow Delta 2 Max (2,048Wh) is the most popular choice in 2026 — it has a good balance of capacity, output (2,400W), solar input (500W), and size/weight (50 lbs). The Bluetti AC200P is another great option with more solar input (700W) at a lower price but slightly heavier. For minimalists, the Anker 535 is compact and efficient."},
        {"q": "Are portable power stations safe inside an RV?", "a": "Yes, modern portable power stations with LFP batteries are generally safe inside an RV when used correctly. They have built-in BMS (Battery Management System) protection against overcharge, over-discharge, over-temperature, and short circuits. However, you should always: keep them ventilated, do not block vents, avoid placing them near heat sources, have working smoke/CO detectors, and never leave them charging unattended for long periods."},
    ],
    "related": [
        {"href": "ecoflow-delta-pro-3.html", "badge": "SPEC&nbsp;SHEET", "badge_class": "bg-electric-500/20 text-electric-400", "border_class": "border-electric-500/30", "badge2": "EcoFlow", "title": "EcoFlow Delta Pro 3 Specs", "desc": "Full specifications for the EcoFlow Delta Pro 3 — 4,096Wh LFP, 4,000W inverter, 1,600W solar input."},
        {"href": "jackery-explorer-2000-plus.html", "badge": "SPEC&nbsp;SHEET", "badge_class": "bg-yellow-500/20 text-yellow-400", "border_class": "border-yellow-500/30", "badge2": "Jackery", "title": "Jackery Explorer 2000 Plus", "desc": "Full specs for the Jackery Explorer 2000 Plus — 2,042Wh LFP, 2,200W output, expandable to 8kWh."},
        {"href": "bluetti-ac200max.html", "badge": "SPEC&nbsp;SHEET", "badge_class": "bg-blue-500/20 text-blue-400", "border_class": "border-blue-500/30", "badge2": "Bluetti", "title": "Bluetti AC200MAX Specs", "desc": "Complete specifications for the Bluetti AC200MAX — 2,048Wh LFP, 2,200W inverter, 900W solar."},
        {"href": "off-grid-solar-system-sizing-guide.html", "badge": "SOLAR&nbsp;SIZING", "badge_class": "bg-orange-500/20 text-orange-400", "border_class": "border-orange-500/30", "badge2": "Guide", "title": "Solar Sizing Guide", "desc": "How to size an off-grid solar system — calculate your load, panel needs, battery bank, and inverter size."},
        {"href": "portable-power-station-for-tailgating.html", "badge": "TAILGATING", "badge_class": "bg-purple-500/20 text-purple-400", "border_class": "border-purple-500/30", "badge2": "Guide", "title": "Tailgating Power Guide", "desc": "Best portable power stations for tailgating — powering TVs, speakers, grills, and outdoor events."},
        {"href": "outdoor-power.html", "badge": "ALL&nbsp;MODELS", "badge_class": "bg-electric-500/20 text-electric-400", "border_class": "border-electric-500/30", "badge2": "Category", "title": "Outdoor Power Hub", "desc": "Browse all portable power station guides, comparisons, specs, and troubleshooting resources in one place."},
    ],
})

print("Generating pages...")

# Generate all pages
os.makedirs(OUTPUT_DIR, exist_ok=True)

for page in PAGES:
    filepath = os.path.join(OUTPUT_DIR, page["filename"])
    html_content = build_page(page)
    with open(filepath, "w") as f:
        f.write(html_content)
    # Count words
    import re
    text = re.sub(r'<[^>]+>', ' ', html_content)
    words = text.split()
    print(f"  Created: {page['filename']}  ({len(words)} words)")

print(f"\nTotal pages created: {len(PAGES)}")
