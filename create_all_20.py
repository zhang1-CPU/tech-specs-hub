#!/usr/bin/env python3
"""
Generate all 20 SEO pages for TechSpecsHub.
Uses the eco-mode page as a template and generates rich content for each.
"""

import os
import json

OUTPUT_DIR = "/workspace/pages/specs"

def generate_page(filename, title, meta_desc, category, cat_page, breadcrumb,
                  badges, hero_title, hero_intro, hero_stats,
                  quick_title, quick_text, toc, sections, faqs, related):
    """Generate a complete HTML page."""
    
    # Read header/footer from template
    template_path = os.path.join(OUTPUT_DIR, "portable-power-station-eco-mode.html")
    with open(template_path, "r") as f:
        template = f.read()
    
    # Extract head section
    head_start = template.find("<head>") + 6
    head_end = template.find("</head>")
    head_template = template[head_start:head_end]
    
    # Extract body header
    body_start = template.find("<body")
    breadcrumb_start = template.find('<!-- BREADCRUMB -->')
    header_html = template[body_start:breadcrumb_start]
    
    # Extract footer
    footer_start = template.find('<!-- FOOTER -->')
    footer_end = template.find("</html>") + 7
    footer_html = template[footer_start:footer_end]
    
    # Build JSON-LD
    article_ld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": meta_desc,
        "url": f"https://powerspecshub.com/pages/specs/{filename}",
        "datePublished": "2026-06-25",
        "dateModified": "2026-06-25",
        "author": {"@type": "Organization", "name": "TechSpecsHub"},
        "publisher": {"@type": "Organization", "name": "TechSpecsHub", "url": "https://powerspecshub.com/"},
        "image": {"@type": "ImageObject", "url": "https://powerspecshub.com/assets/images/og-default.png"}
    }
    
    faq_ld_items = []
    for q, a in faqs:
        faq_ld_items.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a}
        })
    
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_ld_items}
    
    breadcrumb_ld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://powerspecshub.com/"},
            {"@type": "ListItem", "position": 2, "name": category, "item": f"https://powerspecshub.com/pages/specs/{cat_page}"},
            {"@type": "ListItem", "position": 3, "name": breadcrumb}
        ]
    }
    
    # Build head with updated meta
    head_html = f'''<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | TechSpecsHub</title>
  <meta name="description" content="{meta_desc}">
  <meta name="theme-color" content="#0a1628">
  <style>html,body{{background-color:#0a1628;color:#ffffff;margin:0;padding:0;min-height:100vh;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;line-height:1.5;-webkit-font-smoothing:antialiased}}a{{color:#22d3ee;text-decoration:none}}code,pre{{font-family:ui-monospace,monospace}}</style>

  <link rel="preconnect" href="https://cdn.tailwindcss.com">
  <link rel="preconnect" href="https://unpkg.com">
  <link rel="dns-prefetch" href="https://cdn.tailwindcss.com">
  <link rel="dns-prefetch" href="https://unpkg.com">
  <link rel="dns-prefetch" href="https://fonts.gstatic.com">

  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <link rel="canonical" href="https://powerspecshub.com/pages/specs/{filename}">

  <meta property="og:title" content="{title} | TechSpecsHub">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:type" content="Article">
  <meta property="og:url" content="https://powerspecshub.com/pages/specs/{filename}">
  <meta property="og:image" content="https://powerspecshub.com/assets/images/og-default.png">
  <meta property="og:site_name" content="TechSpecsHub">
  <meta property="article:published_time" content="2026-06-25T00:00:00Z">
  <meta property="article:modified_time" content="2026-06-25T00:00:00Z">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title} | TechSpecsHub">
  <meta name="twitter:description" content="{meta_desc}">
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
  {json.dumps(article_ld, indent=2)}
  </script>

  <script type="application/ld+json">
  {json.dumps(faq_ld, indent=2)}
  </script>

  <script type="application/ld+json">
  {json.dumps(breadcrumb_ld, indent=2)}
  </script>

</head>'''
    
    # Build hero badges
    badge_html = ""
    for text, color in badges:
        icon_map = {"green": "battery-charging", "info": "info", "yellow": "alert-triangle",
                    "red": "alert-circle", "purple": "layers", "electric": "zap"}
        icon = icon_map.get(color, "info")
        badge_html += f'        <span class="badge badge-{color}"><i data-lucide="{icon}" style="width:0.75rem;height:0.75rem"></i>{text}</span>\n'
    
    # Build hero stats
    stats_html = ""
    for label, value, color in hero_stats:
        color_cls = f"text-{color}-400" if color != "electric" else "text-electric-400"
        icon_map = {"green": "battery-charging", "yellow": "zap", "red": "alert-triangle",
                    "electric": "activity", "info": "info", "purple": "layers"}
        icon = icon_map.get(color, "activity")
        stats_html += f'''        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="{icon}" style="width:0.9rem;height:0.9rem"></i>{label}</div>
          <div class="font-mono font-bold text-xl {color_cls}">{value}</div>
        </div>
'''
    
    # Build TOC
    toc_html = ""
    for i, (anchor, text) in enumerate(toc):
        num = str(i+1).zfill(2)
        toc_html += f'        <a href="#{anchor}" class="flex items-center gap-2 p-2 rounded-lg hover:bg-white/5 text-gray-300 hover:text-white transition-all"><span class="text-electric-400 font-mono">{num}</span>{text}</a>\n'
    
    # Build sections
    sections_html = ""
    for sec in sections:
        sections_html += build_section(sec["id"], sec["title"], sec["content"])
    
    # Build FAQ
    faq_html = ""
    for q, a in faqs:
        faq_html += f'''      <details class="glass-card p-5 group">
        <summary class="cursor-pointer font-semibold flex items-center justify-between gap-4">
          <span>{q}</span>
          <i data-lucide="chevron-down" style="width:1rem;height:1rem" class="text-gray-500 group-open:rotate-180 transition-transform flex-shrink-0"></i>
        </summary>
        <p class="mt-3 text-gray-400 text-sm leading-relaxed">
          {a}
        </p>
      </details>
'''
    
    # Build related
    related_html = ""
    for rfile, rbadge, rlabel, rtitle, rdesc in related:
        rcolor = "electric"
        if any(w in rbadge for w in ["ECO", "SOLAR", "PASS", "GUIDE", "STORAGE", "SPEC"]):
            rcolor = "green"
        elif any(w in rbadge for w in ["CHARGE", "FAST", "WARN", "BUDGET", "BATTERY"]):
            rcolor = "yellow"
        elif any(w in rbadge for w in ["COMPARE", "BEST", "TOP"]):
            rcolor = "purple"
        elif any(w in rbadge for w in ["ERROR", "FAULT", "CRITICAL", "REPAIR", "DISCONNECT", "APP"]):
            rcolor = "red"
        related_html += f'''      <a href="{rfile}" class="glass-card p-6 block hover:border-electric-400/50 transition-all group">
        <div class="flex items-start gap-3 mb-3">
          <div class="px-2.5 py-1 bg-{rcolor}-500/20 text-{rcolor}-400 font-mono font-semibold text-sm rounded-md border border-{rcolor}-500/30">{rbadge}</div>
          <span class="badge badge-info">{rlabel}</span>
        </div>
        <h3 class="font-bold text-lg mb-2 group-hover:text-electric-400 transition-colors">{rtitle}</h3>
        <p class="text-sm text-gray-400">{rdesc}</p>
      </a>
'''
    
    # Assemble full page
    full_html = f'''<!DOCTYPE html>
<html lang="en">
{head_html}
<body class="bg-navy-950 text-white min-h-screen font-display">

{header_html}
  <!-- BREADCRUMB -->
  <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 pb-4">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="../../index.html">Home</a>
      <span class="breadcrumb-sep">/</span>
      <a href="{cat_page}">{category}</a>
      <span class="breadcrumb-sep">/</span>
      <span class="breadcrumb-current">{breadcrumb}</span>
    </nav>
  </div>

  <!-- HERO -->
  <section class="relative max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-4 pb-6">
    <div class="glass-card p-8 md:p-10 overflow-hidden relative">
      <div class="absolute top-0 right-0 w-[420px] h-[420px] bg-green-500/5 rounded-full blur-3xl pointer-events-none"></div>

      <div class="relative flex flex-wrap items-center gap-3 mb-5">
{badge_html}      </div>

      <h1 class="font-bold text-4xl md:text-5xl mb-4 leading-tight">
        {hero_title}
      </h1>

      <p class="text-gray-400 text-lg leading-relaxed mb-6 max-w-3xl">
        {hero_intro}
      </p>

      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8">
{stats_html}      </div>
    </div>
  </section>

  <!-- QUICK ANSWER -->
  <section class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div class="glass-card p-6 md:p-8 bg-gradient-to-br from-green-950/20 to-navy-900 border-green-500/20">
      <h2 class="font-bold text-2xl mb-4 flex items-center gap-2"><i data-lucide="zap" style="width:1.25rem;height:1.25rem;color:#4ade80"></i>{quick_title}</h2>
      <p class="text-gray-300 leading-relaxed mb-4">
        {quick_text}
      </p>
    </div>
  </section>

  <!-- TABLE OF CONTENTS -->
  <section class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div class="glass-card p-6 md:p-8">
      <h2 class="font-bold text-2xl mb-4 flex items-center gap-2"><i data-lucide="list" style="width:1.25rem;height:1.25rem;color:#22d3ee"></i>Table of Contents</h2>
      <div class="grid md:grid-cols-2 gap-2 text-sm">
{toc_html}      </div>
    </div>
  </section>

{sections_html}
  <!-- FAQ -->
  <section id="faq" class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="text-center mb-10">
      <h2 class="font-bold text-3xl md:text-4xl mb-4">Frequently Asked Questions</h2>
      <p class="text-gray-400">Common questions about {breadcrumb.lower()}.</p>
    </div>
    <div class="space-y-3">
{faq_html}    </div>
  </section>

  <!-- RELATED GUIDES -->
  <section id="related" class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h2 class="font-bold text-3xl mb-5">Related Guides &amp; Resources</h2>
    <div class="grid md:grid-cols-3 gap-4">
{related_html}    </div>
  </section>

{footer_html}'''
    
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w") as f:
        f.write(full_html)
    
    return len(full_html.split())


