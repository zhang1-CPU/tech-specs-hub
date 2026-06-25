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


def build_page(page):
    """Build complete HTML page from page data dict."""
    article_json = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": page["headline"], "description": page["meta_desc"],
        "url": f"{BASE_URL}/{page['filename']}",
        "datePublished": UPDATED_DATE, "dateModified": UPDATED_DATE,
        "author": {"@type": "Organization", "name": SITE_NAME},
        "publisher": {"@type": "Organization", "name": SITE_NAME, "url": "https://powerspecshub.com/"},
        "image": {"@type": "ImageObject", "url": "https://powerspecshub.com/assets/images/og-default.png"}
    }
    faq_json = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in page["faqs"]]
    }
    bc_url = f"{BASE_URL}/{page['cat_url']}"
    breadcrumb_json = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://powerspecshub.com/"},
            {"@type": "ListItem", "position": 2, "name": page["cat_name"], "item": bc_url},
            {"@type": "ListItem", "position": 3, "name": page["bc_name"]}
        ]
    }

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

    # Read body header from template
    template = open(os.path.join(OUTPUT_DIR, "portable-power-station-eco-mode.html")).read()
    body_header = template.split("<!-- BREADCRUMB -->")[0].split("</head>")[1]

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


# ============================================================
# CONTENT GENERATORS - Reusable rich content sections
# ============================================================

def gen_long_paragraphs(topic, count=3):
    """Generate detailed paragraphs about a topic."""
    paragraphs = []
    intros = [
        f"Understanding {topic} is essential for getting the most out of your equipment. Many users overlook important details that can significantly impact performance, safety, and longevity. Taking the time to learn the fundamentals will pay off in better results and fewer problems down the road.",
        f"When it comes to {topic}, there is a lot of misinformation floating around online. Some of it comes from well-meaning but inexperienced users, while some comes from manufacturers trying to sell products. It is important to separate fact from fiction and understand what actually matters in real-world use.",
        f"The science behind {topic} is more complex than most people realize. There are multiple factors at play, and the interaction between them can be surprising. This section breaks down everything you need to know in clear, practical terms without the marketing hype.",
        f"Many people ask about {topic} but few take the time to truly understand it. What seems like a simple question often has a nuanced answer that depends on your specific situation, equipment, and goals. A one-size-fits-all approach rarely works well.",
        f"Over the years, {topic} has evolved significantly as technology has improved. What was true 5 years ago may no longer be the case today with modern equipment. Staying current with the latest information ensures you are making the best decisions for your setup.",
    ]
    for i in range(min(count, len(intros))):
        paragraphs.append(p(intros[i]))
    return paragraphs


# ============================================================
# PAGE DEFINITIONS
# ============================================================

