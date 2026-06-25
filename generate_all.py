#!/usr/bin/env python3
"""
Generate all 20 high-quality SEO pages for TechSpecsHub.
Each page: 3000+ words, full SEO, matching the eco-mode template exactly.
"""

import os
import json
import re
from typing import List, Dict, Any

OUTPUT_DIR = "/workspace/pages/specs"
BASE_URL = "https://powerspecshub.com/pages/specs"
SITE_NAME = "TechSpecsHub"
UPDATED_DATE = "2026-06-25"

# ==================== UTILS ====================

def strip_html(text):
    return re.sub(r'<[^>]+>', ' ', text)

def word_count(html_text):
    text = strip_html(html_text)
    text = re.sub(r'\s+', ' ', text).strip()
    return len(text.split())

def p(text):
    return f'<p class="text-gray-300 leading-relaxed mb-4">{text}</p>'

def ul(items):
    lis = "".join(f"<li>• {x}</li>" for x in items)
    return f'<ul class="text-sm text-gray-300 space-y-1 mb-4">{lis}</ul>'

def table(headers, rows):
    thead = "".join(f"<th>{h}</th>" for h in headers)
    tbody = ""
    for row in rows:
        tbody += "<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>"
    return f'<div class="overflow-x-auto mb-6"><table class="specs-table w-full text-sm"><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table></div>'

def alert(atype, text):
    icon_map = {"info":"lightbulb","warning":"alert-triangle","critical":"alert-octagon","success":"check-circle"}
    icon = icon_map.get(atype, "info")
    return f'<div class="mt-4 alert alert-{atype}"><i data-lucide="{icon}" style="width:1rem;height:1rem;flex-shrink:0;margin-top:0.1rem"></i><p class="text-sm">{text}</p></div>'

def grid(cards, cols=2):
    cards_html = ""
    for c in cards:
        tc = c.get("title_color", "electric-400")
        cards_html += f'<div class="bg-navy-900/80 border border-white/10 rounded-xl p-5"><h4 class="font-semibold text-{tc} mb-2">{c["title"]}</h4><p class="text-sm text-gray-300 mb-2">{c["body"]}</p></div>'
    return f'<div class="grid md:grid-cols-{cols} gap-4 mb-4">{cards_html}</div>'

def steps(slist, color="green"):
    html = ""
    for i, s in enumerate(slist, 1):
        html += f'<div class="flex items-start gap-3"><div class="w-10 h-10 bg-{color}-500/20 rounded-full flex items-center justify-center flex-shrink-0"><span class="font-mono font-bold text-{color}-400">{i}</span></div><div><h4 class="font-semibold text-white">{s["title"]}</h4><p class="text-sm text-gray-400">{s["body"]}</p></div></div>'
    return f'<div class="space-y-4 mb-6">{html}</div>'

def pros_cons(pros, cons):
    ph = "".join(f'<li class="flex items-start gap-2"><i data-lucide="check" style="width:1rem;height:1rem;color:#4ade80;flex-shrink:0;margin-top:0.1rem"></i><span>{x}</span></li>' for x in pros)
    ch = "".join(f'<li class="flex items-start gap-2"><i data-lucide="x" style="width:1rem;height:1rem;color:#f87171;flex-shrink:0;margin-top:0.1rem"></i><span>{x}</span></li>' for x in cons)
    return f'<div class="grid md:grid-cols-2 gap-6 mb-4"><div><h3 class="font-bold text-xl mb-4 text-green-400 flex items-center gap-2"><i data-lucide="check-circle" style="width:1.25rem;height:1.25rem"></i>Pros</h3><ul class="space-y-3 text-sm text-gray-300">{ph}</ul></div><div><h3 class="font-bold text-xl mb-4 text-red-400 flex items-center gap-2"><i data-lucide="x-circle" style="width:1.25rem;height:1.25rem"></i>Cons</h3><ul class="space-y-3 text-sm text-gray-300">{ch}</ul></div></div>'


# ==================== HTML BUILDER ====================