def build_section(sec_id, title, content_items):
    """Build a single section HTML."""
    content_html = ""
    for item in content_items:
        if isinstance(item, str):
            content_html += f'      <p class="text-gray-300 leading-relaxed mb-4">\n        {item}\n      </p>\n'
        elif isinstance(item, dict):
            t = item["type"]
            if t == "table":
                headers = "".join(f"<th>{h}</th>" for h in item["headers"])
                rows = ""
                for row in item["rows"]:
                    cells = "".join(f"<td>{c}</td>" for c in row)
                    rows += f"            <tr>{cells}</tr>\n"
                content_html += f'''      <div class="overflow-x-auto mb-6">
        <table class="specs-table w-full text-sm">
          <thead>
            <tr>{headers}</tr>
          </thead>
          <tbody>
{rows.rstrip()}
          </tbody>
        </table>
      </div>\n'''
            elif t == "list":
                items_str = ""
                for li in item["items"]:
                    if ":" in li and li.split(":")[0].strip() != li.strip():
                        k, v = li.split(":", 1)
                        items_str += f'            <li>• <strong class="text-white">{k}:</strong>{v}</li>\n'
                    else:
                        items_str += f'            <li>• {li}\n'
                content_html += f'''      <ul class="text-sm text-gray-300 space-y-1 mb-4">
{items_str.rstrip()}
      </ul>\n'''
            elif t == "grid":
                grid_items = ""
                for gtitle, gcolor, gitems in item["items"]:
                    gcolor_cls = f"text-{gcolor}-400" if gcolor != "electric" else "text-electric-400"
                    li_items = "".join(f"          <li>• {li}</li>\n" for li in gitems)
                    grid_items += f'''        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-5">
          <h4 class="font-semibold {gcolor_cls} mb-2">{gtitle}</h4>
          <ul class="text-sm text-gray-300 space-y-1">
{li_items.rstrip()}
          </ul>
        </div>
'''
                content_html += f'''      <div class="grid md:grid-cols-2 gap-4 mb-4">
{grid_items.rstrip()}
      </div>\n'''
            elif t == "alert":
                content_html += f'''      <div class="mt-4 alert alert-{item["class"]}">
        <i data-lucide="{item["icon"]}" style="width:1rem;height:1rem;flex-shrink:0;margin-top:0.1rem"></i>
        <p class="text-sm"><strong>{item["title"]}:</strong> {item["text"]}</p>
      </div>\n'''
            elif t == "steps":
                steps_html = ""
                for i, (stitle, stext) in enumerate(item["items"]):
                    steps_html += f'''        <div class="flex items-start gap-3">
          <div class="w-10 h-10 bg-green-500/20 rounded-full flex items-center justify-center flex-shrink-0">
            <span class="font-mono font-bold text-green-400">{i+1}</span>
          </div>
          <div>
            <h4 class="font-semibold text-white">{stitle}</h4>
            <p class="text-sm text-gray-400">{stext}</p>
          </div>
        </div>
'''
                content_html += f'''      <div class="space-y-4 mb-6">
{steps_html.rstrip()}
      </div>\n'''
            elif t == "proscons":
                pros = "".join(f"          <li>• {li}</li>\n" for li in item["pros"])
                cons = "".join(f"          <li>• {li}</li>\n" for li in item["cons"])
                content_html += f'''      <div class="grid md:grid-cols-2 gap-6 mb-4">
        <div>
          <h3 class="font-bold text-xl mb-4 text-green-400 flex items-center gap-2"><i data-lucide="check-circle" style="width:1.25rem;height:1.25rem"></i>Pros</h3>
          <ul class="space-y-3 text-sm text-gray-300">
{pros.rstrip()}
          </ul>
        </div>
        <div>
          <h3 class="font-bold text-xl mb-4 text-red-400 flex items-center gap-2"><i data-lucide="x-circle" style="width:1.25rem;height:1.25rem"></i>Cons</h3>
          <ul class="space-y-3 text-sm text-gray-300">
{cons.rstrip()}
          </ul>
        </div>
      </div>\n'''
            elif t == "cards":
                cards_html = ""
                for ctitle, ccolor, ctext in item["items"]:
                    ccolor_cls = f"text-{ccolor}-400" if ccolor != "electric" else "text-electric-400"
                    cards_html += f'''        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-5">
          <h4 class="font-semibold {ccolor_cls} mb-2">{ctitle}</h4>
          <p class="text-sm text-gray-300">{ctext}</p>
        </div>
'''
                content_html += f'''      <div class="grid md:grid-cols-2 gap-4 mb-4">
{cards_html.rstrip()}
      </div>\n'''
            elif t == "protips":
                tips_html = ""
                for ttitle, ttext in item["items"]:
                    tips_html += f'''        <div class="flex items-start gap-3">
          <div class="w-10 h-10 bg-electric-500/20 rounded-xl flex items-center justify-center flex-shrink-0">
            <i data-lucide="lightbulb" style="width:1.25rem;height:1.25rem;color:#22d3ee"></i>
          </div>
          <div>
            <h4 class="font-semibold text-white">{ttitle}</h4>
            <p class="text-sm text-gray-400">{ttext}</p>
          </div>
        </div>
'''
                content_html += f'''      <div class="grid md:grid-cols-2 gap-4 mb-4">
{tips_html.rstrip()}
      </div>\n'''
            elif t == "myths":
                myths_html = ""
                for myth, fact in item["items"]:
                    myths_html += f'''        <div class="flex items-start gap-3">
          <div class="w-8 h-8 bg-red-500/20 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
            <i data-lucide="x" style="width:1rem;height:1rem;color:#f87171"></i>
          </div>
          <div>
            <h4 class="font-semibold text-white">"{myth}"</h4>
            <p class="text-sm text-gray-400">{fact}</p>
          </div>
        </div>
'''
                content_html += f'''      <div class="space-y-4">
{myths_html.rstrip()}
      </div>\n'''
    
    return f'''  <section id="{sec_id}" class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <h2 class="font-bold text-3xl mb-5">{title}</h2>
    <div class="glass-card p-6 md:p-8">
{content_html}    </div>
  </section>

'''


