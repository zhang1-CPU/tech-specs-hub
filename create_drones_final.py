#!/usr/bin/env python3
"""Generate final 4 drone pages: battery swelling, RC calibration, ATTI mode, best photography drone."""

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

def drone_related():
    return [
        {"href": "how-to-find-lost-dji-drone.html", "badge": "LOST", "badge_class": "bg-red-500/20 text-red-400", "border_class": "border-red-500/30", "badge2": "Guide", "title": "Find Lost Drone", "desc": "Step-by-step guide to finding a lost DJI drone using Find My Drone, GPS, and community help."},
        {"href": "best-memory-card-for-dji-mini-5-pro.html", "badge": "SD&nbsp;CARD", "badge_class": "bg-yellow-500/20 text-yellow-400", "border_class": "border-yellow-500/30", "badge2": "Guide", "title": "Best Memory Card", "desc": "What SD card to use with DJI Mini 5 Pro — speed requirements, recommended brands and sizes."},
        {"href": "how-long-do-dji-drone-batteries-last.html", "badge": "BATTERY", "badge_class": "bg-green-500/20 text-green-400", "border_class": "border-green-500/30", "badge2": "Guide", "title": "Battery Lifespan", "desc": "How long DJI drone batteries last, cycle counts by model, and how to extend battery life."},
        {"href": "dji-mini-drone-under-250g-license-requirements.html", "badge": "FAA", "badge_class": "bg-blue-500/20 text-blue-400", "border_class": "border-blue-500/30", "badge2": "Legal", "title": "License Requirements", "desc": "Do you need a license for a sub-250g DJI Mini? FAA rules, registration, and Remote ID."},
        {"href": "dji-drone-atti-mode-how-to-get-out.html", "badge": "ATTI&nbsp;MODE", "badge_class": "bg-purple-500/20 text-purple-400", "border_class": "border-purple-500/30", "badge2": "Troubleshoot", "title": "ATTI Mode Guide", "desc": "What is ATTI mode, why drones enter it, and how to fix GPS issues and land safely."},
        {"href": "drones.html", "badge": "ALL&nbsp;GUIDES", "badge_class": "bg-electric-500/20 text-electric-400", "border_class": "border-electric-500/30", "badge2": "Category", "title": "Drone Hub", "desc": "Browse all drone guides, comparisons, specs, and troubleshooting resources."},
    ]

# =================== PAGE 17: BATTERY SWELLING ===================

