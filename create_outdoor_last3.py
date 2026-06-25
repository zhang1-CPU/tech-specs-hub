#!/usr/bin/env python3
"""Generate last 3 Outdoor Power pages: extension cords, under $500, UPS mode."""

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

# =================== PAGE 8: EXTENSION CORDS ===================

page8 = {
    "filename": "can-i-use-extension-cord-with-power-station.html",
    "title": "Can I Use an Extension Cord With a Portable Power Station? (2026)",
    "headline": "Can I Use an Extension Cord With a Portable Power Station? (2026)",
    "meta_desc": "Can you use an extension cord with a portable power station? Complete safety guide covering gauge vs length, voltage drop, AC vs DC cords, recommended sizes, and outdoor rated cords.",
    "category": "Outdoor Power",
    "category_link": "outdoor-power.html",
    "breadcrumb_title": "Extension Cord Guide",
    "hero_blur": "bg-blue-500/5",
    "hero_badges": '''<div class="px-3 py-1.5 bg-blue-500/20 text-blue-400 font-mono font-bold text-sm rounded-md border border-blue-500/30">EXTENSION&nbsp;CORDS</div>
        <span class="badge badge-info"><i data-lucide="cable" style="width:0.75rem;height:0.75rem"></i>Safety Guide</span>
        <span class="badge badge-info"><i data-lucide="zap" style="width:0.75rem;height:0.75rem"></i>Voltage Drop</span>''',
    "h1": 'Can I Use an Extension Cord With a Portable Power Station? &mdash; <span class="gradient-text">2026 Safety Guide</span>',
    "hero_desc": "Yes, you can use extension cords with portable power stations — but you need to use the right type and gauge. Using the wrong extension cord causes voltage drop, reduces power output, wastes energy as heat, and in extreme cases can be a fire hazard. This guide covers everything you need to know: how wire gauge works, how length affects capacity, AC vs DC extension cords, which cord to use for different wattages, and outdoor-rated vs indoor cords.",
    "hero_stats": f'''<div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="cable" style="width:0.9rem;height:0.9rem"></i>16 AWG</div>
          <div class="font-mono font-bold text-xl text-yellow-400">Up to 10A</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="cable" style="width:0.9rem;height:0.9rem"></i>14 AWG</div>
          <div class="font-bold text-xl text-green-400">Up to 15A</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="cable" style="width:0.9rem;height:0.9rem"></i>12 AWG</div>
          <div class="font-mono font-bold text-xl text-electric-400">Up to 20A</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="cable" style="width:0.9rem;height:0.9rem"></i>10 AWG</div>
          <div class="font-bold text-xl text-purple-400">Up to 30A</div>
        </div>''',
    "qa_gradient": "from-blue-950/20 to-navy-900 border-blue-500/20",
    "qa_icon_color": "#60a5fa",
    "qa_title": "Can You Use Extension Cords?",
    "qa_text": '<strong class="text-white">Yes, you absolutely can use extension cords with portable power stations — as long as you use the correct gauge (thickness) for the length and wattage.</strong> The key principle is: the longer the cord and the more watts you are pulling, the thicker the wire needs to be. Using a cord that is too thin causes voltage drop — you lose power as heat, devices may not work properly, and the cord can overheat. For most portable power station use cases (under 1,500W, 25ft or less), a standard 14-gauge extension cord works fine. For higher power or longer runs, use 12-gauge or 10-gauge.',
    "qa_extra": f'''<div class="grid md:grid-cols-2 gap-3 mt-4">
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-green-400 font-semibold mb-1 flex items-center gap-2"><i data-lucide="check" style="width:1rem;height:1rem"></i>Safe use</div>
          <p class="text-sm text-gray-300">Use properly rated cords, keep them uncoiled, avoid daisy-chaining, inspect for damage, don\'t run under rugs</p>
        </div>
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-red-400 font-semibold mb-1 flex items-center gap-2"><i data-lucide="x" style="width:1rem;height:1rem"></i>Never do this</div>
          <p class="text-sm text-gray-300">Daisy-chain multiple cords, use damaged cords, overload beyond rating, run through water, bury in ground</p>
        </div>
      </div>''',
    "sections": [
        {
            "id": "gauge-explained",
            "title": "Wire Gauge & Thickness Explained",
            "content": p("Extension cords are rated by AWG (American Wire Gauge), which measures the thickness of the copper wire inside the insulation. Counterintuitively, a lower gauge number means a thicker wire. Thicker wires can carry more current with less voltage drop.") +
            specs_table(
                ["AWG Gauge", "Diameter (inches)", "Max Current (25ft)", "Max Current (50ft)", "Typical Use"],
                [
                    ["<strong>18 AWG</strong>", "0.040\"", "5-7A", "3-4A", "Very low power — lamps, phone chargers only"],
                    ["<strong>16 AWG</strong>", "0.051\"", "10-13A", "6-8A", "Small appliances, up to ~1,000W short runs"],
                    ["<strong>14 AWG</strong>", "0.064\"", "15-18A", "10-12A", "Most common — up to ~1,500W"],
                    ["<strong>12 AWG</strong>", "0.081\"", "20-25A", "15-18A", "Heavy-duty — up to ~2,500W"],
                    ["<strong>10 AWG</strong>", "0.102\"", "30-35A", "20-25A", "Very high power — up to ~3,500W"],
                    ["<strong>8 AWG</strong>", "0.128\"", "40-50A", "30-35A", "Industrial / RV 30A service"],
                ]
            ) +
            p("These are conservative guidelines for typical use. The exact amperage rating depends on ambient temperature, whether the cord is bundled or coiled, and the insulation rating. When in doubt, go one gauge thicker — it never hurts to have extra capacity.") +
            alert("info", "cable", "How to tell what gauge your cord is", "Most extension cords have the gauge printed on the insulation along the length of the cord. Look for text like '14AWG' or '12/3' (12 gauge, 3 conductors). If it is not printed, you can use a wire gauge tool or look up the product model online. Heavier, thicker cords are lower gauge — you can often feel the difference.")
        },
        {
            "id": "voltage-drop",
            "title": "Voltage Drop — Why Gauge Matters",
            "content": p("When electricity flows through a wire, some energy is lost as heat due to the wire's electrical resistance. This is called voltage drop. The longer the wire and the thinner the wire, the more voltage you lose. Too much voltage drop can cause:") +
            '<ul class="space-y-2 text-sm text-gray-300 mb-4">' +
            '<li>• Devices not working properly or not turning on at all</li>' +
            '<li>• Motors running slower and overheating</li>' +
            '<li>• Reduced power output from your power station</li>' +
            '<li>• Wasted battery capacity (lost as heat in the cord)</li>' +
            '<li>• In extreme cases, overheating and fire risk</li>' +
            '</ul>' +
            specs_table(
                ["Gauge", "25 ft (15A load)", "50 ft (15A load)", "100 ft (15A load)", "Acceptable?"],
                [
                    ["<strong>16 AWG</strong>", "~4.2V drop (3.5%)", "~8.4V drop (7%)", "~16.8V drop (14%)", "25ft OK, 50ft+ too much"],
                    ["<strong>14 AWG</strong>", "~2.6V drop (2.2%)", "~5.3V drop (4.4%)", "~10.5V drop (8.8%)", "25-50ft OK, 100ft borderline"],
                    ["<strong>12 AWG</strong>", "~1.6V drop (1.3%)", "~3.3V drop (2.8%)", "~6.6V drop (5.5%)", "All lengths acceptable for 15A"],
                    ["<strong>10 AWG</strong>", "~1.0V drop (0.8%)", "~2.1V drop (1.7%)", "~4.1V drop (3.4%)", "All lengths excellent"],
                ]
            ) +
            p("The generally accepted maximum voltage drop for safe operation is 3-5%. More than that and you start wasting significant power and risking device damage. For sensitive electronics, aim for under 3% drop. For resistive loads like heaters, up to 5% is usually fine.") +
            alert("warning", "flame", "Coiled cords are dangerous", "Never use an extension cord that is tightly coiled or bundled up while under load. Coiled cords cannot dissipate heat properly, and the magnetic fields from each loop interact, causing additional heating. A coiled cord can overheat even at currents that would be safe when uncoiled. Always fully extend extension cords before using them at high power.")
        },
        {
            "id": "ac-vs-dc",
            "title": "AC vs DC Extension Cords",
            "content": p("Portable power stations have both AC (household) outlets and DC outputs (USB, 12V car port, solar input). Each type of output has different extension cord requirements:") +
            '<div class="grid md:grid-cols-2 gap-6 mb-6">' +
            '<div>' +
            '<h3 class="font-bold text-xl mb-4 text-electric-400">AC Extension Cords (120V)</h3>' +
            '<ul class="space-y-3 text-sm text-gray-300">' +
            '<li>• <strong class="text-white">Voltage:</strong> 120V AC — same as wall outlets</li>' +
            '<li>• <strong class="text-white">Gauge matters:</strong> Yes, but less critical than DC due to higher voltage</li>' +
            '<li>• <strong class="text-white">Cord type:</strong> Standard household extension cords work</li>' +
            '<li>• <strong class="text-white">Connectors:</strong> NEMA 5-15 (standard 3-prong plug)</li>' +
            '<li>• <strong class="text-white">Safety:</strong> Use grounded (3-prong) cords for 3-prong devices</li>' +
            '<li>• <strong class="text-white">Rule of thumb:</strong> 14-gauge for most uses, 12-gauge for 1,500W+ or long runs</li>' +
            '</ul></div>' +
            '<div>' +
            '<h3 class="font-bold text-xl mb-4 text-purple-400">DC Extension Cords (12V / Solar)</h3>' +
            '<ul class="space-y-3 text-sm text-gray-300">' +
            '<li>• <strong class="text-white">Voltage:</strong> 12-48V DC — much lower than AC</li>' +
            '<li>• <strong class="text-white">Gauge matters:</strong> Much more critical! Low voltage = high current = more drop</li>' +
            '<li>• <strong class="text-white">Cord type:</strong> Use properly rated DC cord, not AC extension cord</li>' +
            '<li>• <strong class="text-white">Connectors:</strong> MC4 (solar), Anderson, 12V car plug, etc.</li>' +
            '<li>• <strong class="text-white">Safety:</strong> Use the correct gauge, especially for solar and high-current DC</li>' +
            '<li>• <strong class="text-white">Rule of thumb:</strong> 10-12 AWG for 12V 10-30A, shorter is better</li>' +
            '</ul></div></div>' +
            p("The key difference: DC at low voltage (12V, 24V) requires much thicker wires for the same power as AC at 120V. This is because power = voltage × current. At 12V, 120W = 10A. At 120V, 120W = 1A. 10A needs a much thicker wire than 1A. This is why solar panel extension cables are usually thick 10-12 AWG wire with MC4 connectors.") +
            alert("warning", "alert-triangle", "Never use AC extension cords for high-current DC", "Do not use a standard household AC extension cord for 12V high-current applications like a car fridge or trolling motor. The 16-gauge wire in cheap AC cords is way too thin for 10-20A at 12V — the voltage drop will be enormous and the cord can overheat. Always use properly rated DC cables.")
        },
        {
            "id": "recommended-sizes",
            "title": "Recommended Cord Sizes by Wattage",
            "content": p("Here is a practical guide to what gauge extension cord you need for different power levels and cord lengths with AC output:") +
            specs_table(
                ["Watts (120V)", "25 ft cord", "50 ft cord", "100 ft cord", "Typical Devices"],
                [
                    ["<strong>0–300W</strong>", "16 AWG", "16 AWG", "14 AWG", "Phone chargers, laptop, LED lights, small speaker"],
                    ["<strong>300–700W</strong>", "16 AWG", "14 AWG", "14 AWG", "Small fridge, TV, blender, fan"],
                    ["<strong>700–1,200W</strong>", "14 AWG", "14 AWG", "12 AWG", "Microwave, coffee maker, electric skillet"],
                    ["<strong>1,200–1,800W</strong>", "14 AWG", "12 AWG", "12 AWG", "Electric grill, hair dryer, space heater"],
                    ["<strong>1,800–2,500W</strong>", "12 AWG", "12 AWG", "10 AWG", "High-power tools, large appliances"],
                    ["<strong>2,500–3,500W</strong>", "10 AWG", "10 AWG", "8 AWG", "Max output of large power stations"],
                ]
            ) +
            p("These are conservative recommendations for general use. If you are running sensitive electronics, you want to go one gauge thicker. If you are only running simple resistive loads (heaters, incandescent lights), you can push a bit closer to the limit.") +
            step_grid([
                {"title": "How to Choose the Right Cord", "desc": "Step 1: Add up the total watts of all devices you will plug in. Step 2: Determine how long the cord needs to be. Step 3: Use the table above to find the minimum gauge. Step 4: Go one gauge thicker if possible — extra capacity costs a few dollars but gives you safety margin and future-proofing."},
                {"title": "3-Prong vs 2-Prong", "desc": "Always use 3-prong (grounded) extension cords with 3-prong devices. The ground pin is a safety feature that protects you from shock if something goes wrong. Modern portable power stations have grounded outlets, so use grounded cords. 2-prong cords are only appropriate for double-insulated low-power devices."},
            ], "green") +
            alert("info", "dollar-sign", "Cost vs value", "A 14-gauge 25ft cord costs $10-20. A 12-gauge 25ft cord costs $15-30. The price difference is small compared to the cost of a power station and the devices you are powering. Buying the next size up is cheap insurance. We recommend 12-gauge as the general-purpose cord for most people with portable power stations."),
        },
        {
            "id": "outdoor-rated",
            "title": "Outdoor-Rated Cords & Weather Resistance",
            "content": p("If you are using your power station outdoors (camping, tailgating, construction), you need outdoor-rated extension cords. Indoor cords are not designed to withstand moisture, UV light, temperature extremes, or physical abrasion.") +
            specs_table(
                ["Cord Rating", "Weather Resistance", "UV Resistance", "Temperature Range", "Best For"],
                [
                    ["<strong>Indoor (SJTW)</strong>", "None", "None", "Limited", "Indoor use only — never outside"],
                    ["<strong>Outdoor (SJTW-A)</strong>", "Water resistant", "Good", "-40 to +60°C", "General outdoor use, camping, tailgating"],
                    ["<strong>Heavy-duty outdoor (STW)</strong>", "Very water resistant", "Excellent", "-40 to +90°C", "Construction, industrial, extreme conditions"],
                    ["<strong>Submersible (Wet location)</strong>", "Waterproof", "Excellent", "Wide range", "Very specific applications — rare for power stations"],
                ]
            ) +
            p("Look for letters on the cord jacket to identify the rating: S = Service cord (flexible), J = Junior (300V insulation), T = Thermoplastic, W = Weather-resistant, E = Elastomer, O = Oil-resistant. For most portable power station outdoor use, SJTW or STW is perfect.") +
            step_grid([
                {"title": "Outdoor Cord Safety Tips", "desc": "1) Never leave outdoor cords submerged in water. 2) Use a GFCI (ground-fault circuit interrupter) when using power near water. 3) Protect connections from rain with a plastic bag or cord connector cover. 4) Do not run cords through standing water or puddles. 5) Inspect cords before each use — discard if cracked, frayed, or damaged."},
                {"title": "Cold Weather Considerations", "desc": "Cheap extension cords become stiff and brittle in cold weather. Cracks in the insulation can develop when you bend a frozen cord. If you use your power station in freezing temperatures, look for cold-flexible cords rated for low temperatures. These stay flexible even well below freezing."},
            ], "blue") +
            alert("warning", "droplets", "Water and electricity don't mix", "Never use power stations or extension cords in heavy rain or standing water. Most portable power stations are not waterproof — even a splash of water on the outlets can cause a short circuit or shock. If it is raining, put the power station under cover and elevate the cord connections so they do not sit in puddles. When in doubt, wait for better weather.")
        },
        {
            "id": "safety-tips",
            "title": "Extension Cord Safety Best Practices",
            "content": p("Follow these safety rules to use extension cords safely with your portable power station:") +
            '<div class="grid md:grid-cols-2 gap-4">' +
            grid_cards([
                {"title": "Do Not Daisy-Chain", "color": "text-red-400", "desc": "Never plug one extension cord into another to make a longer cord. Each connection adds resistance and is a potential failure point. If you need more length, buy a single longer cord of the appropriate gauge. Daisy-chaining is one of the most common causes of extension cord failures and fires."},
                {"title": "Fully Uncoil Before Use", "color": "text-orange-400", "desc": "Always fully extend extension cords before using them at high power. Coiled cords trap heat and can overheat, even at currents that are safe when uncoiled. This is especially important with retractable cord reels — pull them all the way out before plugging in high-wattage devices."},
                {"title": "Inspect Before Each Use", "color": "text-yellow-400", "desc": "Check cords for damage: frayed insulation, cracked plugs, exposed wires, bent prongs, or signs of overheating (melting, discoloration). If you see any damage, do not use the cord. It is not worth the risk. Replace damaged cords — they are cheap compared to what could go wrong."},
                {"title": "Don't Run Under Rugs/Carpets", "color": "text-purple-400", "desc": "Never run an extension cord under a rug, carpet, or mat. The insulation cannot dissipate heat, and the cord can overheat. It also creates a tripping hazard and can be damaged by foot traffic. If you need to run a cord across a walkway, use a cord cover designed for floor use."},
                {"title": "Use the Right Cord for the Job", "color": "text-green-400", "desc": "Match the cord to the application. Use outdoor-rated cords outside, use the right gauge for the wattage, use grounded cords for grounded devices. Using the wrong cord is asking for trouble. When in doubt, get a heavier-duty cord than you think you need."},
                {"title": "Unplug When Not in Use", "color": "text-blue-400", "desc": "Unplug extension cords when they are not being used. This eliminates the small but real risk of a fault causing a fire when you are not around to notice it. It also reduces standby power draw (though that is minimal with just a cord and no devices)."},
            ], 2) +
            "</div>" +
            alert("critical", "flame", "Know the signs of overheating", "Stop using an extension cord immediately if you notice: the cord feels hot to the touch, the plug or outlet is warm or hot, you smell burning plastic or rubber, the cord is discolored or melted, or you hear buzzing or crackling sounds. Unplug from the power station end first, then inspect. Let it cool completely before investigating. Do not use a damaged or overheating cord.")
        },
        {
            "id": "solar-cables",
            "title": "Solar Panel Extension Cables",
            "content": p("Solar panel extension cables are a special case. They carry DC power at varying voltages (typically 12-48V for portable panels), which means wire gauge is even more important than for AC. Here is what you need to know about solar cables:") +
            specs_table(
                ["Cable Gauge", "Max Current", "Typical Power (at 24V)", "Typical Power (at 48V)", "Max Length (3% drop)"],
                [
                    ["<strong>14 AWG</strong>", "15A", "~360W", "~720W", "25-30ft (at 24V)"],
                    ["<strong>12 AWG</strong>", "20-25A", "~600W", "~1,200W", "50-60ft (at 24V)"],
                    ["<strong>10 AWG</strong>", "30-35A", "~840W", "~1,680W", "80-100ft (at 24V)"],
                    ["<strong>8 AWG</strong>", "40-50A", "~1,200W", "~2,400W", "120-150ft (at 24V)"],
                ]
            ) +
            p("Most portable solar panels use MC4 connectors — the industry standard for solar. When buying extension cables, make sure they have MC4 connectors on both ends (male-female or female-male as needed). Solar extension cables are usually sold in pairs (positive and negative).") +
            step_grid([
                {"title": "Tips for Solar Cables", "desc": "1) Keep solar cables as short as practical — every foot costs you power. 2) Use the proper MC4 connector tool to seat connectors properly — a loose connection causes resistance, heat, and power loss. 3) Use UV-resistant outdoor-rated solar cable (PV wire) for permanent installs. 4) Avoid sharp bends that can damage the wire or insulation. 5) Protect connections from rain and dirt."},
                {"title": "High-Voltage Solar is Better for Long Runs", "desc": "If you need to run solar cables a long distance (50ft+), use higher-voltage panels or wire panels in series to increase voltage. Doubling the voltage halves the current for the same power, which means you can use thinner cables or go twice as far with the same voltage drop. This is why grid-tie solar systems use hundreds of volts — to minimize losses in long wire runs."},
            ], "yellow") +
            alert("info", "sun", "MPPT optimization", "Your power station's MPPT charge controller works best when the solar panel voltage is significantly higher than the battery voltage. If your extension cables cause too much voltage drop, the MPPT might not operate optimally. Aim for less than 3-5% voltage drop in your solar cables for best charging performance and maximum efficiency.")
        },
    ],
    "faqs": [
        {"q": "Can I use an extension cord with a portable power station?", "a": "Yes, absolutely. Extension cords work fine with portable power stations as long as you use the correct gauge (thickness) for the length and wattage you are drawing. The key is to use a cord thick enough to handle the current without excessive voltage drop or overheating. For most uses under 1,500W and 25 feet, a standard 14-gauge extension cord is perfectly safe and adequate."},
        {"q": "What gauge extension cord do I need?", "a": "It depends on how many watts you are using and how long the cord is. For general use (under 1,500W, 25ft or less): 14-gauge. For higher power (1,500-2,500W) or longer cords (50ft+): 12-gauge. For maximum power (2,500-3,500W) or very long runs: 10-gauge. When in doubt, go one gauge thicker — it costs a few dollars more but gives you safety margin and better performance."},
        {"q": "Does using an extension cord reduce power output?", "a": "Yes, slightly. All wires have electrical resistance, so some power is lost as heat. This is called voltage drop. With a properly sized cord, the loss is minimal (1-3%) and you will barely notice it. With an undersized cord, the loss can be significant (5-15%+) — devices may not work properly, the cord can overheat, and you waste battery capacity on heating the cord instead of powering your devices."},
        {"q": "Can I daisy-chain multiple extension cords together?", "a": "No — you should never daisy-chain (plug one extension cord into another). Each connection adds resistance and is a potential point of failure. Daisy-chaining increases voltage drop and creates fire risk. If you need a longer cord, buy a single longer cord of the appropriate gauge. It is safer, more reliable, and you will have less voltage loss."},
        {"q": "Can I use a regular extension cord for solar panels?", "a": "No — do not use standard household extension cords for solar panel connections. Solar panels output DC power, and at typical solar voltages (12-48V), the current can be quite high. Household AC extension cords are usually 16-gauge, which is too thin for high-current DC. Use proper solar extension cables with MC4 connectors and appropriately sized wire (10-14 AWG depending on current and length)."},
        {"q": "Do I need an outdoor-rated extension cord for camping?", "a": "Yes — always use outdoor-rated extension cords when using your power station outside. Outdoor cords have weather-resistant insulation that can handle moisture, UV light, and temperature extremes. Indoor cords become brittle and crack when exposed to sun and rain, creating a shock and fire hazard. Look for 'SJTW' or 'STW' rated cords for outdoor use."},
        {"q": "Is it safe to leave extension cords outside in the rain?", "a": "No, you should not leave extension cords or power stations exposed to heavy rain or standing water. Most outdoor-rated cords are water-resistant, not waterproof. If it rains, make sure connections are elevated and protected from direct rain (use a plastic bag or cord cover). Never submerge cords. If there is lightning, unplug everything and get inside. Water and electricity do not mix — always err on the side of caution."},
        {"q": "How do I know if my extension cord is overheating?", "a": "Signs of an overheating extension cord include: the cord feels hot to the touch (warm is normal, hot is not), the plug or outlet is very warm or hot, you smell burning plastic or rubber, the cord is discolored or melted near connections, or you hear buzzing/crackling. If you notice any of these, unplug immediately (from the power source end first) and let it cool. Do not use a cord that overheats — replace it with a thicker gauge cord."},
        {"q": "Can I use a power strip with my power station?", "a": "Yes, you can use a power strip or surge protector with a portable power station, as long as you do not exceed the power station's output rating. Power strips let you plug in multiple devices from one outlet, which is convenient. However, daisy-chaining multiple power strips or plugging high-wattage devices into a cheap power strip is dangerous. Use a good quality surge protector power strip and be mindful of total wattage."},
        {"q": "How long can an extension cord be with a power station?", "a": "There is no hard limit — it depends on the gauge and the wattage. A 10-gauge cord can run 100+ feet at moderate power without significant loss. A 16-gauge cord should probably not exceed 25-50 feet even at low power. The practical limit for most portable power station use is 50-100 feet with appropriately sized cord. Beyond that, the voltage drop becomes significant and you lose too much power."},
    ],
    "related": std_related(),
}

PAGES = [page8]

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