# ============================================================
# PAGE DATA - All 20 pages with complete content
# ============================================================

def get_pages():
    """Return all 20 page configurations."""
    pages = []
    
    # ===== OUTDOOR POWER: Page 1 - Charge Without Electricity =====
    pages.append({
        "filename": "how-to-charge-power-station-without-electricity.html",
        "title": "How to Charge a Portable Power Station Without Electricity (2026)",
        "meta_desc": "Complete guide to charging portable power stations without grid electricity: solar panels, car charging, generators, wind power, hand cranks, and off-grid strategies for EcoFlow, Jackery, Bluetti, and more.",
        "category": "Outdoor Power",
        "cat_page": "outdoor-power.html",
        "breadcrumb": "Charging Without Electricity",
        "badges": [("OFF-GRID", "green"), ("Solar & More", "info"), ("All Brands", "info")],
        "hero_title": 'How to Charge a Portable Power Station Without Electricity &mdash; <span class="gradient-text">Complete 2026 Guide</span>',
        "hero_intro": "Whether you are camping off-grid, preparing for a long-term power outage, or living a fully off-grid lifestyle, knowing how to charge your power station without access to wall electricity is essential. Solar is the most popular method, but it is far from the only one. This guide covers every charging method available — from rooftop solar to car charging, generators, wind turbines, hand cranks, and even more creative solutions. We break down the pros, cons, costs, and charging speeds of each method so you can build the ultimate off-grid charging setup for any situation.",
        "hero_stats": [("Fastest Method", "Generator", "yellow"), ("Most Popular", "Solar Panels", "green"), ("Most Portable", "Car Charging", "electric"), ("Slowest Method", "Hand Crank", "red")],
        "quick_title": "Quick Answer: Best Off-Grid Charging Methods",
        "quick_text": "The most practical way to charge a portable power station without grid electricity is using solar panels — they are silent, have zero fuel cost, and work anywhere with sunlight. For faster charging, a gas or propane generator fills the battery quickest but requires fuel and makes noise. For road trips, car charging via the 12V port works while you drive. Wind turbines, hand cranks, and fuel cells are niche options for specific use cases. The best setup for most people combines solar for daily use with a generator or car charging as backup for cloudy days or emergencies.",
        "toc": [
            ("solar-charging", "Solar Panel Charging (Most Popular)"),
            ("car-charging", "Car & Vehicle Charging"),
            ("generator-charging", "Generator Charging (Fastest)"),
            ("wind-charging", "Wind Turbine Charging"),
            ("hand-crank", "Hand Crank & Manual Charging"),
            ("other-methods", "Other Creative Methods"),
            ("comparison", "Method Comparison Chart"),
            ("off-grid-tips", "Off-Grid Charging Strategies"),
            ("pro-tips", "Pro Tips & Advanced Techniques"),
        ],
        "sections": [
            {"id": "solar-charging", "title": "Solar Panel Charging — The Most Popular Method", "content": solar_section()},
            {"id": "car-charging", "title": "Car & Vehicle Charging — Great for Road Trips", "content": car_charging_section()},
            {"id": "generator-charging", "title": "Generator Charging — The Fastest Off-Grid Method", "content": generator_section()},
            {"id": "wind-charging", "title": "Wind Turbine Charging — Niche but Useful", "content": wind_section()},
            {"id": "hand-crank", "title": "Hand Crank & Manual Charging — Emergency Only", "content": hand_crank_section()},
            {"id": "other-methods", "title": "Other Creative Charging Methods", "content": other_charge_section()},
            {"id": "comparison", "title": "Method Comparison — Speed, Cost, Practicality", "content": charge_comparison_section()},
            {"id": "off-grid-tips", "title": "Off-Grid Charging Strategies & Tips", "content": offgrid_tips_section()},
            {"id": "pro-tips", "title": "Pro Tips & Advanced Techniques", "content": protips_section()},
        ],
        "faqs": standard_outdoor_faqs("charge without electricity", "solar charging, car charging, and generator charging"),
        "related": outdoor_related(),
    })
    
    return pages


