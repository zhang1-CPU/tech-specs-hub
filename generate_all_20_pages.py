#!/usr/bin/env python3
"""Generate all 20 SEO pages for TechSpecsHub."""

import os
import json
import html
from typing import List, Dict, Any

OUTPUT_DIR = "/workspace/pages/specs"
BASE_URL = "https://powerspecshub.com/pages/specs"
SITE_NAME = "TechSpecsHub"
UPDATED_DATE = "2026-06-25"
UPDATED_DATE_TEXT = "June 25, 2026"


def read_template() -> str:
    """Read the eco-mode template and extract reusable parts."""
    with open(f"{OUTPUT_DIR}/portable-power-station-eco-mode.html", "r") as f:
        content = f.read()
    return content


def build_header(title: str, meta_desc: str, canonical: str, og_image: str, article_json: dict, faq_json: dict, breadcrumb_json: dict) -> str:
    """Build the HTML head section."""
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


def build_body_header() -> str:
    """Build the body header/navigation."""
    return '''<body class="bg-navy-950 text-white min-h-screen font-display">

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


def build_breadcrumb(category: str, category_url: str, page_name: str) -> str:
    """Build breadcrumb navigation."""
    return f'''
  <!-- BREADCRUMB -->
  <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 pb-4">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="../../index.html">Home</a>
      <span class="breadcrumb-sep">/</span>
      <a href="{category_url}">{category}</a>
      <span class="breadcrumb-sep">/</span>
      <span class="breadcrumb-current">{page_name}</span>
    </nav>
  </div>
'''


def build_hero(badges: List[Dict[str, str]], title: str, intro: str, stats: List[Dict[str, str]], accent_color: str = "green") -> str:
    """Build hero section."""
    badges_html = ""
    for badge in badges:
        icon = badge.get("icon", "info")
        text = badge["text"]
        color = badge.get("color", "info")
        badges_html += f'<span class="badge badge-{color}"><i data-lucide="{icon}" style="width:0.75rem;height:0.75rem"></i>{text}</span>\n        '

    stats_html = ""
    for stat in stats:
        icon = stat.get("icon", "zap")
        label = stat["label"]
        value = stat["value"]
        value_color = stat.get("value_color", "white")
        stats_html += f'''        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="{icon}" style="width:0.9rem;height:0.9rem"></i>{label}</div>
          <div class="font-mono font-bold text-xl text-{value_color}">{value}</div>
        </div>
'''

    return f'''
  <!-- HERO -->
  <section class="relative max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-4 pb-6">
    <div class="glass-card p-8 md:p-10 overflow-hidden relative">
      <div class="absolute top-0 right-0 w-[420px] h-[420px] bg-{accent_color}-500/5 rounded-full blur-3xl pointer-events-none"></div>

      <div class="relative flex flex-wrap items-center gap-3 mb-5">
        {badges_html.strip()}
      </div>

      <h1 class="font-bold text-4xl md:text-5xl mb-4 leading-tight">
        {title} &mdash; <span class="gradient-text">Complete 2026 Guide</span>
      </h1>

      <p class="text-gray-400 text-lg leading-relaxed mb-6 max-w-3xl">
        {intro}
      </p>

      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8">
{stats_html.rstrip()}
      </div>
    </div>
  </section>
'''


def build_quick_answer(answer_text: str, accent_color: str = "green") -> str:
    """Build quick answer section."""
    return f'''
  <!-- QUICK ANSWER -->
  <section class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div class="glass-card p-6 md:p-8 bg-gradient-to-br from-{accent_color}-950/20 to-navy-900 border-{accent_color}-500/20">
      <h2 class="font-bold text-2xl mb-4 flex items-center gap-2"><i data-lucide="zap" style="width:1.25rem;height:1.25rem;color:#4ade80"></i>Quick Answer</h2>
      <p class="text-gray-300 leading-relaxed mb-4">
        {answer_text}
      </p>
    </div>
  </section>