def get_page_battery_replacement():
    """Page 2: Battery Replacement Cost"""
    return {
        "filename": "portable-power-station-battery-replacement-cost.html",
        "title": "Portable Power Station Battery Replacement Cost & Options (2026)",
        "meta_desc": "Complete guide to portable power station battery replacement costs by brand (EcoFlow, Jackery, Bluetti, Anker). DIY vs professional, warranty coverage, signs you need a replacement, and how to extend battery life.",
        "headline": "Portable Power Station Battery Replacement Cost & Options (2026)",
        "hero_title": "Portable Power Station Battery Replacement Cost & Options",
        "bc_name": "Battery Replacement Cost",
        "cat_name": "Outdoor Power",
        "cat_url": "outdoor-power.html",
        "accent": "yellow",
        "badges": [
            {"icon":"dollar-sign","text":"COST GUIDE","color":"yellow"},
            {"icon":"battery","text":"Battery Care","color":"info"},
            {"icon":"layers","text":"All Brands","color":"info"},
        ],
        "stats": [
            {"icon":"dollar-sign","label":"Avg Replacement","val":"$300–$1,500","vc":"yellow-400"},
            {"icon":"battery-charging","label":"Cycle Life","val":"500–6,000","vc":"green-400"},
            {"icon":"clock","label":"Typical Lifespan","val":"3–10 yrs","vc":"electric-400"},
            {"icon":"wrench","label":"DIY Possible?","val":"Sometimes","vc":"white"},
        ],
        "hero_intro": "Battery replacement is one of the most important — and most expensive — considerations when buying a portable power station. The battery is the heart of the unit, and eventually, every battery will degrade and need to be replaced. Understanding replacement costs, whether your model even supports replacement, and how to extend battery life can save you hundreds of dollars over the long run. This guide breaks down replacement costs by brand, DIY vs professional options, warranty coverage, and clear signs that your battery needs attention.",
        "quick_answer": "Battery replacement costs for portable power stations range from $300 for small 500Wh units to $1,500+ for large 3,000Wh+ models. Whether you can replace the battery yourself depends on the brand and model — some are designed for easy user replacement, while others require professional service or cannot be replaced at all. Most brands offer 2-5 year warranties that cover battery defects, but normal wear and tear is usually not covered. To maximize battery life, use LiFePO4 chemistry, avoid extreme temperatures, and keep the battery at 50-80% charge for long-term storage.",
        "toc": [
            {"id":"cost","title":"Replacement Cost by Brand & Model"},
            {"id":"worth","title":"Is Battery Replacement Worth It?"},
            {"id":"diy","title":"DIY vs Professional Replacement"},
            {"id":"warranty","title":"Warranty Coverage & What It Includes"},
            {"id":"signs","title":"Signs Your Battery Needs Replacement"},
            {"id":"extend","title":"How to Extend Battery Life"},
            {"id":"types","title":"Battery Chemistry Comparison"},
            {"id":"buying","title":"Buying Tips: Replace vs New Station"},
            {"id":"pro","title":"Pro Tips & Best Practices"},
            {"id":"faq","title":"Frequently Asked Questions"},
            {"id":"related","title":"Related Guides"},
        ],
        "sections": [
            {"id":"cost","title":"Battery Replacement Cost by Brand & Model",
             "parts":[
                p("Battery replacement costs vary dramatically depending on the brand, model, and battery capacity. In general, you can expect to pay 40-70% of the original purchase price for a replacement battery. This is because the battery is the single most expensive component in a portable power station."),
                p("Here is a breakdown of estimated replacement costs for popular brands and models as of 2026:"),
                table(["Brand / Model","Capacity","Est. Replacement Cost","User-Replaceable?"],[
                    ["EcoFlow Delta 2","1,024Wh LFP","$400–$550","Yes (official module)"],
                    ["EcoFlow Delta Pro 3","4,096Wh LFP","$1,200–$1,800","Yes (modular)"],
                    ["Jackery Explorer 1000 v2","1,070Wh Li-ion","$450–$650","Limited / service only"],
                    ["Jackery Explorer 2000 Plus","2,042Wh Li-ion","$800–$1,100","Yes (add-on packs)"],
                    ["Bluetti AC200MAX","2,048Wh LFP","$700–$1,000","Yes (expansion packs)"],
                    ["Bluetti AC500","5,120Wh LFP","$1,500–$2,200","Yes (modular B300S)"],
                    ["Anker 535 PowerHouse","512Wh LFP","$250–$400","No (sealed unit)"],
                    ["Anker 757 PowerHouse","1,229Wh LFP","$500–$750","No (sealed unit)"],
                    ["Goal Zero Yeti 1500X","1,516Wh Li-ion","$700–$1,000","Service center only"],
                    ["Generac GB1000","1,086Wh LFP","$450–$650","No (sealed unit)"],
                ]),
                p("Important note: Prices are estimates based on 2026 market data and can vary. Always check the manufacturer's website or contact support for current pricing and availability. Some brands discontinue battery packs for older models, so availability is not guaranteed for units older than 3-5 years."),
                alert("info","Pro tip: Modular power stations with swappable battery packs (EcoFlow Delta Pro, Bluetti AC500, Jackery Explorer Plus series) are the most cost-effective long-term. Instead of replacing the entire unit, you just swap in a new battery module. This also lets you expand capacity as your needs grow."),
             ]},
            {"id":"worth","title":"Is Battery Replacement Worth It?",
             "parts":[
                p("Whether replacing the battery is worth it depends on several factors: the age of the unit, the cost of replacement vs. buying new, whether the rest of the unit is in good shape, and whether replacement parts are even available. Here is a framework to help you decide:"),
                grid([
                    {"title":"Replacement Makes Sense When...","title_color":"green-400","body":"The unit is less than 5 years old, replacement costs less than 60% of a new comparable unit, the inverter/electronics are still working well, and you like the model's features and performance. Modular units with expansion batteries are almost always worth keeping."},
                    {"title":"Buy New When...","title_color":"red-400","body":"The unit is 7+ years old, replacement costs more than 70% of a new unit, newer models have significantly better features (faster charging, more ports, better app), or the unit has other issues (inverter problems, display failure, etc.). Technology improves quickly — a new $1,000 station today may outperform a $2,000 unit from 5 years ago."},
                ]),
                p("One important consideration is technology advancement. Portable power station technology has improved rapidly since 2020. LiFePO4 chemistry has become standard, charging speeds have doubled or tripled, and features like app control, UPS mode, and smart home integration are now common. If your station is from the pre-LFP era (before ~2021), upgrading to a new model with LFP batteries and modern features may be more cost-effective than replacing the old battery."),
                p("Another factor is warranty. If your battery failed prematurely and is still under warranty, get it replaced under warranty — that is always worth it. The question only applies to out-of-warranty batteries that have reached end-of-life through normal use."),
             ]},
            {"id":"diy","title":"DIY vs Professional Battery Replacement",
             "parts":[
                p("Some power stations are designed for user-replaceable batteries, while others are sealed units that require professional service or cannot be serviced at all. Here is what you need to know about each approach:"),
                steps([
                    {"title":"Official Modular Replacement (Best Option)","body":"Many modern stations use modular battery packs that you can swap without tools. EcoFlow Delta series, Bluetti AC series with expansion packs, and Jackery Explorer Plus series all support this. Just buy the official battery module and slot it in. This preserves warranty and is the safest option."},
                    {"title":"DIY Battery Pack Build","body":"Some hobbyists build their own replacement battery packs using 18650 or 21700 cells and a BMS (Battery Management System). This is cheaper but voids warranty, requires technical knowledge, and can be dangerous if done wrong. Only attempt this if you understand high-voltage DC safety and have experience with lithium batteries."},
                    {"title":"Authorized Service Center","body":"Most brands offer battery replacement through authorized service centers. Cost is higher than DIY, but the work is guaranteed and uses genuine parts. Turnaround is typically 1-4 weeks depending on parts availability. This is the best option for sealed units that you cannot open yourself."},
                    {"title":"Third-Party Repair Shops","body":"Independent electronics repair shops may be able to replace batteries at lower cost than authorized service. Quality varies widely, and you may get aftermarket cells of unknown quality. Check reviews and ask about warranty on the repair before committing."},
                ], "electric"),
                alert("warning","Safety warning: Lithium battery replacement involves working with high-voltage DC systems that can cause serious injury or fire if mishandled. Always follow proper safety procedures, use appropriate PPE, and never work on a swollen or damaged battery. If you are not 100% confident in your abilities, pay a professional."),
             ]},
            {"id":"warranty","title":"Warranty Coverage & What It Includes",
             "parts":[
                p("Nearly all portable power stations come with a manufacturer warranty that covers defects in materials and workmanship. The key question is whether battery degradation is covered — and the answer is almost always no, unless the degradation is caused by a defect."),
                table(["Brand","Warranty Period","Battery Coverage","What Is Not Covered"],[
                    ["EcoFlow","2-5 years (varies by model)","Defects only, not normal wear","Normal degradation, misuse, water damage, physical damage"],
                    ["Jackery","2-5 years (varies by model)","Defects only","Normal degradation, accidental damage, unauthorized repair"],
                    ["Bluetti","2-5 years","Defects + guaranteed capacity warranty","Physical damage, misuse, normal wear below threshold"],
                    ["Anker","18 months - 5 years","Defects only","Normal wear and tear, cosmetic damage, unauthorized modification"],
                    ["Goal Zero","2 years","Defects only","Normal degradation, misuse, consumables"],
                ]),
                p("What counts as a defective battery vs. normal wear? Manufacturers typically consider a battery defective if it drops below 60-70% of rated capacity within the warranty period under normal use. If your battery loses 20% capacity in 3 years, that is considered normal and not covered. If it loses 50% capacity in 1 year, that is likely a defect and should be covered."),
                p("To make a warranty claim, you will usually need to provide proof of purchase, serial number, and evidence of the issue (capacity test results, photos, app screenshots). The process typically takes 2-6 weeks depending on the brand and whether they need to receive the unit for inspection."),
                alert("info","Tip: Register your product with the manufacturer promptly after purchase. Many brands extend the warranty by 6-12 months if you register. Also, keep your receipt and all documentation — you will need it if you ever need to make a claim."),
             ]},
            {"id":"signs","title":"Signs Your Battery Needs Replacement",
             "parts":[
                p("Batteries do not usually fail suddenly — they degrade gradually over hundreds of charge cycles. Here are the most common signs that your battery is reaching the end of its useful life:"),
                grid([
                    {"title":"Noticeably Shorter Runtime","title_color":"yellow-400","body":"The clearest sign. If your station used to power your fridge all weekend and now only lasts half a day, the battery has degraded significantly. Most batteries are considered end-of-life at 60-70% of original capacity."},
                    {"title":"Rapid Voltage Drop","title_color":"red-400","body":"If the battery percentage drops quickly under load — say, from 100% to 50% in 10 minutes — it is a sign of high internal resistance. The battery cannot deliver current effectively even though it shows full voltage at rest."},
                    {"title":"Swollen or Bulging Case","title_color":"red-400","body":"This is a serious safety concern. A swollen battery has developed gas from internal degradation and should be replaced immediately. Do not charge a swollen battery, and handle it carefully. Dispose of it properly at a battery recycling center."},
                    {"title":"Error Codes or BMS Faults","title_color":"yellow-400","body":"Frequent BMS (Battery Management System) errors, cell imbalance warnings, or unexplained shutdowns can indicate a failing battery. The BMS is protecting itself and you from a degraded battery that can no longer operate safely within normal parameters."},
                    {"title":"Slow Charging (When It Was Fast)","title_color":"electric-400","body":"If charging has become significantly slower than it used to be and you have ruled out other causes (cables, charger, temperature), the battery may have developed high internal resistance that prevents it from accepting charge at the normal rate."},
                    {"title":"Age & Cycle Count","title_color":"green-400","body":"Even if it still works OK, if your battery is 5+ years old and has seen heavy use (500+ cycles for Li-ion, 3,000+ for LFP), you should start planning for replacement. It is better to replace proactively than to have it fail when you need it most."},
                ], 3),
                p("How to test your battery capacity? The most accurate method is a full discharge test: charge to 100%, then run a known load (like a 100W light bulb) and measure how long it lasts. If you get less than 60-70% of the rated capacity, the battery is nearing end of life. Most smart stations also show cycle count and health in the app."),
             ]},
            {"id":"extend","title":"How to Extend Battery Life",
             "parts":[
                p("The best way to avoid expensive battery replacement is to make your battery last as long as possible. Here are proven strategies to maximize battery lifespan:"),
                steps([
                    {"title":"Avoid Full Discharges","body":"Draining the battery to 0% puts maximum stress on the cells. Try to keep the battery between 20-80% for daily use. Only do full charges and discharges occasionally (once every few months) for calibration."},
                    {"title":"Store at 50-60% Charge","body":"For long-term storage (more than 1 month), charge the battery to 50-60%, not 100%. Full charge during storage accelerates degradation. Most stations have a storage mode or app reminder to help with this."},
                    {"title":"Keep It Cool","body":"Heat is the #1 enemy of battery life. Avoid leaving your power station in a hot car, in direct sun, or near heat sources. Ideal operating temperature is 20-25°C (68-77°F). Temperatures above 40°C (104°F) accelerate degradation significantly."},
                    {"title":"Use the Right Charge Mode","body":"Fast charging generates more heat and causes slightly more wear. If you do not need the battery quickly, use standard or silent charge mode instead of turbo/fast charging. Your battery will thank you with longer life."},
                ], "green"),
                p("Additional tips: Keep the battery clean and dry, avoid physical shock or vibration, update firmware (manufacturers often optimize battery management), and use the battery regularly — lithium batteries degrade faster when left unused for very long periods. A good rule is to cycle the battery at least once every 3-6 months even if you are not using it regularly."),
                alert("info","LiFePO4 (LFP) batteries last 3-6 times longer than traditional lithium-ion (NMC/NCA) batteries. An LFP battery might last 3,000-6,000 cycles vs. 500-1,000 for Li-ion. If you are buying a new station, choosing LFP chemistry is the single best thing you can do for long-term value and to minimize replacement costs."),
             ]},
            {"id":"types","title":"Battery Chemistry Comparison",
             "parts":[
                p("Not all portable power station batteries are the same. The chemistry type dramatically affects lifespan, safety, cost, and replacement frequency. Here is how the main types compare:"),
                table(["Factor","LiFePO4 (LFP)","Lithium-Ion (NMC/NCA)","Lead-Acid"],[
                    ["Cycle Life (80% capacity)","3,000–6,000 cycles","500–1,000 cycles","200–500 cycles"],
                    ["Typical Lifespan","5–10 years","2–4 years","1–3 years"],
                    ["Energy Density","Lower (heavier for same Wh)","Higher (lighter, more compact)","Lowest (very heavy)"],
                    ["Safety / Thermal Stability","Excellent — very stable","Good — but can thermal runaway","Fair — lead/acid hazards"],
                    ["Cost per kWh","Higher upfront, lower long-term","Moderate upfront","Lowest upfront, highest long-term"],
                    ["Environmental Impact","Less toxic, easier to recycle","Cobalt/nickel concerns","Lead is highly toxic"],
                    ["Used in 2026 stations","Most mid/high-end models","Some budget/lightweight models","Very few (mostly old designs)"],
                ]),
                p("As of 2026, LiFePO4 (LFP) has become the dominant chemistry for portable power stations. The longer cycle life and better safety more than justify the slightly higher upfront cost for most users. The main remaining uses for lithium-ion (NMC) are in ultra-portable models where weight is the primary concern, and in some budget models from lesser-known brands."),
             ]},
            {"id":"buying","title":"Buying Tips: Replace Battery vs Buy New Station",
             "parts":[
                p("When your battery reaches end of life, you have a choice: replace the battery or buy a whole new power station. Here is how to make that decision:"),
                p("First, calculate the cost ratio. If a replacement battery costs more than 60-70% of what a comparable new station costs, just buy new. You get a full warranty, the latest technology, and a brand-new unit (not just a new battery in an old frame)."),
                p("Second, consider technological progress. If your station is from 2020 or earlier, a new model will likely charge 2-3x faster, have better efficiency, more features (app, UPS mode, smart home), and better battery chemistry. The upgrade may be worth it even if replacement is slightly cheaper."),
                p("Third, think about your future needs. Has your power usage grown? If you bought a 500Wh station and now find yourself wanting more capacity, this is a great opportunity to upgrade to a larger model rather than replacing the battery in one that is too small."),
                grid([
                    {"title":"Choose Battery Replacement If...","title_color":"green-400","body":"Replacement cost is less than 60% of new, the unit is less than 4 years old, you are happy with its features and performance, parts are readily available, and the rest of the unit is in excellent condition."},
                    {"title":"Choose New Station If...","title_color":"yellow-400","body":"Replacement is expensive relative to new, the unit is 5+ years old, newer models have significantly better features/specs, you need more capacity than before, or the unit has other issues beyond just the battery."},
                ]),
             ]},
            {"id":"pro","title":"Pro Tips & Best Practices",
             "parts":[
                grid([
                    {"title":"Buy Modular Designs","title_color":"electric-400","body":"When shopping for a new power station, prioritize models with user-replaceable/expandable batteries. They cost a bit more upfront but give you much more flexibility and lower long-term cost of ownership."},
                    {"title":"Track Cycle Count","title_color":"green-400","body":"Most smart stations track cycle count in the app. Keep an eye on it and start planning for replacement when you reach 70-80% of the rated cycle life. Proactive planning beats sudden failure."},
                    {"title":"Sell or Trade In","title_color":"yellow-400","body":"If you decide to upgrade, do not just throw away your old station. Many brands have trade-in programs, or you can sell it as-is on the used market. Someone might want it for parts or to replace their own failed unit."},
                    {"title":"Recycle Properly","title_color":"red-400","body":"Never throw lithium batteries in the trash. Take them to a battery recycling center, big-box store with battery recycling, or household hazardous waste facility. It is illegal in many places and terrible for the environment."},
                ]),
             ]},
        ],
        "faqs": [
            {"q":"How much does it cost to replace a portable power station battery?","a":"Battery replacement costs range from $250 for small 500Wh stations to $2,000+ for large 5,000Wh+ models. On average, you can expect to pay 40-70% of the original purchase price. LiFePO4 batteries are more expensive upfront but last 3-6 times longer, making them cheaper per cycle over the long run."},
            {"q":"Can I replace the battery in my power station myself?","a":"It depends on the model. Some power stations (EcoFlow Delta series, Bluetti with expansion packs, Jackery Explorer Plus) are designed for easy user-replaceable battery modules. Others are sealed units that require professional service or cannot be replaced at all. Check your manual or contact the manufacturer to confirm."},
            {"q":"How long do portable power station batteries last?","a":"Battery lifespan depends on chemistry and usage. LiFePO4 (LFP) batteries typically last 3,000-6,000 charge cycles (about 5-10 years of typical use) before dropping to 80% capacity. Traditional lithium-ion (NMC) batteries last 500-1,000 cycles (2-4 years). Actual lifespan depends on how you use and maintain the battery."},
            {"q":"Does warranty cover battery replacement?","a":"Warranties cover defective batteries but not normal wear and tear from regular use. If your battery drops below 60-70% capacity within the warranty period (typically 2-5 years) under normal use, it may be considered defective and covered. Gradual degradation over hundreds of cycles is considered normal and is not covered."},
            {"q":"How do I know if my battery needs replacing?","a":"Key signs include: significantly shorter runtime (less than 60-70% of original), rapid voltage drop under load, swollen or bulging battery case, frequent BMS errors or cell imbalance warnings, slow charging when it used to be fast, and high cycle count (500+ for Li-ion, 3,000+ for LFP)."},
            {"q":"Is it better to replace the battery or buy a new power station?","a":"Replace the battery if: cost is less than 60% of a new comparable unit, the station is less than 4 years old, and you are happy with its performance. Buy new if: replacement is expensive relative to new, the unit is 5+ years old, newer models have much better features, or you need more capacity."},
            {"q":"Can I use third-party replacement batteries?","a":"Technically yes in some cases, but it is not recommended. Third-party batteries may use lower quality cells, lack proper safety certification, and will void your warranty. For modular stations, always use official manufacturer battery modules for safety and compatibility."},
            {"q":"How can I make my battery last longer?","a":"Top tips for longer battery life: avoid full discharges (keep above 20%), store at 50-60% charge for long periods, avoid extreme heat, use standard charging instead of fast charging when possible, use the battery regularly (cycle at least every 3-6 months), and choose LiFePO4 chemistry for 3-6x longer cycle life."},
            {"q":"What do I do with my old power station battery?","a":"Never throw lithium batteries in the trash — they are a fire hazard and environmental hazard. Take them to a battery recycling center, a big-box store with battery recycling (like Home Depot or Lowe's), or your local household hazardous waste facility. Some manufacturers also have take-back programs for their products."},
            {"q":"Do LiFePO4 batteries need replacement less often?","a":"Yes — LiFePO4 (LFP) batteries last 3-6 times longer than traditional lithium-ion. LFP typically lasts 3,000-6,000 cycles vs. 500-1,000 for NMC Li-ion. For a typical user, that means 5-10 years of use vs. 2-4 years. The higher upfront cost of LFP is almost always worth it for the much longer lifespan."},
        ],
        "related": [
            {"url":"how-to-store-portable-power-station.html","title":"Storage Guide","desc":"How to store a portable power station long-term — ideal charge level, temperature, cycling.","badge_color":"green","badge_text":"STORAGE","sub_badge":"Guide"},
            {"url":"portable-power-station-overheating-hot.html","title":"Overheating Guide","desc":"Why power stations overheat, temperature effects on battery life, cooling tips.","badge_color":"red","badge_text":"HEAT","sub_badge":"Universal"},
            {"url":"portable-power-station-eco-mode.html","title":"ECO Mode Guide","desc":"How ECO mode works, battery savings, and optimization for maximum runtime.","badge_color":"purple","badge_text":"ECO MODE","sub_badge":"All Brands"},
            {"url":"lifepo4-vs-lithium-ion-power-station.html","title":"LFP vs Li-ion","desc":"Complete comparison of LiFePO4 vs lithium-ion — cycle life, safety, cost, which to choose.","badge_color":"electric","badge_text":"COMPARE","sub_badge":"Chemistry"},
            {"url":"portable-power-station-not-charging.html","title":"Not Charging","desc":"Troubleshoot AC, solar, and DC charging problems step-by-step.","badge_color":"yellow","badge_text":"FIX","sub_badge":"Universal"},
            {"url":"outdoor-power.html","title":"Power Station Comparison","desc":"Compare all major portable power station models side by side.","badge_color":"purple","badge_text":"COMPARE","sub_badge":"All Brands"},
        ],
    }