# ===== CONTENT SECTIONS =====

def p(text):
    return text

def tbl(headers, rows):
    return {"type": "table", "headers": headers, "rows": rows}

def lst(items):
    return {"type": "list", "items": items}

def grd(items):
    return {"type": "grid", "items": items}

def alrt(cls, icon, title, text):
    return {"type": "alert", "class": cls, "icon": icon, "title": title, "text": text}

def stps(items):
    return {"type": "steps", "items": items}

def proscons(pros, cons):
    return {"type": "proscons", "pros": pros, "cons": cons}

def crds(items):
    return {"type": "cards", "items": items}

def ptips(items):
    return {"type": "protips", "items": items}

def myt(items):
    return {"type": "myths", "items": items}


def solar_section():
    return [
        p("Solar charging is the most popular and practical way to charge a portable power station off-grid. It is silent, requires no fuel, and with enough panels, you can fully recharge even large stations in a single day of good sun. Every major portable power station brand supports solar charging via an MPPT charge controller built directly into the unit."),
        p("The basic setup is simple: connect one or more solar panels to the solar input port on your power station using the appropriate cable. The MPPT controller inside the station automatically converts the variable DC output from the panels into the correct voltage to charge the battery. Most stations display real-time solar wattage on the screen or in the companion app, so you can see exactly how much power you are getting at any moment."),
        p("How much solar do you actually need? It depends on your station's capacity and how fast you want to charge. As a general rule of thumb for real-world conditions:"),
        tbl(["Station Size", "100W Panel", "200W Panel", "400W Panel"], [
            ["500Wh", "7-9 hrs full sun", "3.5-5 hrs", "~2 hrs"],
            ["1,000Wh", "14-18 hrs", "7-9 hrs", "3.5-5 hrs"],
            ["2,000Wh", "28-36 hrs", "14-18 hrs", "7-9 hrs"],
            ["4,000Wh", "56+ hrs", "28+ hrs", "14-18 hrs"],
        ]),
        p("Real-world charging is usually slower than the math suggests due to suboptimal angle, temperature effects, partial shading, dust on panels, and panel inefficiency. Expect 70-80% of the panel's rated wattage in optimal conditions, and much less on cloudy days or early/late in the day. On a heavily overcast day, you might only get 10-20% of rated output."),
        lst([
            "MPPT (Maximum Power Point Tracking) is included in all modern power stations",
            "Most stations accept 12-60V or 12-100V solar input voltage",
            "Panels can be wired in series or parallel depending on voltage requirements",
            "Each brand uses different connectors (MC4, Anderson, XT60, proprietary)",
            "Solar charging works with pass-through on all modern stations",
        ]),
        alrt("info", "lightbulb", "Pro tip for maximum solar power", "Tilt your panels at roughly your latitude angle, face them directly south (in the northern hemisphere), and avoid any shading — even partial shading on one panel cell can drastically reduce output from the entire string. For best results, adjust the angle every 2-3 hours as the sun moves across the sky."),
    ]

def car_charging_section():
    return [
        p("Car charging is one of the most underrated off-grid charging methods. If you are driving anyway, you can top up your power station essentially for free using your vehicle's alternator. Most power stations come with a 12V car charger cable that plugs into the cigarette lighter / accessory port."),
        p("Charging speed from a car is typically 100-200W — slower than wall charging but steady and essentially free while you drive. A 1,000Wh station takes roughly 5-10 hours of driving to fully charge from a car. This makes it perfect for road trips where you drive during the day and use the power station at camp at night. You can arrive at your destination with a full battery without ever plugging into the grid."),
        p("Important considerations for car charging:"),
        lst([
            "Your car must be running to charge at full speed — with the engine off, you risk draining your car battery",
            "Most cars limit the 12V port to 100-150W even if your station can accept more",
            "Some power stations support faster charging via direct battery terminal connection",
            "Charging while driving puts minimal extra load on your alternator",
            "Check your car manual for the 12V port wattage limit before using",
            "Electric vehicles can also charge power stations from their 12V outlet",
        ]),
        crds([
            ("Gas Cars: Standard 12V", "green", "Most gas and diesel cars have a 12V accessory port that outputs 100-150W. This works for trickle-charging smaller power stations while you drive. It is not fast, but it is free if you are driving anyway. Perfect for adding a few hundred watt-hours on a road trip."),
            ("EVs: V2L / V2H", "electric", "Electric vehicles with Vehicle-to-Load (V2L) capability can output 120V/240V AC power from their main battery. This lets you charge a power station at full AC charging speed — much faster than a 12V port. Hyundai Ioniq 5, Kia EV6, and Ford F-150 Lightning all support this feature."),
            ("Direct Battery Connection", "yellow", "For faster 12V charging, connect directly to the car battery terminals with heavy-gauge wire and a fuse. This bypasses the 100-150W limit of the accessory port. Only do this if you know what you are doing — improper wiring can damage your car's electrical system or cause a fire."),
            ("Battery Isolators", "purple", "If you want to charge your power station from the car while parked for extended periods, install a battery isolator. It allows the alternator to charge both the car battery and your power station battery, but prevents the station from draining the car battery when the engine is off. Popular with overlanders and van lifers."),
        ]),
        alrt("warning", "alert-triangle", "Safety note about car batteries", "Never charge a power station from your car battery with the engine off for extended periods. You could drain the car battery enough that it will not start. If you need to charge while parked for a long time, use a battery isolator or start the engine every couple of hours to top up the car battery."),
    ]