def build_page(page):
    """Build complete HTML page from page data dict."""

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
        "mainEntity": [{"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in page["faqs"]]
    }
    bc_url = f"{BASE_URL}/{page['cat_url']}"
    breadcrumb_json = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://powerspecshub.com/"},
            {"@type": "ListItem", "position": 2, "name": page["cat_name"], "item": bc_url},
            {"@type": "ListItem", "position": 3, "name": page["bc_name"]}
        ]
    }

    # Head
    head = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{page['title']} | {SITE_NAME}</title>
  <meta name="description" content="{page['meta_desc']}">
  <meta name="theme-color" content="#0a1628">
  <style>html,body{{background-color:#0a1628;color:#ffffff;margin:0;padding:0;min-height:100vh;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;line-height:1.5;-webkit-font-smoothing:antialiased}}a{{color:#22d3ee;text-decoration:none}}code,pre{{font-family:ui-monospace,monospace}}</style>
  <link rel="preconnect" href="https://cdn.tailwindcss.com">
  <link rel="preconnect" href="https://unpkg.com">
  <link rel="dns-prefetch" href="https://cdn.tailwindcss.com">
  <link rel="dns-prefetch" href="https://unpkg.com">
  <link rel="dns-prefetch" href="https://fonts.gstatic.com">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <link rel="canonical" href="{BASE_URL}/{page['filename']}">
  <meta property="og:title" content="{page['title']} | {SITE_NAME}">
  <meta property="og:description" content="{page['meta_desc']}">
  <meta property="og:type" content="Article">
  <meta property="og:url" content="{BASE_URL}/{page['filename']}">
  <meta property="og:image" content="https://powerspecshub.com/assets/images/og-default.png">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="article:published_time" content="{UPDATED_DATE}T00:00:00Z">
  <meta property="article:modified_time" content="{UPDATED_DATE}T00:00:00Z">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{page['title']} | {SITE_NAME}">
  <meta name="twitter:description" content="{page['meta_desc']}">
  <meta name="twitter:image" content="https://powerspecshub.com/assets/images/og-default.png">
  <meta name="twitter:site" content="@TechSpecsHub">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com" defer></script>
  <script>
    tailwind.config = {{ theme: {{ extend: {{
      colors: {{ navy: {{950:'#0a1628',900:'#0f1d32',800:'#162544',700:'#1e3259'}}, electric: {{300:'#67e8f9',400:'#22d3ee',500:'#06b6d4',600:'#0891b2'}} }},
      fontFamily: {{ display: ['Space Grotesk','system-ui','sans-serif'], mono: ['JetBrains Mono','monospace'] }}
    }} }} }}
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

    # Body start with header (same for all pages)
    body_header = open("/workspace/pages/specs/portable-power-station-eco-mode.html").read().split("<!-- BREADCRUMB -->")[0].split("</head>")[1]

    # Breadcrumb
    breadcrumb = f'''
  <!-- BREADCRUMB -->
  <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 pb-4">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="../../index.html">Home</a>
      <span class="breadcrumb-sep">/</span>
      <a href="{page['cat_url']}">{page['cat_name']}</a>
      <span class="breadcrumb-sep">/</span>
      <span class="breadcrumb-current">{page['bc_name']}</span>
    </nav>
  </div>
'''

    # Hero
    badges_html = ""
    for b in page["badges"]:
        badges_html += f'<span class="badge badge-{b["color"]}"><i data-lucide="{b["icon"]}" style="width:0.75rem;height:0.75rem"></i>{b["text"]}</span>\n        '
    stats_html = ""
    for s in page["stats"]:
        stats_html += f'''        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="{s['icon']}" style="width:0.9rem;height:0.9rem"></i>{s['label']}</div>
          <div class="font-mono font-bold text-xl text-{s['vc']}">{s['val']}</div>
        </div>\n'''
    hero = f'''  <!-- HERO -->
  <section class="relative max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-4 pb-6">
    <div class="glass-card p-8 md:p-10 overflow-hidden relative">
      <div class="absolute top-0 right-0 w-[420px] h-[420px] bg-{page['accent']}-500/5 rounded-full blur-3xl pointer-events-none"></div>
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
    qa = f'''  <!-- QUICK ANSWER -->
  <section class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div class="glass-card p-6 md:p-8 bg-gradient-to-br from-{page['accent']}-950/20 to-navy-900 border-{page['accent']}-500/20">
      <h2 class="font-bold text-2xl mb-4 flex items-center gap-2"><i data-lucide="zap" style="width:1.25rem;height:1.25rem;color:#4ade80"></i>Quick Answer</h2>
      <p class="text-gray-300 leading-relaxed mb-4">
        {page['quick_answer']}
      </p>
    </div>
  </section>
'''

    # TOC
    toc_items = ""
    for i, t in enumerate(page["toc"], 1):
        num = f"{i:02d}"
        toc_items += f'        <a href="#{t["id"]}" class="flex items-center gap-2 p-2 rounded-lg hover:bg-white/5 text-gray-300 hover:text-white transition-all"><span class="text-electric-400 font-mono">{num}</span>{t["title"]}</a>\n'
    toc_sec = f'''  <!-- TABLE OF CONTENTS -->
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
    sections_html = ""
    for sec in page["sections"]:
        content = "\n".join(sec["parts"])
        sections_html += f'''  <section id="{sec["id"]}" class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
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
          <span>{f["q"]}</span>
          <i data-lucide="chevron-down" style="width:1rem;height:1rem" class="text-gray-500 group-open:rotate-180 transition-transform flex-shrink-0"></i>
        </summary>
        <p class="mt-3 text-gray-400 text-sm leading-relaxed">
          {f["a"]}
        </p>
      </details>\n'''
    faq_sec = f'''  <!-- FAQ -->
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

    # Related
    rel_html = ""
    for r in page["related"]:
        bc = r.get("badge_color", "electric")
        bt = r.get("badge_text", "GUIDE")
        sb = r.get("sub_badge", "All Brands")
        rel_html += f'''      <a href="{r["url"]}" class="glass-card p-6 block hover:border-electric-400/50 transition-all group">
        <div class="flex items-start gap-3 mb-3">
          <div class="px-2.5 py-1 bg-{bc}-500/20 text-{bc}-400 font-mono font-semibold text-sm rounded-md border border-{bc}-500/30">{bt}</div>
          <span class="badge badge-info">{sb}</span>
        </div>
        <h3 class="font-bold text-lg mb-2 group-hover:text-electric-400 transition-colors">{r["title"]}</h3>
        <p class="text-sm text-gray-400">{r["desc"]}</p>
      </a>\n'''
    rel_sec = f'''  <!-- RELATED GUIDES -->
  <section id="related" class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h2 class="font-bold text-3xl mb-5">Related Guides &amp; Resources</h2>
    <div class="grid md:grid-cols-3 gap-4">
{rel_html.rstrip()}
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

    return head + body_header + breadcrumb + hero + qa + toc_sec + sections_html + faq_sec + rel_sec + footer


# ==================== PAGE DATA ====================

def get_pages():
    """Return list of all 20 page data dicts."""
    pages = []

    # ===== OUTDOOR POWER =====

    # Page 1: already exists - skip but include for count
    # We'll regenerate it too for consistency

    pages.append({
        "filename": "how-to-charge-power-station-without-electricity.html",
        "title": "How to Charge a Portable Power Station Without Electricity (2026)",
        "meta_desc": "Complete guide to charging portable power stations without grid electricity: solar panels, car charging, generators, wind power, hand cranks, and off-grid strategies for EcoFlow, Jackery, Bluetti, and more.",
        "headline": "How to Charge a Portable Power Station Without Electricity (2026)",
        "hero_title": "How to Charge a Portable Power Station Without Electricity",
        "bc_name": "Charging Without Electricity",
        "cat_name": "Outdoor Power",
        "cat_url": "outdoor-power.html",
        "accent": "green",
        "badges": [
            {"icon":"battery-charging","text":"OFF-GRID","color":"green"},
            {"icon":"sun","text":"Solar & More","color":"info"},
            {"icon":"layers","text":"All Brands","color":"info"},
        ],
        "stats": [
            {"icon":"zap","label":"Fastest Method","val":"Generator","vc":"yellow-400"},
            {"icon":"battery-charging","label":"Most Popular","val":"Solar Panels","vc":"green-400"},
            {"icon":"activity","label":"Most Portable","val":"Car Charging","vc":"electric-400"},
            {"icon":"alert-triangle","label":"Slowest Method","val":"Hand Crank","vc":"red-400"},
        ],
        "hero_intro": "Whether you are camping off-grid, preparing for a long-term power outage, or living a fully off-grid lifestyle, knowing how to charge your power station without access to wall electricity is essential. Solar is the most popular method, but it is far from the only one. This guide covers every charging method available — from rooftop solar to car charging, generators, wind turbines, hand cranks, and even more creative solutions. We break down the pros, cons, costs, and charging speeds of each method so you can build the ultimate off-grid charging setup for any situation.",
        "quick_answer": "The most practical way to charge a portable power station without grid electricity is using solar panels — they are silent, have zero fuel cost, and work anywhere with sunlight. For faster charging, a gas or propane generator fills the battery quickest but requires fuel and makes noise. For road trips, car charging via the 12V port works while you drive. Wind turbines, hand cranks, and fuel cells are niche options for specific use cases. The best setup for most people combines solar for daily use with a generator or car charging as backup.",
        "toc": [
            {"id":"solar","title":"Solar Panel Charging (Most Popular)"},
            {"id":"car","title":"Car / Vehicle Charging"},
            {"id":"generator","title":"Gas & Propane Generator Charging"},
            {"id":"wind","title":"Wind Turbine Charging"},
            {"id":"hand","title":"Hand Crank & Manual Charging"},
            {"id":"other","title":"Other Creative Charging Methods"},
            {"id":"compare","title":"Method Comparison & Speed Chart"},
            {"id":"offgrid","title":"Off-Grid Charging Strategies"},
            {"id":"pro","title":"Pro Tips & Advanced Techniques"},
            {"id":"faq","title":"Frequently Asked Questions"},
            {"id":"related","title":"Related Guides"},
        ],
        "sections": [
            {"id":"solar","title":"Solar Panel Charging — The Most Popular Off-Grid Method",
             "parts":[
                p("Solar charging is the most popular and practical way to charge a portable power station off-grid. It is silent, requires no fuel, and with enough panels, you can fully recharge even large stations in a single day of good sun. Every major portable power station brand supports solar charging via an MPPT charge controller built directly into the unit."),
                p("The basic setup is simple: connect one or more solar panels to the solar input port on your power station using the appropriate cable. The MPPT controller inside the station automatically converts the variable DC output from the panels into the correct voltage to charge the battery. Most stations display real-time solar wattage on the screen or in the companion app, so you can see exactly how much power you are getting."),
                p("How much solar do you actually need? It depends on your station's capacity and how fast you want to charge. As a general rule of thumb for real-world conditions (not lab conditions):"),
                table(["Station Size","100W Panel","200W Panel","400W Panel"],[
                    ["500Wh","7-9 hrs full sun","3.5-5 hrs","~2 hrs"],
                    ["1,000Wh","14-18 hrs","7-9 hrs","3.5-5 hrs"],
                    ["2,000Wh","28-36 hrs","14-18 hrs","7-9 hrs"],
                    ["4,000Wh","56+ hrs","28+ hrs","14-18 hrs"],
                ]),
                p("Real-world charging is usually slower than the math suggests due to suboptimal angle, temperature effects, partial shading, and panel inefficiency. Expect 70-80% of the panel's rated wattage in optimal conditions, and much less on cloudy days or early/late in the day."),
                alert("info","Pro tip for maximum solar: Tilt your panels at roughly your latitude angle, face them directly south (in the northern hemisphere), and avoid any shading — even partial shading on one panel cell can drastically reduce output from the entire string. For best results, adjust the angle every 2-3 hours as the sun moves."),
             ]},
            {"id":"car","title":"Car & Vehicle Charging — Great for Road Trips",
             "parts":[
                p("Car charging is one of the most underrated off-grid charging methods. If you are driving anyway, you can top up your power station essentially for free using your vehicle's alternator. Most power stations come with a 12V car charger cable that plugs into the cigarette lighter / accessory port."),
                p("Charging speed from a car is typically 100-200W — slower than wall charging but steady and essentially free while you drive. A 1,000Wh station takes roughly 5-10 hours of driving to fully charge from a car. This makes it perfect for road trips where you drive during the day and use the power station at camp at night. You can arrive at your destination with a full battery without ever plugging into the grid."),
                p("Important considerations for car charging:"),
                ul([
                    "Your car must be running to charge at full speed — with the engine off, you risk draining your car battery",
                    "Most cars limit the 12V port to 100-150W even if your station can accept more",
                    "Some power stations support faster charging via direct battery terminal connection (Anderson plugs or alligator clips)",
                    "Charging while driving puts minimal extra load on your alternator — usually not a concern for modern cars",
                    "Check your car manual for the 12V port wattage limit before using high-power charging",
                    "Electric vehicles can also charge power stations from their 12V outlet, though efficiency is lower than charging directly from the traction battery via V2L if available",
                ]),
                alert("warning","Safety note about car batteries: Never charge a power station from your car battery with the engine off for extended periods. You could drain the car battery enough that it will not start. If you need to charge while parked for a long time, use a battery isolator or start the engine every couple of hours to top up the car battery."),
             ]},
            {"id":"generator","title":"Generator Charging — The Fastest Off-Grid Method",
             "parts":[
                p("When you need the fastest possible charging without grid power, a portable generator is the answer. Generators can charge even the largest power stations in 1-2 hours. They are the go-to option for emergency backup where speed matters more than fuel cost or noise, and they pair beautifully with solar for hybrid off-grid setups."),
                p("To charge with a generator, simply plug the power station's AC charging cable into the generator's AC outlet, exactly like you would plug into a wall. Most power stations charge at their maximum AC charge rate when connected to a generator — 500W to 3,000W depending on the model. The generator just needs to be able to supply more power than the station's max charge rate."),
                p("Generator sizing: you only need a generator that can output slightly more than your power station's maximum AC charge rate. For example, if your station charges at 1,800W max, a 2,000W generator is sufficient. You do not need a massive 5,000W generator just for charging — save the money and get something smaller and more fuel-efficient."),
                pros_cons(
                    ["Fastest charging speed available off-grid","Works day or night, rain or shine, no sun needed","Portable — bring it anywhere you can drive","Pair with solar for the ultimate hybrid off-grid system","Widely available — you can buy a generator anywhere"],
                    ["Requires fuel (gasoline, propane, or diesel)","Noisy — 60-90 dB typical depending on size and load","Fuel storage and safety concerns — gas goes bad, propane tanks need care","Ongoing fuel cost per kWh charged (typically $0.30-0.80/kWh)","Emissions — cannot use indoors or in enclosed spaces","Regular maintenance required for reliable operation"]
                ),
                alert("critical","Critical generator safety: Never run a generator indoors, in a garage, basement, or near open windows. Carbon monoxide poisoning from generators kills hundreds of people every year. Always place generators at least 20 feet from buildings with the exhaust pointed away from people and structures. Use a battery-powered CO detector nearby."),
             ]},
            {"id":"wind","title":"Wind Turbine Charging — Niche but Useful",
             "parts":[
                p("Wind charging is less common than solar for portable power stations but can be extremely useful in certain situations — particularly if you camp in consistently windy areas, sail, or need overnight charging. Small portable wind turbines (100-500W) can charge a power station directly, though most require a separate charge controller to properly regulate the power."),
                p("The biggest advantage of wind over solar is that it works at night and in cloudy weather. If you have consistent wind, a turbine can keep your battery topped up 24/7. The disadvantages are bulk, noise, and the fact that wind is less predictable than solar in most locations. Wind output also varies dramatically with wind speed — output is proportional to the cube of wind speed, so doubling the wind speed gives you 8x the power."),
                p("What to know about portable wind charging:"),
                ul([
                    "Most portable wind turbines are 100-400W — roughly equivalent to 1-2 solar panels in good wind",
                    "Output is highly dependent on wind speed — turbines are rated at specific wind speeds (usually 10-15 m/s or 22-33 mph)",
                    "Real-world output is often 20-50% of rated power in typical camping wind conditions (5-10 mph)",
                    "You need a proper charge controller between the turbine and power station to prevent overcharging",
                    "Turbines must be mounted on a pole or tripod high enough to catch clean, undisturbed wind (at least 20-30 feet high ideally)",
                    "Portability varies — some fold up small enough to fit in a backpack, others are quite bulky and heavy",
                    "Wind + solar hybrid systems are the gold standard for long-term off-grid — solar handles the day, wind handles the night",
                ]),
                p("For most campers and casual users, solar is the better primary charging method. But if you spend a lot of time in consistently windy places like mountains, coasts, or plains, adding a wind turbine to your setup can dramatically increase your off-grid independence."),
             ]},
            {"id":"hand","title":"Hand Crank & Manual Charging — Emergency Only",
             "parts":[
                p("Hand crank charging is exactly what it sounds like — turning a crank by hand to generate electricity. While it sounds primitive and old-fashioned, it can be a genuine lifesaver in true emergency situations where you have no other options. That said, the amount of power you can actually generate by hand is surprisingly small, and it is nowhere near a practical daily charging method."),
                p("A healthy adult cranking vigorously can produce about 50-100W of mechanical power, which translates to roughly 20-50W of electrical power after losses in the generator and regulator. To put that in perspective: cranking for one hour might add 20-50Wh to your battery, enough for a few phone charges or a few minutes of AC power. It would take 20-50 hours of continuous cranking to charge a 1,000Wh station. That is multiple full days of hard work."),
                p("Hand crank options for power stations:"),
                ul([
                    "<strong class=\"text-white\">Built-in hand cranks:</strong> a few emergency-focused power stations have integrated cranks, usually 10-30W max output",
                    "<strong class=\"text-white\">Portable crank generators:</strong> separate units that plug into your station, 30-100W output depending on size and how fast you crank",
                    "<strong class=\"text-white\">Bicycle generators:</strong> use a regular bike on a trainer stand to generate power, 50-200W depending on fitness level — much more efficient than hand cranking",
                    "<strong class=\"text-white\">Emergency radios with cranks:</strong> tiny cranks designed for radios and phone charging, not useful for power stations",
                    "<strong class=\"text-white\">Foot pedal generators:</strong> like a stationary bike but smaller, 30-80W output, easier to sustain than hand cranking",
                ]),
                alert("warning","Reality check on manual charging: Hand crank charging is an emergency last resort, not a practical daily charging method. If you are considering buying a hand crank for regular use, save your money and buy an extra solar panel instead. You will get far more power with far less effort. Think of hand cranking as the fire extinguisher of charging — you hope you never need it, but it is good to have just in case."),
             ]},
            {"id":"other","title":"Other Creative Charging Methods",
             "parts":[
                p("Beyond the main four methods (solar, car, generator, wind), there are several other ways to charge a power station without grid electricity. Some are practical, some are niche, and some are just fun to know about and experiment with."),
                p("Hydroelectric charging: Small portable hydro turbines can charge from a stream or river if you camp near moving water. Like wind, hydro works 24/7 if you have consistent flow, and the output is very steady. Portable hydro turbines for power stations are available but not widely used, and you need a good-sized stream with decent flow to get meaningful power."),
                p("Thermoelectric generators: These generate electricity from a temperature difference — typically from a wood stove or campfire. A thermoelectric generator sits on your stove and uses the heat difference between the hot side (stove top) and cold side (air or water cooling) to produce power. Output is modest (10-50W) but can be useful if you are running a wood stove anyway for heat or cooking."),
                p("Fuel cell charging: Hydrogen fuel cells are an emerging technology for portable power. They run on hydrogen canisters and produce electricity silently with only water as a byproduct. Current portable fuel cells are expensive and hydrogen is hard to find in most places, but they may become more common in the future as hydrogen infrastructure improves."),
                p("Battery swapping: Not exactly charging, but one of the fastest ways to get a full battery. Many modular power stations (like EcoFlow Delta Pro, Bluetti AC500, and Anker 555) let you swap battery modules. Bring extra fully-charged batteries from home and swap them as needed — zero charging time, just swap and go. It is expensive but incredibly convenient for short trips."),
                p("Vehicle-to-Load (V2L): If you have an electric car or truck with V2L capability (like the Hyundai Ioniq 5, Kia EV6, or Ford F-150 Lightning), you can plug your power station into the car's AC outlet and charge it from the car's massive battery. It is like having a giant 60-200 kWh power bank on wheels."),
             ]},
            {"id":"compare","title":"Method Comparison — Speed, Cost, and Practicality",
             "parts":[
                p("Here is how all the charging methods compare across key factors so you can choose the right mix for your needs:"),
                table(["Method","Charge Speed","Upfront Cost","Fuel Cost","Portability","Best For"],[
                    ["Solar Panels","Slow-Medium","$$ ($200-800)","$0","Good","Daily off-grid use"],
                    ["Car Charging","Slow","$ ($20-50)","Minimal","Excellent","Road trips"],
                    ["Generator","Very Fast","$$ ($300-1500)","High","Good","Emergency backup"],
                    ["Wind Turbine","Slow","$$-$$$ ($300-1000)","$0","Fair","Windy locations"],
                    ["Hand Crank","Very Slow","$ ($50-200)","$0","Good","Emergency only"],
                    ["Fuel Cell","Medium","$$$$ ($1000+)","Very High","Good","Specialized use"],
                    ["Battery Swap","Instant","$$$$ ($500-3000)","$0","Fair","Short trips with prep"],
                    ["Hydroelectric","Slow-Medium","$$ ($300-800)","$0","Poor","Riverside camping"],
                ]),
                p("The best method for you depends entirely on your situation. For most people, solar + car charging covers 90% of off-grid scenarios. Add a generator if you need fast backup charging for emergencies or live in cloudy climates. The most resilient setups combine multiple methods so you always have a backup if one fails."),
             ]},
            {"id":"offgrid","title":"Off-Grid Charging Strategies & Tips",
             "parts":[
                p("Whether you are a weekend camper or a full-time off-gridder, these strategies will help you get the most out of your off-grid charging setup and maximize your energy independence."),
                grid([
                    {"title":"Charge During Peak Sun","title_color":"yellow-400","body":"Solar panels produce the most power between 10 AM and 3 PM. Plan high-power activities around this window. Run appliances, charge devices, and fill the battery when sun is strongest. Use pass-through charging to power devices directly from solar."},
                    {"title":"Use a Proper Solar Mount","title_color":"green-400","body":"Folding panels laid on the ground are convenient but inefficient. Even a simple tilt mount can increase output by 20-30%. For best results, adjust the angle 2-3 times per day as the sun moves. Consider a portable panel stand for optimal positioning."},
                    {"title":"Combine Multiple Methods","title_color":"electric-400","body":"The best off-grid setups use multiple charging methods. Solar for daytime, generator for cloudy days or quick top-ups. Car charging on travel days adds free power while you drive. Having redundancy means you never run out of power."},
                    {"title":"Monitor Your Usage","title_color":"purple-400","body":"Use your power station's app or display to track usage patterns. Understanding daily consumption helps you size your system correctly. Track solar input vs usage to see if you need more panels. Set up low-battery alerts so you are never caught off guard."},
                    {"title":"Start With a Full Battery","title_color":"green-400","body":"Always start your trip with a 100% charge from the grid. Think of your battery as a full gas tank when you leave home. Use alternative charging to extend your trip, not start from empty. Top up whenever you have access to grid power."},
                    {"title":"Minimize Power Use","title_color":"yellow-400","body":"The easiest way to make battery last is to use less power. Switch to LED lighting — it uses 10x less than incandescent. Use efficient appliances and turn things off when not in use. Every watt you save is a watt you do not need to generate."},
                ]),
             ]},
            {"id":"pro","title":"Pro Tips & Advanced Techniques",
             "parts":[
                grid([
                    {"title":"Dual-Source Charging","title_color":"electric-400","body":"Most modern power stations support simultaneous charging from multiple sources (e.g. solar + AC, solar + car). Using two sources at once fills the battery faster than any single source alone. This is great for cloudy days or when you are in a hurry."},
                    {"title":"MPPT vs PWM","title_color":"green-400","body":"All modern power stations use MPPT (Maximum Power Point Tracking) charge controllers, which are 20-30% more efficient than older PWM controllers, especially in partial shading or low light. If you have an older station with PWM, consider upgrading for much better solar performance."},
                    {"title":"Panel Tilt Angle Formula","title_color":"yellow-400","body":"For fixed panels, the optimal tilt angle is roughly your latitude ±15° depending on season. In winter, add 15° for lower sun. In summer, subtract 15° for higher sun. Adjust monthly for best year-round performance."},
                    {"title":"Series vs Parallel Panels","title_color":"purple-400","body":"Wiring panels in series increases voltage (good for long cable runs, works with higher voltage MPPT inputs). Parallel wiring increases current (better in partial shading). Check your station's max solar voltage before wiring in series — exceeding it can damage the MPPT controller."},
                    {"title":"Clean Your Panels","title_color":"red-400","body":"Dust, dirt, and bird droppings can reduce solar output by 10-25%. Clean your panels periodically with a soft cloth and water. This is especially important if you camp in dusty areas or park under trees."},
                    {"title":"Use Pass-Through Charging","title_color":"blue-400","body":"Nearly all modern stations support pass-through charging — you can use the outputs while the battery charges. This lets you run devices directly from solar during the day, saving battery for night use. It is more efficient than charging first then discharging."},
                ]),
             ]},
        ],
        "faqs": [
            {"q":"What is the fastest way to charge a power station without electricity?","a":"A gas or propane generator is the fastest way to charge a portable power station off-grid. Most generators can supply enough power to charge a station at its maximum AC charge rate — typically 500-3,000W depending on the model. A 2,000Wh station with 1,800W charging can go from 0-80% in about an hour with a sufficiently sized generator."},
            {"q":"Can you charge a power station with solar and AC at the same time?","a":"Yes, most modern portable power stations support simultaneous charging from multiple sources. You can charge from solar panels and AC (wall or generator) at the same time, and many stations also support car charging simultaneously. This is often called dual or multi-source charging, and it fills the battery faster than any single source alone."},
            {"q":"How long does it take to charge a power station with a 100W solar panel?","a":"It depends on the station size and sun conditions. A 100W panel produces roughly 60-80W in real-world use. A 500Wh station takes about 7-9 hours of good sun. A 1,000Wh station takes 14-18 hours. A 2,000Wh station takes 28-36 hours. In practice, you get about 4-6 hours of peak sun per day, so plan for multiple days with small panels."},
            {"q":"Can you charge a power station while it is in use?","a":"Yes, nearly all modern portable power stations support pass-through charging — you can use the output ports while the battery is charging. Some budget models do not support this, or they limit output while charging, but all major brands (EcoFlow, Jackery, Bluetti, Anker) support full pass-through on their current 2025-2026 models."},
            {"q":"Will car charging drain my car battery?","a":"If your engine is running, no — the alternator powers the charging and keeps the car battery topped up at the same time. If the engine is off, yes, charging will slowly drain your car battery. Most car ports shut off automatically when the ignition is off, but some do not. To be safe, only charge from your car while the engine is running, or use a battery isolator if you need stationary charging."},
            {"q":"How many solar panels do I need for a 2000Wh power station?","a":"It depends on how fast you want to charge and how much sun you get. For a full charge in one day (5-6 hours of peak sun), you need roughly 400-500W of solar panels for a 2,000Wh station. For two days of charging, 200-250W works fine. Always oversize slightly for real-world conditions — panel output is rarely 100% of rated power, and you lose efficiency to heat, angle, and dust."},
            {"q":"Can I use any brand of solar panel with my power station?","a":"Generally yes, as long as the panel's voltage is within your station's acceptable input range and you have the right connector. Most stations accept 12-60V or 12-100V solar input. You may need an adapter cable if your panel uses a different connector (MC4, Anderson, XT60, etc.). Check your station's manual for the exact voltage range and supported connector types."},
            {"q":"What is MPPT and why does it matter for solar charging?","a":"MPPT (Maximum Power Point Tracking) is a technology that maximizes the power output from solar panels by continuously finding the optimal voltage and current combination. It can increase charging efficiency by 20-30% compared to older PWM charge controllers, especially in partial shading, low-light conditions, or when panels are at suboptimal angles. All modern power stations use MPPT."},
            {"q":"How do I charge my power station during a long blackout?","a":"During a blackout, your options depend on what you have prepared ahead of time. Solar panels work as long as the sun is out, even in a blackout. A generator can charge it anytime you have fuel. If you have an electric car with vehicle-to-load (V2L), you can use it as a giant power source. The key is to plan ahead — have your charging method ready and tested before the blackout hits."},
            {"q":"Is it cheaper to charge with solar or a generator?","a":"Solar is much cheaper over the long term despite the higher upfront cost. Once you buy the panels, the energy is free. A 400W solar panel setup costs about $400-600 and will last 20+ years. A generator costs about the same upfront but then costs $0.50-1.00 per kWh in fuel. If you use it regularly, solar pays for itself in 1-3 years and is free after that."},
        ],
        "related": [
            {"url":"portable-power-station-not-charging.html","title":"Not Charging Fixes","desc":"Troubleshoot AC, solar, and DC charging problems with step-by-step diagnostics.","badge_color":"yellow","badge_text":"FIX","sub_badge":"Universal"},
            {"url":"solar-charging-0w-power-station.html","title":"Solar 0W Guide","desc":"Deep dive into solar charging issues — causes with step-by-step fixes for MPPT, wiring, and panels.","badge_color":"orange","badge_text":"SOLAR","sub_badge":"Universal"},
            {"url":"off-grid-solar-system-sizing-guide.html","title":"Solar Sizing Guide","desc":"How to calculate the right solar panel size for your off-grid power needs.","badge_color":"green","badge_text":"SOLAR","sub_badge":"Guide"},
            {"url":"can-portable-power-station-charge-while-in-use.html","title":"Pass-Through Charging","desc":"Can you use a power station while charging it? Complete guide to pass-through charging.","badge_color":"purple","badge_text":"PASS-THRU","sub_badge":"All Brands"},
            {"url":"lifepo4-vs-lithium-ion-power-station.html","title":"LFP vs Li-ion","desc":"Complete comparison of battery chemistries — cycle life, safety, cost, and which to choose.","badge_color":"electric","badge_text":"COMPARE","sub_badge":"Chemistry"},
            {"url":"outdoor-power.html","title":"All Power Stations","desc":"Compare all major portable power station models side by side.","badge_color":"purple","badge_text":"COMPARE","sub_badge":"All Brands"},
        ],
    })

    # ======== PAGE 2: Battery Replacement Cost ========
    # (Will continue with remaining 19 pages)
    # ... more pages to be added

    return pages


def generate_all():
    """Generate all pages and return word counts."""
    pages = get_pages()
    results = []
    for pg in pages:
        html = build_page(pg)
        path = os.path.join(OUTPUT_DIR, pg["filename"])
        with open(path, "w") as f:
            f.write(html)
        wc = word_count(html)
        results.append((pg["filename"], wc))
    return results


if __name__ == "__main__":
    results = generate_all()
    print("Generated pages:")
    total = 0
    for fn, wc in results:
        print(f"  {fn}: {wc:,} words")
        total += wc
    print(f"\nTotal: {len(results)} pages, {total:,} words")
