#!/usr/bin/env python3
"""
Final script to generate all 20 SEO pages for TechSpecsHub.
Each page: 3000+ words, full SEO, matching eco-mode template exactly.
"""

import os
import json
import html
import re
from typing import List, Dict, Any

OUTPUT_DIR = "/workspace/pages/specs"
BASE_URL = "https://powerspecshub.com/pages/specs"
SITE_NAME = "TechSpecsHub"
UPDATED_DATE = "2026-06-25"


# ===================== HELPER FUNCTIONS =====================

def p(text: str) -> str:
    return f'<p class="text-gray-300 leading-relaxed mb-4">{text}</p>'

def ul(items: List[str]) -> str:
    lis = "".join([f"<li>• {item}</li>" for item in items])
    return f'<ul class="text-sm text-gray-300 space-y-1 mb-4">{lis}</ul>'

def table(headers: List[str], rows: List[List[str]]) -> str:
    thead = "".join([f"<th>{h}</th>" for h in headers])
    tbody = ""
    for row in rows:
        tbody += "<tr>" + "".join([f"<td>{cell}</td>" for cell in row]) + "</tr>"
    return f'''<div class="overflow-x-auto mb-6">
        <table class="specs-table w-full text-sm">
          <thead><tr>{thead}</tr></thead>
          <tbody>{tbody}</tbody>
        </table></div>'''

def alert(alert_type: str, text: str, icon: str = None) -> str:
    icon_map = {"info": "lightbulb", "warning": "alert-triangle", "critical": "alert-octagon", "success": "check-circle"}
    icon_name = icon or icon_map.get(alert_type, "info")
    return f'''<div class="mt-4 alert alert-{alert_type}">
        <i data-lucide="{icon_name}" style="width:1rem;height:1rem;flex-shrink:0;margin-top:0.1rem"></i>
        <p class="text-sm"><strong>{text.split(":",1)[0] if ":" in text else ""}</strong>{(":"+text.split(":",1)[1]) if ":" in text else text}</p>
      </div>'''

def grid_cards(cards: List[Dict], cols: int = 2) -> str:
    html_cards = ""
    for card in cards:
        tc = card.get("title_color", "electric-400")
        html_cards += f'''<div class="bg-navy-900/80 border border-white/10 rounded-xl p-5">
          <h4 class="font-semibold text-{tc} mb-2">{card["title"]}</h4>
          <p class="text-sm text-gray-300 mb-2">{card["body"]}</p>
        </div>'''
    return f'<div class="grid md:grid-cols-{cols} gap-4 mb-4">{html_cards}</div>'

def numbered_steps(steps: List[Dict], color: str = "green") -> str:
    html_steps = ""
    for i, s in enumerate(steps, 1):
        html_steps += f'''<div class="flex items-start gap-3">
          <div class="w-10 h-10 bg-{color}-500/20 rounded-full flex items-center justify-center flex-shrink-0">
            <span class="font-mono font-bold text-{color}-400">{i}</span>
          </div>
          <div>
            <h4 class="font-semibold text-white">{s["title"]}</h4>
            <p class="text-sm text-gray-400">{s["body"]}</p>
          </div>
        </div>'''
    return f'<div class="space-y-4 mb-6">{html_steps}</div>'

def pros_cons(pros: List[str], cons: List[str]) -> str:
    pros_html = "".join([f'<li class="flex items-start gap-2"><i data-lucide="check" style="width:1rem;height:1rem;color:#4ade80;flex-shrink:0;margin-top:0.1rem"></i><span>{x}</span></li>' for x in pros])
    cons_html = "".join([f'<li class="flex items-start gap-2"><i data-lucide="x" style="width:1rem;height:1rem;color:#f87171;flex-shrink:0;margin-top:0.1rem"></i><span>{x}</span></li>' for x in cons])
    return f'''<div class="grid md:grid-cols-2 gap-6 mb-4">
        <div><h3 class="font-bold text-xl mb-4 text-green-400 flex items-center gap-2"><i data-lucide="check-circle" style="width:1.25rem;height:1.25rem"></i>Pros</h3>
          <ul class="space-y-3 text-sm text-gray-300">{pros_html}</ul></div>
        <div><h3 class="font-bold text-xl mb-4 text-red-400 flex items-center gap-2"><i data-lucide="x-circle" style="width:1.25rem;height:1.25rem"></i>Cons</h3>
          <ul class="space-y-3 text-sm text-gray-300">{cons_html}</ul></div></div>'''

def section(sec_id: str, title: str, content_parts: List[str]) -> str:
    content = "\n".join(content_parts)
    return f'''  <section id="{sec_id}" class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <h2 class="font-bold text-3xl mb-5">{title}</h2>
    <div class="glass-card p-6 md:p-8">
      {content}
    </div>
  </section>'''


# ===================== FULL PAGE TEMPLATE =====================