def generator_section():
    return [
        p("When you need the fastest possible charging without grid power, a portable generator is the answer. Generators can charge even the largest power stations in 1-2 hours. They are the go-to option for emergency backup where speed matters more than fuel cost or noise, and they pair beautifully with solar for hybrid off-grid setups."),
        p("To charge with a generator, simply plug the power station's AC charging cable into the generator's AC outlet, exactly like you would plug into a wall. Most power stations charge at their maximum AC charge rate when connected to a generator — 500W to 3,000W depending on the model. The generator just needs to be able to supply more power than the station's max charge rate."),
        p("Generator sizing: you only need a generator that can output slightly more than your power station's maximum AC charge rate. For example, if your station charges at 1,800W max, a 2,000W generator is sufficient. You do not need a massive 5,000W generator just for charging — save the money and get something smaller and more fuel-efficient."),
        proscons(
            pros=[
                "Fastest charging speed available off-grid — fills the battery in hours, not days",
                "Works day or night, rain or shine, no sun or wind needed",
                "Portable — bring it anywhere you can drive or carry it",
                "Pair with solar for the ultimate hybrid off-grid system",
                "Widely available — you can buy a generator at any hardware store",
                "Multiple fuel options — gasoline, propane, dual-fuel, diesel",
            ],
            cons=[
                "Requires fuel which costs money and can be hard to store long-term",
                "Noisy — 60-90 dB typical — you will not want one right next to your tent",
                "Fuel storage and safety concerns — gas goes bad, propane tanks need care",
                "Ongoing fuel cost per kWh charged — much more expensive than solar over time",
                "Emissions — cannot use indoors or in enclosed spaces, carbon monoxide risk",
                "Regular maintenance required — oil changes, spark plugs, etc.",
            ]
        ),
        crds([
            ("Inverter Generators", "green", "Inverter generators produce clean, stable power that is safe for sensitive electronics. They are also quieter and more fuel-efficient than conventional generators. This is the type we recommend for charging power stations. 2,000-3,000W models are perfect for most power stations and use surprisingly little fuel at partial load."),
            ("Conventional Generators", "yellow", "Conventional generators are cheaper but noisier and produce dirty power. While they will charge a power station fine (the station's charger converts AC to DC anyway), they are not ideal for directly powering sensitive electronics. Stick with inverter generators if you can afford the upgrade — the difference in noise alone is worth it."),
            ("Dual Fuel Generators", "purple", "Dual fuel generators can run on gasoline or propane, giving you flexibility. Propane stores better long-term and burns cleaner, while gasoline is more widely available and produces slightly more power. Great for emergency preparedness where you want fuel flexibility and do not know what will be available."),
            ("Solar + Generator Hybrid", "electric", "The ultimate off-grid setup combines solar panels with a generator. Solar handles the daily charging for free, and the generator is there as backup for cloudy days or when you need a quick top-up. This gives you the best of both worlds — free, silent solar most of the time, with the speed and reliability of a generator when you need it."),
        ]),
        alrt("critical", "alert-octagon", "Critical generator safety", "Never run a generator indoors, in a garage, basement, or near open windows. Carbon monoxide poisoning from generators kills hundreds of people every year. Always place generators at least 20 feet from buildings with the exhaust pointed away from people and structures. Use a battery-powered CO detector nearby and never leave a running generator unattended for long periods."),
    ]

def wind_section():
    return [
        p("Wind charging is less common than solar for portable power stations but can be extremely useful in certain situations — particularly if you camp in consistently windy areas, sail, or need overnight charging. Small portable wind turbines (100-500W) can charge a power station directly, though most require a separate charge controller to properly regulate the power."),
        p("The biggest advantage of wind over solar is that it works at night and in cloudy weather. If you have consistent wind, a turbine can keep your battery topped up 24/7. The disadvantages are bulk, noise, and the fact that wind is less predictable than solar in most locations. Wind output also varies dramatically with wind speed — output is proportional to the cube of wind speed, so doubling the wind speed gives you 8x the power."),
        p("What to know about portable wind charging:"),
        lst([
            "Most portable wind turbines are 100-400W — roughly equivalent to 1-2 solar panels in good wind",
            "Output is highly dependent on wind speed — turbines are rated at specific wind speeds",
            "Real-world output is often 20-50% of rated power in typical camping wind conditions",
            "You need a proper charge controller between the turbine and power station",
            "Turbines must be mounted on a pole or tripod high enough to catch clean wind",
            "Wind + solar hybrid systems are the gold standard for long-term off-grid",
        ]),
        tbl(["Wind Speed (mph)", "100W Turbine", "200W Turbine", "400W Turbine"], [
            ["5 mph", "~3W", "~6W", "~12W"],
            ["10 mph", "~15W", "~30W", "~60W"],
            ["15 mph", "~50W", "~100W", "~200W"],
            ["20 mph", "~100W", "~200W", "~400W"],
            ["25 mph", "~150W", "~300W", "~600W"],
        ]),
        p("For most campers and casual users, solar is the better primary charging method. But if you spend a lot of time in consistently windy places like mountains, coasts, plains, or on a boat, adding a wind turbine to your setup can dramatically increase your off-grid independence. The best long-term off-grid setups combine both solar and wind for maximum reliability and consistent power day and night."),
    ]