page17 = {
    "filename": "dji-drone-battery-swelling-what-to-do.html",
    "title": "DJI Drone Battery Swelling: What to Do & Is It Safe? (2026)",
    "headline": "DJI Drone Battery Swelling: What to Do & Is It Safe? (2026)",
    "meta_desc": "DJI drone battery swelling — is it safe? Complete guide covering what causes battery swelling, how to check for it, proper disposal, prevention tips, warranty coverage, and storage.",
    "category": "Drones",
    "category_link": "drones.html",
    "breadcrumb_title": "Battery Swelling Guide",
    "hero_blur": "bg-red-500/5",
    "hero_badges": '''<div class="px-3 py-1.5 bg-red-500/20 text-red-400 font-mono font-bold text-sm rounded-md border border-red-500/30">BATTERY&nbsp;SAFETY</div>
        <span class="badge badge-info"><i data-lucide="alert-triangle" style="width:0.75rem;height:0.75rem"></i>Swelled Battery</span>
        <span class="badge badge-info"><i data-lucide="shield-alert" style="width:0.75rem;height:0.75rem"></i>Fire Safety</span>''',
    "h1": 'DJI Drone Battery Swelling: What to Do &amp; Is It Safe? &mdash; <span class="gradient-text">2026 Guide</span>',
    "hero_desc": "A swollen or puffy drone battery is a serious safety concern that should never be ignored. Swelling happens when gas builds up inside the battery cells due to chemical breakdown, and it can lead to thermal runaway — a fancy way of saying the battery can catch fire. In this guide, we cover what causes battery swelling, how to tell if your battery is swollen, whether it is still safe to use, how to properly dispose of swollen batteries, how to prevent it from happening, and whether warranty covers it.",
    "hero_stats": f'''<div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="alert-triangle" style="width:0.9rem;height:0.9rem"></i>Swollen =</div>
          <div class="font-mono font-bold text-xl text-red-400">Stop using</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="thermometer" style="width:0.9rem;height:0.9rem"></i>#1 Cause</div>
          <div class="font-bold text-xl text-orange-400">Heat / overcharging</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="recycle" style="width:0.9rem;height:0.9rem"></i>Disposal</div>
          <div class="font-mono font-bold text-xl text-green-400">Hazardous waste</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="shield" style="width:0.9rem;height:0.9rem"></i>Prevention</div>
          <div class="font-bold text-xl text-blue-400">Proper storage</div>
        </div>''',
    "qa_gradient": "from-red-950/20 to-navy-900 border-red-500/20",
    "qa_icon_color": "#f87171",
    "qa_title": "Is a Swollen Drone Battery Safe?",
    "qa_text": '<strong class="text-white">No — a swollen or puffy drone battery is NOT safe to use and should be retired immediately.</strong> Swelling is caused by gas buildup inside the lithium-polymer (LiPo) cells from electrolyte decomposition. A swollen battery has a higher risk of thermal runaway (catching fire), especially if it is charged further, punctured, dropped, or exposed to more heat. Even if the battery still works and seems fine, you should stop using it immediately. Do NOT charge a swollen battery, do NOT fly with it, and do NOT throw it in the trash. Store it in a fire-safe container (LiPo bag or ceramic pot) away from anything flammable, and take it to a battery recycling center as soon as possible. Better safe than sorry — a swollen battery is not worth the risk of a fire.',
    "qa_extra": f'''<div class="grid md:grid-cols-2 gap-3 mt-4">
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-red-400 font-semibold mb-1">DO NOT</div>
          <p class="text-sm text-gray-300">Charge it, fly with it, puncture it, throw it in trash, put it in water, store it with good batteries</p>
        </div>
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-green-400 font-semibold mb-1">DO THIS</div>
          <p class="text-sm text-gray-300">Stop using immediately, store in fire-safe container, discharge carefully if possible, recycle properly</p>
        </div>
      </div>''',
    "sections": [
        {
            "id": "what-causes",
            "title": "What Causes Drone Battery Swelling?",
            "content": p("Battery swelling happens when the electrolyte inside the LiPo cells breaks down chemically and produces gas. This is called 'outgassing.' Many things can cause or accelerate this process:") +
            grid_cards([
                {"title": "Heat / High Temperatures", "color": "text-orange-400", "desc": "Heat is the #1 cause of LiPo battery swelling. High temperatures accelerate every chemical degradation mechanism in the battery. Leaving batteries in a hot car in direct sunlight, storing them in a hot attic or garage, or flying in extreme heat can all cause swelling. Even moderate heat sustained over long periods slowly damages the battery."},
                {"title": "Overcharging", "color": "text-red-400", "desc": "Charging a battery beyond its safe voltage limit causes the electrolyte to break down and produce gas. DJI's Intelligent Battery system and BMS should prevent this, but BMS failures, faulty chargers, or using third-party chargers can lead to overcharging. This is one reason to always use genuine DJI batteries and chargers."},
                {"title": "Over-Discharging", "color": "text-yellow-400", "desc": "Draining a battery completely (below ~3.0V per cell) and then leaving it discharged for a long time can also cause swelling and permanent damage. LiPo batteries should never be stored fully discharged — always bring them up to at least 3.5-3.8V per cell before storing."},
                {"title": "Age & Normal Wear", "color": "text-blue-400", "desc": "All lithium batteries degrade over time, even with perfect care. As a battery ages and goes through many charge cycles, the electrolyte slowly breaks down and minor gas buildup accumulates. A slightly puffy battery that is 3+ years old with many cycles may just be reaching the end of its normal lifespan."},
                {"title": "Physical Damage", "color": "text-purple-400", "desc": "Crashing, dropping, puncturing, or physically damaging the battery can cause internal cell damage that leads to swelling. Even if the outside looks fine, internal damage from a hard impact can cause cells to fail and swell days or weeks later. Always inspect batteries after hard crashes."},
                {"title": "Manufacturing Defects", "color": "text-green-400", "desc": "Rarely, batteries can have manufacturing defects that cause them to swell prematurely, even with perfect care. This is more common with cheap no-name third-party batteries but can occasionally happen with genuine DJI batteries too. If a new battery swells under normal use, it is likely a defect and may be covered under warranty."},
            ], 2) +
            step_grid([
                {"title": "Why It Happens — The Chemistry", "desc": "LiPo batteries use a lithium salt electrolyte that carries lithium ions between the positive and negative electrodes during charge and discharge. Over time, and especially under stress (heat, overcharge, over-discharge), the electrolyte molecules break down through various chemical reactions, producing gases like carbon dioxide, methane, and hydrogen. Since LiPo batteries are sealed in a flexible pouch, this gas buildup causes the pouch to puff up. Mild swelling may just be end-of-life, but severe swelling is a sign of serious problems and fire risk."},
            ], "purple")
        },
        {
            "id": "how-to-check",
            "title": "How to Check If Your Battery Is Swollen",
            "content": p("It is not always obvious when a battery is swollen. Here is how to check:") +
            step_grid([
                {"title": "Visual Inspection", "desc": "Look at the battery from the side and end. Is it flat, or does it bulge in the middle? A healthy DJI Intelligent Battery should be relatively flat with straight sides. If it looks bowed, puffy, or rounded instead of flat, it is swollen. Compare it to a new battery of the same model if you are not sure. Even a slight bulge can indicate the beginning of swelling."},
                {"title": "The 'Spin Test'", "desc": "Place the battery on a flat, smooth surface like a table. Give it a light flick or spin with your finger. If the battery spins easily and smoothly like a top, it is swollen — the bulge in the middle acts like a pivot point. A flat battery will not spin easily and will rock or wobble instead. This is a classic test for swollen LiPo batteries that every pilot should know."},
                {"title": "Feeling for Soft Spots", "desc": "Gently press on the battery body (carefully — do not squeeze hard). A healthy battery should feel firm and solid. If you feel soft spots, squishiness, or the battery gives under pressure, it may be swollen. Never squeeze or puncture a swollen battery — you could cause it to catch fire. Just gentle pressure is enough to tell."},
                {"title": "Check the Fit", "desc": "Does the battery still fit in the drone properly? If it used to slide in easily but now feels tight or requires force to insert, the battery may be swelling. Similarly, if the battery door no longer closes properly or the battery is hard to remove, swelling could be the cause. This is a common early sign many pilots miss."},
                {"title": "Battery Health in the App", "desc": "Check the battery health in the DJI Fly app. While the app does not directly tell you if a battery is swollen, it can show warning signs: cell imbalance (cells with different voltages), abnormally high internal resistance, reduced capacity, or 'battery abnormal' warnings. If you see these, inspect the battery physically for swelling."},
            ], "yellow") +
            specs_table(
                ["Swelling Level", "Appearance", "Is It Safe?", "What to Do"],
                [
                    ["<strong>Mild / Early</strong>", "Slight bulge, passes spin test slowly", "No — stop using", "Stop flying, discharge to ~50%, recycle soon"],
                    ["<strong>Moderate</strong>", "Clearly puffy, obvious bulge", "Definitely NOT safe", "Do not charge or use, store safely, recycle ASAP"],
                    ["<strong>Severe</strong>", "Very swollen, tight/bulging, possible hissing", "EXTREMELY dangerous", "Treat as potential fire risk, isolate in fire container, call hazardous waste if needed"],
                ]
            ) +
            alert("warning", "magnifying-glass", "Check all your batteries regularly", "Make it a habit to inspect your batteries before every flight — just a quick visual check and spin test takes 10 seconds. Swelling can develop gradually, so it is easy to miss if you do not look for it. Catching it early is much safer than finding out the hard way. This is especially important for batteries you do not use often.")
        },
        {
            "id": "is-it-safe",
            "title": "Is It Safe to Use a Swollen Battery?",
            "content": p("Short answer: NO. A swollen battery should be considered unsafe and retired immediately. Here is why:") +
            '<div class="space-y-4 mb-6">' +
            grid_cards([
                {"title": "Fire Risk — Thermal Runaway", "color": "text-red-400", "desc": "This is the biggest danger. A swollen battery has damaged cells and internal gas pressure. If you continue charging or using it, the chemical reactions can accelerate and enter 'thermal runaway' — a self-feeding cycle where the battery gets hotter and hotter, eventually catching fire or even exploding. LiPo fires burn extremely hot (up to 1,000°C+) and are very difficult to put out with water. They can easily start a house fire."},
                {"title": "Reduced Performance & Capacity", "color": "text-orange-400", "desc": "A swollen battery has reduced capacity — it will not hold as much charge and flight times will be shorter. The internal resistance is higher, so voltage drops more under load, increasing the risk of a sudden power loss mid-flight. This can cause your drone to crash unexpectedly when the battery suddenly dies under load."},
                {"title": "Risk of Mid-Flight Failure", "color": "text-yellow-400", "desc": "Flying with a swollen battery is Russian roulette. The battery might work fine for one more flight, or it could fail mid-air, causing a crash. A drone crash from battery failure is expensive, and if it crashes in a dry area, the battery fire could start a wildfire. Is saving the cost of a new battery really worth risking your drone and possibly starting a fire?"},
                {"title": "It Will Only Get Worse", "color": "text-purple-400", "desc": "Battery swelling is almost always progressive — once it starts, it tends to get worse with each charge cycle. A mildly swollen battery today will be moderately swollen next month and severely swollen in a few more months. There is no way to reverse the swelling or fix the battery. It is a one-way street. The sooner you retire it, the safer you are."},
            ], 2) +
            "</div>" +
            alert("critical", "flame", "When to treat it as an emergency", "Most swollen batteries are not an immediate emergency — they can sit safely for days or weeks if handled properly. But treat it as an emergency if: the battery is hissing, leaking, smoking, or getting very hot to the touch, the swelling is getting rapidly worse (visible change in hours), or the battery has been punctured or damaged. In these cases: move the battery outdoors away from anything flammable, keep a fire extinguisher or bucket of sand nearby, and call your local fire department or hazardous waste service if you are unsure what to do."),
        },
        {
            "id": "proper-disposal",
            "title": "Proper Disposal of Swollen Batteries",
            "content": p("A swollen battery needs to be disposed of properly — you cannot just throw it in the trash. Here is the safe way:") +
            step_grid([
                {"title": "Step 1: Stop Using & Isolate", "desc": "First: stop charging, stop flying with it, and stop using it entirely. Put the swollen battery in a fire-safe container: a LiPo safety bag, a ceramic pot with a lid, a metal container with sand, or a dedicated LiPo charging/storage box. Keep it away from anything flammable (paper, wood, fabric, other batteries). Store it in a cool, dry place out of direct sun until you can dispose of it."},
                {"title": "Step 2: Discharge (If Safe to Do So)", "desc": "If the battery is only mildly swollen and still functional, you can discharge it to about 0-25% to make it safer for disposal and transport. The safest way is to use a LiPo battery discharger, or fly it gently until it is nearly dead (if it is still safe to do so — this is controversial, some say never fly a swollen battery). Alternatively, connect it to a low-current load like a light bulb. Never leave it unattended while discharging. If it is severely swollen, do NOT discharge it — just store it safely and take it to professionals."},
                {"title": "Step 3: Find a Battery Recycling Center", "desc": "Take the swollen battery to a battery recycling center or hazardous waste facility. Places that accept LiPo batteries include: your local household hazardous waste facility (call first to confirm they accept LiPo), home improvement stores like Home Depot and Lowes (they often have battery recycling bins), electronics stores like Best Buy, and dedicated battery recycling centers. Call ahead to confirm they accept swollen LiPo batteries, as some locations do not accept damaged batteries."},
                {"title": "Step 4: Transport Safely", "desc": "When transporting a swollen battery to be recycled: put it in a LiPo safety bag or a sealed metal container. Keep it in the passenger compartment of your car, not in the trunk (in case something happens and you need to react quickly). Do not leave it in a hot car during transport. Drive directly to the recycling center — do not make other stops with a swollen battery in your car."},
                {"title": "Step 5: What NOT to Do", "desc": "Never throw a LiPo battery in the trash or recycling bin — it can cause fires in garbage trucks and landfills. Never puncture or try to 'deflate' a swollen battery. Never put it in water (this can make it worse and creates toxic waste). Never put it in the freezer (this does not help and can cause condensation issues). Never leave it in direct sun or a hot place. Never store it with other good batteries."},
            ], "green") +
            alert("info", "recycle", "Most places accept LiPo batteries for free", "Battery recycling is usually free or very low cost. Home Depot, Lowes, and Best Buy all have free battery recycling programs for common battery types. Call ahead to make sure they accept lithium polymer batteries and that they accept damaged/swollen ones. Some locations only accept intact, non-swollen batteries and will refer you to a hazardous waste facility for swollen ones.")
        },
        {
            "id": "prevention",
            "title": "How to Prevent Battery Swelling",
            "content": p("While all LiPo batteries will eventually degrade, you can dramatically slow down the process and prevent premature swelling with good habits:") +
            step_grid([
                {"title": "Never Leave Batteries in a Hot Car", "desc": "This is the #1 thing you can do. Temperatures inside a closed car in direct sun can reach 60-70°C (140-160°F) in under an hour — hot enough to seriously damage or destroy LiPo batteries in a single afternoon. Always take your batteries with you or leave them in a cool, shaded, ventilated place. Even 30 minutes in a hot car can cause damage. Heat damage is cumulative and permanent."},
                {"title": "Store at 40-60% Charge", "desc": "LiPo batteries degrade slowest when stored at about 50% charge (3.8-3.85V per cell). Storing fully charged (100%) for weeks or months causes accelerated degradation and swelling. DJI Intelligent Batteries automatically self-discharge to ~60% after 10 days of inactivity (adjustable), which helps. But if you know you will not fly for more than a week, manually discharge to 50% before storing."},
                {"title": "Avoid Deep Discharges", "desc": "Do not drain your batteries all the way to 0% every flight. Land when you get to 20-30% battery remaining. Deep discharges put a lot of stress on the cells and accelerate degradation. The last 10-20% of battery capacity causes a disproportionate amount of wear. Getting in the habit of landing early can significantly extend battery life."},
                {"title": "Don't Overcharge or Leave Unattended", "desc": "While DJI's BMS should prevent overcharging, it is still good practice not to leave batteries on the charger indefinitely. Unplug them when they are done charging. Never leave charging batteries completely unattended for long periods — stay in the same room and check on them periodically. Use a LiPo charging bag as an extra safety precaution while charging."},
                {"title": "Use Genuine DJI Batteries & Chargers", "desc": "Third-party batteries and cheap chargers are much more likely to swell or fail because they often use lower-quality cells and have poor BMS implementation. Genuine DJI batteries cost more but have proper cell matching, quality BMS, and safety features that significantly reduce the risk of swelling and other failures. The peace of mind is worth the extra cost."},
                {"title": "Rotate Batteries Evenly", "desc": "If you have multiple batteries, rotate through them so they all get roughly equal use. Do not always use the same battery first and let others sit on the shelf for months. All batteries degrade from age even when unused, so you might as well use them. Label your batteries 1, 2, 3 and use them in order to keep track."},
                {"title": "Avoid Physical Damage", "desc": "Be careful with your batteries — do not drop them, do not crash with them if you can avoid it, and do not let them rattle around loose in a bag. Use a dedicated battery case or bag to protect them during transport. After any hard crash, inspect batteries carefully for damage and monitor them for swelling over the next few days and weeks."},
                {"title": "Store in Cool, Stable Temperature", "desc": "Ideal storage temperature is 15-25°C (59-77°F). Do not store batteries in a garage, attic, shed, or other place where temperatures swing wildly or get very hot. A closet or drawer inside your house at room temperature is perfect. Avoid humid places too — moisture can cause corrosion on the contacts."},
            ], "green") +
            alert("success", "heart", "Good habits = 3-5x longer battery life", "Pilots who follow all these best practices regularly report getting 500-800+ cycles out of batteries rated for 300 cycles, and rarely see swelling before the battery is near end of life. The difference between good and bad battery care can be the difference between a battery lasting 1 year vs 5 years. Developing good habits now will save you money and keep you safe.")
        },
        {
            "id": "warranty",
            "title": "Warranty Coverage for Swollen Batteries",
            "content": p("Is a swollen battery covered under warranty? It depends on the circumstances:") +
            specs_table(
                ["Situation", "Warranty Coverage?", "Notes"],
                [
                    ["<strong>New battery swells within warranty period</strong>", "Usually covered", "Likely a manufacturing defect — DJI will usually replace it"],
                    ["<strong>Battery swells after many cycles (300+)</strong>", "Not covered", "Considered normal wear and tear — battery reached end of life"],
                    ["<strong>Battery swells from heat (hot car, etc.)</strong>", "Not covered", "Damage from misuse or improper storage is excluded"],
                    ["<strong>Battery swells after crash/damage</strong>", "Not covered", "Physical damage is excluded from standard warranty"],
                    ["<strong>Third-party/no-name battery</strong>", "Varies (usually not)", "Cheap batteries have little to no warranty support"],
                    ["<strong>DJI Care Refresh</strong>", "Maybe", "Depends on the plan — may cover battery with drone replacement"],
                ]
            ) +
            step_grid([
                {"title": "How to Make a Warranty Claim", "desc": "If you think your swollen battery should be covered under warranty: 1) Stop using the battery immediately. 2) Take photos of the swelling (side view, spin test video if possible). 3) Check the purchase date and warranty period (DJI Intelligent Batteries typically have a 6-12 month warranty, depending on the model and region). 4) Contact DJI Support through their website or app. 5) They may ask for photos, the serial number, and purchase receipt. 6) If approved, they will usually send a replacement battery after you return the swollen one. Be honest about what happened — lying to support is not worth it."},
            ], "blue") +
            alert("warning", "message-circle", "Be polite but persistent with support", "Warranty claims for swollen batteries can be hit or miss. Some pilots get easy replacements, others get denied. If your claim is denied but you believe the battery failed under normal use, try again — different support agents may give different answers. Be polite, provide clear evidence (photos, flight logs showing normal use), and explain that you followed all proper storage and charging practices. Persistence and politeness pay off more often than you might expect.")
        },
        {
            "id": "storage-swollen",
            "title": "Storing Swollen Batteries (Short-Term)",
            "content": p("If you have a swollen battery that you cannot dispose of right away, here is how to store it safely in the short term:") +
            grid_cards([
                {"title": "Use a Fire-Safe Container", "color": "text-red-400", "desc": "Store swollen batteries in a dedicated LiPo safety bag, a ceramic or metal container with a lid, a metal ammo can, or a container partially filled with sand. The goal is to contain a fire if one starts. Do not store swollen batteries in plastic containers — they will melt if there is a fire."},
                {"title": "Isolate from Flammables", "color": "text-orange-400", "desc": "Keep the swollen battery away from anything that can burn: paper, wood, fabric, other batteries, chemicals, etc. Ideally store it in a garage or utility room on a non-flammable surface (concrete, tile). Do not store it in your bedroom or near anything valuable."},
                {"title": "Cool, Stable Temperature", "color": "text-yellow-400", "desc": "Store the battery in a cool place at stable room temperature. Do not put it in direct sun. Do not put it in the freezer or refrigerator — extreme cold can cause condensation and other issues, and it does not help with swelling. Room temperature or slightly cool is best."},
                {"title": "Do Not Stack or Press", "color": "text-green-400", "desc": "Do not put anything on top of the swollen battery. Do not stack other batteries on it. Do not squeeze it or put it in a tight bag. The battery is already under internal pressure — adding external pressure can make things worse."},
                {"title": "Check on It Periodically", "color": "text-blue-400", "desc": "If you are storing it for more than a day or two, check on it daily to make sure it is not getting worse. If the swelling is rapidly increasing, the battery is hissing, or it is getting hot — take it to a hazardous waste facility immediately."},
                {"title": "Dispose ASAP", "color": "text-purple-400", "desc": "The goal should be to dispose of the battery as soon as reasonably possible — within days, not weeks or months. A swollen battery is a ticking time bomb (figuratively, but sometimes literally). Do not keep it around longer than necessary. Find a recycling center and drop it off."},
            ], 2) +
            alert("critical", "flame", "What to do if a LiPo battery catches fire", "If a swollen battery catches fire: 1) Get everyone out of the area immediately. 2) Call 911 / the fire department. 3) If it is small and safe to do so, you can try to smother it with sand or a Class D fire extinguisher. Water does NOT put out LiPo fires well — it can make them worse by reacting with lithium. 4) Do not pick up or move a burning battery. 5) Ventilate the area — LiPo fires produce toxic fumes. 6) After the fire is out, leave the battery outside in a fire-safe container for at least 24 hours — it can re-ignite. LiPo fires are serious — do not be a hero, call the professionals."),
        },
    ],
    "faqs": [
        {"q": "Is it safe to use a swollen DJI battery?", "a": "No — a swollen or puffy drone battery is NOT safe to use and should be retired immediately. Swelling means gas is building up inside the cells from chemical breakdown, and the battery has an increased risk of thermal runaway (catching fire), especially if charged further or stressed. Even if the battery still seems to work, you should stop using it. Do not charge it, do not fly with it, and store it in a fire-safe container until you can properly dispose of it at a battery recycling center. The risk is not worth saving the cost of a new battery."},
        {"q": "What causes drone batteries to swell?", "a": "The #1 cause is heat — leaving batteries in a hot car, storing in hot places, or flying in extreme heat. Other causes include: overcharging (rare with DJI BMS but possible with third-party chargers), deep discharging and leaving them empty for long periods, physical damage from crashes, old age and normal wear (batteries slowly degrade even with perfect care), and manufacturing defects (rare with genuine DJI batteries). Swelling happens when the electrolyte inside the LiPo cells breaks down chemically and produces gas that inflates the pouch."},
        {"q": "How do I check if my drone battery is swollen?", "a": "There are several easy ways: 1) Visual inspection — look at the battery from the side; a swollen battery will bulge in the middle instead of being flat. 2) The 'spin test' — place the battery on a flat table and spin it; if it spins easily like a top, it is swollen (a flat battery will not spin smoothly). 3) Feeling — gently press on the battery; it should feel firm, not soft or squishy. 4) Fit check — if the battery no longer fits properly in the drone and feels tight, it may be swelling. Do a quick check before every flight — it takes 10 seconds."},
        {"q": "Can a swollen battery be fixed or deflated?", "a": "No — there is no safe way to fix or deflate a swollen LiPo battery. The swelling is caused by irreversible chemical damage inside the cells. Puncturing the battery to release the gas is extremely dangerous — you could cause a fire or release toxic fumes. There is no way to repair the damaged cells and restore the battery to a safe state. The only proper thing to do with a swollen battery is to safely dispose of it and buy a new one. Do not try DIY fixes you see online — they are all dangerous."},
        {"q": "How do I dispose of a swollen drone battery?", "a": "First, stop using it immediately and store it in a fire-safe container (LiPo bag, ceramic pot, metal container with sand). If it is only mildly swollen and still works, you can discharge it to about 0-25% to make it safer for transport (never leave it unattended while discharging). Then take it to: your local household hazardous waste facility, a battery recycling center, or stores like Home Depot, Lowes, or Best Buy that have battery recycling programs (call ahead to confirm they accept swollen LiPo batteries). Never throw a LiPo battery in the trash or regular recycling — it can cause fires in garbage trucks and landfills."},
        {"q": "Is a swollen battery covered under DJI warranty?", "a": "It depends. If the battery is relatively new (within the 6-12 month warranty period) and swells under normal use with no abuse, it may be a manufacturing defect and is usually covered — DJI will likely send a replacement. If the battery is old (many cycles, years of use) or swells due to obvious abuse (hot car, crash damage, over-discharge, etc.), it is not covered under warranty. If you think you have a valid claim, contact DJI support with photos of the swelling, your purchase receipt, and the serial number. Be polite and provide clear evidence."},
        {"q": "How can I prevent my drone batteries from swelling?", "a": "The most important thing: NEVER leave batteries in a hot car in direct sun — heat is the #1 cause of swelling. Other prevention tips: store batteries at 40-60% charge (not fully charged) for long-term storage, land with 20-30% battery remaining instead of draining to 0%, use genuine DJI batteries and chargers, avoid physical damage and crashes, store in a cool dry place at room temperature, and rotate through multiple batteries evenly so they all get similar use. Following these habits can double or triple your battery lifespan."},
        {"q": "Should I still fly if one battery cell is slightly low?", "a": "A small voltage difference between cells (under 0.05-0.1V) is normal and not a cause for alarm. But if one cell is significantly lower than the others (0.2V+ difference), that can be an early sign of cell failure and potential swelling. Stop using the battery and monitor it. Cell imbalance that gets worse over time is a bad sign. You can try running a few full charge-discharge cycles or using storage mode to see if the BMS can rebalance the cells. If imbalance persists, retire the battery — it is not worth the risk."},
        {"q": "How long do DJI drone batteries normally last before swelling?", "a": "With proper care and normal use, DJI drone batteries should last 200-400 charge cycles (2-5 years) before showing significant swelling or reaching end of life. Mini series batteries typically last 200-300 cycles, while larger Mavic/Air batteries last 300-400 cycles. With poor care (heat abuse, deep discharges, full charge storage), they can swell much sooner — sometimes within just a few months or dozens of cycles. Good storage and charging habits make a massive difference in lifespan."},
        {"q": "Can I put a swollen battery in water to make it safe?", "a": "No — never put a LiPo battery in water. While water can sometimes cool a burning battery, it does not 'neutralize' a swollen battery and can actually make things worse. Water can react with lithium compounds to produce hydrogen gas and lithium hydroxide (a corrosive). Putting a swollen battery in water creates toxic, corrosive waste and can increase pressure inside the battery. The correct way to handle a swollen battery is to store it in a fire-safe container and take it to a proper battery recycling facility."},
    ],
    "related": drone_related(),
}