'''


def build_toc(toc_items: List[Dict[str, str]]) -> str:
    """Build table of contents."""
    items_html = ""
    for i, item in enumerate(toc_items, 1):
        num = f"{i:02d}"
        items_html += f'        <a href="#{item["id"]}" class="flex items-center gap-2 p-2 rounded-lg hover:bg-white/5 text-gray-300 hover:text-white transition-all"><span class="text-electric-400 font-mono">{num}</span>{item["title"]}</a>\n'

    return f'''
  <!-- TABLE OF CONTENTS -->
  <section class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div class="glass-card p-6 md:p-8">
      <h2 class="font-bold text-2xl mb-4 flex items-center gap-2"><i data-lucide="list" style="width:1.25rem;height:1.25rem;color:#22d3ee"></i>Table of Contents</h2>
      <div class="grid md:grid-cols-2 gap-2 text-sm">
{items_html.rstrip()}
      </div>
    </div>
  </section>
'''


def build_section(section_id: str, title: str, content_html: str) -> str:
    """Build a content section."""
    return f'''
  <section id="{section_id}" class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <h2 class="font-bold text-3xl mb-5">{title}</h2>
    <div class="glass-card p-6 md:p-8">
{content_html}
    </div>
  </section>
'''


def build_faq(faqs: List[Dict[str, str]]) -> str:
    """Build FAQ section with details/summary."""
    faqs_html = ""
    for faq in faqs:
        faqs_html += f'''      <details class="glass-card p-5 group">
        <summary class="cursor-pointer font-semibold flex items-center justify-between gap-4">
          <span>{faq["question"]}</span>
          <i data-lucide="chevron-down" style="width:1rem;height:1rem" class="text-gray-500 group-open:rotate-180 transition-transform flex-shrink-0"></i>
        </summary>
        <p class="mt-3 text-gray-400 text-sm leading-relaxed">
          {faq["answer"]}
        </p>
      </details>
'''

    return f'''
  <!-- FAQ -->
  <section id="faq" class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="text-center mb-10">
      <h2 class="font-bold text-3xl md:text-4xl mb-4">Frequently Asked Questions</h2>
      <p class="text-gray-400">Common questions about this topic.</p>
    </div>
    <div class="space-y-3">
{faqs_html.rstrip()}
    </div>
  </section>
'''


def build_related(related: List[Dict[str, str]]) -> str:
    """Build related guides section."""
    cards_html = ""
    for r in related:
        badge_color = r.get("badge_color", "electric")
        badge_text = r.get("badge_text", "GUIDE")
        sub_badge = r.get("sub_badge", "All Brands")
        cards_html += f'''      <a href="{r["url"]}" class="glass-card p-6 block hover:border-electric-400/50 transition-all group">
        <div class="flex items-start gap-3 mb-3">
          <div class="px-2.5 py-1 bg-{badge_color}-500/20 text-{badge_color}-400 font-mono font-semibold text-sm rounded-md border border-{badge_color}-500/30">{badge_text}</div>
          <span class="badge badge-info">{sub_badge}</span>
        </div>
        <h3 class="font-bold text-lg mb-2 group-hover:text-electric-400 transition-colors">{r["title"]}</h3>
        <p class="text-sm text-gray-400">{r["desc"]}</p>
      </a>
'''

    return f'''
  <!-- RELATED GUIDES -->
  <section id="related" class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h2 class="font-bold text-3xl mb-5">Related Guides &amp; Resources</h2>
    <div class="grid md:grid-cols-3 gap-4">
{cards_html.rstrip()}
    </div>
  </section>
'''


def build_footer() -> str:
    """Build page footer."""
    return '''
  <!-- FOOTER -->
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


def make_article_json(headline: str, description: str, url: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": headline,
        "description": description,
        "url": url,
        "datePublished": UPDATED_DATE,
        "dateModified": UPDATED_DATE,
        "author": {
            "@type": "Organization",
            "name": SITE_NAME
        },
        "publisher": {
            "@type": "Organization",
            "name": SITE_NAME,
            "url": "https://powerspecshub.com/"
        },
        "image": {
            "@type": "ImageObject",
            "url": "https://powerspecshub.com/assets/images/og-default.png"
        }
    }


def make_faq_json(faqs: List[Dict[str, str]]) -> dict:
    entities = []
    for faq in faqs:
        entities.append({
            "@type": "Question",
            "name": faq["question"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["answer"]
            }
        })
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities
    }


def make_breadcrumb_json(category: str, category_url: str, page_name: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": "https://powerspecshub.com/"
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": category,
                "item": category_url
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": page_name
            }
        ]
    }