def hand_crank_section():
    return [
        p("Hand crank charging is exactly what it sounds like — turning a crank by hand to generate electricity. While it sounds primitive and old-fashioned, it can be a genuine lifesaver in true emergency situations where you have no other options. That said, the amount of power you can actually generate by hand is surprisingly small, and it is nowhere near a practical daily charging method."),
        p("A healthy adult cranking vigorously can produce about 50-100W of mechanical power, which translates to roughly 20-50W of electrical power after losses in the generator and regulator. To put that in perspective: cranking for one hour might add 20-50Wh to your battery, enough for a few phone charges or a few minutes of AC power. It would take 20-50 hours of continuous cranking to charge a 1,000Wh station. That is multiple full days of hard physical work."),
        p("Hand crank and manual charging options for power stations:"),
        lst([
            "Built-in hand cranks: a few emergency-focused power stations have integrated cranks",
            "Portable crank generators: separate units that plug into your station, 30-100W output",
            "Bicycle generators: use a regular bike on a trainer stand to generate power, 50-200W",
            "Foot pedal generators: like small exercise bikes, 30-80W output, easier to sustain",
            "Water power (micro hydro): not human-powered but another off-grid option",
        ]),
        crds([
            ("Hand Crank Generators", "yellow", "Portable hand crank generators produce 20-50W of power when cranked vigorously. They are compact, lightweight, and require no fuel. But they are physically tiring — you cannot sustain high output for long. Best for emergency phone charging and small devices, not for charging a large power station. Think of them as a last resort."),
            ("Bicycle Generators", "green", "Bicycle generators (bike on a trainer stand) are the most efficient human-powered charging method. A fit person can produce 100-200W for extended periods. It is also a great workout! If you already have a bike, a generator trainer is a relatively inexpensive way to add human-powered charging to your off-grid setup."),
            ("Foot Pedal Generators", "purple", "Foot pedal generators are like small exercise bikes designed specifically for power generation. They produce 30-80W and are more portable than a full bike trainer. Easier on your body than hand cranking since you use your legs, which are much stronger. Good for emergency use but not practical for daily charging of large batteries."),
            ("Micro Hydro Power", "electric", "If you are camping near a stream or river, a micro hydro turbine can generate power 24/7 — no cranking required. Portable hydro units produce 10-500W depending on water flow and head (drop height). It is not human-powered, but it is another off-grid charging option to consider if you have moving water available at your campsite."),
        ]),
        alrt("warning", "alert-triangle", "Reality check on manual charging", "Hand crank charging is an emergency last resort, not a practical daily charging method. If you are considering buying a hand crank for regular use, save your money and buy an extra solar panel instead. You will get far more power with far less effort. Think of hand cranking as the fire extinguisher of charging — you hope you never need it, but it is good to have just in case."),
    ]

def other_charge_section():
    return [
        p("Beyond the main four methods (solar, car, generator, wind), there are several other ways to charge a power station without grid electricity. Some are practical, some are niche, and some are just fun to know about and experiment with. Here are the most interesting alternative charging methods available in 2026."),
        crds([
            ("Hydroelectric Charging", "green", "Small portable hydro turbines can charge from a stream or river if you camp near moving water. Like wind, hydro works 24/7 if you have consistent flow, and the output is very steady and predictable. Portable hydro turbines for power stations are available but not widely used, and you need a good-sized stream with decent flow and some drop (head) to get meaningful power. Output ranges from 10W for tiny turbines to 500W+ for larger units."),
            ("Thermoelectric Generators", "yellow", "Thermoelectric generators (TEGs) generate electricity from a temperature difference — typically from a wood stove or campfire. A TEG sits on your stove and uses the heat difference between the hot side (stove top) and cold side (air or water cooling) to produce power. Output is modest (10-50W) but can be useful if you are running a wood stove anyway for heat or cooking. Great for winter camping."),
            ("Fuel Cell Charging", "purple", "Hydrogen fuel cells are an emerging technology for portable power. They run on hydrogen canisters and produce electricity silently with only water as a byproduct — zero emissions, zero noise. Current portable fuel cells are expensive ($1,000+) and hydrogen is hard to find in most places, but they may become more common in the future as hydrogen infrastructure improves. Output ranges from 100-500W for portable units."),
            ("Battery Swapping", "electric", "Not exactly charging, but one of the fastest ways to get a full battery. Many modular power stations (like EcoFlow Delta Pro, Bluetti AC500, and Anker 555) let you swap battery modules. Bring extra fully-charged batteries from home and swap them as needed — zero charging time, just swap and go. It is expensive but incredibly convenient for short trips where you can pre-charge batteries at home."),
            ("Vehicle-to-Load (V2L)", "yellow", "If you have an electric car or truck with V2L capability (like the Hyundai Ioniq 5, Kia EV6, or Ford F-150 Lightning), you can plug your power station into the car's AC outlet and charge it from the car's massive battery. It is like having a giant 60-200 kWh power bank on wheels. Perfect for road trips in an EV — you can charge your power station from the car whenever you need to, even in the middle of nowhere."),
            ("Inductive / Wireless Charging", "info", "Wireless charging is starting to appear on some premium power stations. It works just like wireless phone charging but for the power station battery — place the station on a charging pad and it charges through induction. Convenient but slower than wired charging and less efficient overall. Not a primary charging method for most people, but a nice convenience feature for daily top-ups if you have a compatible charging pad."),
        ]),
        p("Which of these alternative methods is worth considering? It depends entirely on your situation. If you camp near a year-round stream, micro hydro is amazing. If you always have a campfire or wood stove, a thermoelectric generator gives you free power from heat you are already producing. If you drive an EV, V2L is game-changing for road trips. For most people though, solar + car + generator covers all the bases and these alternatives are fun to know about but not essential for most use cases."),
    ]

def charge_comparison_section():
    return [
        p("Here is how all the charging methods compare across key factors so you can choose the right mix for your specific needs and situation. There is no single best method — the best setup combines multiple methods for energy resilience."),
        tbl(["Method", "Charge Speed", "Upfront Cost", "Fuel Cost", "Portability", "Best For"], [
            ["Solar Panels", "Slow-Medium", "$$ ($200-800)", "$0", "Good", "Daily off-grid use"],
            ["Car Charging", "Slow", "$ ($20-50)", "Minimal", "Excellent", "Road trips"],
            ["Generator", "Very Fast", "$$ ($300-1500)", "High", "Good", "Emergency backup"],
            ["Wind Turbine", "Slow", "$$-$$$ ($300-1000)", "$0", "Fair", "Windy locations"],
            ["Hand Crank", "Very Slow", "$ ($50-200)", "$0", "Good", "Emergency only"],
            ["Fuel Cell", "Medium", "$$$$ ($1000+)", "Very High", "Good", "Specialized use"],
            ["Battery Swap", "Instant", "$$$$ ($500-3000)", "$0", "Fair", "Short trips with prep"],
            ["Hydroelectric", "Slow-Medium", "$$ ($300-800)", "$0", "Poor", "Riverside camping"],
            ["V2L (EV)", "Fast", "$$ (if you have EV)", "Low", "Excellent", "EV road trips"],
            ["Thermoelectric", "Very Slow", "$$ ($200-500)", "Low", "Good", "Stove/campfire heat"],
        ]),
        p("The best method for you depends entirely on your situation. For most people, solar + car charging covers 90% of off-grid scenarios. Add a generator if you need fast backup charging for emergencies or live in cloudy climates. The most resilient setups combine multiple methods so you always have a backup if one fails — this is called 'energy resilience' and it is the whole point of having multiple charging options available."),
        crds([
            ("Weekend Camping Setup", "green", "For weekend camping trips, 200-400W of solar panels + car charging to and from the campsite covers most people's needs. You arrive with a full battery, top up with solar during the day, and have enough power for lights, phones, a small fridge, and cooking devices. Budget: $300-800 total for panels and cables."),
            ("Week-Long Off-Grid", "yellow", "For week-long off-grid stays, you need more capacity and more charging. 400-800W of solar + a 2,000-4,000Wh station + a small generator for cloudy days is a solid setup. Solar handles the sunny days, generator handles the cloudy ones. Budget: $1,500-3,500 for the full system."),
            ("Full-Time Off-Grid", "electric", "For full-time off-grid living, go all-in: 800-1,600W of solar panels (or more), an expandable battery bank (4,000-8,000Wh+), a generator for backup, and possibly wind or hydro if you have the resources. Oversize everything by 50% for worst-case conditions. Budget: $3,000-10,000+ depending on size."),
            ("Emergency Home Backup", "red", "For emergency home backup, charging speed is critical. A generator is the fastest option — it can charge a large station in 1-2 hours. Pair with solar for daily trickle-charging to keep the battery topped up between outages. Make sure you have fuel stored safely for the generator. Budget: $500-2,000 depending on station size and generator quality."),
        ]),
    ]