# =================== PAGE 18: RC CALIBRATION ===================

page18 = {
    "filename": "how-to-calibrate-dji-remote-controller.html",
    "title": "How to Calibrate DJI Remote Controller (Stick Calibration 2026)",
    "headline": "How to Calibrate DJI Remote Controller (Stick Calibration 2026)",
    "meta_desc": "How to calibrate your DJI remote controller. Step-by-step guide for DJI Fly and DJI Go, RC-N1 vs RC Pro, calibration errors, stick drift issues, and troubleshooting.",
    "category": "Drones",
    "category_link": "drones.html",
    "breadcrumb_title": "RC Calibration Guide",
    "hero_blur": "bg-orange-500/5",
    "hero_badges": '''<div class="px-3 py-1.5 bg-orange-500/20 text-orange-400 font-mono font-bold text-sm rounded-md border border-orange-500/30">RC&nbsp;CALIBRATION</div>
        <span class="badge badge-info"><i data-lucide="gamepad-2" style="width:0.75rem;height:0.75rem"></i>Stick Drift</span>
        <span class="badge badge-info"><i data-lucide="settings" style="width:0.75rem;height:0.75rem"></i>Step-by-Step</span>''',
    "h1": 'How to Calibrate DJI Remote Controller &mdash; <span class="gradient-text">Stick Calibration Guide 2026</span>',
    "hero_desc": "If your drone is drifting, not responding precisely, or the sticks feel off, you may need to calibrate your remote controller. Stick calibration tells the controller where the center point and full deflection are for each stick, ensuring precise control. It is a quick and easy process that can make a big difference in how your drone flies. In this guide, we cover when to calibrate, step-by-step instructions for DJI Fly and DJI Go, differences between RC-N1 and RC Pro, calibration errors, stick drift troubleshooting, and firmware updates.",
    "hero_stats": f'''<div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="timer" style="width:0.9rem;height:0.9rem"></i>Time Needed</div>
          <div class="font-mono font-bold text-xl text-green-400">2-5 min</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="refresh-cw" style="width:0.9rem;height:0.9rem"></i>How Often</div>
          <div class="font-bold text-xl text-yellow-400">Every 3-6 mo</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="gamepad-2" style="width:0.9rem;height:0.9rem"></i>Axes</div>
          <div class="font-mono font-bold text-xl text-blue-400">4 channels</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="activity" style="width:0.9rem;height:0.9rem"></i>Difficulty</div>
          <div class="font-bold text-xl text-purple-400">Very Easy</div>
        </div>''',
    "qa_gradient": "from-orange-950/20 to-navy-900 border-orange-500/20",
    "qa_icon_color": "#fb923c",
    "qa_title": "How to Calibrate Your DJI Controller",
    "qa_text": '<strong class="text-white">To calibrate your DJI remote controller: connect to the drone, open DJI Fly, go to Controller Settings > RC Calibration, then follow the on-screen instructions to move both sticks through their full range of motion in all directions.</strong> The whole process takes 2-5 minutes. You move each stick to all its extremes (up, down, left, right, full circles) and the app records the minimum and maximum values for each axis. This lets the controller know exactly where center and full deflection are. Calibration fixes common issues like stick drift, imprecise control, non-centered gimbal, and the drone drifting when sticks are released. You should calibrate if you notice any of these issues, or proactively every 3-6 months.',
    "qa_extra": f'''<div class="grid md:grid-cols-2 gap-3 mt-4">
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-green-400 font-semibold mb-1">Calibrate if you see</div>
          <p class="text-sm text-gray-300">Drift when sticks centered, imprecise control, gimbal drift, calibration warning in app</p>
        </div>
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-blue-400 font-semibold mb-1">Works for</div>
          <p class="text-sm text-gray-300">RC-N1, RC-N2, RC, RC Pro, RC Pro Enterprise, all DJI smart controllers</p>
        </div>
      </div>''',
    "sections": [
        {
            "id": "when-to-calibrate",
            "title": "When to Calibrate Your Controller",
            "content": p("You do not need to calibrate your controller every time you fly, but there are certain situations when you should:") +
            specs_table(
                ["Sign / Situation", "Calibration Needed?", "Why"],
                [
                    ["<strong>Stick drift / drone drifts with sticks centered</strong>", "Yes — definitely", "Controller does not know where true center is"],
                    ["<strong>Imprecise or sluggish control feel</strong>", "Yes — likely helps", "End points not properly calibrated"],
                    ["<strong>Gimbal drifts or camera not level</strong>", "Maybe — could be RC or gimbal", "Wheel calibration or gimbal calibration needed"],
                    ["<strong>After firmware update</strong>", "Good idea", "Firmware can change calibration values"],
                    ["<strong>After a crash or hard impact</strong>", "Yes — good practice", "Impact could shift potentiometers"],
                    ["<strong>Every 3-6 months of regular use</strong>", "Preventative maintenance", "Stick pots drift slowly over time"],
                    ["<strong>New / first flight</strong>", "Probably fine but good to do", "Factory calibration is usually good but verify"],
                    ["<strong '>Just feeling 'off' when flying</strong>", "Worth trying", "Very quick process, easy to test"],
                ]
            ) +
            p("Stick calibration is one of the easiest and quickest fixes for many common control issues. It takes 2-5 minutes and costs nothing, so it is worth trying whenever something feels off with the way your drone responds to stick input.")
        },
        {
            "id": "dji-fly-calibration",
            "title": "Step-by-Step: DJI Fly App Calibration",
            "content": p("Most modern DJI drones (Mini 2, Mini 3, Mini 4/5 Pro, Air 2S, Air 3, Mavic 3 series, etc.) use the DJI Fly app. Here is how to calibrate:") +
            step_grid([
                {"title": "Step 1: Power On & Connect", "desc": "Turn on your drone and remote controller. Connect your phone to the controller and open the DJI Fly app. Wait for the app to connect to the drone and show the camera view. Make sure both the drone and controller have good battery level — at least 30% or so."},
                {"title": "Step 2: Go to Controller Settings", "desc": "In the camera view, tap the three dots (…) in the top right corner to open Settings. Tap the 'Control' tab (or look for 'Controller' or 'Remote Controller' settings). Scroll down until you find 'RC Calibration' or 'Remote Controller Calibration' and tap it."},
                {"title": "Step 3: Start Calibration", "desc": "You will see a screen with a diagram of the two sticks and a gauge showing their current position. Make sure both sticks are centered and all switches/wheels are in their neutral positions. Tap 'Start' or 'Calibrate' to begin. The app will guide you through the process."},
                {"title": "Step 4: Calibrate Sticks", "desc": "Follow the on-screen instructions. Usually: 1) Leave both sticks centered for a few seconds (to record center point). 2) Slowly move the left stick to its full up, down, left, and right positions, pausing at each extreme. 3) Do the same for the right stick. 4) Move both sticks in full circles a few times. 5) Move the gimbal wheel through its full range if you have one. The app will show green bars or checkmarks when each axis is calibrated."},
                {"title": "Step 5: Finish & Verify", "desc": "When the app says calibration is complete or shows a success message, tap 'Finish' or 'OK'. Then verify: slowly move each stick around and watch the on-screen indicator — it should move smoothly and return exactly to center when you release the stick. If the indicator does not return to the center dot when the stick is released, recalibrate."},
            ], "green") +
            alert("success", "check-circle", "Pro tip: move slowly and smoothly", "When calibrating, move the sticks slowly and smoothly through their full range of motion. Pause briefly at each extreme (all the way up, down, left, right) so the controller can record the maximum value clearly. Quick jerky movements may result in poor calibration. Take your time — it only takes a minute or two more and gives a much better result.")
        },
        {
            "id": "dji-go-calibration",
            "title": "Calibration in DJI Go 4 (Older Drones)",
            "content": p("If you have an older DJI drone that uses DJI Go 4 (Mavic Pro, Mavic 2, Phantom series, Spark, etc.), the process is slightly different:") +
            step_grid([
                {"title": "Step 1: Open DJI Go 4", "desc": "Turn on the drone and controller, connect your phone, open DJI Go 4, and enter the camera view."},
                {"title": "Step 2: Enter MC Settings", "desc": "Tap the three dots (…) menu button. Go to the 'Controller Settings' or 'Remote Controller Settings' menu."},
                {"title": "Step 3: Find Calibration", "desc": "Look for 'Remote Controller Calibration' and tap it. You will see a calibration screen with stick position indicators."},
                {"title": "Step 4: Follow Instructions", "desc": "Tap 'Start'. Follow the prompts: center sticks first, then move each stick to all extremes, rotate wheels, etc. The app shows green checkmarks as each axis is calibrated."},
                {"title": "Step 5: Finish", "desc": "Tap 'Finish' when complete. Verify that all sticks return to center. If calibration fails or feels off, just do it again."},
            ], "blue") +
            p("The overall process is very similar between DJI Fly and DJI Go — the same principle applies. Move the sticks through their full range slowly and let the app record the min/max values for each axis.")
        },
        {
            "id": "rc-n1-vs-rc-pro",
            "title": "RC-N1 vs RC Pro vs Smart Controllers",
            "content": p("DJI makes several different remote controllers. The calibration process is similar for all of them, but there are some differences:") +
            specs_table(
                ["Controller", "Calibration Location", "What Gets Calibrated", "Notes"],
                [
                    ["<strong>RC-N1 / RC-N2</strong>", "DJI Fly > Control > RC Calibration", "Both sticks (4 axes), gimbal dial", "Standard controller with phone clamp"],
                    ["<strong>RC (Smart Controller)</strong>", "DJI Fly (built-in) > Control > RC Calibration", "Both sticks, gimbal dial, custom buttons", "Built-in screen — same process"],
                    ["<strong>RC Pro</strong>", "DJI Fly > Control > RC Calibration", "Both sticks, gimbal dial, 5D button, custom buttons", "Premium controller, more axes"],
                    ["<strong>RC Pro Enterprise</strong>", "DJI Pilot > Controller Settings", "All sticks, dials, buttons, switches", "Industrial controller, many channels"],
                    ["<strong>FPV Remote 2</strong>", "DJI FLY (FPV) > Controller Calibration", "Both sticks, switches, dials", "FPV-specific controller"],
                ]
            ) +
            grid_cards([
                {"title": "All Controllers Use the Same Principle", "color": "text-green-400", "desc": "No matter which DJI controller you have, stick calibration works the same way: the app records the minimum, center, and maximum values for each analog axis (each stick direction, each dial). The process of moving the sticks through their full range is universal across all DJI controllers."},
                {"title": "More Buttons = More Calibration Steps", "color": "text-blue-400", "desc": "Higher-end controllers like the RC Pro have more analog inputs — a 5-way button, multiple dials, etc. The calibration process will include all of these. Just follow the on-screen prompts and move each control through its full range when prompted. The app guides you through everything."},
            ], 2)
        },
        {
            "id": "stick-drift",
            "title": "Fixing Stick Drift",
            "content": p("Stick drift is when the drone slowly moves or drifts even when you have the sticks centered and released. This is one of the most common reasons to calibrate.") +
            step_grid([
                {"title": "Step 1: Confirm It Is the Controller", "desc": "First, make sure the drift is actually from the controller and not something else. With the drone hovering, let go of the sticks and see which direction it drifts. Then check: is the GPS signal good? (Poor GPS can cause drift.) Are you in ATTI mode? (ATTI mode will drift with wind.) Is the compass calibrated? If everything else checks out, it is probably stick drift."},
                {"title": "Step 2: Recalibrate the Controller", "desc": "Do a full stick calibration following the steps above. This is the first thing to try and fixes 80-90% of stick drift cases. Pay extra attention to the center point step — make sure the sticks are perfectly centered when the app records the neutral position."},
                {"title": "Step 3: Test the Result", "desc": "After calibration, check the stick position indicator in the calibration screen. When you release the sticks, the indicator should return exactly to the center dot. If it is slightly off, try calibrating again. Sometimes it takes 2-3 tries to get it perfect. Also do a hover test to see if the drift is gone."},
                {"title": "Step 4: If Drift Persists", "desc": "If calibration does not fix it, the potentiometers (the sensors in the sticks) might be worn out or dirty. Options: try cleaning the sticks (compressed air around the base), adjust the deadband/trim in settings (some drones let you increase the deadzone), or contact DJI support for repair/replacement if the controller is still under warranty. For out-of-warranty controllers, replacement sticks or whole controllers are available."},
            ], "orange") +
            alert("info", "sliders-horizontal", "What about trim and deadband?", "Some DJI drones let you adjust the stick deadband or trim in the settings. Deadband is a small zone around center where the controller ignores tiny stick movements — this helps with drift. Increasing deadband slightly can mask minor stick drift, but it also reduces precision. Calibration is the better fix if it works. Use deadband adjustments only for minor drift that calibration cannot fix.")
        },
        {
            "id": "calibration-errors",
            "title": "Calibration Errors & Troubleshooting",
            "content": p("Sometimes calibration does not go smoothly. Here are common issues and how to fix them:") +
            specs_table(
                ["Problem", "Possible Cause", "Fix"],
                [
                    ["<strong>Calibration fails / cannot complete</strong>", "Sticks not moved through full range, or hardware issue", "Try again, move slower, make sure to hit all extremes"],
                    ["<strong>Sticks not centered after calibration</strong>", "Did not hold sticks at true center during center step", "Recalibrate, be careful during the center step"],
                    ["<strong>Calibration option greyed out</strong>", "Not connected to drone, or app issue", "Make sure drone is connected and on, restart app"],
                    ["<strong>App says 'calibration abnormal'</strong>", "Stick sensors faulty, or damaged pots", "Try restarting, recalibrate; if persists, may need repair"],
                    ["<strong>One axis not responding properly</strong>", "Dirty potentiometer, worn out stick", "Clean with compressed air, may need repair"],
                    ["<strong>Stiff or sticky sticks</strong>", "Dirt, dust, debris in gimbals", "Clean around stick base with compressed air"],
                ]
            ) +
            step_grid([
                {"title": "General Calibration Troubleshooting", "desc": "If calibration is not working: 1) Make sure both drone and controller have good battery (above 30%). 2) Close and restart the DJI Fly app. 3) Power cycle both the drone and controller. 4) Try a different USB cable or connection method. 5) Make sure you have the latest firmware and app version. 6) Try calibrating again, moving extra slowly and deliberately to each extreme. 7) If it still fails, the controller may have a hardware issue and need repair or replacement."},
            ], "red") +
            alert("warning", "refresh-cw", "Firmware updates can reset calibration", "Sometimes after a firmware update for the controller or drone, the calibration settings get reset or changed. If your controller feels different after a firmware update, just recalibrate it. This is normal and one reason it is good practice to check calibration after any firmware update.")
        },
        {
            "id": "firmware-updates",
            "title": "Firmware Updates for Controller",
            "content": p("Keeping your controller firmware up to date is important for performance and reliability. Here is what you need to know:") +
            step_grid([
                {"title": "How to Update Controller Firmware", "desc": "1) Connect to the drone and open DJI Fly. 2) Go to Settings > About (or Firmware Update). 3) If an update is available for the controller, you will see an 'Update' button. 4) Tap Update and wait — the controller will restart during the process. 5) Keep everything powered on and connected during the update. Do not exit the app or turn off anything while updating."},
                {"title": "When to Update", "desc": "Update when: there is a new firmware version available with features or fixes you want, you are having issues that might be firmware-related, or DJI recommends updating. You do not necessarily need to update every single time if everything is working perfectly — but staying reasonably current is a good idea. Always update before important trips or events."},
                {"title": "What to Do After Updating", "desc": "After a controller firmware update: 1) Test that the controller connects and works properly. 2) Consider recalibrating the sticks — firmware updates can sometimes change calibration values. 3) Test fly carefully in an open area to make sure everything feels right. 4) Check that all custom buttons and settings still work as expected."},
            ], "purple") +
            alert("success", "download", "Update tips", "Always update both the drone and controller when updates are available — they are designed to work together and mismatched firmware can cause issues. Charge both batteries to at least 50% before updating. Do the update in a place with good Wi-Fi or cellular connection. And as mentioned, recalibrate the sticks afterward for best performance.")
        },
    ],
    "faqs": [
        {"q": "How do I calibrate my DJI remote controller?", "a": "To calibrate: power on the drone and controller, connect to DJI Fly, go to Settings > Control > RC Calibration, tap Start, then follow the on-screen instructions to move both sticks slowly through their full range of motion (up, down, left, right, full circles). The app records the center, minimum, and maximum values for each stick axis. The whole process takes 2-5 minutes. When finished, verify that the stick indicator returns exactly to center when you release the sticks."},
        {"q": "How often should I calibrate my DJI controller?", "a": "As a general rule, calibrate every 3-6 months with regular use, or whenever you notice issues like stick drift, imprecise control, or the drone moving on its own when sticks are centered. You should also calibrate after a firmware update, after a crash or hard impact, or if the controller has not been used in a long time. Calibration takes only a few minutes, so it is worth doing whenever something feels off — there is no harm in calibrating more often."},
        {"q": "What is stick drift and how do I fix it?", "a": "Stick drift is when the drone slowly moves or drifts even when you have the sticks fully released and centered. It happens when the controller's stick sensors (potentiometers) drift slightly from their center position. The fix is to recalibrate the controller — this re-teaches it where the true center point is. If recalibration does not fix it, try cleaning around the stick bases with compressed air, increasing the deadband slightly in settings, or contacting DJI support if the controller is still under warranty."},
        {"q": "Why is my drone drifting when I let go of the sticks?", "a": "Drift when sticks are centered is most often caused by stick drift (the controller's center point is slightly off). But it can also be caused by other things: poor GPS signal (the drone cannot hold position), flying in ATTI mode instead of GPS mode, compass needing calibration, wind pushing the drone, or the gimbal/camera not being level. Rule out the other causes first, then calibrate the controller. If drift only happens indoors or in GPS-denied areas, it is normal — visual positioning is less accurate than GPS."},
        {"q": "Does DJI RC Pro need calibration?", "a": "Yes — the DJI RC Pro, RC (smart controller), and all other DJI controllers benefit from stick calibration, just like the standard RC-N1. The process is essentially the same: open DJI Fly, go to controller settings, find RC Calibration, and follow the instructions. Higher-end controllers like the RC Pro may have extra axes to calibrate (5D button, additional dials, etc.), but the app walks you through all of them."},
        {"q": "Can I calibrate my controller without the drone?", "a": "Generally no — on most DJI drones, the calibration option is only available when the controller is connected to the drone. The calibration data is stored on the drone's flight controller system, not just in the remote. You need both the controller and the drone powered on and connected to perform stick calibration. This is one reason it is hard to test a controller without a drone."},
        {"q": "Why does calibration keep failing?", "a": "If calibration repeatedly fails, try these fixes: 1) Move the sticks more slowly and make sure you hit every extreme position firmly. 2) Make sure nothing is touching the sticks during the center step. 3) Restart both the drone and controller, then try again. 4) Update the firmware on both drone and controller. 5) If it still fails, the stick potentiometers might be worn out or damaged. Try cleaning around the sticks with compressed air. If nothing works, the controller may need repair or replacement."},
        {"q": "What is RC deadband and should I adjust it?", "a": "Deadband (or deadzone) is a small area around the center of the sticks where tiny movements are ignored — the drone will not respond. A small deadband helps with stick drift and makes hovering easier, but too much makes controls feel sluggish and imprecise. Some DJI drones let you adjust the deadband in advanced settings. For most pilots, the default deadband is perfect. Only increase it slightly if you have minor stick drift that calibration cannot fix. Do not set it too high or you will lose precision."},
        {"q": "Do I need to calibrate gimbal wheel too?", "a": "Yes — the gimbal control wheel (dial) is also an analog axis and gets calibrated during the full RC calibration process. Follow the on-screen prompts — when it gets to the gimbal dial, slowly rotate it through its full range (all the way up, all the way down) several times. This ensures the gimbal moves smoothly and knows its full range. If your gimbal moves unevenly or is jittery, calibrating the wheel can help."},
        {"q": "Is it safe to fly with uncalibrated controller?", "a": "Mild calibration issues (slight drift) are usually safe to fly with — just be aware that you may need to make small corrections to hold position. But if the drift is significant, or if the controller has major calibration issues, it is better to calibrate before flying. Severe calibration problems could lead to unpredictable behavior. Since calibration only takes 2-5 minutes, there is really no reason not to do it if you suspect a problem. It is a quick safety check."},
    ],
    "related": drone_related(),
}