def build_full_page(page: Dict) -> str:
    """Build a complete HTML page from page data."""

    # JSON-LD
    article_json = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": page["headline"],
        "description": page["meta_desc"],
        "url": f"{BASE_URL}/{page['filename']}",
        "datePublished": UPDATED_DATE,
        "dateModified": UPDATED_DATE,
        "author": {"@type": "Organization", "name": SITE_NAME},
        "publisher": {"@type": "Organization", "name": SITE_NAME, "url": "https://powerspecshub.com/"},
        "image": {"@type": "ImageObject", "url": "https://powerspecshub.com/assets/images/og-default.png"}
    }

    faq_json = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": f["question"], "acceptedAnswer": {"@type": "Answer", "text": f["answer"]}} for f in page["faqs"]]
    }

    bc_url = f"{BASE_URL}/{page['category_url']}"
    breadcrumb_json = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://powerspecshub.com/"},
            {"@type": "ListItem", "position": 2, "name": page["category"], "item": bc_url},
            {"@type": "ListItem", "position": 3, "name": page["breadcrumb_name"]}
        ]
    }

    # Head
    head = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(page['title'])} | {SITE_NAME}</title>
  <meta name="description" content="{html.escape(page['meta_desc'])}">
  <meta name="theme-color" content="#0a1628">
  <style>html,body{{background-color:#0a1628;color:#ffffff;margin:0;padding:0;min-height:100vh;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;line-height:1.5;-webkit-font-smoothing:antialiased}}a{{color:#22d3ee;text-decoration:none}}code,pre{{font-family:ui-monospace,monospace}}</style>

  <link rel="preconnect" href="https://cdn.tailwindcss.com">
  <link rel="preconnect" href="https://unpkg.com">
  <link rel="dns-prefetch" href="https://cdn.tailwindcss.com">
  <link rel="dns-prefetch" href="https://unpkg.com">
  <link rel="dns-prefetch" href="https://fonts.gstatic.com">

  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <link rel="canonical" href="{BASE_URL}/{page['filename']}">

  <meta property="og:title" content="{html.escape(page['title'])} | {SITE_NAME}">
  <meta property="og:description" content="{html.escape(page['meta_desc'])}">
  <meta property="og:type" content="Article">
  <meta property="og:url" content="{BASE_URL}/{page['filename']}">
  <meta property="og:image" content="https://powerspecshub.com/assets/images/og-default.png">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="article:published_time" content="{UPDATED_DATE}T00:00:00Z">
  <meta property="article:modified_time" content="{UPDATED_DATE}T00:00:00Z">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(page['title'])} | {SITE_NAME}">
  <meta name="twitter:description" content="{html.escape(page['meta_desc'])}">
  <meta name="twitter:image" content="https://powerspecshub.com/assets/images/og-default.png">
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

    # Body header (navigation)
    body_header = '''<body class="bg-navy-950 text-white min-h-screen font-display">

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

    # Breadcrumb
    breadcrumb = f'''  <!-- BREADCRUMB -->
  <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 pb-4">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="../../index.html">Home</a>
      <span class="breadcrumb-sep">/</span>
      <a href="{page['category_url']}">{page['category']}</a>
      <span class="breadcrumb-sep">/</span>
      <span class="breadcrumb-current">{page['breadcrumb_name']}</span>
    </nav>
  </div>
'''

    # Hero badges
    badges_html = ""
    for b in page["badges"]:
        badges_html += f'<span class="badge badge-{b["color"]}"><i data-lucide="{b["icon"]}" style="width:0.75rem;height:0.75rem"></i>{b["text"]}</span>\n        '

    # Hero stats
    stats_html = ""
    for s in page["hero_stats"]:
        stats_html += f'''        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="{s['icon']}" style="width:0.9rem;height:0.9rem"></i>{s['label']}</div>
          <div class="font-mono font-bold text-xl text-{s['value_color']}">{s['value']}</div>
        </div>
'''

    hero = f'''  <!-- HERO -->
  <section class="relative max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-4 pb-6">
    <div class="glass-card p-8 md:p-10 overflow-hidden relative">
      <div class="absolute top-0 right-0 w-[420px] h-[420px] bg-{page['accent_color']}-500/5 rounded-full blur-3xl pointer-events-none"></div>

      <div class="relative flex flex-wrap items-center gap-3 mb-5">
        {badges_html.strip()}
      </div>

      <h1 class="font-bold text-4xl md:text-5xl mb-4 leading-tight">
        {page['hero_title']} &mdash; <span class="gradient-text">Complete 2026 Guide</span>
      </h1>

      <p class="text-gray-400 text-lg leading-relaxed mb-6 max-w-3xl">
        {page['hero_intro']}
      </p>

      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8">
{stats_html.rstrip()}
      </div>
    </div>
  </section>
'''

    # Quick answer
    quick_answer = f'''  <!-- QUICK ANSWER -->
  <section class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div class="glass-card p-6 md:p-8 bg-gradient-to-br from-{page['accent_color']}-950/20 to-navy-900 border-{page['accent_color']}-500/20">
      <h2 class="font-bold text-2xl mb-4 flex items-center gap-2"><i data-lucide="zap" style="width:1.25rem;height:1.25rem;color:#4ade80"></i>Quick Answer</h2>
      <p class="text-gray-300 leading-relaxed mb-4">
        {page['quick_answer']}
      </p>
    </div>
  </section>
'''

    # Table of contents
    toc_items = ""
    for i, toc in enumerate(page["toc"], 1):
        num = f"{i:02d}"
        toc_items += f'        <a href="#{toc["id"]}" class="flex items-center gap-2 p-2 rounded-lg hover:bg-white/5 text-gray-300 hover:text-white transition-all"><span class="text-electric-400 font-mono">{num}</span>{toc["title"]}</a>\n'

    toc_section = f'''  <!-- TABLE OF CONTENTS -->
  <section class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div class="glass-card p-6 md:p-8">
      <h2 class="font-bold text-2xl mb-4 flex items-center gap-2"><i data-lucide="list" style="width:1.25rem;height:1.25rem;color:#22d3ee"></i>Table of Contents</h2>
      <div class="grid md:grid-cols-2 gap-2 text-sm">
{toc_items.rstrip()}
      </div>
    </div>
  </section>
'''

    # Content sections
    content_sections = ""
    for sec in page["sections"]:
        content = "\n".join(sec["parts"])
        content_sections += f'''  <section id="{sec["id"]}" class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <h2 class="font-bold text-3xl mb-5">{sec["title"]}</h2>
    <div class="glass-card p-6 md:p-8">
      {content}
    </div>
  </section>
'''

    # FAQ
    faq_items = ""
    for f in page["faqs"]:
        faq_items += f'''      <details class="glass-card p-5 group">
        <summary class="cursor-pointer font-semibold flex items-center justify-between gap-4">
          <span>{f["question"]}</span>
          <i data-lucide="chevron-down" style="width:1rem;height:1rem" class="text-gray-500 group-open:rotate-180 transition-transform flex-shrink-0"></i>
        </summary>
        <p class="mt-3 text-gray-400 text-sm leading-relaxed">
          {f["answer"]}
        </p>
      </details>
'''

    faq_section = f'''  <!-- FAQ -->
  <section id="faq" class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="text-center mb-10">
      <h2 class="font-bold text-3xl md:text-4xl mb-4">Frequently Asked Questions</h2>
      <p class="text-gray-400">Common questions about this topic.</p>
    </div>
    <div class="space-y-3">
{faq_items.rstrip()}
    </div>
  </section>
'''

    # Related guides
    related_html = ""
    for r in page["related"]:
        bc = r.get("badge_color", "electric")
        bt = r.get("badge_text", "GUIDE")
        sb = r.get("sub_badge", "All Brands")
        related_html += f'''      <a href="{r["url"]}" class="glass-card p-6 block hover:border-electric-400/50 transition-all group">
        <div class="flex items-start gap-3 mb-3">
          <div class="px-2.5 py-1 bg-{bc}-500/20 text-{bc}-400 font-mono font-semibold text-sm rounded-md border border-{bc}-500/30">{bt}</div>
          <span class="badge badge-info">{sb}</span>
        </div>
        <h3 class="font-bold text-lg mb-2 group-hover:text-electric-400 transition-colors">{r["title"]}</h3>
        <p class="text-sm text-gray-400">{r["desc"]}</p>
      </a>
'''

    related_section = f'''  <!-- RELATED GUIDES -->
  <section id="related" class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h2 class="font-bold text-3xl mb-5">Related Guides &amp; Resources</h2>
    <div class="grid md:grid-cols-3 gap-4">
{related_html.rstrip()}
    </div>
  </section>
'''

    # Footer
    footer = '''  <!-- FOOTER -->
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

    return head + body_header + breadcrumb + hero + quick_answer + toc_section + content_sections + faq_section + related_section + footer


def count_words(html_text: str) -> int:
    """Rough word count by stripping HTML tags."""
    text = re.sub(r'<[^>]+>', ' ', html_text)
    text = re.sub(r'\s+', ' ', text)
    return len(text.split())


# ===================== PAGE GENERATION =====================

def generate_page_2():
    """Battery Replacement Cost"""
    return {
        "filename": "portable-power-station-battery-replacement-cost.html",
        "title": "Portable Power Station Battery Replacement Cost & Options (2026)",
        "meta_desc": "Complete guide to portable power station battery replacement costs by brand (EcoFlow, Jackery, Bluetti, Anker). DIY vs professional, warranty coverage, signs you need a replacement, and how to extend battery life.",
        "headline": "Portable Power Station Battery Replacement Cost & Options (2026)",
        "hero_title": "Portable Power Station Battery Replacement Cost & Options",
        "breadcrumb_name": "Battery Replacement Cost",
        "category": "Outdoor Power",
        "category_url": "outdoor-power.html",
        "accent_color": "yellow",
        "badges": [
            {"icon": "dollar-sign", "text": "COST GUIDE", "color": "yellow"},
            {"icon": "battery", "text": "Battery Care", "color": "info"},
            {"icon": "layers", "text": "All Brands", "color": "info"},
        ],
        "hero_intro": "Battery replacement is one of the most important — and most expensive — considerations when buying a portable power station. The battery is the heart of the unit, and eventually, every battery will degrade and need to be replaced. Understanding replacement costs, whether your model even supports replacement, and how to extend battery life can save you hundreds of dollars over the long run. This guide breaks down replacement costs by brand, DIY vs professional options, warranty coverage, and clear signs that your battery needs attention.",
        "hero_stats": [
            {"icon": "dollar-sign", "label": "Avg Replacement", "value": "$300–$1,500", "value_color": "yellow-400"},
            {"icon": "battery-charging", "label": "Cycle Life", "value": "500–6,000", "value_color": "green-400"},
            {"icon": "clock", "label": "Typical Lifespan", "value": "3–10 yrs", "value_color": "electric-400"},
            {"icon": "wrench", "label": "DIY Possible?", "value": "Sometimes", "value_color": "white"},
        ],
        "quick_answer": "Battery replacement costs for portable power stations range from $300 for small 500Wh units to $1,500+ for large 3,000Wh+ models. Whether you can replace the battery yourself depends on the brand and model — some are designed for easy user replacement, while others require professional service or cannot be replaced at all. Most brands offer 2-5 year warranties that cover battery defects, but normal wear and tear is usually not covered. To maximize battery life, use LiFePO4 chemistry, avoid extreme temperatures, and keep the battery at 50-80% charge for long-term storage.",
        "toc": [
            {"id": "cost-by-brand", "title": "Replacement Cost by Brand & Model"},
            {"id": "is-it-worth-it", "title": "Is Battery Replacement Worth It?"},
            {"id": "diy-vs-pro", "title": "DIY vs Professional Replacement"},
            {"id": "warranty", "title": "Warranty Coverage & What It Includes"},
            {"id": "signs", "title": "Signs Your Battery Needs Replacement"},
            {"id": "extend-life", "title": "How to Extend Battery Life"},
            {"id": "battery-types", "title": "Battery Chemistry Comparison"},
            {"id": "buying-tips", "title": "Buying Tips: Replace vs New Station"},
            {"id": "pro-tips", "title": "Pro Tips & Best Practices"},
            {"id": "faq", "title": "Frequently Asked Questions"},
            {"id": "related", "title": "Related Guides"},
        ],
        "sections": [
            {
                "id": "cost-by-brand", "title": "Battery Replacement Cost by Brand & Model",
                "parts": [
                    p("Battery replacement costs vary dramatically depending on the brand, model, and battery capacity. In general, you can expect to pay 40-70% of the original purchase price for a replacement battery. This is because the battery is the single most expensive component in a portable power station."),
                    p("Here is a breakdown of estimated replacement costs for popular brands and models as of 2026:"),
                    table(["Brand / Model", "Capacity", "Est. Replacement Cost", "User-Replaceable?"], [
                        ["EcoFlow Delta 2", "1,024Wh LFP", "$400–$550", "Yes (official module)"],
                        ["EcoFlow Delta Pro 3", "4,096Wh LFP", "$1,200–$1,800", "Yes (modular)"],
                        ["Jackery Explorer 1000 v2", "1,070Wh Li-ion", "$450–$650", "Limited / service only"],
                        ["Jackery Explorer 2000 Plus", "2,042Wh Li-ion", "$800–$1,100", "Yes (add-on packs)"],
                        ["Bluetti AC200MAX", "2,048Wh LFP", "$700–$1,000", "Yes (expansion packs)"],
                        ["Bluetti AC500", "5,120Wh LFP", "$1,500–$2,200", "Yes (modular B300S)"],
                        ["Anker 535 PowerHouse", "512Wh LFP", "$250–$400", "No (sealed unit)"],
                        ["Anker 757 PowerHouse", "1,229Wh LFP", "$500–$750", "No (sealed unit)"],
                        ["Goal Zero Yeti 1500X", "1,516Wh Li-ion", "$700–$1,000", "Service center only"],
                        ["Generac GB1000", "1,086Wh LFP", "$450–$650", "No (sealed unit)"],
                    ]),
                    p("Important note: Prices are estimates based on 2026 market data and can vary. Always check the manufacturer's website or contact support for current pricing and availability. Some brands discontinue battery packs for older models, so availability is not guaranteed for units older than 3-5 years."),
                    alert("info", "Pro tip: Modular power stations with swappable battery packs (EcoFlow Delta Pro, Bluetti AC500, Jackery Explorer Plus series) are the most cost-effective long-term. Instead of replacing the entire unit, you just swap in a new battery module. This also lets you expand capacity as your needs grow."),
                ]
            },
            {
                "id": "is-it-worth-it", "title": "Is Battery Replacement Worth It?",
                "parts": [
                    p("Whether replacing the battery is worth it depends on several factors: the age of the unit, the cost of replacement vs. buying new, whether the rest of the unit is in good shape, and whether replacement parts are even available. Here is a framework to help you decide:"),
                    grid_cards([
                        {"title": "Replacement Makes Sense When...", "title_color": "green-400", "body": "The unit is less than 5 years old, replacement costs less than 60% of a new comparable unit, the inverter/electronics are still working well, and you like the model's features and performance. Modular units with expansion batteries are almost always worth keeping."},
                        {"title": "Buy New When...", "title_color": "red-400", "body": "The unit is 7+ years old, replacement costs more than 70% of a new unit, newer models have significantly better features (faster charging, more ports, better app), or the unit has other issues (inverter problems, display failure, etc.). Technology improves quickly — a new $1,000 station today may outperform a $2,000 unit from 5 years ago."},
                    ]),
                    p("One important consideration is technology advancement. Portable power station technology has improved rapidly since 2020. LiFePO4 chemistry has become standard, charging speeds have doubled or tripled, and features like app control, UPS mode, and smart home integration are now common. If your station is from the pre-LFP era (before ~2021), upgrading to a new model with LFP batteries and modern features may be more cost-effective than replacing the old battery."),
                    p("Another factor is warranty. If your battery failed prematurely and is still under warranty, get it replaced under warranty — that is always worth it. The question only applies to out-of-warranty batteries that have reached end-of-life through normal use."),
                ]
            },
            {
                "id": "diy-vs-pro", "title": "DIY vs Professional Battery Replacement",
                "parts": [
                    p("Some power stations are designed for user-replaceable batteries, while others are sealed units that require professional service or cannot be serviced at all. Here is what you need to know about each approach:"),
                    numbered_steps([
                        {"title": "Official Modular Replacement (Best Option)", "body": "Many modern stations use modular battery packs that you can swap without tools. EcoFlow Delta series, Bluetti AC series with expansion packs, and Jackery Explorer Plus series all support this. Just buy the official battery module and slot it in. This preserves warranty and is the safest option."},
                        {"title": "DIY Battery Pack Build", "body": "Some hobbyists build their own replacement battery packs using 18650 or 21700 cells and a BMS (Battery Management System). This is cheaper but voids warranty, requires technical knowledge, and can be dangerous if done wrong. Only attempt this if you understand high-voltage DC safety and have experience with lithium batteries."},
                        {"title": "Authorized Service Center", "body": "Most brands offer battery replacement through authorized service centers. Cost is higher than DIY, but the work is guaranteed and uses genuine parts. Turnaround is typically 1-4 weeks depending on parts availability. This is the best option for sealed units that you cannot open yourself."},
                        {"title": "Third-Party Repair Shops", "body": "Independent electronics repair shops may be able to replace batteries at lower cost than authorized service. Quality varies widely, and you may get aftermarket cells of unknown quality. Check reviews and ask about warranty on the repair before committing."},
                    ], "electric"),
                    alert("warning", "Safety warning: Lithium battery replacement involves working with high-voltage DC systems that can cause serious injury or fire if mishandled. Always follow proper safety procedures, use appropriate PPE, and never work on a swollen or damaged battery. If you are not 100% confident in your abilities, pay a professional."),
                ]
            },
            {
                "id": "warranty", "title": "Warranty Coverage & What It Includes",
                "parts": [
                    p("Nearly all portable power stations come with a manufacturer warranty that covers defects in materials and workmanship. The key question is whether battery degradation is covered — and the answer is almost always no, unless the degradation is caused by a defect."),
                    table(["Brand", "Warranty Period", "Battery Coverage", "What Is Not Covered"], [
                        ["EcoFlow", "2-5 years (varies by model)", "Defects only, not normal wear", "Normal degradation, misuse, water damage, physical damage"],
                        ["Jackery", "2-5 years (varies by model)", "Defects only", "Normal degradation, accidental damage, unauthorized repair"],
                        ["Bluetti", "2-5 years", "Defects + guaranteed capacity warranty", "Physical damage, misuse, normal wear below threshold"],
                        ["Anker", "18 months - 5 years", "Defects only", "Normal wear and tear, cosmetic damage, unauthorized modification"],
                        ["Goal Zero", "2 years", "Defects only", "Normal degradation, misuse, consumables"],
                    ]),
                    p("What counts as a defective battery vs. normal wear? Manufacturers typically consider a battery defective if it drops below 60-70% of rated capacity within the warranty period under normal use. If your battery loses 20% capacity in 3 years, that is considered normal and not covered. If it loses 50% capacity in 1 year, that is likely a defect and should be covered."),
                    p("To make a warranty claim, you will usually need to provide proof of purchase, serial number, and evidence of the issue (capacity test results, photos, app screenshots). The process typically takes 2-6 weeks depending on the brand and whether they need to receive the unit for inspection."),
                    alert("info", "Tip: Register your product with the manufacturer promptly after purchase. Many brands extend the warranty by 6-12 months if you register. Also, keep your receipt and all documentation — you will need it if you ever need to make a claim."),
                ]
            },
            {
                "id": "signs", "title": "Signs Your Battery Needs Replacement",
                "parts": [
                    p("Batteries do not usually fail suddenly — they degrade gradually over hundreds of charge cycles. Here are the most common signs that your battery is reaching the end of its useful life:"),
                    grid_cards([
                        {"title": "Noticeably Shorter Runtime", "title_color": "yellow-400", "body": "The clearest sign. If your station used to power your fridge all weekend and now only lasts half a day, the battery has degraded significantly. Most batteries are considered end-of-life at 60-70% of original capacity."},
                        {"title": "Rapid Voltage Drop", "title_color": "red-400", "body": "If the battery percentage drops quickly under load — say, from 100% to 50% in 10 minutes — it is a sign of high internal resistance. The battery cannot deliver current effectively even though it shows full voltage at rest."},
                        {"title": "Swollen or Bulging Case", "title_color": "red-400", "body": "This is a serious safety concern. A swollen battery has developed gas from internal degradation and should be replaced immediately. Do not charge a swollen battery, and handle it carefully. Dispose of it properly at a battery recycling center."},
                        {"title": "Error Codes or BMS Faults", "title_color": "yellow-400", "body": "Frequent BMS (Battery Management System) errors, cell imbalance warnings, or unexplained shutdowns can indicate a failing battery. The BMS is protecting itself and you from a degraded battery that can no longer operate safely within normal parameters."},
                        {"title": "Slow Charging (When It Was Fast)", "title_color": "electric-400", "body": "If charging has become significantly slower than it used to be and you have ruled out other causes (cables, charger, temperature), the battery may have developed high internal resistance that prevents it from accepting charge at the normal rate."},
                        {"title": "Age & Cycle Count", "title_color": "green-400", "body": "Even if it still works OK, if your battery is 5+ years old and has seen heavy use (500+ cycles for Li-ion, 3,000+ for LFP), you should start planning for replacement. It is better to replace proactively than to have it fail when you need it most."},
                    ], 3),
                    p("How to test your battery capacity? The most accurate method is a full discharge test: charge to 100%, then run a known load (like a 100W light bulb) and measure how long it lasts. If you get less than 60-70% of the rated capacity, the battery is nearing end of life. Most smart stations also show cycle count and health in the app."),
                ]
            },
            {
                "id": "extend-life", "title": "How to Extend Battery Life",
                "parts": [
                    p("The best way to avoid expensive battery replacement is to make your battery last as long as possible. Here are proven strategies to maximize battery lifespan:"),
                    numbered_steps([
                        {"title": "Avoid Full Discharges", "body": "Draining the battery to 0% puts maximum stress on the cells. Try to keep the battery between 20-80% for daily use. Only do full charges and discharges occasionally (once every few months) for calibration."},
                        {"title": "Store at 50-60% Charge", "body": "For long-term storage (more than 1 month), charge the battery to 50-60%, not 100%. Full charge during storage accelerates degradation. Most stations have a storage mode or app reminder to help with this."},
                        {"title": "Keep It Cool", "body": "Heat is the #1 enemy of battery life. Avoid leaving your power station in a hot car, in direct sun, or near heat sources. Ideal operating temperature is 20-25°C (68-77°F). Temperatures above 40°C (104°F) accelerate degradation significantly."},
                        {"title": "Use the Right Charge Mode", "body": "Fast charging generates more heat and causes slightly more wear. If you do not need the battery quickly, use standard or silent charge mode instead of turbo/fast charging. Your battery will thank you with longer life."},
                    ], "green"),
                    p("Additional tips: Keep the battery clean and dry, avoid physical shock or vibration, update firmware (manufacturers often optimize battery management), and use the battery regularly — lithium batteries degrade faster when left unused for very long periods. A good rule is to cycle the battery at least once every 3-6 months even if you are not using it regularly."),
                    alert("info", "LiFePO4 (LFP) batteries last 3-6 times longer than traditional lithium-ion (NMC/NCA) batteries. An LFP battery might last 3,000-6,000 cycles vs. 500-1,000 for Li-ion. If you are buying a new station, choosing LFP chemistry is the single best thing you can do for long-term value and to minimize replacement costs."),
                ]
            },
            {
                "id": "battery-types", "title": "Battery Chemistry Comparison",
                "parts": [
                    p("Not all portable power station batteries are the same. The chemistry type dramatically affects lifespan, safety, cost, and replacement frequency. Here is how the main types compare:"),
                    table(["Factor", "LiFePO4 (LFP)", "Lithium-Ion (NMC/NCA)", "Lead-Acid"], [
                        ["Cycle Life (80% capacity)", "3,000–6,000 cycles", "500–1,000 cycles", "200–500 cycles"],
                        ["Typical Lifespan", "5–10 years", "2–4 years", "1–3 years"],
                        ["Energy Density", "Lower (heavier for same Wh)", "Higher (lighter, more compact)", "Lowest (very heavy)"],
                        ["Safety / Thermal Stability", "Excellent — very stable", "Good — but can thermal runaway", "Fair — lead/acid hazards"],
                        ["Cost per kWh", "Higher upfront, lower long-term", "Moderate upfront", "Lowest upfront, highest long-term"],
                        ["Environmental Impact", "Less toxic, easier to recycle", "Cobalt/nickel concerns", "Lead is highly toxic"],
                        ["Used in 2026 stations", "Most mid/high-end models", "Some budget/lightweight models", "Very few (mostly old designs)"],
                    ]),
                    p("As of 2026, LiFePO4 (LFP) has become the dominant chemistry for portable power stations. The longer cycle life and better safety more than justify the slightly higher upfront cost for most users. The main remaining uses for lithium-ion (NMC) are in ultra-portable models where weight is the primary concern, and in some budget models from lesser-known brands."),
                ]
            },
            {
                "id": "buying-tips", "title": "Buying Tips: Replace Battery vs Buy New Station",
                "parts": [
                    p("When your battery reaches end of life, you have a choice: replace the battery or buy a whole new power station. Here is how to make that decision:"),
                    p("First, calculate the cost ratio. If a replacement battery costs more than 60-70% of what a comparable new station costs, just buy new. You get a full warranty, the latest technology, and a brand-new unit (not just a new battery in an old frame)."),
                    p("Second, consider technological progress. If your station is from 2020 or earlier, a new model will likely charge 2-3x faster, have better efficiency, more features (app, UPS mode, smart home), and better battery chemistry. The upgrade may be worth it even if replacement is slightly cheaper."),
                    p("Third, think about your future needs. Has your power usage grown? If you bought a 500Wh station and now find yourself wanting more capacity, this is a great opportunity to upgrade to a larger model rather than replacing the battery in one that is too small."),
                    grid_cards([
                        {"title": "Choose Battery Replacement If...", "title_color": "green-400", "body": "Replacement cost is less than 60% of new, the unit is less than 4 years old, you are happy with its features and performance, parts are readily available, and the rest of the unit is in excellent condition."},
                        {"title": "Choose New Station If...", "title_color": "yellow-400", "body": "Replacement is expensive relative to new, the unit is 5+ years old, newer models have significantly better features/specs, you need more capacity than before, or the unit has other issues beyond just the battery."},
                    ]),
                ]
            },
            {
                "id": "pro-tips", "title": "Pro Tips & Best Practices",
                "parts": [
                    grid_cards([
                        {"title": "Buy Modular Designs", "title_color": "electric-400", "body": "When shopping for a new power station, prioritize models with user-replaceable/expandable batteries. They cost a bit more upfront but give you much more flexibility and lower long-term cost of ownership."},
                        {"title": "Track Cycle Count", "title_color": "green-400", "body": "Most smart stations track cycle count in the app. Keep an eye on it and start planning for replacement when you reach 70-80% of the rated cycle life. Proactive planning beats sudden failure."},
                        {"title": "Sell or Trade In", "title_color": "yellow-400", "body": "If you decide to upgrade, do not just throw away your old station. Many brands have trade-in programs, or you can sell it as-is on the used market. Someone might want it for parts or to replace their own failed unit."},
                        {"title": "Recycle Properly", "title_color": "red-400", "body": "Never throw lithium batteries in the trash. Take them to a battery recycling center, big-box store with battery recycling, or household hazardous waste facility. It is illegal in many places and terrible for the environment."},
                    ]),
                ]
            },
        ],
        "faqs": [
            {"question": "How much does it cost to replace a portable power station battery?", "answer": "Battery replacement costs range from $250 for small 500Wh stations to $2,000+ for large 5,000Wh+ models. On average, you can expect to pay 40-70% of the original purchase price. LiFePO4 batteries are more expensive upfront but last 3-6 times longer, making them cheaper per cycle over the long run."},
            {"question": "Can I replace the battery in my power station myself?", "answer": "It depends on the model. Some power stations (EcoFlow Delta series, Bluetti with expansion packs, Jackery Explorer Plus) are designed for easy user-replaceable battery modules. Others are sealed units that require professional service or cannot be replaced at all. Check your manual or contact the manufacturer to confirm."},
            {"question": "How long do portable power station batteries last?", "answer": "Battery lifespan depends on chemistry and usage. LiFePO4 (LFP) batteries typically last 3,000-6,000 charge cycles (about 5-10 years of typical use) before dropping to 80% capacity. Traditional lithium-ion (NMC) batteries last 500-1,000 cycles (2-4 years). Actual lifespan depends on how you use and maintain the battery."},
            {"question": "Does warranty cover battery replacement?", "answer": "Warranties cover defective batteries but not normal wear and tear from regular use. If your battery drops below 60-70% capacity within the warranty period (typically 2-5 years) under normal use, it may be considered defective and covered. Gradual degradation over hundreds of cycles is considered normal and is not covered."},
            {"question": "How do I know if my battery needs replacing?", "answer": "Key signs include: significantly shorter runtime (less than 60-70% of original), rapid voltage drop under load, swollen or bulging battery case, frequent BMS errors or cell imbalance warnings, slow charging when it used to be fast, and high cycle count (500+ for Li-ion, 3,000+ for LFP)."},
            {"question": "Is it better to replace the battery or buy a new power station?", "answer": "Replace the battery if: cost is less than 60% of a new comparable unit, the station is less than 4 years old, and you are happy with its performance. Buy new if: replacement is expensive relative to new, the unit is 5+ years old, newer models have much better features, or you need more capacity."},
            {"question": "Can I use third-party replacement batteries?", "answer": "Technically yes in some cases, but it is not recommended. Third-party batteries may use lower quality cells, lack proper safety certification, and will void your warranty. For modular stations, always use official manufacturer battery modules for safety and compatibility."},
            {"question": "How can I make my battery last longer?", "answer": "Top tips for longer battery life: avoid full discharges (keep above 20%), store at 50-60% charge for long periods, avoid extreme heat, use standard charging instead of fast charging when possible, use the battery regularly (cycle at least every 3-6 months), and choose LiFePO4 chemistry for 3-6x longer cycle life."},
            {"question": "What do I do with my old power station battery?", "answer": "Never throw lithium batteries in the trash — they are a fire hazard and environmental hazard. Take them to a battery recycling center, a big-box store with battery recycling (like Home Depot or Lowe's), or your local household hazardous waste facility. Some manufacturers also have take-back programs for their products."},
            {"question": "Do LiFePO4 batteries need replacement less often?", "answer": "Yes — LiFePO4 (LFP) batteries last 3-6 times longer than traditional lithium-ion. LFP typically lasts 3,000-6,000 cycles vs. 500-1,000 for NMC Li-ion. For a typical user, that means 5-10 years of use vs. 2-4 years. The higher upfront cost of LFP is almost always worth it for the much longer lifespan."},
        ],
        "related": [
            {"url": "how-to-store-portable-power-station.html", "title": "Storage Guide", "desc": "How to store a portable power station long-term — ideal charge level, temperature, and cycling schedule.", "badge_color": "green", "badge_text": "STORAGE", "sub_badge": "Guide"},
            {"url": "portable-power-station-overheating-hot.html", "title": "Overheating Guide", "desc": "Why power stations overheat, temperature effects on battery life, and how to keep your station cool.", "badge_color": "red", "badge_text": "HEAT", "sub_badge": "Universal"},
            {"url": "portable-power-station-eco-mode.html", "title": "ECO Mode Guide", "desc": "How ECO mode works, how much battery it saves, and how to optimize it for maximum runtime.", "badge_color": "purple", "badge_text": "ECO MODE", "sub_badge": "All Brands"},
            {"url": "lifepo4-vs-lithium-ion-power-station.html", "title": "LFP vs Li-ion", "desc": "Complete comparison of LiFePO4 vs lithium-ion power stations — cycle life, safety, cost, and which to choose.", "badge_color": "electric", "badge_text": "COMPARE", "sub_badge": "Chemistry"},
            {"url": "portable-power-station-not-charging.html", "title": "Not Charging", "desc": "Troubleshoot AC, solar, and DC charging problems with step-by-step diagnostics for all major brands.", "badge_color": "yellow", "badge_text": "CHARGE", "sub_badge": "Universal"},
            {"url": "outdoor-power.html", "title": "Power Station Comparison", "desc": "Compare all major portable power station models side by side — capacity, output, solar input, and more.", "badge_color": "purple", "badge_text": "COMPARE", "sub_badge": "All Brands"},
        ],
    }


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pages = []

    # Page 2 (page 1 already exists: how-to-charge-power-station-without-electricity.html)
    pages.append(generate_page_2())

    # Generate each page
    for page_data in pages:
        html_content = build_full_page(page_data)
        filepath = os.path.join(OUTPUT_DIR, page_data["filename"])
        with open(filepath, "w") as f:
            f.write(html_content)
        wc = count_words(html_content)
        print(f"  Generated: {page_data['filename']} ({wc:,} words)")

    print(f"\nTotal pages generated: {len(pages)}")


if __name__ == "__main__":
    main()