def offgrid_tips_section():
    return [
        p("Whether you are a weekend camper or a full-time off-gridder, these strategies will help you get the most out of your off-grid charging setup and maximize your energy independence. Small optimizations add up to big improvements in runtime and reliability."),
        grd([
            ("Charge During Peak Sun Hours", "yellow", [
                "Solar panels produce the most power between 10 AM and 3 PM",
                "Plan high-power activities around this window",
                "Run appliances, charge devices, and fill the battery when sun is strongest",
                "Use pass-through charging to power devices directly from solar",
                "Save low-power activities for morning and evening hours",
            ]),
            ("Use a Proper Solar Mount", "green", [
                "Folding panels laid on the ground are convenient but inefficient",
                "Even a simple tilt mount can increase output by 20-30%",
                "Adjust the angle 2-3 times per day as the sun moves",
                "Consider a portable panel stand for optimal positioning",
                "Mount panels above ground to avoid shading from grass and rocks",
            ]),
            ("Combine Multiple Methods", "electric", [
                "The best off-grid setups use multiple charging methods",
                "Solar for daytime, generator for cloudy days or quick top-ups",
                "Car charging on travel days adds free power while you drive",
                "Having redundancy means you never run out of power",
                "Each charging method has its strengths — use all of them",
            ]),
            ("Monitor Your Usage Patterns", "info", [
                "Use your power station's app or display to track usage patterns",
                "Understanding daily consumption helps you size your system correctly",
                "Track solar input vs usage to see if you need more panels",
                "Set up low-battery alerts so you are never caught off guard",
                "Most stations show detailed usage history in the app",
            ]),
            ("Always Start With a Full Battery", "green", [
                "Always start your trip with a 100% charge from the grid",
                "Think of your battery as a full gas tank when you leave home",
                "Use alternative charging to extend your trip, not start from empty",
                "Top up whenever you have access to grid power",
                "Pre-charge spare batteries before your trip too if you have them",
            ]),
            ("Minimize Your Power Usage", "yellow", [
                "The easiest way to make battery last is to use less power",
                "Switch to LED lighting — it uses 10x less than incandescent",
                "Use efficient appliances and turn things off when not in use",
                "Every watt you save is a watt you do not need to generate",
                "ECO mode on your station can save 5-20% by eliminating vampire drain",
            ]),
        ]),
    ]

def protips_section():
    return [
        p("These advanced tips come from experienced off-grid users and solar professionals. They can take your charging setup from basic to truly optimized and help you get the most out of every watt of power you generate."),
        ptips([
            ("String Panels in Series for Longer Runs", "Most MPPT controllers support higher voltage solar inputs. Wiring panels in series (positive to negative) increases voltage and reduces current loss through long cables. This is especially important if your panels are far from your station — 20+ feet away. Higher voltage = less current = less loss in the wires. Check your station's maximum solar input voltage before wiring — you do not want to exceed it and damage the MPPT controller."),
            ("Use the Right Cable Gauge for the Job", "Thin cables cause voltage drop, especially with high current over long distances. Use 12AWG or thicker cables for solar runs longer than 10 feet. For runs over 20 feet, go with 10AWG. The thicker the cable, the more power actually reaches your battery instead of being lost as heat in the wire. This applies to both solar DC cables and AC extension cords from generators."),
            ("Clean Your Panels Regularly", "Dust, dirt, pollen, and bird droppings on solar panels can reduce output by 10-30%, sometimes more. Wipe them down with a soft cloth and water periodically — especially if you camp in dusty or wooded areas. Clean panels produce more power, which means faster charging and more energy independence. Rain helps, but it is not enough — a quick wipe every couple of weeks makes a noticeable difference."),
            ("Charge While You Drive on Road Trips", "On road trips, plug in your power station as soon as you start driving. Even 2-3 hours of driving can add significant charge to your battery. Combine with solar at camp and you might never need to plug into the grid at all. Just be careful not to drain your car battery when the engine is off — only charge while driving or with the engine running. This is free power you are already paying for in gas/electricity anyway."),
            ("Size Your System for Worst-Case Conditions", "When planning your off-grid setup, size your solar and battery for the worst conditions — shortest winter days, a full week of cloudy weather, higher-than-expected usage. Oversize by 30-50% and you will rarely run into trouble. It is better to have too much capacity than too little, especially if you rely on power for essential needs like medical devices or refrigeration."),
            ("Use Pass-Through Charging Wisely", "Most modern power stations support pass-through charging — using power while the battery charges. This means you can run devices directly from solar or generator power without draining the battery first, which is more efficient overall. Use pass-through for high-power devices during peak sun hours to save battery for nighttime and cloudy days. It also reduces battery wear since you cycle the battery less."),
            ("Keep the Battery Cool While Charging", "Heat is the enemy of battery life and charging speed. If you are charging in hot weather, keep the power station in shade if possible. Elevate it off hot surfaces like asphalt or hot ground. Make sure the cooling vents are clear and unobstructed. If it is extremely hot (over 95°F / 35°C), consider charging more slowly to reduce heat buildup and preserve battery health long-term."),
            ("Learn Your Station's Charge Curve", "Every power station charges at different speeds at different states of charge. Most charge fastest from 0-80% (constant current phase) and then slow down significantly for the last 20% (constant voltage phase). If you need a quick top-up, charging to 80% takes much less time than charging all the way to 100%. Plan accordingly — charge to 80% when you need speed, and let it top up to 100% when you have time."),
        ]),
    ]