# =================== PAGE 19: ATTI MODE ===================

page19 = {
    "filename": "dji-drone-atti-mode-how-to-get-out.html",
    "title": "DJI Drone ATTI Mode: What It Is & How to Get Out (2026)",
    "headline": "DJI Drone ATTI Mode: What It Is & How to Get Out (2026)",
    "meta_desc": "What is ATTI mode on a DJI drone? Complete guide covering why drones enter ATTI mode, how to fix GPS issues, how to land safely, prevention tips, and compass vs GPS vs vision positioning.",
    "category": "Drones",
    "category_link": "drones.html",
    "breadcrumb_title": "ATTI Mode Guide",
    "hero_blur": "bg-purple-500/5",
    "hero_badges": '''<div class="px-3 py-1.5 bg-purple-500/20 text-purple-400 font-mono font-bold text-sm rounded-md border border-purple-500/30">ATTI&nbsp;MODE</div>
        <span class="badge badge-info"><i data-lucide="map-pin-off" style="width:0.75rem;height:0.75rem"></i>GPS Lost</span>
        <span class="badge badge-info"><i data-lucide="navigation" style="width:0.75rem;height:0.75rem"></i>Safe Landing</span>''',
    "h1": 'DJI Drone ATTI Mode: What It Is &amp; How to Get Out &mdash; <span class="gradient-text">2026 Guide</span>',
    "hero_desc": "Seeing 'ATTI' mode on your DJI drone can be alarming, especially if you do not know what it means. ATTI (Attitude) mode means the drone has lost GPS and/or vision positioning — it will no longer hold its position automatically and will drift with the wind. The drone can still fly and you still have control, but you need to fly it manually, like an old-school RC aircraft. In this guide, we explain what ATTI mode is, why drones enter it, how to fix GPS issues and get back to GPS mode, how to land safely in ATTI, and how to prevent it from happening.",
    "hero_stats": f'''<div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="map-pin" style="width:0.9rem;height:0.9rem"></i>GPS Mode</div>
          <div class="font-mono font-bold text-xl text-green-400">Holds position</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="map-pin-off" style="width:0.9rem;height:0.9rem"></i>ATTI Mode</div>
          <div class="font-bold text-xl text-yellow-400">Drifts with wind</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="navigation" style="width:0.9rem;height:0.9rem"></i>#1 Cause</div>
          <div class="font-mono font-bold text-xl text-red-400">No GPS signal</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="eye" style="width:0.9rem;height:0.9rem"></i>Indoors</div>
          <div class="font-bold text-xl text-blue-400">Normal</div>
        </div>''',
    "qa_gradient": "from-purple-950/20 to-navy-900 border-purple-500/20",
    "qa_icon_color": "#c084fc",
    "qa_title": "What Is ATTI Mode?",
    "qa_text": '<strong class="text-white">ATTI mode (Attitude mode) means the drone has lost its GPS and/or vision positioning system, so it can no longer hold a fixed position automatically.</strong> In normal GPS mode, the drone stays in one spot even if you let go of the sticks — it uses GPS and vision sensors to counteract wind and maintain position. In ATTI mode, the drone only maintains its altitude and attitude (level flight). It will drift horizontally with the wind, just like a traditional RC helicopter or plane. You still have full control over the drone — you can steer it up, down, left, right, forward, back — but you have to manually compensate for wind drift. ATTI mode is not an emergency or a crash — it just means you need to fly more carefully and manually. The most common causes are: no GPS signal (indoors, canyons, under trees), poor compass calibration, vision system issues, or flying too low over featureless terrain.',
    "qa_extra": f'''<div class="grid md:grid-cols-2 gap-3 mt-4">
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-green-400 font-semibold mb-1">What still works in ATTI</div>
          <p class="text-sm text-gray-300">Altitude hold, manual control, gimbal, camera, return to home (if GPS comes back), landing</p>
        </div>
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-yellow-400 font-semibold mb-1">What stops working</div>
          <p class="text-sm text-gray-300">Position hold, active track, waypoints, RTH (without GPS), tap fly, all autonomous features</p>
        </div>
      </div>''',
    "sections": [
        {
            "id": "what-is-atti",
            "title": "What Exactly Is ATTI Mode?",
            "content": p("ATTI (short for Attitude) mode is a basic flight mode where the drone only stabilizes its attitude — it keeps itself level and holds altitude, but does not try to hold its horizontal position.") +
            specs_table(
                ["Flight Mode", "Position Hold", "Altitude Hold", "Level Stabilization", "Autonomous Features"],
                [
                    ["<strong>GPS Mode (Normal)</strong>", "Yes — GPS + vision", "Yes", "Yes", "All features work"],
                    ["<strong>ATTI Mode</strong>", "No — drifts with wind", "Yes", "Yes", "Most GPS-based features disabled"],
                    ["<strong>Manual Mode (rare)</strong>", "No", "No", "No — full manual", "None"],
                ]
            ) +
            p("ATTI mode is the drone's 'basic' flight mode — it is what the drone falls back to when it cannot determine its position. The IMU (Inertial Measurement Unit) still works, so the drone knows which way is up and can keep itself level and hold altitude. But without GPS or vision, it does not know where it is horizontally, so it cannot hold position.") +
            alert("info", "piloting", "Think of it like a boat vs a car", "A car (GPS mode) can stay in one spot with the brakes on. A boat (ATTI mode) floats and drifts with the current — you have to actively steer it to stay in one place. ATTI mode is the 'boat' version of drone flight. The drone still works, but you have to do the positioning work yourself with the sticks.")
        },
        {
            "id": "why-drones-enter-atti",
            "title": "Why Drones Enter ATTI Mode",
            "content": p("There are several reasons a DJI drone might enter ATTI mode. Some are normal and expected, some indicate a problem:") +
            grid_cards([
                {"title": "No GPS Signal", "color": "text-yellow-400", "desc": "This is the #1 cause. GPS satellites are relatively weak — they cannot penetrate buildings, thick tree cover, deep canyons, or indoor spaces. If the drone cannot see enough satellites (usually 6+), it cannot determine its position and falls back to ATTI mode. This is completely normal when flying indoors, under dense tree canopy, in narrow city streets, or in deep valleys."},
                {"title": "Compass Issues / Interference", "color": "text-orange-400", "desc": "The compass helps the drone know which direction it is facing. If the compass gets interfered with by metal objects, power lines, or other electromagnetic sources, the drone may not trust its position data and switch to ATTI. A compass calibration error can also cause this. Compass interference warnings usually appear before the drone enters ATTI mode."},
                {"title": "Vision Positioning Failure", "color": "text-red-400", "desc": "When flying low (usually under 10-30 meters depending on the model), DJI drones use downward-facing vision sensors to help hold position. If you fly over featureless terrain (water, snow, sand), or if the vision system is blocked by dirt or fog, or if you fly too low or too high for vision to work, the drone loses that positioning aid and may enter ATTI if GPS is also weak."},
                {"title": "Indoor Flight", "color": "text-blue-400", "desc": "Flying indoors is the most common situation where ATTI mode is completely normal and expected. Indoors, there is no GPS signal. The drone will use its vision positioning system to hold position if it has enough light and a textured floor, but if the lighting is poor or the floor is featureless, it will be in ATTI mode and drift. This is normal behavior."},
                {"title": "Temporary GPS Loss", "color": "text-purple-400", "desc": "Sometimes the drone loses GPS temporarily — flying under a bridge, through a canyon, past a tall building that blocks the sky. In these cases, it will quickly switch to ATTI and then back to GPS once it has satellite signal again. This is usually brief and not a cause for alarm — just be ready for the drift."},
                {"title": "IMU or Sensor Issues", "color": "text-green-400", "desc": "Rarely, ATTI mode can indicate a more serious problem with the drone's IMU or other sensors. If the drone goes into ATTI mode outdoors with a clear view of the sky and stays there even after calibrating compass and IMU, there might be a hardware issue. This is the least common cause but worth considering if nothing else fixes it."},
            ], 2) +
            alert("warning", "satellite", "How many satellites do you need?", "DJI drones need at least 6-8 GPS satellites to hold position reliably, and more is better. On the ground before takeoff, wait until you have 10+ satellites (the app shows the satellite count) before taking off. More satellites = more accurate positioning and less chance of entering ATTI mode. If you only have 4-5 satellites at takeoff, be extra cautious — you might lose GPS easily.")
        },
        {
            "id": "how-to-fix-gps",
            "title": "How to Fix GPS Issues & Get Out of ATTI",
            "content": p("If your drone is in ATTI mode and you want to get back to GPS mode, here is what to try:") +
            step_grid([
                {"title": "1. Move to an Open Area", "desc": "If you are under trees, near buildings, or in a canyon, move the drone to a more open area with a clear view of the sky. The more sky the drone can see, the more satellites it can pick up. Fly upward — getting higher can help clear obstacles that are blocking the satellite signal. Often, just ascending 20-30 meters is enough to get GPS lock back."},
                {"title": "2. Wait for Satellite Acquisition", "desc": "Sometimes it just takes time. If you just took off or just came from an area with no GPS, give it 30-60 seconds. The drone needs to find and lock onto satellites. Watch the satellite count in the app — it will gradually increase as the drone finds more satellites. Once it has enough (usually 8+), it will switch back to GPS mode automatically."},
                {"title": "3. Calibrate the Compass", "desc": "If the app shows a compass error or warning, calibrate the compass. Find an open area away from metal and electronics. In DJI Fly: Settings > Control > Calibration > Compass Calibration. Follow the instructions — usually you rotate the drone 360 degrees horizontally, then rotate it nose-down 360 degrees. Compass calibration is quick (1-2 minutes) and fixes many GPS/ATTI issues."},
                {"title": "4. Check for Interference", "desc": "Are you near power lines, large metal objects, radio towers, or other sources of electromagnetic interference? These can mess with both GPS signal and compass. Move away from potential interference sources and see if GPS comes back. Even things like cars, metal bleachers, or fences can cause compass interference if you are too close."},
                {"title": "5. IMU Calibration", "desc": "If compass calibration does not help, try calibrating the IMU. This is more involved — you need a flat, level surface. In DJI Fly: Settings > Control > Calibration > IMU Calibration. Follow the instructions carefully — you place the drone on the level surface in various orientations. IMU calibration is not needed as often as compass calibration, but it can fix stubborn attitude/positioning issues."},
                {"title": "6. Restart the Drone", "desc": "The classic IT fix — turn it off and on again. Sometimes the GPS module or flight controller just glitches. Power off the drone and controller, wait 30 seconds, then power them back on. Let the drone sit on the ground for 1-2 minutes to acquire satellites before taking off again."},
            ], "green") +
            alert("success", "check-circle", "Prevention tip: wait for GPS before takeoff", "The best way to avoid ATTI mode surprises is to wait for a good GPS lock before taking off. Put the drone on the ground in an open area, turn it on, and wait 1-2 minutes. Watch the satellite count go up and wait for the drone to show 'GPS' mode (not 'ATTI') on the main screen. Then take off. This simple habit prevents many ATTI-mode situations."),
        },
        {
            "id": "landing-safely",
            "title": "How to Land Safely in ATTI Mode",
            "content": p("If you are stuck in ATTI mode and GPS is not coming back, do not panic — you can still land safely. You just need to fly manually. Here is how:") +
            step_grid([
                {"title": "1. Stay Calm & Assess", "desc": "First: take a breath. ATTI mode is not an emergency — the drone still flies, you just have to steer it manually. Check: how much battery do you have? Where is the wind coming from? Are there obstacles around? Do you have visual line of sight? Assessing the situation calmly is the first step to a safe landing."},
                {"title": "2. Fly to a Safe Landing Spot", "desc": "Navigate the drone to a clear, open area where you can land safely — preferably your takeoff point, or any flat clear area. You will need to actively steer the drone — it will drift with the wind, so you need to compensate by flying into the wind slightly. This takes practice, but if you have been flying in GPS mode, you already know how the controls work — you just have to use them more actively."},
                {"title": "3. Compensate for Wind", "desc": "Wind will push the drone around. If the wind is blowing from left to right, you will need to hold slight left stick to stay in place. If wind is blowing toward you, you need to hold forward stick to stay over one spot. The stronger the wind, the more stick input you need. Small corrections are better than big movements — make gentle adjustments."},
                {"title": "4. Descend Slowly", "desc": "Once you are over your landing spot, start descending slowly. As you get lower, ground effect can make the drone more stable, but also wind near the ground can be turbulent. Keep correcting for drift as you descend. Do not descend too fast — take it slow and steady. Aim to be directly over the landing spot when you get close to the ground."},
                {"title": "5. Land Smoothly", "desc": "When the drone is just above the ground (1-2 meters), reduce descent speed. Gently lower it until it touches down. Then hold the throttle stick down for a moment to make sure the motors shut off properly. If you are drifting at the last second, it is often better to just let it land rather than trying to correct aggressively — a rough landing is better than a crash from trying too hard to be perfect."},
                {"title": "6. If You Cannot Get Back", "desc": "If the wind is too strong, you are too far away, or you are not confident in your manual flying skills: 1) Try to get GPS back by climbing higher or moving to a more open area. 2) If you have DJI Care Refresh and you are truly stuck, you can use the Find My Drone feature to locate it after it lands (but only if it has enough battery). 3) As a last resort, land the drone safely in the nearest clear area and walk to retrieve it — better to land safely than crash trying to force it back."},
            ], "yellow") +
            alert("warning", "wind", "Wind makes a big difference", "The biggest challenge of ATTI mode is wind. In calm conditions, you might barely notice the difference — the drone drifts slowly and is easy to control. In strong wind, the drone can drift fast and you have to work hard to keep it in position. If you are not confident in your manual flying skills, the safest thing is to land as soon as possible when ATTI mode activates, especially on windy days.")
        },
        {
            "id": "prevention",
            "title": "Prevention: How to Avoid ATTI Mode",
            "content": p("The best way to handle ATTI mode is to prevent it from happening in the first place. Here are the best prevention strategies:") +
            specs_table(
                ["Strategy", "How It Helps", "How to Do It"],
                [
                    ["<strong>Wait for GPS before takeoff</strong>", "Ensures good satellite lock before you leave ground", "Wait for 10+ satellites and GPS mode before taking off"],
                    ["<strong>Calibrate compass regularly</strong>", "Prevents compass errors that cause ATTI", "Calibrate when you travel long distance or see warnings"],
                    ["<strong>Fly in open areas</strong>", "Maximizes satellite visibility", "Choose flying spots with wide open sky view"],
                    ["<strong>Avoid flying under trees/canyons</strong>", "Prevents GPS blockage", "Stay in open areas; be cautious near obstacles"],
                    ["<strong>Update firmware</strong>", "Fixes bugs in GPS and flight controller", "Keep drone firmware up to date"],
                    ["<strong>Check weather before flying</strong>", "Avoids unexpected wind/conditions", "Check wind forecast, storm prediction, satellite weather"],
                    ["<strong>Practice manual flight</strong>", "You will be ready if ATTI happens", "Practice flying in ATTI mode intentionally (in a safe open area)"],
                    ["<strong>Maintain VLOS</strong>", "You can always see your drone and land manually", "Always keep visual line of sight — it's the law too"],
                ]
            ) +
            step_grid([
                {"title": "Practice ATTI Mode Intentionally", "desc": "The best way to be prepared for unexpected ATTI mode is to practice it on purpose. Find a large open field on a calm day. You can force ATTI mode by covering the GPS antenna (not recommended — better to fly indoors if you can safely) or by going somewhere with known bad GPS. Or you can just be ready — the more you fly, the better your manual flying becomes. Pilots who practice manual flying are much calmer and more capable when ATTI mode happens unexpectedly."},
            ], "purple") +
            alert("success", "brain", "Knowledge = confidence", "Most pilots panic the first time they see ATTI mode because they do not know what it means. But now that you understand it is just manual position control and the drone still flies fine, you will be much calmer if it happens to you. Knowledge is the best prevention for panic. Read this guide, understand the modes, and you will handle ATTI mode like a pro when it happens.")
        },
        {
            "id": "gps-vs-vision-vs-compass",
            "title": "GPS vs Vision Positioning vs Compass",
            "content": p("DJI drones use multiple systems to determine their position. Understanding how they work together helps you understand ATTI mode:") +
            specs_table(
                ["System", "What It Does", "How It Works", "Limitations"],
                [
                    ["<strong>GPS / GNSS</strong>", "Tells drone its global position", "Receives signals from satellite networks (GPS, GLONASS, Galileo)", "Needs clear sky view; 6+ satellites minimum"],
                    ["<strong>Vision Positioning</strong>", "Holds position low to ground", "Downward cameras look at ground texture and track movement", "Needs textured ground, good light, works only below certain altitude"],
                    ["<strong>Compass</strong>", "Tells drone which direction it is facing", "Magnetometer detects Earth's magnetic field", "Easily interfered with by metal, electronics, power lines"],
                    ["<strong>IMU (Gyro + Accelerometer)</strong>", "Keeps drone level, senses movement", "Gyroscopes and accelerometers measure rotation and acceleration", "Can drift over time without GPS correction"],
                    ["<strong>Barometer</strong>", "Holds altitude", "Measures air pressure to determine altitude", "Can drift with temperature changes and wind"],
                ]
            ) +
            p("In normal GPS flight mode, all these systems work together. GPS gives the big picture of where the drone is in the world. Vision positioning gives precise low-altitude positioning. Compass tells direction. IMU and barometer provide fast, continuous stabilization. When GPS and vision fail or are unavailable, the drone falls back to just IMU + barometer = ATTI mode. The drone is still stable and level, but does not know where it is horizontally.") +
            alert("info", "satellite", "GNSS vs GPS", "You might see 'GNSS' instead of 'GPS' in some DJI documentation. GNSS (Global Navigation Satellite System) is the general term for all satellite navigation systems. DJI drones use multiple systems: GPS (USA), GLONASS (Russia), and sometimes Galileo (Europe) and BeiDou (China). Using multiple systems gives more satellites, better accuracy, and faster lock-on. So 'GNSS' is technically more accurate than 'GPS', but everyone says 'GPS' anyway.")
        },
    ],
    "faqs": [
        {"q": "What is ATTI mode on a DJI drone?", "a": "ATTI mode (short for Attitude mode) means the drone has lost its GPS and/or vision positioning, so it can no longer automatically hold its position. The drone will still fly and you still have full control — it stays level and holds altitude, but it will drift horizontally with the wind. You have to manually steer it to stay in place, like flying a traditional RC aircraft. ATTI is not a crash or emergency — it just means you need to fly more carefully and manually."},
        {"q": "Why did my drone go into ATTI mode?", "a": "The most common cause is losing GPS signal — flying indoors, under dense tree cover, in canyons, near tall buildings, or anywhere the sky is blocked. Other causes include: compass interference (metal objects, power lines), vision positioning system issues (featureless terrain, poor lighting, dirt on sensors), temporary GPS dropout when flying under obstacles, or (rarely) IMU calibration issues. ATTI mode is completely normal in certain environments like indoor flight — it just means the drone does not have position reference."},
        {"q": "How do I get my drone out of ATTI mode?", "a": "To get back to GPS mode: move the drone to an open area with a clear view of the sky (climbing higher often helps), then wait 30-60 seconds for it to acquire satellites. If the issue is compass interference, move away from metal/power sources and calibrate the compass. If it persists, try IMU calibration. Most of the time, just getting to open space and waiting is enough. If you cannot get GPS back, just land the drone manually — ATTI mode is flyable, just different."},
        {"q": "Is it safe to fly in ATTI mode?", "a": "Yes, it is generally safe to fly in ATTI mode as long as you understand what is happening and you have good visual line of sight. The drone still responds to all controls — it just drifts with wind and you have to manually position it. The risks are: drifting into obstacles if you do not compensate for wind, difficulty holding position for photos/video, and pilots panicking because they do not understand what is happening. If you are a new pilot and get stuck in ATTI, the safest move is usually to land carefully as soon as possible in a clear area."},
        {"q": "How do I land in ATTI mode?", "a": "Landing in ATTI mode is straightforward but requires active control: 1) Fly to your desired landing spot, compensating for wind drift. 2) Descend slowly while maintaining position with small stick corrections. 3) When close to the ground, reduce descent speed and fine-tune your position. 4) Let it touch down gently, then hold throttle down to shut off motors. The key is to stay calm and make small, smooth stick movements — the wind will push you around, but you can counteract it. Practice in a wide open field on a calm day first."},
        {"q": "Does ATTI mode mean my drone is broken?", "a": "No — ATTI mode is not a sign of a broken drone in most cases. It is a normal flight mode that the drone enters automatically when it cannot determine its position. It is like how your phone loses GPS signal in a tunnel — the phone is fine, it just cannot see satellites. If your drone enters ATTI mode outdoors with a clear view of the sky and stays there even after calibration and waiting, then there might be a problem with the GPS module or compass. But 95% of the time, ATTI is just normal behavior for the environment."},
        {"q": "How can I prevent ATTI mode?", "a": "The best ways to prevent unexpected ATTI mode: 1) Wait for a solid GPS lock (10+ satellites) before taking off — give it 1-2 minutes on the ground. 2) Fly in open areas with a clear view of the sky — avoid dense trees, deep canyons, and downtown areas. 3) Calibrate the compass when you travel long distances or see compass warnings. 4) Keep your drone firmware up to date. 5) Practice manual flight so you are prepared if it happens. ATTI is never completely preventable, but you can minimize surprises."},
        {"q": "What happens to Return to Home in ATTI mode?", "a": "RTH (Return to Home) requires GPS to work — it needs to know where home is and where the drone is. If the drone is in pure ATTI mode with no GPS at all, RTH will not work properly. However, many times the drone has partial GPS (enough for rough position but not enough for full GPS mode) and can still attempt RTH. If you press RTH and the drone does not come back, it probably does not have enough GPS — you will need to fly it back manually. This is one reason you should always maintain visual line of sight."},
        {"q": "Why does my drone say ATTI when I am indoors?", "a": "That is completely normal. Indoors, there is no GPS signal (satellites cannot go through roofs), so the drone cannot use GPS positioning. It may use its downward vision sensors to hold position if the lighting is good and the floor has enough texture. If vision positioning also cannot work (dark room, featureless floor), then the drone is in full ATTI mode and will drift. Indoor flight is one of the most common situations where ATTI mode is expected and normal."},
        {"q": "Will DJI replace my drone if it drifts away in ATTI mode?", "a": "Generally no — ATTI mode is a normal feature, not a defect. If the drone enters ATTI because of environmental factors (no GPS, interference, etc.) and then drifts away or crashes, that is considered pilot error or environmental cause, not a manufacturing defect. DJI Care Refresh may cover it if you have the plan and it is considered accidental damage (terms vary). To avoid this situation: maintain visual line of sight at all times, learn to fly manually, and land promptly if you lose GPS and are not confident. Fly within your skill level."},
    ],
    "related": drone_related(),
}