def get_page_rv():
    """Page 3: Best Portable Power Station for RV"""
    return {
        "filename": "best-portable-power-station-for-rv.html",
        "title": "Best Portable Power Station for RV & Boondocking (2026)",
        "meta_desc": "Best portable power stations for RV use and boondocking. Complete guide to RV power needs, TT-30 30A hookups, solar for RVs, installation tips, and top picks for every RV size.",
        "headline": "Best Portable Power Station for RV & Boondocking (2026)",
        "hero_title": "Best Portable Power Station for RV & Boondocking",
        "bc_name": "RV Power Guide",
        "cat_name": "Outdoor Power",
        "cat_url": "outdoor-power.html",
        "accent": "green",
        "badges": [
            {"icon":"home","text":"RV & BOONDOCKING","color":"green"},
            {"icon":"zap","text":"30A Ready","color":"info"},
            {"icon":"award","text":"Top Picks","color":"yellow"},
        ],
        "stats": [
            {"icon":"battery-charging","label":"Recommended Min","val":"2,000Wh+","vc":"green-400"},
            {"icon":"zap","label":"Output Needed","val":"2,000W+","vc":"yellow-400"},
            {"icon":"sun","label":"Solar Input","val":"400–1,600W","vc":"electric-400"},
            {"icon":"plug","label":"RV Standard","val":"TT-30 30A","vc":"white"},
        ],
        "hero_intro": "Powering an RV off-grid is one of the most common — and most demanding — uses for portable power stations. Whether you are a weekend camper or a full-time RVer, having reliable electricity can make or break your experience. But not all power stations are suited for RV use. You need enough capacity to run essential appliances, enough output to handle startup surges from AC units and microwaves, and ideally, the ability to charge from solar while you are parked. This guide covers everything you need to know to choose the right power station for your RV lifestyle.",
        "quick_answer": "The best portable power station for most RVs is one with at least 2,000Wh capacity and 2,000W output, ideally with LiFePO4 batteries for long life. Top picks include the EcoFlow Delta Pro 3 (best overall, 4096Wh, 4000W), Bluetti AC500 (best expandable, up to 18432Wh), and Jackery Explorer 2000 Plus (best mid-range, 2042Wh, 3000W). For smaller travel trailers and van builds, the EcoFlow Delta 2 Max (2048Wh, 2400W) offers excellent value. Pair any of these with 400-800W of solar panels for indefinite off-grid boondocking.",
        "toc": [
            {"id":"needs","title":"How Much Power Does an RV Need?"},
            {"id":"tt30","title":"TT-30 30A RV Hookup Explained"},
            {"id":"small","title":"Top Picks: Small RVs & Vans"},
            {"id":"medium","title":"Top Picks: Medium Travel Trailers"},
            {"id":"large","title":"Top Picks: Large RVs & 5th Wheels"},
            {"id":"solar","title":"Solar Panels for RV Boondocking"},
            {"id":"hookup","title":"Hookups vs Boondocking Power"},
            {"id":"install","title":"Installation & Setup Tips"},
            {"id":"pro","title":"Pro Tips for RV Power"},
            {"id":"faq","title":"Frequently Asked Questions"},
            {"id":"related","title":"Related Guides"},
        ],
        "sections": [
            {"id":"needs","title":"How Much Power Does an RV Need?",
             "parts":[
                p("The first step in choosing a power station for your RV is understanding how much electricity you actually use. RV power consumption varies dramatically depending on the size of your rig, what appliances you run, and whether you are conservative or lavish with electricity. Here is a breakdown of typical RV appliance power draws:"),
                table(["Appliance","Running Watts","Surge Watts","Daily Use (hrs)","Daily Wh"],[
                    ["RV AC (13,500 BTU)","1,200–1,800W","3,500–5,000W","4–8","4,800–14,400"],
                    ["Microwave (1,000W)","1,000–1,200W","1,500–2,000W","0.5","500–600"],
                    ["Refrigerator (residential)","100–200W","300–600W","8–12 (compressor)","1,200–2,400"],
                    ["Refrigerator (RV 12V)","50–100W","100–200W","8–12","400–1,200"],
                    ["Water Heater (electric)","1,200–1,500W","1,500–2,000W","1–2","1,200–3,000"],
                    ["Coffee Maker","800–1,200W","1,200–1,800W","0.25","200–300"],
                    ["LED Lights (10x)","30–60W total","N/A","4–6","120–360"],
                    ["TV (32\")","40–80W","60–120W","2–4","80–320"],
                    ["Phone/Laptop Charging","20–100W","N/A","4–8","80–800"],
                    ["Water Pump","50–100W","100–200W","0.5","25–50"],
                    ["RV Furnace Blower","50–150W","100–250W","4–8","200–1,200"],
                ]),
                p("As you can see, air conditioning is by far the biggest power draw. If you want to run AC from your power station, you need a large unit — at least 3,000W output and 3,000Wh+ capacity, and even then you will only get a few hours of AC. Most boondockers who rely on solar for power do not run AC and instead use fans, evaporative coolers, or simply travel to cooler climates in summer."),
                grid([
                    {"title":"Minimalist / Van Life","title_color":"green-400","body":"1,000–2,000Wh capacity, 1,500–2,000W output. Powers lights, fridge, phone/laptop charging, water pump, small appliances. No AC, no microwave. Good for weekend trips with careful power use."},
                    {"title":"Standard Boondocking","title_color":"electric-400","body":"2,000–4,000Wh capacity, 2,000–3,500W output. Powers fridge, lights, water pump, microwave occasionally, TV, devices, coffee maker. With 400–800W solar, you can stay off-grid indefinitely with careful use."},
                    {"title":"Luxury / Full-Time","title_color":"yellow-400","body":"5,000–15,000+ Wh capacity, 3,500–5,000W+ output. Can run AC for several hours, electric water heater, all appliances. With 1,000–2,000W solar array, comfortable full-time off-grid living with most modern conveniences."},
                ], 3),
             ]},
            {"id":"tt30","title":"TT-30 30A RV Hookup Explained",
             "parts":[
                p("The TT-30 connector is the standard 30-amp RV plug in North America. Understanding what it provides and how a portable power station relates to it is essential for RVers."),
                p("A TT-30 30A hookup provides 120V AC at up to 30 amps, which equals 3,600 watts maximum. This is enough to run most appliances in a small-to-medium RV, but not everything at once. Most campground pedestals have 30A and/or 50A outlets."),
                p("Here is the important part: a portable power station does NOT replace a 30A hookup in terms of continuous power delivery. Even a 4,000W power station can only deliver that power for about an hour before the battery is drained. The 30A hookup delivers 3,600W continuously, indefinitely, as long as you pay for the site. Think of a power station as a battery buffer that supplements your power, not as a complete replacement for shore power."),
                steps([
                    {"title":"Using Power Station with Shore Power","body":"When plugged into shore power, the power station can act as a UPS — it charges from shore power and provides seamless backup if power goes out. This is useful in campgrounds with unreliable power. You can also use the station's battery during peak hours if the campground charges by the kWh."},
                    {"title":"Using Power Station for Boondocking","body":"When off-grid with no hookups, the power station is your primary power source. Charge it with solar panels during the day, use it at night. Size your battery + solar array so that you generate at least as much power during the day as you use in a full 24-hour period."},
                    {"title":"Adapters and Connections","body":"Most portable power stations have standard 15A household outlets (NEMA 5-15), not TT-30. To plug your RV into a power station, you need a 15A-to-30A adapter (dogbone adapter). This is perfectly safe — it just means you are limited to 15A (1,800W) per outlet. Use multiple outlets with splitters if needed, or use a station with a dedicated 30A output."},
                ], "electric"),
                alert("warning","Important: Never exceed your power station's wattage rating. RV appliances like AC units and microwaves have high startup surges. Make sure your station's surge/peak rating exceeds the startup draw of any appliance you plan to use. Running an AC on an undersized station can damage the inverter or trigger overload protection."),
             ]},
            {"id":"small","title":"Top Picks: Small RVs, Vans & Teardrops",
             "parts":[
                p("For small RVs, camper vans, teardrop trailers, and weekend camping trips where you want basic power without the bulk and cost of a large system, these compact power stations deliver excellent value."),
                grid([
                    {"title":"EcoFlow Delta 2 — Best Overall Compact","title_color":"electric-400","body":"1,024Wh LFP (expandable to 3,072Wh), 1,800W output (2,700W surge), 500W solar input max. Lightweight at 27 lbs. Excellent for van builds and small campers. Fast AC charging (0-80% in 50 min). App control and UPS mode. Great value at ~$800."},
                    {"title":"Jackery Explorer 1000 v2 — Best Lightweight","title_color":"yellow-400","body":"1,070Wh Li-ion, 1,500W output (2,000W surge). Extremely portable at 22 lbs. Simple to use — no app required. Good for casual campers who value simplicity and portability above all. Compatible with Jackery's 200W solar panels."},
                    {"title":"Bluetti EB3A — Best Budget Pick","title_color":"green-400","body":"268Wh LFP, 600W output (1,200W surge). Tiny and very affordable (~$200). Perfect for van lifers with minimal power needs, or as a supplementary station for charging devices. Can be charged with 200W solar. Not enough for fridges or microwaves."},
                    {"title":"Anker 535 PowerHouse — Most Reliable","title_color":"red-400","body":"512Wh LFP, 500W output. Rock-solid build quality from Anker, excellent customer support. 200W solar input. Good for van life basics — lights, charging, small fridge. Quiet operation and long-lasting LFP battery."},
                ]),
                p("For small RV use, the sweet spot is typically 1,000-2,000Wh. Below 1,000Wh and you will be constantly worrying about power. Above 2,000Wh and you start getting into significant weight and cost that may not be necessary for weekend use."),
             ]},
            {"id":"medium","title":"Top Picks: Medium Travel Trailers & Class C",
             "parts":[
                p("For medium RVs (20-30 ft travel trailers, Class C motorhomes) and serious boondocking, you need more capacity and output. These stations can handle fridges, microwaves, TVs, and all your basic needs for multiple days without solar, or indefinitely with a good solar array."),
                grid([
                    {"title":"EcoFlow Delta 2 Max — Best Value","title_color":"electric-400","body":"2,048Wh LFP (expandable to 6,144Wh with extra batteries), 2,400W output (4,800W surge), 1,000W solar input max. The sweet spot for most RVers. Enough capacity for 2-3 days of boondocking without solar, and with 800W panels you can stay off-grid indefinitely. ~$1,500 base unit."},
                    {"title":"Jackery Explorer 2000 Plus — Best for Simplicity","title_color":"yellow-400","body":"2,042Wh Li-ion (expandable to 4,084Wh), 3,000W output (6,000W surge), 600W solar input. More output than Delta 2 Max but less solar input. Great if you need to run high-wattage appliances occasionally. Simple, reliable, no app needed. ~$1,800 base."},
                    {"title":"Bluetti AC200MAX — Best Expandability","title_color":"green-400","body":"2,048Wh LFP (expandable to 8,192Wh with B230 modules), 2,200W output (4,800W surge), 900W solar input. Highly expandable, lots of output ports, built like a tank. Good choice if you want to start small and add capacity later. ~$1,300 base unit."},
                    {"title":"EcoFlow Delta Pro — Best Overall Mid-Size","title_color":"purple-400","body":"3,600Wh LFP (expandable to 25,000Wh+), 3,600W output (7,200W surge), 1,600W solar input. Incredible output and solar input. Can run an RV AC for several hours. A bit heavy at 68 lbs but worth it for the power. ~$2,500 base unit."},
                ]),
                p("For most serious boondockers with medium RVs, we recommend starting with at least 2,000Wh and 2,000W output. Pair it with 400-800W of solar panels. This setup will power your fridge, lights, water pump, devices, and occasional microwave use indefinitely as long as you get decent sun."),
             ]},
            {"id":"large","title":"Top Picks: Large RVs, 5th Wheels & Full-Time",
             "parts":[
                p("For large RVs, 5th wheels, motorhomes, and anyone living full-time on the road who wants maximum comfort and the ability to run air conditioning, these high-capacity systems are the way to go."),
                grid([
                    {"title":"EcoFlow Delta Pro 3 — Best Overall","title_color":"electric-400","body":"4,096Wh LFP (expandable to 24,576Wh with 5 extra batteries), 4,000W output (8,000W surge), 1,600W solar input (8,000W with optimization). The gold standard for full-time RVing. Can run a 13,500 BTU AC for 4-6 hours on a single charge. ~$3,000 base unit."},
                    {"title":"Bluetti AC500 + B300S — Most Expandable","title_color":"green-400","body":"5,120Wh per B300S module (up to 6 modules = 30,720Wh), 5,000W output (10,000W surge), 3,000W solar input max. Insane expandability. Can run multiple AC units if needed. Split-phase 120/240V capable with two units. ~$3,500 for AC500 + 1 module."},
                    {"title":"Goal Zero Yeti 6000X — Premium Build","title_color":"yellow-400","body":"6,071Wh LFP, 2,000W output (4,000W surge). Lower output than competitors but legendary build quality and customer support. Goal Zero is the premium brand with premium pricing. Good for people who value reliability and support over raw specs. ~$5,000."},
                    {"title":"Generac GB1000 + Expansion — Brand Name","title_color":"red-400","body":"1,086Wh LFP base, expandable up to ~5,000Wh. 1,600W output. Generac is a well-known generator brand expanding into power stations. Good warranty and service network. Solid choice if you prefer a brand you recognize. Pricing varies by configuration."},
                ]),
                alert("info","Pro tip: If you want to run RV air conditioning, aim for at least 3,500W output and 3,000Wh capacity. A 13,500 BTU AC draws roughly 1,300-1,800W running and 3,500-5,000W startup. Even a large power station will only run AC for a few hours — solar helps extend this, but AC on battery alone is always limited."),
             ]},
            {"id":"solar","title":"Solar Panels for RV Boondocking",
             "parts":[
                p("Solar panels are what turn a portable power station from a weekend toy into a full-time off-grid power system. With enough solar, you can live indefinitely off-grid as long as the sun shines. Here is what you need to know about solar for RVs:"),
                p("How much solar do you need? The rule of thumb is to size your solar array so that you generate at least as much power per day as you use. If you use 2,000Wh per day and you get 5 hours of peak sun, you need 400W of solar panels (400W × 5h = 2,000Wh). In practice, oversize by 25-50% for real-world conditions (clouds, shade, suboptimal angle, dirt)."),
                table(["Daily Usage","Min Solar Needed","Recommended Solar","Typical Setup"],[
                    ["500–1,000Wh","100–200W","200–300W","1-2x 100W panels"],
                    ["1,000–2,000Wh","200–400W","400–600W","2-3x 200W panels"],
                    ["2,000–4,000Wh","400–800W","600–1,000W","3-5x 200W panels"],
                    ["4,000–8,000Wh","800–1,600W","1,200–2,000W","6-10x 200W panels"],
                ]),
                steps([
                    {"title":"Roof-Mounted Solar","body":"Permanent panels mounted on the RV roof. Always deployed, no setup time. Most convenient but fixed angle means lower efficiency. Typically 100-400W on a typical RV roof. Best for full-timers who want zero hassle."},
                    {"title":"Portable Solar Panels","body":"Folding panels that you set up on the ground when parked. Can be angled optimally for maximum power. More efficient per watt but require setup time and storage space. 100-400W per panel, easy to bring multiple."},
                    {"title":"Hybrid Approach","body":"Best of both worlds: roof-mounted panels for trickle charging and convenience, plus portable panels you can deploy for extra power when boondocking for extended periods. Many full-timers use this setup."},
                ], "green"),
             ]},
            {"id":"hookup","title":"Hookups vs Boondocking: Power Strategy",
             "parts":[
                p("How you use your power station depends dramatically on whether you are mostly staying at campgrounds with hookups or boondocking off-grid. Let us compare the two approaches:"),
                grid([
                    {"title":"Campground with Full Hookups","title_color":"electric-400","body":"When you have shore power, the power station acts as: (1) UPS backup if power goes out, (2) battery buffer for peak shaving if electricity is metered, (3) extra power if the 30A hookup is not enough for everything at once, (4) power for devices while driving between campgrounds. Charging happens automatically from shore power."},
                    {"title":"Boondocking (No Hookups)","title_color":"green-400","body":"When boondocking, the power station is your entire electrical system. You rely on solar to recharge during the day and battery power at night. You need to be mindful of usage — turn things off when not in use, use efficient appliances, and size your system appropriately. Solar is essential for stays longer than 2-3 days."},
                ]),
                p("Many RVers split their time between campgrounds and boondocking. In that case, having a power station that charges quickly from AC (for when you do have hookups) and has good solar input (for when you do not) is ideal. Look for stations with both fast AC charging (500W+) and high max solar input (400W+)."),
                p("Driving days are another consideration. If you move every few days, you can charge your power station while driving using the car/vehicle charging cable. Many RVers also have alternator charging systems that charge the house battery while driving, and you can use the same 12V source to top up your portable power station."),
             ]},
            {"id":"install","title":"Installation & Setup Tips",
             "parts":[
                p("Setting up a portable power station in your RV is straightforward but there are a few things to know for best results."),
                steps([
                    {"title":"Choose the Right Location","body":"Place the power station in a well-ventilated area, away from extreme heat and direct sun. Good spots: under a dinette seat, in a storage bay, or on a shelf in a cabinet. Make sure there is airflow around the unit — do not enclose it completely. The unit needs ventilation for cooling during charging and high-output use."},
                    {"title":"Secure It for Travel","body":"A 50+ pound power station becomes a dangerous projectile in a crash. Secure it with straps, brackets, or in a cabinet with a latch. Many brands sell mounting brackets or bags. At minimum, use a ratchet strap to tie it down to something solid. Never leave it loose on a counter or seat."},
                    {"title":"Wiring and Connections","body":"For permanent installs, consider running a dedicated 12V line from your RV's house battery or alternator for charging while driving. For AC output, use heavy-duty extension cords (14 gauge or thicker) for high-wattage appliances. Use a 15A-to-30A adapter to plug your RV's power cord into the station's AC outlets."},
                    {"title":"Solar Panel Wiring","body":"If installing roof-mounted solar, run the cables through a roof vent or cable gland to avoid leaks. Use MC4 connectors for solar panel connections. Make sure the panels are angled for best sun exposure — fixed roof panels are usually flat (less efficient), while portable panels can be tilted optimally."},
                ], "yellow"),
                alert("warning","Safety note: Always turn off AC output before plugging/unplugging high-wattage appliances. Make sure all connections are tight and cables are rated for the amperage. Do not daisy-chain power strips and extension cords excessively. Keep the area around the power station clear of flammable materials."),
             ]},
            {"id":"pro","title":"Pro Tips for RV Power",
             "parts":[
                grid([
                    {"title":"Start with a Power Audit","title_color":"electric-400","body":"Before buying anything, track your actual power usage for a few days. Use a kill-a-watt meter on appliances, or check your RV's battery monitor if you have one. Real data beats estimates every time and ensures you buy the right size system."},
                    {"title":"Size for Solar, Not Just Battery","title_color":"green-400","body":"Battery capacity is important, but solar input matters more for long boondocking trips. A 2,000Wh station with 1,000W solar input is often more useful than a 4,000Wh station with only 200W solar. The battery gets you through the night; solar gets you through the week."},
                    {"title":"Switch to Efficient Appliances","title_color":"yellow-400","body":"The cheapest watt is the one you do not use. LED lights, efficient fridges, and propane appliances (instead of electric) dramatically reduce your power needs. A 12V RV fridge uses 1/4 the power of a residential fridge. Propane for cooking and water heating saves tons of electricity."},
                    {"title":"12V System + Power Station Combo","title_color":"red-400","body":"Many full-time RVers combine a 12V house battery bank (for lights, fridge, water pump, 12V appliances) with a portable power station (for AC appliances like microwave, coffee maker, tools). This gives you the best of both worlds — efficient 12V for always-on things and AC when you need it."},
                ]),
             ]},
        ],
        "faqs": [
            {"q":"What size portable power station do I need for my RV?","a":"For small vans and weekend trips: 1,000-2,000Wh with 1,500-2,000W output. For medium travel trailers and regular boondocking: 2,000-4,000Wh with 2,000-3,500W output. For large RVs and full-time living: 4,000-15,000+ Wh with 3,500-5,000W+ output. Pair with 400-1,000W+ of solar panels for off-grid use."},
            {"q":"Can a portable power station run an RV air conditioner?","a":"Yes, but only for a limited time and you need a large station. A 13,500 BTU RV AC draws 1,200-1,800W running and 3,500-5,000W surge. You need at least 3,500W output (surge rating) and 3,000Wh+ capacity. A 4,000Wh station might run AC for 2-4 hours. With solar, you can extend this somewhat during the day, but AC is very power-hungry."},
            {"q":"Can I plug my 30A RV into a portable power station?","a":"Yes, you just need a 15A-to-30A adapter (dogbone adapter). Most power stations have standard 15A household outlets. The adapter lets you plug your RV's 30A power cord into the station. You will be limited to the power station's output (typically 1,800-5,000W depending on model), not the full 3,600W of a 30A hookup."},
            {"q":"How many solar panels do I need for my RV?","a":"As a rule of thumb, you need enough solar to replace your daily usage. If you use 2,000Wh per day and get 5 hours of peak sun, you need 400W of panels. Oversize by 25-50% for real-world conditions. Most boondockers do well with 400-800W of solar. Full-time RVers running lots of appliances may need 1,000-2,000W."},
            {"q":"How long can I boondock with a portable power station?","a":"It depends on your usage, station size, and solar. Without solar: 1-3 days for a 1,000-2,000Wh station with moderate use, 3-7 days for 3,000-5,000Wh. With enough solar to match your daily usage, you can boondock indefinitely. Most serious boondockers aim for net-zero or net-positive solar production so they never run out of power."},
            {"q":"Is LiFePO4 better for RV use?","a":"Yes, LiFePO4 (LFP) is strongly recommended for RV use. LFP batteries last 3-6 times longer (3,000-6,000 cycles vs 500-1,000 for Li-ion), handle more charge/discharge cycles, are safer (no thermal runaway risk), and perform better in hot RV environments. The higher upfront cost is well worth it for the much longer lifespan."},
            {"q":"Can I charge the power station while driving?","a":"Yes, most portable power stations can charge from your vehicle's 12V port while driving. Charging speed is typically 100-200W from a standard 12V outlet, which is slow but adds up over a long drive. For faster charging while driving, you can use a DC-DC charger connected directly to your RV's alternator or house battery system."},
            {"q":"What is the best power station for full-time RV living?","a":"For full-time RVing, we recommend the EcoFlow Delta Pro 3 (4,096Wh, 4,000W, 1,600W solar) or Bluetti AC500 + B300S (5,120Wh per module, expandable to 30,720Wh, 5,000W). Both have excellent solar input, are highly expandable, and can handle all your appliances. Pair with 800-2,000W of solar for off-grid independence."},
            {"q":"How do I keep my RV fridge running on battery?","a":"A 12V RV fridge draws 50-100W and runs the compressor 30-50% of the time, using roughly 400-1,200Wh per day. A 2,000Wh power station can run it for 2-5 days without solar. With 200-400W of solar, you can run it indefinitely. Residential fridges use 2-3x more power, so upgrade to a 12V fridge if boondocking regularly."},
            {"q":"Should I get a modular/expandable power station?","a":"Yes, modular is almost always better for RVers. Start with a base unit that fits your current needs and budget, then add battery modules later as your needs grow or as you can afford it. Modular designs also mean you can replace just the battery pack when it wears out, instead of buying a whole new station."},
        ],
        "related": [
            {"url":"how-to-charge-power-station-without-electricity.html","title":"Off-Grid Charging","desc":"Complete guide to off-grid charging — solar, car, generator, wind, and more.","badge_color":"green","badge_text":"OFF-GRID","sub_badge":"Solar & More"},
            {"url":"can-portable-power-station-run-refrigerator.html","title":"Run a Refrigerator","desc":"How long can a power station run a fridge? Complete math and real-world testing.","badge_color":"blue","badge_text":"FRIDGE","sub_badge":"Runtime"},
            {"url":"off-grid-solar-system-sizing-guide.html","title":"Solar Sizing Guide","desc":"How to calculate the right solar panel size for your off-grid power needs.","badge_color":"yellow","badge_text":"SOLAR","sub_badge":"Guide"},
            {"url":"portable-power-station-ups-mode-explained.html","title":"UPS Mode Guide","desc":"How UPS mode works — switchover speed, use cases, and which brands support it.","badge_color":"purple","badge_text":"UPS","sub_badge":"All Brands"},
            {"url":"ecoflow-delta-pro-3.html","title":"EcoFlow Delta Pro 3 Specs","desc":"Full specifications — 4,096Wh LFP, 4,000W inverter, 1,600W solar.","badge_color":"electric","badge_text":"SPECS","sub_badge":"EcoFlow"},
            {"url":"outdoor-power.html","title":"All Power Stations","desc":"Compare all major portable power station models side by side.","badge_color":"purple","badge_text":"COMPARE","sub_badge":"All Brands"},
        ],
    }