# ===== FAQS =====

def standard_outdoor_faqs(topic, methods):
    """Generate 10 FAQs for outdoor power topics."""
    return [
        (f"What is the best way to charge a power station {topic}?", f"The best method depends on your situation, but solar panels are the most popular and cost-effective for most people. They are silent, have zero ongoing fuel cost, and work anywhere with sunlight. For faster charging when you need it, a generator is the quickest option. For road trips, car charging is very convenient. The ideal setup combines {methods} so you have options for any situation."),
        ("How long does it take to charge a power station with solar panels?", "It depends on the station size, panel wattage, and sun conditions. As a rough estimate, a 100W panel produces about 60-80W in real use. A 500Wh station takes 7-9 hours of good sun with a 100W panel. A 1,000Wh station takes 14-18 hours. A 2,000Wh station takes 28-36 hours. You get roughly 4-6 hours of peak sun per day, so multiple panels are needed for larger stations."),
        ("Can you charge a power station while using it?", "Yes, nearly all modern portable power stations support pass-through charging — you can use the output ports while the battery is charging simultaneously. Some budget models do not support this, or they limit output while charging, but all major brands (EcoFlow, Jackery, Bluetti, Anker) support full pass-through on their current models. This is very useful for running devices directly from solar without draining the battery."),
        ("What is MPPT and why does it matter?", "MPPT (Maximum Power Point Tracking) is a technology that maximizes the power output from solar panels by continuously finding the optimal voltage and current combination. It can increase charging efficiency by 20-30% compared to older PWM charge controllers, especially in partial shading, low-light conditions, or when panels are at suboptimal angles. All modern power stations use MPPT technology."),
        ("Will car charging drain my car battery?", "If your engine is running, no — the alternator powers the charging and keeps the car battery topped up at the same time. If the engine is off, yes, charging will slowly drain your car battery. Most car ports shut off automatically when the ignition is off, but some do not. To be safe, only charge from your car while the engine is running, or use a battery isolator if you need stationary charging while parked for extended periods."),
        ("How many solar panels do I need for my power station?", "It depends on how fast you want to charge and how much sun you get. For a full charge in one day (5-6 hours of peak sun), divide your station's Wh capacity by 5 to get the minimum panel wattage needed. For example, a 2,000Wh station needs roughly 400W of panels for a one-day charge. Always oversize slightly for real-world conditions — panel output is rarely 100% of rated power."),
        ("Can I use any brand of solar panels with my power station?", "Generally yes, as long as the panel's voltage is within your station's acceptable input range and you have the right connector. Most stations accept 12-60V or 12-100V solar input. You may need an adapter cable if your panel uses a different connector (MC4, Anderson, XT60, etc.). Check your station's manual for the exact voltage range and supported connector types before buying third-party panels."),
        ("How do I charge my power station during a blackout?", "During a blackout, your options depend on what you have prepared ahead of time. Solar panels work as long as the sun is out, even in a blackout. A generator can charge it anytime you have fuel. If you have an electric car with vehicle-to-load (V2L), you can use it as a giant power source. The key is to plan ahead — have your charging method ready and tested before the blackout hits, not after the power goes out."),
        ("Is it cheaper to charge with solar or a generator?", "Solar is much cheaper over the long term despite the higher upfront cost. Once you buy the panels, the energy is free forever. A 400W solar panel setup costs about $400-600 and will last 20+ years. A generator costs about the same upfront but then costs $0.50-1.00 per kWh in fuel. If you use it regularly, solar pays for itself in 1-3 years and is essentially free after that. Generator is cheaper only for very infrequent use."),
        ("What is the fastest way to charge a power station off-grid?", "A gas or propane generator is the fastest way to charge a portable power station without grid power. Most generators can supply enough power to charge a station at its maximum AC charge rate — typically 500-3,000W depending on the model. A 2,000Wh station with 1,800W charging can go from 0-80% in about an hour with a sufficiently sized generator. Multi-source charging (solar + AC at the same time) is even faster if your station supports it."),
    ]


# ===== RELATED PAGES =====

def outdoor_related():
    return [
        ("can-portable-power-station-charge-while-in-use.html", "PASS-THROUGH", "All Brands", "Pass-Through Charging Guide", "Can a power station charge and discharge at the same time? How pass-through works and its limitations."),
        ("solar-charging-0w-power-station.html", "SOLAR&nbsp;0W", "Universal", "Solar 0W Troubleshooting", "Fix solar charging showing 0 watts — MPPT issues, wiring problems, and panel faults."),
        ("portable-power-station-not-charging.html", "CHARGE&nbsp;FAULT", "Universal", "Not Charging Guide", "Troubleshoot AC, solar, and DC charging problems for all major brands."),
        ("portable-power-station-eco-mode.html", "ECO&nbsp;MODE", "All Brands", "ECO Mode Guide", "Save battery with ECO mode — how it works, how much it saves, and how to configure it."),
        ("lifepo4-vs-lithium-ion-power-station.html", "BATTERY", "Compare", "LiFePO4 vs Lithium-Ion", "Complete comparison of battery chemistries — lifespan, safety, cost, weight."),
        ("outdoor-power.html", "COMPARE", "All Brands", "Power Station Comparison", "Compare all major portable power station models side by side by capacity, output, and price."),
    ]


# ===== MAIN =====

def main():
    print("Generating 20 SEO pages for TechSpecsHub...\n")
    
    pages = get_pages()
    total_words = 0
    
    for i, page_data in enumerate(pages):
        wc = generate_page(page_data)
        total_words += wc
        print(f"  [{i+1:02d}] {wc:>5,} words - {page_data['filename']}")
    
    print(f"\n{'='*60}")
    print(f"  Generated: {len(pages)} pages")
    print(f"  Total words: {total_words:,}")
    print(f"  Average: {total_words//len(pages):,} words per page")
    print(f"{'='*60}")


def generate_page(d):
    return generate_page_func(
        d["filename"], d["title"], d["meta_desc"], d["category"], d["cat_page"],
        d["breadcrumb"], d["badges"], d["hero_title"], d["hero_intro"], d["hero_stats"],
        d["quick_title"], d["quick_text"], d["toc"], d["sections"], d["faqs"], d["related"]
    )

# We need to import/use the generate_page function from earlier
# Let's define it here for completeness
generate_page_func = generate_page if 'generate_page' in globals() else None

if __name__ == "__main__":
    # We'll use the generate_page function from the module scope
    # For now, just print a message
    print("This module contains page data. Run from the main generation script.")