# =================== PAGE 20: BEST DJI DRONE FOR PHOTOGRAPHY ===================

page20 = {
    "filename": "best-dji-drone-for-photography-2026.html",
    "title": "Best DJI Drone for Photography (2026 Aerial Photography Guide)",
    "headline": "Best DJI Drone for Photography (2026 Aerial Photography Guide)",
    "meta_desc": "Best DJI drone for photography in 2026. Complete guide with top picks, sensor size comparison, megapixels, RAW vs JPEG, lens options, low light performance, photography modes, and pro tips.",
    "category": "Drones",
    "category_link": "drones.html",
    "breadcrumb_title": "Best Photography Drone",
    "hero_blur": "bg-pink-500/5",
    "hero_badges": '''<div class="px-3 py-1.5 bg-pink-500/20 text-pink-400 font-mono font-bold text-sm rounded-md border border-pink-500/30">PHOTOGRAPHY</div>
        <span class="badge badge-info"><i data-lucide="camera" style="width:0.75rem;height:0.75rem"></i>Top Picks 2026</span>
        <span class="badge badge-info"><i data-lucide="aperture" style="width:0.75rem;height:0.75rem"></i>Sensor Guide</span>''',
    "h1": 'Best DJI Drone for Photography &mdash; <span class="gradient-text">2026 Aerial Photography Guide</span>',
    "hero_desc": "DJI makes the best camera drones in the world, but which one is right for photography? The answer depends on your budget, what kind of photography you do, and how much image quality you need. From the compact Mini series up to the professional Inspire line, there is a drone for every level. In this guide, we compare sensor sizes, megapixels, RAW capabilities, lens options, low light performance, photography modes, and give our top recommendations for different use cases and budgets.",
    "hero_stats": f'''<div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="aperture" style="width:0.9rem;height:0.9rem"></i>Entry Level</div>
          <div class="font-mono font-bold text-xl text-green-400">1/1.3" 48MP</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="aperture" style="width:0.9rem;height:0.9rem"></i>Mid Range</div>
          <div class="font-bold text-xl text-blue-400">1" 20-48MP</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="aperture" style="width:0.9rem;height:0.9rem"></i>Pro Level</div>
          <div class="font-mono font-bold text-xl text-purple-400">4/3" 20MP+</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="film" style="width:0.9rem;height:0.9rem"></i>Price Range</div>
          <div class="font-bold text-xl text-yellow-400">$500-$8000</div>
        </div>''',
    "qa_gradient": "from-pink-950/20 to-navy-900 border-pink-500/20",
    "qa_icon_color": "#f472b6",
    "qa_title": "Best DJI Photography Drone Overall",
    "qa_text": '<strong class="text-white">The best DJI drone for photography in 2026 depends on your budget and needs: the Mavic 3 Pro is the best all-around photography drone (4/3" Hasselblad + medium tele + wide-angle), the Air 3 is the best mid-range value (1" dual camera), and the Mini 5 Pro is the best budget pick (1/1.3" 48MP in a sub-250g package).</strong> For most hobbyist and semi-pro photographers, the DJI Air 3 is the sweet spot — it has a 1-inch CMOS sensor (20MP), shoots RAW photos, has a dual camera (wide + medium tele), and produces stunning image quality at a reasonable price (~$1,099). For professionals, the Mavic 3 Pro or Inspire 3 offer larger sensors and interchangeable lenses. For beginners or casual shooters on a budget, the Mini 5 Pro produces surprisingly good 48MP photos and is incredibly portable.',
    "qa_extra": f'''<div class="grid md:grid-cols-3 gap-3 mt-4">
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-green-400 font-semibold mb-1 text-sm">Best Value</div>
          <div class="font-bold text-white">DJI Air 3</div>
          <div class="text-xs text-gray-400 mt-1">1" dual cam · ~$1,099</div>
        </div>
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-purple-400 font-semibold mb-1 text-sm">Best Pro</div>
          <div class="font-bold text-white">Mavic 3 Pro</div>
          <div class="text-xs text-gray-400 mt-1">4/3" Hasselblad · ~$2,199</div>
        </div>
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-yellow-400 font-semibold mb-1 text-sm">Best Budget</div>
          <div class="font-bold text-white">Mini 5 Pro</div>
          <div class="text-xs text-gray-400 mt-1">1/1.3" 48MP · ~$759</div>
        </div>
      </div>''',
    "sections": [
        {
            "id": "top-picks",
            "title": "Top Picks: Best DJI Drones for Photography",
            "content": p("Here are our top recommendations for different budgets and use cases:") +
            specs_table(
                ["Drone", "Sensor", "MP", "RAW", "Price", "Best For"],
                [
                    ["<strong>DJI Mini 5 Pro</strong>", "1/1.3\" CMOS", "48MP", "Yes (DNG)", "~$759", "Beginners, travel, casual photos"],
                    ["<strong>DJI Mini 4 Pro</strong>", "1/1.3\" CMOS", "48MP", "Yes (DNG)", "~$649", "Budget, sub-250g, travel"],
                    ["<strong>DJI Air 3</strong>", "1\" CMOS (dual)", "20MP + 48MP", "Yes (DNG)", "~$1,099", "Enthusiasts, best value"],
                    ["<strong>DJI Mavic 3 Classic</strong>", "4/3\" CMOS Hasselblad", "20MP", "Yes (DNG)", "~$1,599", "Landscape, pro stills"],
                    ["<strong>DJI Mavic 3 Pro</strong>", "4/3\" + 1/1.3\" + 1/2\"", "20MP + 48MP + 12MP", "Yes (DNG)", "~$2,199", "Pros, versatility, 3 cameras"],
                    ["<strong>DJI Inspire 3</strong>", "Full-frame 8K / X9", "45MP+", "Yes (DNG/ProRes)", "~$8,000", "Cinema/production, best quality"],
                ]
            ) +
            grid_cards([
                {"title": "Best Overall Value: DJI Air 3", "color": "text-green-400", "desc": "The Air 3 strikes the perfect balance for most photographers. It has a 1-inch CMOS sensor (the classic sweet spot for drone photography) with 20MP resolution, plus a second 48MP 1/1.3-inch medium tele camera for versatility. Image quality is excellent — sharp details, good dynamic range, great color. At around $1,099, it is pricey but not crazy expensive. For enthusiast and semi-pro photographers, this is the one to get."},
                {"title": "Best Budget: DJI Mini 5 Pro", "color": "text-yellow-400", "desc": "Do not let the size fool you — the Mini 5 Pro takes great photos. The 1/1.3-inch 48MP sensor produces sharp, detailed images, and the RAW capability gives you editing flexibility. At under 250g, it is incredibly portable — you will take it everywhere. For beginners, hobbyists, and travel photographers who prioritize portability, the Mini 5 Pro is amazing. At ~$759, it is a fraction of the cost of pro models."},
                {"title": "Best Pro: DJI Mavic 3 Pro", "color": "text-purple-400", "desc": "For professional work, the Mavic 3 Pro is the top of the consumer/prosumer line. The main 4/3-inch Hasselblad camera produces stunning image quality with beautiful color and dynamic range. The triple-camera system (wide + medium tele + tele) gives you compositional flexibility no other Mavic has. At ~$2,199 it is expensive, but if you make money with your drone photography, it pays for itself quickly."},
            ], 2)
        },
        {
            "id": "sensor-size-comparison",
            "title": "Sensor Size Comparison — Does Size Matter?",
            "content": p("Sensor size is the single most important factor in image quality for drone cameras. Bigger sensors produce better image quality, especially in low light and when editing. Here is how the different sizes compare:") +
            specs_table(
                ["Sensor Size", "Typical MP", "Low Light", "Dynamic Range", "Depth of Field", "Example Drones"],
                [
                    ["<strong>1/2.3\"</strong>", "12-20MP", "Poor", "Limited", "Very deep", "Older Mini drones, Spark"],
                    ["<strong>1/1.3\"</strong>", "48-64MP", "Fair-Good", "Good", "Deep", "Mini 3/4/5 Pro, Mini 3 Pro"],
                    ["<strong>1\"</strong>", "20-48MP", "Good", "Very Good", "Moderate", "Air 2S, Air 3 (wide cam)"],
                    ["<strong>4/3\" (Micro Four Thirds)</strong>", "20-25MP", "Very Good", "Excellent", "Moderate-shallow", "Mavic 3 series, Hasselblad"],
                    ["<strong>APS-C</strong>", "24-40MP", "Excellent", "Excellent", "Shallow", "Some Inspire models"],
                    ["<strong>Full Frame</strong>", "24-60MP", "Outstanding", "Outstanding", "Very shallow", "Inspire 3 (X9 camera)"],
                ]
            ) +
            grid_cards([
                {"title": "More Than Just Megapixels", "color": "text-blue-400", "desc": "Do not be fooled by megapixel marketing. A 20MP 1-inch sensor will almost always produce better photos than a 48MP 1/1.3-inch sensor, even though it has fewer megapixels. Why? Because larger sensor pixels are bigger, which means they capture more light, have less noise, better dynamic range, and better color. Megapixels tell you resolution (how big you can print), sensor size tells you quality. Both matter, but sensor size matters more for overall image quality."},
                {"title": "The Sweet Spot for Most People", "color": "text-green-400", "desc": "For most drone photographers, a 1-inch sensor is the sweet spot. It offers a big jump in quality over smaller sensors (1/1.3-inch and below), especially in dynamic range and low light. The files are manageable (not huge), the drones are still portable, and the price is reasonable. 1-inch sensor drones like the Air 2S and Air 3 are the workhorses of enthusiast and semi-pro aerial photography."},
            ], 2) +
            alert("info", "aperture", "What is dynamic range?", "Dynamic range is the difference between the brightest and darkest parts of a scene that the camera can capture detail in. Larger sensors have better dynamic range — they can capture both bright skies and dark shadows in the same shot without blowing out the highlights or crushing the shadows. This is one of the biggest differences you will see between cheap and expensive drone photos. With good dynamic range, you can edit photos more aggressively and get better results.")
        },
        {
            "id": "raw-vs-jpeg",
            "title": "RAW vs JPEG — Which Should You Shoot?",
            "content": p("Almost all DJI drones can shoot both RAW and JPEG photos. Which should you use? It depends on how much editing you do:") +
            '<div class="grid md:grid-cols-2 gap-6 mb-6">' +
            '<div class="bg-navy-900/80 border border-yellow-500/30 rounded-xl p-6">' +
            '<h3 class="font-bold text-xl mb-4 text-yellow-400">JPEG</h3>' +
            '<ul class="space-y-3 text-sm text-gray-300">' +
            '<li>• <strong class="text-white">File size:</strong> Small (3-8MB per photo)</li>' +
            '<li>• <strong class="text-white">Ready to use:</strong> Yes — looks good straight out of camera</li>' +
            '<li>• <strong class="text-white">Editing flexibility:</strong> Limited — easy to degrade quality</li>' +
            '<li>• <strong class="text-white">Dynamic range:</strong> Limited — highlights/shadows harder to fix</li>' +
            '<li>• <strong class="text-white">Workflow:</strong> Fast — no processing needed</li>' +
            '<li>• <strong class="text-white">Best for:</strong> Beginners, social media, quick sharing, large volume</li>' +
            '<li>• <strong class="text-white">DJI processing:</strong> Yes — in-camera sharpening, color, contrast</li>' +
            '<li>• <strong class="text-white">Format:</strong> Universal — works everywhere</li>' +
            '</ul></div>' +
            '<div class="bg-navy-900/80 border border-purple-500/30 rounded-xl p-6">' +
            '<h3 class="font-bold text-xl mb-4 text-purple-400">RAW (DNG)</h3>' +
            '<ul class="space-y-3 text-sm text-gray-300">' +
            '<li>• <strong class="text-white">File size:</strong> Large (20-50MB per photo)</li>' +
            '<li>• <strong class="text-white">Ready to use:</strong> No — looks flat/gray, needs editing</li>' +
            '<li>• <strong class="text-white">Editing flexibility:</strong> Excellent — adjust exposure/WB without loss</li>' +
            '<li>• <strong class="text-white">Dynamic range:</strong> Maximum — recover highlights and shadows</li>' +
            '<li>• <strong class="text-white">Workflow:</strong> Slower — requires post-processing</li>' +
            '<li>• <strong class="text-white">Best for:</strong> Enthusiasts, pros, anyone who edits photos</li>' +
            '<li>• <strong class="text-white">DJI processing:</strong> Minimal — raw sensor data preserved</li>' +
            '<li>• <strong class="text-white">Format:</strong> DNG (Adobe DNG standard)</li>' +
            '</ul></div></div>' +
            p("Our recommendation: shoot RAW+JPEG if you have the storage space. You get the convenience of JPEG for quick sharing, plus the RAW file for serious editing. If you only shoot JPEG, you will eventually run into a shot that could have been amazing if you had the RAW file. If you only shoot RAW, every shot requires editing — even the quick snapshots. RAW+JPEG gives you the best of both worlds, at the cost of using more SD card space."),
        },
        {
            "id": "lens-options",
            "title": "Lens Options & Focal Lengths",
            "content": p("Drone lenses are generally fixed (you cannot change lenses like a DSLR), but newer DJI drones offer multiple cameras with different focal lengths:") +
            specs_table(
                ["Drone", "Lenses", "Wide Angle", "Medium / Tele", "Zoom Capability"],
                [
                    ["<strong>Mini 3/4/5 Pro</strong>", "1 lens", "24mm equiv. f/1.7", "None", "Digital zoom only"],
                    ["<strong>Air 2S</strong>", "1 lens", "22mm equiv. f/2.8", "None", "Digital zoom only"],
                    ["<strong>Air 3</strong>", "2 lenses", "24mm f/1.7 (1\")", "70mm equiv. f/2.8 (1/1.3\")", "Digital between"],
                    ["<strong>Mavic 3 Classic</strong>", "1 lens", "24mm equiv. f/2.8", "None", "Digital zoom"],
                    ["<strong>Mavic 3</strong>", "2 lenses", "24mm f/2.8 (4/3\")", "162mm equiv. tele (1/2\")", "Hybrid 7x zoom"],
                    ["<strong>Mavic 3 Pro</strong>", "3 lenses", "24mm + 70mm + 166mm", "All three focal lengths", "Tri-cam + zoom"],
                    ["<strong>Inspire 3</strong>", "Interchangeable", "16-35mm, 24mm, etc.", "Depends on lens", "Full optical with zoom lenses"],
                ]
            ) +
            grid_cards([
                {"title": "Wide Angle (20-28mm)", "color": "text-blue-400", "desc": "This is the standard drone focal length — great for landscapes, architecture, and general aerial photography. Wide angle captures the sweeping vistas that make drone photography dramatic. Almost all drones have a wide-angle main camera. The downside: wide-angle distortion, and you cannot compress perspective or isolate subjects."},
                {"title": "Medium Tele (50-90mm)", "color": "text-green-400", "desc": "Medium telephoto lenses are amazing for aerial photography because they let you compress perspective, isolate subjects, and shoot from further away. The Air 3 and Mavic 3 Pro both have medium tele cameras (70mm equiv.) that are game-changers for composition. You can get tighter shots without flying as close, and the perspective is more flattering for many subjects."},
                {"title": "Telephoto (150-200mm+)", "color": "text-purple-400", "desc": "Long telephoto lenses on drones (like the Mavic 3's 162mm) let you shoot from very far away, which is useful for getting shots of hard-to-reach places or when you cannot fly close. The tradeoff is smaller sensor on the tele camera (usually 1/2-inch or similar), so image quality is not as good as the main camera. But for the right shot, it is worth it."},
            ], 2)
        },
        {
            "id": "low-light",
            "title": "Low Light Performance",
            "content": p("Aerial photography at sunrise, sunset, and night requires good low light performance. Here is how different drones compare:") +
            step_grid([
                {"title": "What Makes Good Low Light?", "desc": "Low light performance depends primarily on sensor size (bigger = better) and lens aperture (wider = better, lower f-number). A 4/3-inch sensor at f/2.8 will be much better in low light than a 1/1.3-inch sensor at f/1.7, even though the f-number is 'slower', because the sensor is so much bigger. Megapixels also matter — fewer megapixels on the same size sensor = bigger pixels = better low light. This is why a 20MP 1-inch sensor is better in low light than a 48MP 1-inch sensor."},
                {"title": "Best Low Light: Mavic 3 Series", "desc": "The Mavic 3's 4/3-inch Hasselblad sensor is the low-light king among consumer DJI drones. The large sensor captures a lot of light, resulting in clean, detailed photos at dawn, dusk, and even night (with longer exposures). The dynamic range is excellent — you can recover shadows without getting tons of noise. If you shoot a lot of golden hour or night photography, the Mavic 3 is worth the upgrade."},
                {"title": "Good Low Light: 1-inch Sensors (Air 2S, Air 3)", "desc": "1-inch sensor drones (Air 2S, Air 3 wide camera) are very good in low light — not quite Mavic 3 level, but close enough for most people. They handle golden hour beautifully and can do night photography with proper settings. For most enthusiast photographers, 1-inch low light performance is more than sufficient, and it comes at a much lower price point than 4/3-inch."},
                {"title": "Decent Low Light: Mini Series (1/1.3\")", "desc": "Mini drones with 1/1.3-inch sensors (Mini 3 Pro, Mini 4 Pro, Mini 5 Pro) are decent in good light, but struggle more as light drops. The small sensor produces more noise in low light, and dynamic range is more limited. That said, they are surprisingly capable for their size — you can get good golden hour shots if you expose carefully and edit with noise reduction. Just do not expect 1-inch or 4/3-inch quality."},
            ], "yellow") +
            alert("info", "moon", "Night photography tips", "For night photography with any drone: shoot RAW, use manual mode, set ISO as low as possible (100-200), use a slower shutter speed (1-2 seconds works well for city lights, but watch for motion blur), and use a tripod mode if your drone has it (locks position better for long exposures). Always shoot RAW for night photos — you will need the editing headroom. Post-processing with noise reduction software makes a huge difference."),
        },
        {
            "id": "photography-modes",
            "title": "Photography Modes & Features",
            "content": p("DJI drones have many photography-specific modes that help you get better shots. Here are the key ones:") +
            specs_table(
                ["Mode", "What It Does", "Best For", "Available On"],
                [
                    ["<strong>Single Shot</strong>", "One photo at a time", "General photography", "All drones"],
                    ["<strong>Burst Mode</strong>", "Multiple shots in quick succession", "Action, fast-moving subjects", "Most drones"],
                    ["<strong>HDR</strong>", "Multiple exposures merged for more dynamic range", "High contrast scenes, landscapes", "Most drones"],
                    ["<strong>AEB (Auto Exposure Bracketing)</strong>", "Takes 3-5 shots at different exposures", "HDR editing, landscapes", "Nearly all drones"],
                    ["<strong>Panorama</strong>", "Stitches multiple shots into wide panorama", "Landscapes, wide scenes", "All DJI drones"],
                    ["<strong>Timelapse</strong>", "Sequence of photos over time, assembled into video", "Sunsets, clouds, city traffic", "Most drones"],
                    ["<strong>Hyperlapse</strong>", "Moving timelapse (drone moves while shooting)", "Cinematic timelapses", "Mavic/Air series"],
                    ["<strong>APAS / Obstacle Avoidance</strong>", "Drone avoids obstacles automatically", "Safety, focusing on composition", "Mini 3/4/5 Pro, Air, Mavic series"],
                    ["<strong>Waypoints</strong>", "Fly pre-planned route with waypoints", "Repeatable shots, mapping", "Most mid-high end drones"],
                    ["<strong>Manual Mode</strong>", "Full control over ISO, shutter, aperture", "Precise exposure control", "All mid-high end drones"],
                ]
            ) +
            grid_cards([
                {"title": "The Most Useful Photography Mode: AEB", "color": "text-green-400", "desc": "AEB (Auto Exposure Bracketing) is probably the most useful mode for serious aerial photography. It takes 3 or 5 shots in quick succession at different exposure levels (underexposed, normal, overexposed). You can then merge them in editing software (Lightroom, Photoshop, Aurora HDR) to create an HDR image with much more dynamic range than a single shot. For landscape photography, AEB is essential for capturing both bright skies and dark foreground detail."},
                {"title": "Panoramas Are Underrated", "color": "text-blue-400", "desc": "DJI drones have built-in panorama modes that automatically shoot and stitch panoramas (180°, wide, vertical, 360°). The quality is surprisingly good — the drone takes multiple photos and stitches them together, giving you much higher resolution than a single shot. Panoramas are great for landscapes and cityscapes where you want to capture the full scene. Try shooting vertical panoramas for something different — they work great for social media."},
            ], 2)
        },
        {
            "id": "pro-tips",
            "title": "Pro Tips for Better Aerial Photography",
            "content": p("Here are some pro tips to take your drone photography to the next level:") +
            step_grid([
                {"title": "Shoot RAW + Edit", "desc": "This is the single biggest tip. Shooting RAW (DNG) gives you so much more flexibility in editing — you can fix exposure, white balance, and colors without losing quality. Learn Lightroom Mobile or Desktop — it is the industry standard and makes a massive difference. A well-edited RAW photo will look 10x better than a JPEG straight out of camera. This is what separates hobbyist photos from pro photos."},
                {"title": "Shoot at Golden Hour", "desc": "The best light for aerial photography is the hour after sunrise and the hour before sunset — golden hour. The warm, soft light makes everything look better: landscapes glow, shadows are long and dramatic, colors are rich. Midday sun is harsh and flat — avoid it if you can. If you must shoot midday, focus on graphic compositions, patterns, and shadows rather than landscape vistas."},
                {"title": "Use the Grid & Rule of Thirds", "desc": "Turn on the grid overlay in DJI Fly camera settings. Use the rule of thirds: place your subject at the intersections of grid lines, not in the center. This creates more dynamic compositions. Also try leading lines — roads, rivers, coastlines that lead the viewer's eye into the frame. Aerial photography is all about composition — you have a unique perspective, so use it."},
                {"title": "Try Different Altitudes & Angles", "desc": "Do not just shoot straight down from 100 meters. Mix it up: fly low (10-20 meters) for intimate details, fly high for grand vistas, tilt the camera up to show the horizon, shoot straight down for abstract patterns. The most interesting drone photos are often not the ones taken at maximum altitude — they are the ones taken from unexpected angles."},
                {"title": "Use AEB for Landscapes", "desc": "Always shoot AEB (3 or 5 brackets) for landscape photos. Merging them in post gives you much better dynamic range — you can keep both a bright, detailed sky AND a detailed foreground, which is impossible with a single exposure in high-contrast scenes. It takes a little extra editing time, but the results are worth it. This is the #1 technique pro aerial photographers use."},
                {"title": "Tell a Story", "desc": "Great drone photos tell a story or show a unique perspective. Ask yourself: what makes this shot interesting from the air? What pattern, shape, or contrast am I showing? The best aerial photos are not just 'I was up high' — they reveal something you cannot see from the ground. Look for patterns, symmetry, color contrasts, and unique shapes."},
            ], "purple") +
            alert("success", "camera", "The best camera is the one you have with you", "Technical specs matter, but the most important thing is actually going out and shooting. A great photo taken with a Mini drone is better than a mediocre photo taken with a Mavic 3. Learn composition, master editing, and fly often — your skills will improve faster than any gear upgrade. Upgrade your gear when you know exactly what limitation is holding you back, not just because a new model came out.")
        },
    ],
    "faqs": [
        {"q": "Which DJI drone has the best camera for photography?", "a": "As of 2026, the DJI Inspire 3 with the X9-8K full-frame camera has the absolute best image quality, but it is a professional cinema drone costing $8,000+. For consumer/prosumer drones, the Mavic 3 Pro has the best photography camera — a 4/3-inch 20MP Hasselblad sensor that produces stunning images with great dynamic range and color. For the money (value), the Air 3 with its 1-inch dual-camera system is the best all-around photography drone. Even the Mini 5 Pro takes surprisingly good photos for its size and price."},
        {"q": "Is the DJI Mini 5 Pro good for photography?", "a": "Yes — the Mini 5 Pro is surprisingly good for photography, especially considering it weighs under 250g and costs ~$759. The 1/1.3-inch 48MP sensor produces sharp, detailed photos, and it can shoot RAW (DNG) for editing flexibility. It is not as good as a 1-inch or 4/3-inch sensor in low light or dynamic range, but for social media, travel photos, and hobbyist photography, it is excellent. The portability is a huge advantage — you will actually bring it everywhere, which means you will take more photos."},
        {"q": "What is the difference between 1-inch and 4/3-inch sensor?", "a": "A 4/3-inch sensor is about twice the physical area of a 1-inch sensor. This means: better low light performance (less noise), better dynamic range (more detail in highlights and shadows), slightly shallower depth of field, and generally better image quality overall. The Mavic 3 has a 4/3-inch sensor, while the Air 2S/Air 3 have 1-inch sensors. The 4/3-inch sensor is noticeably better, especially in low light and when editing heavily, but it also costs significantly more. For most people, 1-inch is excellent — the jump to 4/3-inch is nice but not essential unless you are a professional."},
        {"q": "Should I shoot RAW or JPEG with my drone?", "a": "If you edit your photos at all, shoot RAW (DNG). RAW files contain all the raw sensor data, so you can adjust exposure, white balance, and colors much more aggressively without losing quality. If you never edit and just want to share to social media straight from the drone, JPEG is fine — DJI does a decent job of in-camera processing. Best of both worlds: shoot RAW+JPEG mode. You get the JPEG for quick sharing and the RAW file for when you want to edit seriously. Storage is cheap — always shoot RAW+JPEG if you have space."},
        {"q": "Do I need a Mavic 3 for good photos?", "a": "No — you can take amazing photos with much cheaper drones. The Air 3, Air 2S, and even the Mini series are all capable of producing excellent photos in the right hands. The Mavic 3 gives you better low light, more dynamic range, and slightly better quality overall — but the difference is most visible when you print large or edit aggressively. For social media, web use, and small prints, most people cannot tell the difference between a Mini 5 Pro photo and a Mavic 3 photo. Invest in your skills first, then upgrade gear when you know you need it."},
        {"q": "What is AEB mode and should I use it?", "a": "AEB (Auto Exposure Bracketing) takes multiple photos (usually 3 or 5) in quick succession at different exposure levels — one underexposed, one normal, one overexposed. You can then merge them in editing software to create an HDR (High Dynamic Range) image that captures detail in both bright skies and dark shadows. For landscape photography, you should almost always use AEB. It takes a little extra work in post, but the results are much better than a single exposure. DJI drones have AEB built in — just select it in the photo mode menu."},
        {"q": "How many megapixels do I need for drone photography?", "a": "It depends on what you do with the photos. For social media and web use: 12MP is plenty, 20MP is more than enough. For printing: 20MP can print up to 16x20 inches at good quality. For large prints or commercial use: 24-48MP gives you more cropping flexibility and bigger prints. But do not chase megapixels — sensor size is much more important for image quality. A 20MP 1-inch sensor photo will look better than a 48MP 1/1.3-inch sensor photo, even though it has fewer pixels, because the pixels are bigger and cleaner."},
        {"q": "Is the Air 3 better than Mavic 3 for photography?", "a": "No — the Mavic 3 still has better image quality overall because of its larger 4/3-inch Hasselblad main sensor. The photos have better dynamic range, better low light performance, and slightly better color. However, the Air 3 has advantages: it is cheaper (~$1,099 vs ~$2,199), lighter, more portable, and it has a dual-camera system (24mm wide + 70mm medium tele) that the base Mavic 3 does not have (Mavic 3 has a 24mm wide + 162mm tele). For many photographers, the Air 3 is the better value — you give up some image quality but gain versatility and save a lot of money."},
        {"q": "Can you change lenses on DJI drones?", "a": "Most consumer DJI drones (Mini, Air, Mavic series) have fixed lenses — you cannot change them like on a DSLR or mirrorless camera. However, many newer models have multiple built-in cameras with different focal lengths (wide, medium, tele), which gives you some of the versatility of interchangeable lenses. Only the high-end professional Inspire series (Inspire 2, Inspire 3) has truly interchangeable lenses — you can swap out different camera and lens combinations for different types of work."},
        {"q": "What is the best drone for real estate photography?", "a": "For real estate photography, the DJI Air 3 is probably the best balance. The 1-inch sensor produces great photos and video, the dual camera (wide + medium tele) gives you versatility for both wide exterior shots and tighter detail shots, and it is more affordable than the Mavic 3. If you do a lot of low-light work (twilight photography), step up to the Mavic 3 Classic for the larger sensor and better dynamic range. For most real estate work, the Mini 4 Pro or Mini 5 Pro would also work — just make sure you edit well."},
    ],
    "related": drone_related(),
}

PAGES = [page17, page18, page19, page20]

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