def p(text: str) -> str:
    return f'<p class="text-gray-300 leading-relaxed mb-4">\n        {text}\n      </p>'


def ul(items: List[str]) -> str:
    lis = ""
    for item in items:
        lis += f'          <li>• {item}</li>\n'
    return f'      <ul class="text-sm text-gray-300 space-y-1 mb-4">\n{lis.rstrip()}\n      </ul>'


def table(headers: List[str], rows: List[List[str]]) -> str:
    thead = ""
    for h in headers:
        thead += f"<th>{h}</th>"
    tbody = ""
    for row in rows:
        trow = ""
        for cell in row:
            trow += f"<td>{cell}</td>"
        tbody += f"            <tr>{trow}</tr>\n"
    return f'''      <div class="overflow-x-auto mb-6">
        <table class="specs-table w-full text-sm">
          <thead>
            <tr>{thead}</tr>
          </thead>
          <tbody>
{tbody.rstrip()}
          </tbody>
        </table>
      </div>'''


def alert(alert_type: str, text: str, icon: str = "info") -> str:
    icon_map = {
        "info": "lightbulb",
        "warning": "alert-triangle",
        "critical": "alert-octagon",
        "success": "check-circle"
    }
    icon_name = icon_map.get(alert_type, icon)
    return f'''      <div class="mt-4 alert alert-{alert_type}">
        <i data-lucide="{icon_name}" style="width:1rem;height:1rem;flex-shrink:0;margin-top:0.1rem"></i>
        <p class="text-sm">{text}</p>
      </div>'''


def grid_cards(cards: List[Dict[str, str]], cols: int = 2) -> str:
    cards_html = ""
    for card in cards:
        title_color = card.get("title_color", "electric-400")
        cards_html += f'''        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-5">
          <h4 class="font-semibold text-{title_color} mb-2">{card["title"]}</h4>
          <p class="text-sm text-gray-300 mb-2">{card["body"]}</p>
        </div>
'''
    return f'      <div class="grid md:grid-cols-{cols} gap-4 mb-4">\n{cards_html.rstrip()}\n      </div>'


def numbered_steps(steps: List[Dict[str, str]], color: str = "green") -> str:
    steps_html = ""
    for i, step in enumerate(steps, 1):
        steps_html += f'''        <div class="flex items-start gap-3">
          <div class="w-10 h-10 bg-{color}-500/20 rounded-full flex items-center justify-center flex-shrink-0">
            <span class="font-mono font-bold text-{color}-400">{i}</span>
          </div>
          <div>
            <h4 class="font-semibold text-white">{step["title"]}</h4>
            <p class="text-sm text-gray-400">{step["body"]}</p>
          </div>
        </div>
'''
    return f'      <div class="space-y-4 mb-6">\n{steps_html.rstrip()}\n      </div>'


def pros_cons(pros: List[str], cons: List[str]) -> str:
    pros_html = ""
    for item in pros:
        pros_html += f'          <li class="flex items-start gap-2"><i data-lucide="check" style="width:1rem;height:1rem;color:#4ade80;flex-shrink:0;margin-top:0.1rem"></i><span>{item}</span></li>\n'
    cons_html = ""
    for item in cons:
        cons_html += f'          <li class="flex items-start gap-2"><i data-lucide="x" style="width:1rem;height:1rem;color:#f87171;flex-shrink:0;margin-top:0.1rem"></i><span>{item}</span></li>\n'
    return f'''      <div class="grid md:grid-cols-2 gap-6 mb-4">
        <div>
          <h3 class="font-bold text-xl mb-4 text-green-400 flex items-center gap-2"><i data-lucide="check-circle" style="width:1.25rem;height:1.25rem"></i>Pros</h3>
          <ul class="space-y-3 text-sm text-gray-300">
{pros_html.rstrip()}
          </ul>
        </div>
        <div>
          <h3 class="font-bold text-xl mb-4 text-red-400 flex items-center gap-2"><i data-lucide="x-circle" style="width:1.25rem;height:1.25rem"></i>Cons</h3>
          <ul class="space-y-3 text-sm text-gray-300">
{cons_html.rstrip()}
          </ul>
        </div>
      </div>'''