def get_page_disposal():
    """Page 4: How to Dispose of a Portable Power Station"""
    return {
        "filename": "how-to-dispose-of-portable-power-station.html",
        "title": "How to Dispose of a Portable Power Station (Battery Recycling 2026)",
        "meta_desc": "Complete guide to properly disposing of and recycling portable power stations. Battery types, recycling centers, hazardous waste concerns, donation options, legal requirements by state, and environmental impact.",
        "headline": "How to Dispose of a Portable Power Station (Battery Recycling 2026)",
        "hero_title": "How to Dispose of a Portable Power Station",
        "bc_name": "Disposal & Recycling",
        "cat_name": "Outdoor Power",
        "cat_url": "outdoor-power.html",
        "accent": "green",
        "badges": [
            {"icon":"recycle","text":"RECYCLING","color":"green"},
            {"icon":"shield-alert","text":"Safety Guide","color":"red"},
            {"icon":"scale","text":"Legal Info","color":"info"},
        ],
        "stats": [
            {"icon":"trash-2","label":"Never Trash","val":"Always Recycle","vc":"red-400"},
            {"icon":"recycle","label":"Recyclable Parts","val":"90%+","vc":"green-400"},
            {"icon":"alert-triangle","label":"Fire Risk","val":"High if Damaged","vc":"yellow-400"},
            {"icon":"clock","label":"Battery Lifespan","val":"3–10 yrs","vc":"electric-400"},
        ],
        "hero_intro": "Proper disposal of portable power stations is important for both safety and the environment. These devices contain lithium batteries that can be dangerous if thrown in the trash — they can cause fires in garbage trucks and landfills, and the toxic metals can leach into soil and groundwater. The good news is that there are many options for proper disposal and recycling, and some programs even accept working units for donation or refurbishment. This guide covers everything you need to know to dispose of your power station responsibly.",
        "quick_answer": "Never throw a portable power station in the trash — it contains lithium batteries that are a fire hazard and environmental hazard. Instead, take it to a battery recycling center, a big-box store with battery recycling (Home Depot, Lowe's, Best Buy), your local household hazardous waste facility, or use a manufacturer take-back program. For working units, consider selling, donating, or trading in instead of recycling. Laws vary by state, but most require lithium battery recycling and prohibit disposal in regular trash.",
        "toc": [
            {"id":"why","title":"Why Proper Disposal Matters"},
            {"id":"types","title":"Battery Types & Environmental Impact"},
            {"id":"methods","title":"Proper Disposal Methods"},
            {"id":"finding","title":"Finding Recycling Centers Near You"},
            {"id":"donation","title":"Donation & Resale Options"},
            {"id":"repair","title":"Repair Before You Replace"},
            {"id":"legal","title":"Legal Requirements by State"},
            {"id":"prepare","title":"How to Prepare for Disposal"},
            {"id":"pro","title":"Pro Tips & Best Practices"},
            {"id":"faq","title":"Frequently Asked Questions"},
            {"id":"related","title":"Related Guides"},
        ],
        "sections": [
            {"id":"why","title":"Why Proper Disposal Matters",
             "parts":[
                p("Portable power stations are not like regular electronics. They contain large lithium batteries that pose significant risks if disposed of improperly. Here is why proper disposal matters:"),
                steps([
                    {"title":"Fire Hazard","body":"Lithium batteries can short-circuit and catch fire if damaged. In garbage trucks, compaction can puncture battery cells, causing thermal runaway and fires. These fires can destroy garbage trucks, spread to entire waste facilities, and are extremely difficult to put out. Lithium battery fires in landfills can burn underground for years."},
                    {"title":"Environmental Contamination","body":"Lithium batteries contain heavy metals (cobalt, nickel, manganese), toxic electrolytes, and other harmful substances. When batteries break down in landfills, these chemicals can leach into soil and groundwater, contaminating drinking water supplies and harming ecosystems. Proper recycling recovers these materials safely."},
                    {"title":"Resource Recovery","body":"Batteries contain valuable materials — lithium, cobalt, nickel, copper, aluminum — that can be recovered and used to make new batteries. Recycling reduces the need for mining of these materials, which has its own environmental and human costs. The more we recycle, the less we need to mine."},
                    {"title":"Legal Compliance","body":"Many states and localities have laws requiring proper disposal of lithium batteries. Throwing them in the trash can result in fines. Commercial generators (businesses) have even stricter requirements under RCRA (Resource Conservation and Recovery Act). Always check your local regulations."},
                ], "red"),
                alert("critical","Critical: Never put lithium batteries in the trash or recycling bin. Even small batteries can cause fires. Always take them to a designated battery recycling location. If the battery is swollen, damaged, or leaking, handle with extreme care and tape the terminals before transport."),
             ]},
            {"id":"types","title":"Battery Types & Environmental Impact",
             "parts":[
                p("Different battery chemistries have different environmental impacts and recycling considerations. Here is how the main types compare:"),
                table(["Chemistry","Toxic Materials","Recyclability","Fire Risk","Common Use"],[
                    ["LiFePO4 (LFP)","Low — iron phosphate, no cobalt/nickel","Good — easier to recycle","Low — very stable","Most 2026 power stations"],
                    ["Lithium-ion (NMC/NCA)","High — cobalt, nickel, manganese","Moderate — valuable but toxic metals","High — thermal runway risk","Older/budget stations, laptops"],
                    ["Lead-Acid","High — lead is highly toxic","Very good — 90%+ recycled","Low — but acid hazard","Very old/cheap stations"],
                    ["Nickel-Cadmium (NiCd)","High — cadmium is very toxic","Good — well-established recycling","Low","Vintage devices only"],
                ]),
                p("LiFePO4 (LFP) batteries are generally better for the environment than NMC/NCA lithium-ion. They do not contain cobalt or nickel — two of the most problematic materials in lithium batteries. LFP is also more chemically stable and less likely to catch fire. However, all lithium batteries should be recycled regardless of chemistry."),
                p("The good news is that battery recycling technology is improving rapidly. New processes can recover 90%+ of the lithium, cobalt, nickel, and copper from old batteries. These recycled materials can be used to make new battery cells, creating a circular economy. Some manufacturers are even building their own recycling facilities to close the loop."),
             ]},
            {"id":"methods","title":"Proper Disposal Methods",
             "parts":[
                p("There are several proper ways to dispose of a portable power station. Which method is best depends on whether the unit is working, its condition, and what options are available in your area."),
                grid([
                    {"title":"Household Hazardous Waste (HHW)","title_color":"yellow-400","body":"Most counties and cities have a household hazardous waste facility that accepts lithium batteries, often for free or a small fee. These facilities are set up to handle dangerous materials safely. Many also hold periodic HHW collection events at convenient locations. This is the most reliable disposal method for non-working units."},
                    {"title":"Big-Box Store Drop-Off","title_color":"green-400","body":"Many national retailers accept rechargeable batteries for recycling at no cost. Home Depot, Lowe's, Best Buy, and Staples all have battery recycling bins near the entrance. These programs are designed for consumer batteries and usually accept power tool batteries, phone batteries, and sometimes larger items. Call ahead to confirm they accept power station-sized batteries."},
                    {"title":"Manufacturer Take-Back Programs","title_color":"electric-400","body":"Some power station manufacturers offer take-back or recycling programs for their products. EcoFlow, Jackery, Bluetti, and others may have recycling options, sometimes for free and sometimes for a small fee. Check the manufacturer's website or contact support to see what programs they offer. This is often the easiest way if you are buying a new unit from the same brand."},
                    {"title":"Specialty Battery Recyclers","title_color":"purple-400","body":"Companies like Call2Recycle, Battery Solutions, and Redwood Materials specialize in battery recycling. Some offer mail-in programs — you ship the battery to them and they recycle it properly. Some are free, some charge a fee depending on battery size and type. Search for 'lithium battery recycling near me' to find local options."},
                ]),
                p("For very large or commercial quantities, you may need to work with a licensed hazardous waste transporter and disposal facility. This is more expensive but required for businesses and organizations generating large volumes of battery waste. Always verify that the recycler is properly licensed and follows environmental regulations."),
                alert("info","Tip: Call2Recycle (call2recycle.org) is a free national program that helps consumers find battery recycling locations. Enter your zip code on their website to find drop-off locations near you. They partner with thousands of retailers and municipalities across the United States."),
             ]},
            {"id":"finding","title":"Finding Recycling Centers Near You",
             "parts":[
                p("Finding the right recycling location can take a bit of research, but there are many resources available. Here are the best ways to find battery recycling near you:"),
                steps([
                    {"title":"Use Online Locators","body":"Websites like Call2Recycle.org, Earth911.com, and your local waste management company's website have search tools to find recycling locations. Enter your zip code and what you want to recycle (lithium-ion batteries, portable power stations, e-waste) and you will get a list of nearby options."},
                    {"title":"Check with Local Government","body":"Your city or county solid waste department usually runs a household hazardous waste program. Check their website or call their customer service line. Many have permanent facilities and/or periodic collection events. This is often free for residents."},
                    {"title":"Visit Retailers","body":"Home Depot, Lowe's, Best Buy, Staples, and other big-box stores often have battery recycling bins. Some accept only small batteries (AA, AAA, phone batteries), while others accept larger items. Best Buy in particular has a fairly comprehensive electronics recycling program. Always call ahead to confirm what they accept."},
                    {"title":"Ask the Manufacturer","body":"If you cannot find a local option, contact the power station manufacturer. They may have a take-back program or be able to point you to authorized recycling partners in your area. Some brands even offer discounts on new products when you recycle an old one."},
                ], "green"),
                p("When you go to drop off your battery, you may be asked for your zip code (for tracking purposes), what type of battery it is, and whether it is damaged. Some facilities have limits on how many batteries you can drop off per visit (e.g., 5-10 per household per day). If you have a large quantity, you may need to make an appointment or use a commercial service."),
             ]},
            {"id":"donation","title":"Donation & Resale Options (For Working Units)",
             "parts":[
                p("If your power station still works (or even if it just needs a new battery), consider donating or selling it instead of recycling. Reuse is even better for the environment than recycling, since it avoids the energy and materials needed to make a new product."),
                grid([
                    {"title":"Sell It Used","title_color":"green-400","body":"There is a robust market for used power stations. Even older models sell well on Facebook Marketplace, Craigslist, eBay, and Reddit communities like r/ULgeartrade and r/Marketplace. Be honest about condition, cycle count, and any issues. Include photos and the original specs. Working units usually sell for 40-70% of retail depending on age and condition."},
                    {"title":"Donate to Charity","title_color":"yellow-400","body":"Many organizations can use working power stations: emergency response teams (CERT, Red Cross), community groups, schools with STEM programs, outdoor education programs, animal shelters, disaster relief organizations, and local mutual aid groups. You may even be able to claim a tax deduction for the donation. Call ahead to see if they accept power equipment."},
                    {"title":"Trade-In Programs","title_color":"electric-400","body":"Some manufacturers and retailers offer trade-in programs where you get credit toward a new unit when you send in your old one. EcoFlow, Jackery, and other brands occasionally run trade-in promotions. Even if there is no formal program, it never hurts to ask customer support about trade-in options."},
                    {"title":"Gift or Give Away","title_color":"purple-400","body":"Know someone who camps or is into preparedness? A used power station makes a great gift. You can also list it for free on Freecycle, Buy Nothing groups, or Craigslist free section. Someone will be happy to take it off your hands. Just be clear about the condition so there are no surprises."},
                ]),
                p("What if the battery is dead but the rest works? You can still sell or donate it — some people buy non-working units for parts or to replace the battery themselves. Just be very clear in the listing that the battery is dead/needs replacement and sell it as-is for parts or repair."),
             ]},
            {"id":"repair","title":"Repair Before You Replace",
             "parts":[
                p("Before you dispose of a power station, consider whether it can be repaired. Many common issues are fixable, and repairing is almost always better than recycling from an environmental standpoint (and usually cheaper than buying new)."),
                table(["Issue","Fixable?","Typical Cost","Difficulty"],[
                    ["Dead / degraded battery","Yes (on most models)","$300–$1,500","Easy–Moderate"],
                    ["AC output not working","Often fixable","$100–$500","Moderate–Hard"],
                    ["Display not working","Often fixable","$50–$200","Easy–Moderate"],
                    ["Charging port loose/broken","Yes","$50–$150","Moderate"],
                    ["Fan making noise","Yes","$20–$100","Easy–Moderate"],
                    ["Swollen battery","No (replace battery only)","$300–$1,500","Moderate"],
                    ["Water damage / corrosion","Sometimes","Variable","Hard"],
                    ["Physical damage (cracked case)","Cosmetic only","$0–$50","Easy"],
                ]),
                p("Where to get repairs? Options include: manufacturer's authorized service centers, local electronics repair shops, specialty battery shops, and DIY (if you are technically inclined). Always get a quote before committing to repairs — sometimes the repair cost is close to the cost of a new unit, especially for budget models."),
                alert("warning","Safety note: Do not attempt to repair a swollen, leaking, or damaged lithium battery. These can be dangerous. Dispose of swollen batteries properly at a hazardous waste facility. Only work on electronics if you have the proper tools, knowledge, and safety equipment."),
             ]},
            {"id":"legal","title":"Legal Requirements by State",
             "parts":[
                p("Laws regarding lithium battery disposal vary by state and locality. In general, it is illegal to throw lithium batteries in the trash in most states, but enforcement varies. Here is a summary of the regulatory landscape as of 2026:"),
                p("At the federal level, lithium batteries are regulated under the Resource Conservation and Recovery Act (RCRA) when they become waste. However, household waste (batteries from personal use) is generally exempt from federal hazardous waste rules, which means it is regulated at the state and local level instead. Commercial/business waste is subject to full RCRA requirements."),
                grid([
                    {"title":"California","title_color":"red-400","body":"California has some of the strictest e-waste and battery laws. The California Battery Recovery Act requires retailers to accept rechargeable batteries for recycling. It is illegal to dispose of lithium batteries in the trash. The state has an extensive network of recycling centers and collection events."},
                    {"title":"New York","title_color":"yellow-400","body":"New York State's Rechargeable Battery Law requires manufacturers to fund collection and recycling of rechargeable batteries. Retailers that sell rechargeable batteries must accept them for recycling free of charge. NYC has additional rules requiring battery recycling at many locations."},
                    {"title":"Minnesota","title_color":"green-400","body":"Minnesota has a comprehensive battery recycling program run by the state. The Minnesota Battery Management Act covers rechargeable batteries and requires proper disposal. The state runs periodic collection events and maintains a list of accepted locations."},
                ], 3),
                p("Most other states have some form of battery recycling requirement or program, but details vary. The trend is clearly toward more regulation, not less. Even if it is not explicitly illegal where you live, proper disposal is still the right thing to do for safety and environmental reasons."),
                p("When in doubt, contact your local solid waste department or environmental health agency. They can tell you exactly what the rules are in your area and where you can take batteries for proper disposal."),
             ]},
            {"id":"prepare","title":"How to Prepare Your Power Station for Disposal",
             "parts":[
                p("Before taking your power station in for recycling or disposal, there are a few important steps to take for safety and to protect your personal data."),
                steps([
                    {"title":"Discharge the Battery","body":"If possible, discharge the battery to about 20-30% before disposal. A fully discharged battery is safer to transport and handle. Do not discharge all the way to 0% — 20-30% is ideal for storage and transport. If the battery is completely dead already, that is fine too — just handle it carefully."},
                    {"title":"Wipe Your Data","body":"If your power station has Wi-Fi, app connectivity, or stores any personal data, do a factory reset before disposing of it. Log out of any accounts, remove any Wi-Fi passwords, and reset to factory settings if the option exists. This protects your privacy and security, just like wiping a phone or computer before selling it."},
                    {"title":"Inspect for Damage","body":"Check the battery and case for any signs of damage: swelling, bulging, leaking, cracks, burn marks. If the battery is swollen or damaged, you need to handle it with extra care. Tape over the terminals with electrical tape or Kapton tape to prevent short circuits. Place it in a non-conductive container (plastic bucket, cardboard box) for transport."},
                    {"title":"Package for Transport","body":"For transport, place the power station in its original box if you still have it, or in a sturdy cardboard box with padding. If the battery is damaged, place it in a fire-resistant container (metal box, concrete bucket, sand) if possible. Do not put damaged batteries in the trunk of a hot car for long periods. Take them directly to the recycling facility."},
                ], "yellow"),
                alert("critical","Critical safety: If a battery is swollen, leaking, smoking, or otherwise damaged, do NOT charge it, do NOT put it in a closed container that could build up pressure, and do NOT throw it in the trash. Handle with gloves and eye protection if available. Tape the terminals. Take it immediately to a hazardous waste facility that accepts damaged lithium batteries. Call ahead to confirm they accept damaged batteries."),
             ]},
            {"id":"pro","title":"Pro Tips & Best Practices",
             "parts":[
                grid([
                    {"title":"Choose Products with Recycling in Mind","title_color":"green-400","body":"When buying a new power station, consider the brand's sustainability and recycling programs. Brands that offer take-back programs, use easily recyclable chemistries (LFP), and design for repairability are better for the planet long-term. Do your research before you buy."},
                    {"title":"Extend Battery Life","title_color":"electric-400","body":"The best thing you can do for the environment is make your power station last as long as possible. Follow battery care best practices: avoid extreme heat, store at 50-60% charge, avoid full discharges, use LiFePO4 chemistry. Every year you extend the life is one less battery that needs to be manufactured and recycled."},
                    {"title":"Buy Used When Possible","title_color":"yellow-400","body":"Consider buying a used or refurbished power station instead of new. Reusing is even better than recycling. Many used units have plenty of life left and sell for a fraction of the new price. Just be sure to test thoroughly and check battery health before buying."},
                    {"title":"Support Battery Recycling Policy","title_color":"purple-400","body":"Support policies and programs that improve battery recycling infrastructure. The more demand there is for proper recycling, the more options will become available. Vote for candidates who support environmental initiatives, and tell manufacturers you want better recycling programs."},
                ]),
             ]},
        ],
        "faqs": [
            {"q":"Can I throw a portable power station in the trash?","a":"No — never throw a portable power station in the trash. It contains lithium batteries that can cause fires in garbage trucks and landfills, and the toxic materials can contaminate the environment. Most states and localities also prohibit disposing of lithium batteries in regular trash. Always recycle properly at a designated facility."},
            {"q":"Where can I recycle a portable power station?","a":"Options include: household hazardous waste facilities, big-box stores with battery recycling (Home Depot, Lowe's, Best Buy), manufacturer take-back programs, specialty battery recyclers (Call2Recycle, Battery Solutions, Redwood Materials), and local e-waste collection events. Use Call2Recycle.org or Earth911.com to find locations near you."},
            {"q":"How much does it cost to recycle a power station?","a":"Many recycling options are free for consumers. Household hazardous waste facilities are usually free for residents. Big-box store drop-offs are typically free. Some specialty recyclers and manufacturer programs charge a fee ($20-100 depending on battery size). Call ahead to confirm pricing and whether they accept your specific item."},
            {"q":"What should I do with a swollen power station battery?","a":"A swollen battery is a safety hazard. Do NOT charge it, do not use it, and do not throw it in the trash. Handle with care — wear gloves and eye protection. Tape the terminals with electrical tape to prevent short circuits. Place it in a non-conductive, non-sealed container. Take it immediately to a household hazardous waste facility or battery recycler that accepts damaged lithium batteries. Call ahead to confirm."},
            {"q":"Can I donate or sell a working power station?","a":"Yes, absolutely! Reuse is even better than recycling. You can sell working units on Facebook Marketplace, Craigslist, eBay, or Reddit. You can donate to emergency response teams, schools, community groups, shelters, or disaster relief organizations. Some manufacturers also offer trade-in programs. Always be honest about condition, age, and any issues."},
            {"q":"Is it better to repair or recycle a broken power station?","a":"Repair is almost always better if it is economically feasible. If the battery is the only issue and replacement costs less than 60% of a new unit, replacing the battery is better for the environment and your wallet. If the repair would cost nearly as much as a new unit, or if there are multiple issues, recycling is the right call."},
            {"q":"What parts of a power station are recyclable?","a":"About 90% of a power station is recyclable. The battery cells are the most important part to recycle — lithium, cobalt, nickel, copper, and aluminum can all be recovered. The metal case, wiring, circuit boards, and plastic components can also be recycled by e-waste recyclers. Overall, power stations are quite recyclable when processed at proper facilities."},
            {"q":"Are there laws requiring battery recycling?","a":"Yes, many states and localities have laws requiring proper disposal of rechargeable batteries. California, New York, Minnesota, and several other states have specific battery recycling laws. Even in states without explicit laws, lithium batteries may be classified as hazardous waste under certain conditions, making improper disposal illegal. When in doubt, recycle — it is the right thing to do."},
            {"q":"How do I prepare my power station for recycling?","a":"Discharge the battery to about 20-30% if possible (do not fully discharge to 0%). Do a factory reset to wipe personal data and Wi-Fi passwords. Inspect for damage — if swollen or damaged, tape terminals and handle with extra care. Package in a sturdy box for transport. Do not put damaged batteries in hot cars or sealed containers."},
            {"q":"Are LiFePO4 batteries better for the environment?","a":"Generally yes. LiFePO4 (LFP) batteries do not contain cobalt or nickel (which have significant environmental and human rights concerns in mining). LFP is also more chemically stable and safer, reducing fire risk during use and disposal. However, all lithium batteries should be recycled properly regardless of chemistry. LFP still contains lithium, copper, aluminum, and other materials that can and should be recovered."},
        ],
        "related": [
            {"url":"portable-power-station-battery-replacement-cost.html","title":"Battery Replacement Cost","desc":"Battery replacement costs by brand, DIY vs professional, warranty coverage.","badge_color":"yellow","badge_text":"COST","sub_badge":"All Brands"},
            {"url":"how-to-store-portable-power-station.html","title":"Storage Guide","desc":"How to store a portable power station long-term — ideal charge level, temperature, cycling.","badge_color":"green","badge_text":"STORAGE","sub_badge":"Guide"},
            {"url":"portable-power-station-overheating-hot.html","title":"Overheating Guide","desc":"Why power stations overheat, temperature effects on battery life, cooling tips.","badge_color":"red","badge_text":"HEAT","sub_badge":"Universal"},
            {"url":"dji-drone-battery-swelling-what-to-do.html","title":"Swollen Battery Guide","desc":"What to do with a swollen drone battery — causes, safety, proper disposal.","badge_color":"orange","badge_text":"SAFETY","sub_badge":"DJI"},
            {"url":"portable-power-station-not-charging.html","title":"Not Charging Fixes","desc":"Before you recycle a station that won't charge, try these troubleshooting steps first.","badge_color":"yellow","badge_text":"FIX","sub_badge":"Universal"},
            {"url":"outdoor-power.html","title":"Power Station Comparison","desc":"Compare all major portable power station models side by side.","badge_color":"purple","badge_text":"COMPARE","sub_badge":"All Brands"},
        ],
    }


# ============================================================
# MAIN
# ============================================================

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    pages = [
        get_page_battery_replacement(),
        get_page_rv(),
        get_page_disposal(),
    ]

    # Regenerate page 1 for consistency
    # (we'll skip it since it already exists and is good)

    results = []
    for pg in pages:
        filepath = os.path.join(OUTPUT_DIR, pg["filename"])
        try:
            html_content = build_page(pg)
            with open(filepath, "w") as f:
                f.write(html_content)
            wc = word_count(html_content)
            results.append((pg["filename"], wc, "OK"))
        except Exception as e:
            results.append((pg["filename"], 0, f"ERROR: {e}"))

    print("\n" + "="*70)
    print("PAGE GENERATION RESULTS")
    print("="*70)
    total_words = 0
    ok_count = 0
    for fn, wc, status in results:
        if status == "OK":
            ok_count += 1
            total_words += wc
            print(f"  ✓ {fn}: {wc:,} words")
        else:
            print(f"  ✗ {fn}: {status}")

    print(f"\nTotal: {ok_count}/{len(pages)} pages generated successfully")
    print(f"Total words: {total_words:,}")
    if ok_count > 0:
        print(f"Average words per page: {total_words // ok_count:,}")
    print("="*70)


if __name__ == "__main__":
    main()
