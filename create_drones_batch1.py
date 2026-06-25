#!/usr/bin/env python3
"""Generate first 5 Drone pages."""

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
        {"href": "best-memory-card-for-dji-mini-5-pro.html", "badge": "SD&nbsp;CARD", "badge_class": "bg-yellow-500/20 text-yellow-400", "border_class": "border-yellow-500/30", "badge2": "Guide", "title": "Best Memory Card", "desc": "What SD card to use with DJI Mini 5 Pro — speed requirements, recommended brands and sizes."},
        {"href": "how-long-do-dji-drone-batteries-last.html", "badge": "BATTERY", "badge_class": "bg-green-500/20 text-green-400", "border_class": "border-green-500/30", "badge2": "Guide", "title": "Battery Lifespan", "desc": "How long DJI drone batteries last, cycle counts by model, and how to extend battery life."},
        {"href": "dji-mini-drone-under-250g-license-requirements.html", "badge": "FAA", "badge_class": "bg-blue-500/20 text-blue-400", "border_class": "border-blue-500/30", "badge2": "Legal", "title": "License Requirements", "desc": "Do you need a license for a sub-250g DJI Mini? FAA rules, registration, and Remote ID."},
        {"href": "dji-drone-battery-swelling-what-to-do.html", "badge": "SAFETY", "badge_class": "bg-red-500/20 text-red-400", "border_class": "border-red-500/30", "badge2": "Safety", "title": "Battery Swelling", "desc": "What causes DJI drone battery swelling, is it safe, and what to do with swollen batteries."},
        {"href": "dji-drone-atti-mode-how-to-get-out.html", "badge": "ATTI&nbsp;MODE", "badge_class": "bg-purple-500/20 text-purple-400", "border_class": "border-purple-500/30", "badge2": "Troubleshoot", "title": "ATTI Mode Guide", "desc": "What is ATTI mode, why drones enter it, and how to fix GPS issues and land safely."},
        {"href": "drones.html", "badge": "ALL&nbsp;GUIDES", "badge_class": "bg-electric-500/20 text-electric-400", "border_class": "border-electric-500/30", "badge2": "Category", "title": "Drone Hub", "desc": "Browse all drone guides, comparisons, specs, and troubleshooting resources."},
    ]

# =================== PAGE 11: FIND LOST DJI DRONE ===================

page11 = {
    "filename": "how-to-find-lost-dji-drone.html",
    "title": "How to Find a Lost DJI Drone: Step-by-Step Guide (2026)",
    "headline": "How to Find a Lost DJI Drone: Step-by-Step Guide (2026)",
    "meta_desc": "Lost your DJI drone? Complete step-by-step guide to finding it. Use Find My Drone, flight logs, last GPS coordinates, community help, and prevention tips. What to do if found and insurance info.",
    "category": "Drones",
    "category_link": "drones.html",
    "breadcrumb_title": "Find Lost Drone",
    "hero_blur": "bg-red-500/5",
    "hero_badges": '''<div class="px-3 py-1.5 bg-red-500/20 text-red-400 font-mono font-bold text-sm rounded-md border border-red-500/30">LOST&nbsp;DRONE</div>
        <span class="badge badge-info"><i data-lucide="map-pin" style="width:0.75rem;height:0.75rem"></i>Step-by-Step</span>
        <span class="badge badge-info"><i data-lucide="radar" style="width:0.75rem;height:0.75rem"></i>Find My Drone</span>''',
    "h1": 'How to Find a Lost DJI Drone &mdash; <span class="gradient-text">Step-by-Step Guide (2026)</span>',
    "hero_desc": "Losing a drone is stressful, but there are many things you can do to find it. DJI drones have built-in features like Find My Drone, flight logs, and last known GPS coordinates that dramatically increase your chances of recovery. In this guide, we walk you through exactly what to do the moment you realize your drone is lost, how to use DJI's tools, how to search effectively, how to get community help, and how to prevent loss in the first place.",
    "hero_stats": f'''<div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="map-pin" style="width:0.9rem;height:0.9rem"></i>GPS Accuracy</div>
          <div class="font-mono font-bold text-xl text-green-400">~5-10m</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="timer" style="width:0.9rem;height:0.9rem"></i>Golden Window</div>
          <div class="font-bold text-xl text-yellow-400">First 24h</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="percent" style="width:0.9rem;height:0.9rem"></i>Recovery Rate</div>
          <div class="font-mono font-bold text-xl text-blue-400">~50-70%</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="battery-low" style="width:0.9rem;height:0.9rem"></i>Battery Life</div>
          <div class="font-bold text-xl text-red-400">~30 min standby</div>
        </div>''',
    "qa_gradient": "from-red-950/20 to-navy-900 border-red-500/20",
    "qa_icon_color": "#f87171",
    "qa_title": "First Steps When Your Drone Is Lost",
    "qa_text": '<strong class="text-white">If your DJI drone is lost, immediately open the DJI Fly app and check Find My Drone for the last known GPS location. Do not turn off the remote controller or app — keep them running to maintain connection if possible.</strong> Walk toward the last known coordinates while watching the signal strength. If the drone is still airborne, try to re-establish connection and bring it home. If it has landed, navigate to the GPS coordinates and search visually. The first hour after losing a drone is critical, because the battery is still running the GPS and you might still have a signal. After that, you rely entirely on the last recorded position and good old-fashioned searching.',
    "qa_extra": f'''<div class="grid md:grid-cols-2 gap-3 mt-4">
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-green-400 font-semibold mb-1">Do This First</div>
          <p class="text-sm text-gray-300">Check Find My Drone, keep RC on, go to last GPS, look/listen, check flight logs, post on community groups</p>
        </div>
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-red-400 font-semibold mb-1">Don\'t Do This</div>
          <p class="text-sm text-gray-300">Don\'t close the app, don\'t turn off RC, don\'t wait too long, don\'t trespass, don\'t give up too early</p>
        </div>
      </div>''',
    "sections": [
        {
            "id": "immediate-steps",
            "title": "Immediate Steps When You Lose Your Drone",
            "content": p("The first 10-60 minutes after losing a drone are the most critical. Here is exactly what to do, in order of priority:") +
            step_grid([
                {"title": "Stay Calm & Keep Everything On", "desc": "Do not turn off the remote controller. Do not close the DJI Fly (or DJI Go) app. Do not log out. The drone may still be transmitting — if you turn off your equipment, you lose your chance to reconnect. Take a deep breath and think clearly. Panic leads to mistakes."},
                {"title": "Check Signal & Try to Reconnect", "desc": "Look at the signal bars in the app. If you have any signal at all, the drone is still on and within range. Try to use Return to Home (RTH) — press the RTH button on the remote controller. If the signal is weak, move to a higher position or closer to where the drone was last seen to improve reception. Walk around slowly while watching the signal meter."},
                {"title": "Open Find My Drone", "desc": "In the DJI Fly app, go to Profile > Find My Drone. This shows you the last known GPS coordinates of the drone on a map. The timestamp tells you when that position was recorded. Note the battery level at the time of disconnect — this tells you how long the drone might still be transmitting after landing."},
                {"title": "Navigate to the Last Known Position", "desc": "Start walking or driving toward the last GPS coordinates. Use the map to guide you. As you get closer, pay attention to signal strength — if it comes back, great! Use the Find My Drone feature to make the drone beep if it is on the ground and still has battery."},
                {"title": "Search Visually & Listen", "desc": "When you arrive at the location, look up first (it might still be in the air if you lost connection momentarily). Then scan the ground. Listen for the beeping or the sound of motors. Call the drone\'s name out loud if you have a speaker. Bring binoculars if you have them — they are extremely helpful for spotting a drone in trees or on rooftops."},
            ], "red") +
            alert("warning", "clock", "Battery is ticking", "Most DJI drones have a standby time of 30-90 minutes after landing, depending on the model and remaining battery. During this time, the drone is still using power for the GPS module and receiver. After the battery dies, you only have the last known coordinates to go on, and the Find My Drone beep feature will not work. Move quickly but safely."),
        },
        {
            "id": "find-my-drone",
            "title": "Using Find My Drone Feature",
            "content": p("DJI's Find My Drone feature is your most powerful tool for locating a lost drone. Here is how to use it effectively:") +
            step_grid([
                {"title": "How to Access Find My Drone", "desc": "In DJI Fly: Open the app, tap Profile (person icon) in the bottom right, scroll down and tap 'Find My Drone'. In DJI Go 4: Open the app, tap the menu icon, go to 'Find My Drone'. The feature shows a map with the last known position of both the drone and your remote controller/phone."},
                {"title": "What You See on the Map", "desc": "The map shows: 1) Drone's last known position (drone icon), 2) Your current position (blue dot / RC icon), 3) The distance between you and the drone, 4) Timestamp of when the position was recorded, 5) Battery level at time of disconnect. You can tap the drone icon for more details like altitude, flight time, and last known heading."},
                {"title": "Using the Beep Feature", "desc": "If the drone is still on and connected (or reconnects), you can tap 'Beep' in Find My Drone to make the drone emit a loud beeping sound. This is extremely helpful when you are near the drone but cannot see it (e.g., in tall grass, bushes, or tree canopy). Walk around and listen for the beep."},
                {"title": "Directions & Navigation", "desc": "The app provides basic directions — distance and compass heading. For more precise navigation, you can note the GPS coordinates (latitude and longitude) and enter them into Google Maps or a hiking GPS app. This lets you use turn-by-turn navigation to get to the general area, then switch to visual search."},
            ], "blue") +
            specs_table(
                ["DJI App", "Find My Drone Location", "Beep Feature", "Flight Log Access"],
                [
                    ["<strong>DJI Fly</strong>", "Profile > Find My Drone", "Yes (when connected)", "Profile > Flight Records"],
                    ["<strong>DJI Go 4</strong>", "Main Menu > Find My Drone", "Yes (when connected)", "Main Menu > Flight Records"],
                    ["<strong>DJI Mimo</strong>", "Limited (for Osmo products)", "No", "Limited"],
                    ["<strong>DJI Assistant</strong>", "Not available", "No", "Can sync logs from drone"],
                ]
            ) +
            alert("info", "wifi", "Offline mode still works", "Find My Drone stores the last known position locally on your phone/tablet even if you do not have internet service. The map tiles might not load if you are offline, but the GPS coordinates will still be there. Write down the latitude and longitude before you leave the area, just in case."),
        },
        {
            "id": "flight-logs",
            "title": "Flight Logs & Last GPS Coordinates",
            "content": p("Flight logs record every detail of your flight: position, altitude, speed, battery level, signal strength, and more. They can help you figure out exactly what happened and where the drone likely went down.") +
            step_grid([
                {"title": "Accessing Flight Logs", "desc": "In DJI Fly: Profile > Flight Records. Tap the relevant flight to see the full log with a map path. In DJI Go 4: Me > Flight Records. Each flight shows date, duration, distance, max altitude, and a map view of the flight path. You can also view detailed telemetry data."},
                {"title": "What to Look For", "desc": "Scroll to the end of the flight log to see where the connection was lost. Note: the position at disconnect, altitude at disconnect (if it was high up, it may have drifted while descending), heading and speed (which direction was it going?), battery level (how much flight time was left?), signal strength (did signal drop gradually or suddenly?)."},
                {"title": "Calculating Where It Landed", "desc": "If the drone was moving when it lost signal, it likely continued in the same direction until it landed (either via auto-landing or RTH attempt). Use the last known speed, heading, and remaining battery to estimate a search radius. If it was at 100m altitude, it takes ~10-20 seconds to descend — at 10m/s ground speed, that means it could land 100-200m from the last known position."},
                {"title": "Downloading & Sharing Logs", "desc": "You can export flight logs as .txt or .csv files (varies by app). Some third-party tools like Airdata (formerly Healthy Drones) can analyze flight logs in more detail. If you are asking for help online, sharing the flight log helps others give you better advice on where to look."},
            ], "yellow") +
            p("Pro tip: sync your flight logs regularly. DJI Fly can sync flights to your DJI account so they are available even if you lose your phone. Enable auto-sync in settings.")
        },
        {
            "id": "search-strategies",
            "title": "Effective Search Strategies",
            "content": p("Once you are at the last known location, how you search matters. Here are proven strategies for finding a lost drone:") +
            grid_cards([
                {"title": "Grid Search Pattern", "color": "text-blue-400", "desc": "The most systematic approach. Divide the search area into a grid and walk each row methodically. Start with a tight grid near the last known position, then expand outward. Use landmarks or GPS waypoints to mark where you have searched. This is slow but thorough — great if you are fairly confident of the location."},
                {"title": "Radio Direction Finding", "color": "text-green-400", "desc": "Walk around while watching the signal strength bars in the app. If the signal gets stronger as you move in a certain direction, keep going that way. This is like playing 'hot and cold' with the drone's radio signal. Works best when the drone is still powered on and transmitting."},
                {"title": "Call Out & Listen", "color": "text-yellow-400", "desc": "If you have the beep feature, use it frequently as you search. If not, clap your hands or call out — some drones have obstacle avoidance sensors or cameras that might pick up movement, but listening is more useful. Be quiet periodically and just listen for any beeping or whirring sounds."},
                {"title": "Look Up & Around", "color": "text-purple-400", "desc": "Drones get stuck in trees, on rooftops, on power lines, and on fences more often than you might think. Scan upward as much as you scan the ground. Bring binoculars — they are game-changing for spotting a drone high in a tree. Look for glints of light reflecting off the plastic or camera lens."},
                {"title": "Ask for Help", "color": "text-red-400", "desc": "Bring friends — more pairs of eyes dramatically increase your chances. Post in local drone groups on Facebook or Reddit — drone pilots will often come help search for a fellow pilot. Offer a reward for the finder — this motivates people who might stumble upon it later."},
                {"title": "Come Back Later", "color": "text-electric-400", "desc": "If you cannot find it after several hours of searching, do not give up. Come back the next day, and the day after. People find drones days or even weeks later. The drone might have landed somewhere you did not think to look, or someone might have found it and will eventually post about it online."},
            ], 2) +
            alert("info", "home", "Check the takeoff point too", "Sometimes drones successfully return home but land somewhere nearby that you did not expect — behind a bush, on a roof across the street, etc. Always double-check the takeoff location and a 50m radius around it before assuming it is gone for good.")
        },
        {
            "id": "community-help",
            "title": "Community & Online Help",
            "content": p("The drone community is incredibly helpful when someone loses a drone. Here is how to leverage community resources:") +
            step_grid([
                {"title": "Local Drone Groups", "desc": "Search Facebook for '[Your City/Area] Drone Pilots' or similar groups. Post a clear description: drone model, color, when and where it was lost, last known coordinates if you have them, your contact info, and whether you are offering a reward. Local pilots often know the area well and may offer to help search."},
                {"title": "Reddit & Forums", "desc": "Post in r/dji, r/drones, or the DJI Forum. Include as much detail as possible — flight log screenshot, last known GPS coordinates, circumstances of the loss. The community can help analyze what went wrong and give search tips. Be respectful — people are more likely to help if you are polite."},
                {"title": "Lost & Found Platforms", "desc": "Check local lost and found groups on Facebook, Nextdoor, Craigslist, and local police departments' lost and found. Some areas have drone-specific lost and found groups. Post there too. Someone who found your drone might be looking for the owner — especially if there is a reward."},
                {"title": "Offer a Reward", "desc": "Offering a reward significantly increases your chances of getting the drone back. $50-$200 is typical, depending on the value of the drone and how much data is on it. State clearly that no questions will be asked — this makes people more willing to return it even if they feel they should not have picked it up."},
                {"title": "Contact Local Authorities", "desc": "If your drone is expensive or has sensitive data on it, file a police report for lost property. This creates an official record, which may help with insurance claims. Do not call 911 unless there is an emergency — use the non-emergency line. Be honest about what happened; flying a drone is not illegal, but you should know the local rules."},
            ], "purple") +
            alert("warning", "user-check", "Be respectful of privacy and property", "Do not trespass on private property to search for your drone. If the drone is clearly on someone's private land, knock on the door and ask politely to search. Most people will be helpful. If you cannot find the owner or they say no, you may need to accept the loss. Trespassing can get you in legal trouble and is not worth it for a drone.")
        },
        {
            "id": "prevention",
            "title": "Prevention Tips to Avoid Losing Your Drone",
            "content": p("The best way to deal with losing a drone is to prevent it from happening in the first place. Here are proven prevention strategies:") +
            specs_table(
                ["Prevention Method", "How It Helps", "Cost", "Difficulty"],
                [
                    ["<strong>Set proper RTH altitude</strong>", "Prevents crashing into buildings/trees on return", "Free", "Easy"],
                    ["<strong>Update firmware regularly</strong>", "Fixes bugs that can cause flyaways", "Free", "Easy"],
                    ["<strong>Calibrate compass before flight</strong>", "Prevents GPS drift and incorrect navigation", "Free", "Easy"],
                    ["<strong>Use Return to Home early & often</strong>", "Practice RTH so you know it works", "Free", "Easy"],
                    ["<strong>Drone tracker / GPS tag</strong>", "Independent tracking even if drone battery dies", "$20-$100", "Easy"],
                    ["<strong>Tile / AirTag attached</strong>", "Crowd-sourced finding via Apple/Google network", "$20-$30", "Very Easy"],
                    ["<strong>Fly with a spotter</strong>", "Extra eyes keep visual line of sight", "Free", "Easy"],
                    ["<strong>Label your drone</strong>", "Whoever finds it can contact you directly", "$0-$10", "Very Easy"],
                    ["<strong>Drone insurance</strong>", "Covers cost if it is lost or damaged beyond recovery", "$50-$200/year", "Easy"],
                    ["<strong>Stay within VLOS</strong>", "Visual line of sight = you always know where it is", "Free", "Medium"],
                ]
            ) +
            step_grid([
                {"title": "Label Your Drone", "desc": "Put your phone number or email on the drone body with a sticker or permanent marker. If someone finds it, they can contact you directly. This is the simplest and cheapest prevention measure. You can also put a return address label inside the battery compartment if it is removable."},
                {"title": "Use a GPS Tracker", "desc": "Attach a small GPS tracker or an Apple AirTag / Samsung SmartTag to your drone. These use Bluetooth and crowd-sourced networks to help you find the drone even after the drone battery dies. Some pilots use 3M tape or Velcro to attach them. Make sure it does not affect the center of gravity or flight performance."},
                {"title": "Know Your RTH Settings", "desc": "Before every flight, confirm: 1) Home point is correctly set, 2) RTH altitude is high enough to clear obstacles in the area, 3) RTH behavior is set correctly (hover, land, or return). Test RTH at the start of every flight to make sure it works properly. Practice manual RTH too — do not rely solely on automatic features."},
            ], "green") +
            alert("info", "shield", "Insurance is worth it for expensive drones", "If you have a drone worth $1,000+, drone insurance from DJI Care, State Farm, or a specialty drone insurer is usually worth it. Plans typically cost $50-$200 per year and cover accidental damage, flyaways, and loss. Read the fine print carefully — some plans only cover crash damage and not flyaways or lost drones.")
        },
        {
            "id": "if-found",
            "title": "What to Do If You Find a Lost Drone",
            "content": p("If you are on the other side — you found someone's drone — here is how to do the right thing and get it back to its owner:") +
            step_grid([
                {"title": "Check for Labels or Contact Info", "desc": "Look on the drone body, battery compartment, and underneath for any stickers, labels, or markings with contact information. If there is a phone number or email, that is the easiest path — just reach out directly."},
                {"title": "Check the SD Card", "desc": "If there is an SD card inside the drone (look in the camera gimbal area), you can look at the photos and videos for clues about the owner. Do not share or post personal photos — just look for identifying information like license plates, faces, or locations that might help identify who it belongs to."},
                {"title": "Post About It Online", "desc": "Post in local drone groups, Nextdoor, Craigslist, and lost and found groups. Describe the drone (model, color, any distinguishing marks) and roughly where you found it. Do not give every detail — let the owner prove it is theirs by describing unique features or what is on the SD card."},
                {"title": "Turn It In to Police", "desc": "If you cannot find the owner after a reasonable effort, you can turn it in to the local police department's lost and found. They will hold it for a period of time (varies by jurisdiction) and if no one claims it, it may become yours. Laws about found property vary — check your local regulations."},
                {"title": "Do Not Keep It Quietly", "desc": "Keeping a found drone is legally theft or misappropriation in most places if you do not make a reasonable effort to find the owner. Drones are expensive ($500-$5,000+), and keeping one that you found can have serious legal consequences. Plus, it is just not the right thing to do — someone is heartbroken over losing their drone."},
            ], "green") +
            alert("success", "heart", "Be the hero", "Drone pilots are a community. If you find a lost drone, going the extra mile to return it means a lot to the owner. Many pilots will offer a reward as a thank you. And the karma is real — next time you lose a drone, you will hope someone does the same for you.")
        },
    ],
    "faqs": [
        {"q": "How do I find my lost DJI drone?", "a": "The first thing to do is open the DJI Fly or DJI Go app and go to Find My Drone — this shows the last known GPS coordinates. Keep the remote controller and app running (do not turn them off) in case the drone reconnects. Navigate to the last known position, use the beep feature if the drone is still powered on, and search methodically using a grid pattern. Check flight logs for more details about where and why the connection was lost. Post in local drone communities for additional help."},
        {"q": "Can I track my DJI drone if it is turned off?", "a": "No — the built-in Find My Drone feature only works when the drone is powered on and has a signal. Once the battery dies, you only have the last recorded GPS position to go by. However, if you attached an independent GPS tracker (like an AirTag or Tile) to your drone, those can still work via Bluetooth crowd-sourcing even when the drone itself is off. For this reason, many pilots attach a Bluetooth tracker as a backup."},
        {"q": "How accurate is DJI Find My Drone GPS?", "a": "DJI drones use GPS (and often GLONASS + Galileo) for positioning, which is typically accurate to 5-10 meters under good conditions. In areas with poor satellite reception (deep canyons, dense tree cover, tall buildings), accuracy can drop to 20-50 meters or worse. The accuracy also depends on how many satellites the drone was locked onto when the connection was lost. More satellites = better accuracy."},
        {"q": "What happens if I lose my DJI drone?", "a": "If you cannot find it, you have a few options: keep searching (many drones are found days or weeks later), file an insurance claim if you have drone insurance, or accept the loss and get a replacement. DJI's Fly Away Coverage (part of DJI Care Refresh) covers flyaways on some models — check your policy. Always report the loss to DJI as well, so if someone tries to register or use the drone, DJI can potentially help you get it back."},
        {"q": "How far can a DJI drone fly before losing signal?", "a": "It depends on the model and environment. DJI consumer drones have advertised transmission ranges of 6-15+ km (O2, O3, O4 transmission systems). In practice, with obstacles and interference, you might lose signal at 1-5 km. Always keep visual line of sight as required by law in most countries. The RTH (Return to Home) feature automatically brings the drone back if signal is lost or battery is low — but it is not 100% reliable, especially with obstacles."},
        {"q": "Does DJI have a lost and found?", "a": "DJI does not operate a central lost and found service. However, if you register your drone with DJI (which you do when you activate it), DJI has your contact information linked to the drone's serial number. If someone contacts DJI about a found drone, DJI may be able to connect you. There are also third-party lost and found platforms for drones, and local drone communities are usually very helpful."},
        {"q": "Should I put an AirTag on my drone?", "a": "Yes — an Apple AirTag, Samsung SmartTag, or Tile is a cheap and effective way to help find your drone if it is lost. It only adds a few grams of weight (negligible for most drones), and it provides a backup tracking method that works even after the drone battery dies. Attach it securely with 3M tape or Velcro on the top or bottom of the drone body. Just make sure it does not interfere with the gimbal, sensors, or aerodynamics."},
        {"q": "What do I do if my drone flies away?", "a": "First, stay calm and do not turn off the controller. Try to re-establish connection by moving to a higher vantage point. Press the Return to Home button repeatedly. If it does not come back, immediately check Find My Drone for the last position and go there to search. Review the flight log afterward to understand what caused the flyaway. If you have DJI Care Refresh with flyaway coverage, you may be eligible for a replacement at a discount."},
        {"q": "How long do drone batteries last when lost?", "a": "After a drone lands, the battery continues to power the GPS module, receiver, and other systems. How long it lasts depends on the remaining charge when it landed, the drone model, and temperature. As a rough estimate: 30 minutes to 2 hours of standby time after landing. In cold weather, battery life is shorter. After the battery dies, the drone stops transmitting and you only have the last GPS coordinates."},
        {"q": "Does drone insurance cover lost drones?", "a": "It depends on the policy. Some drone insurance policies cover accidental loss and flyaways, while others only cover crash damage. DJI Care Refresh on most models includes 'Flyaway Coverage' that lets you get a replacement drone for a discounted fee if it flies away. Always read the policy details carefully. For third-party insurance (like State Farm or specialty drone insurers), make sure 'mysterious disappearance' or 'flyaway' is specifically covered."},
    ],
    "related": drone_related(),
}

# =================== PAGE 12: BEST MEMORY CARD DJI MINI 5 PRO ===================

page12 = {
    "filename": "best-memory-card-for-dji-mini-5-pro.html",
    "title": "Best Memory Card for DJI Mini 5 Pro (SD Card Guide 2026)",
    "headline": "Best Memory Card for DJI Mini 5 Pro (SD Card Guide 2026)",
    "meta_desc": "Best SD card for DJI Mini 5 Pro in 2026. Complete guide covering UHS-I vs UHS-II, speed requirements for 4K video, recommended brands and sizes, reliability comparison, formatting tips, and common issues.",
    "category": "Drones",
    "category_link": "drones.html",
    "breadcrumb_title": "Mini 5 Pro SD Card",
    "hero_blur": "bg-yellow-500/5",
    "hero_badges": '''<div class="px-3 py-1.5 bg-yellow-500/20 text-yellow-400 font-mono font-bold text-sm rounded-md border border-yellow-500/30">SD&nbsp;CARD</div>
        <span class="badge badge-info"><i data-lucide="sd-card" style="width:0.75rem;height:0.75rem"></i>Storage Guide</span>
        <span class="badge badge-info"><i data-lucide="film" style="width:0.75rem;height:0.75rem"></i>4K Video</span>''',
    "h1": 'Best Memory Card for DJI Mini 5 Pro &mdash; <span class="gradient-text">SD Card Guide 2026</span>',
    "hero_desc": "The DJI Mini 5 Pro shoots 4K video at up to 60fps and takes 48MP photos — so you need a fast, reliable microSD card to keep up. Not all SD cards are created equal: a slow card will cause dropped frames, corrupted footage, and lost shots. In this guide, we cover the exact speed requirements, which brands are most reliable, what size to get, UHS-I vs UHS-II, how to format properly, and common SD card issues to watch out for.",
    "hero_stats": f'''<div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="film" style="width:0.9rem;height:0.9rem"></i>Video Bitrate</div>
          <div class="font-mono font-bold text-xl text-yellow-400">150 Mbps</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="sd-card" style="width:0.9rem;height:0.9rem"></i>Min Speed</div>
          <div class="font-bold text-xl text-green-400">U3 / V30</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="hard-drive" style="width:0.9rem;height:0.9rem"></i>Storage</div>
          <div class="font-mono font-bold text-xl text-blue-400">64-256GB</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="type" style="width:0.9rem;height:0.9rem"></i>Format</div>
          <div class="font-bold text-xl text-purple-400">exFAT</div>
        </div>''',
    "qa_gradient": "from-yellow-950/20 to-navy-900 border-yellow-500/20",
    "qa_icon_color": "#facc15",
    "qa_title": "Best SD Card Overall",
    "qa_text": '<strong class="text-white">The best microSD card for DJI Mini 5 Pro is the SanDisk Extreme Pro 128GB or Samsung EVO Select 128GB.</strong> Both are U3/V30 rated, which means they have the sustained write speed needed for 4K 60fps video. The SanDisk Extreme Pro is the most widely recommended by drone pilots for its reliability and speed. The Samsung EVO Select offers great value and comparable performance. Avoid cheap no-name cards — they are the #1 cause of corrupted footage and lost photos/videos. For most people, 128GB is the sweet spot: enough for 3-5 hours of 4K video, and not so expensive that you cry if you lose the drone.',
    "qa_extra": f'''<div class="grid md:grid-cols-3 gap-3 mt-4">
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-yellow-400 font-semibold mb-1 text-sm">Best Overall</div>
          <div class="font-bold text-white">SanDisk Extreme Pro</div>
          <div class="text-xs text-gray-400 mt-1">128GB ~$18-25</div>
        </div>
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-blue-400 font-semibold mb-1 text-sm">Best Value</div>
          <div class="font-bold text-white">Samsung EVO Select</div>
          <div class="text-xs text-gray-400 mt-1">128GB ~$12-18</div>
        </div>
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-green-400 font-semibold mb-1 text-sm">Most Reliable</div>
          <div class="font-bold text-white">Lexar Professional</div>
          <div class="text-xs text-gray-400 mt-1">128GB ~$20-30</div>
        </div>
      </div>''',
    "sections": [
        {
            "id": "speed-requirements",
            "title": "DJI Mini 5 Pro SD Card Requirements",
            "content": p("The DJI Mini 5 Pro has specific SD card speed requirements to record video without dropped frames. Here is what you need to know:") +
            specs_table(
                ["Video Mode", "Resolution", "Frame Rate", "Bitrate", "Required Speed Class"],
                [
                    ["<strong>4K Normal</strong>", "3840×2160", "24/30fps", "~50-100 Mbps", "U1 / V10 minimum"],
                    ["<strong>4K High Frame Rate</strong>", "3840×2160", "48/50/60fps", "~100-150 Mbps", "U3 / V30 recommended"],
                    ["<strong>2.7K</strong>", "2720×1530", "24-60fps", "~35-100 Mbps", "U1 / V10 minimum"],
                    ["<strong>1080p</strong>", "1920×1080", "24-120fps", "~15-80 Mbps", "U1 / V10 minimum"],
                    ["<strong>Slow Motion</strong>", "1080p", "120/200fps", "~50-100 Mbps", "U3 / V30 recommended"],
                    ["<strong>48MP Photos</strong>", "—", "—", "~15-25 MB per photo", "Any Class 10 card"],
                ]
            ) +
            p("DJI officially recommends UHS-I Speed Grade 3 (U3) or Video Speed Class 30 (V30) microSD cards for the Mini 5 Pro, especially for recording high-bitrate 4K video. Cheaper cards with lower ratings may work for 1080p or low-bitrate recording but can cause dropped frames or recording stops when shooting 4K 60fps.") +
            alert("info", "gauge", "Understanding speed class ratings", "SD card speed classes can be confusing. Here is the shorthand: Class 10 = minimum 10MB/s write (old standard, for 1080p). U1 = minimum 10MB/s sustained write (UHS bus). U3 = minimum 30MB/s sustained write (for 4K). V10 = 10MB/s video speed. V30 = 30MB/s video speed. V60 = 60MB/s (for 8K or 4K 120fps). For the Mini 5 Pro, U3/V30 is the sweet spot."),
        },
        {
            "id": "uhs1-vs-uhs2",
            "title": "UHS-I vs UHS-II — Does It Matter?",
            "content": p("You might have seen UHS-II SD cards with faster read/write speeds and wondered if they are worth the extra cost for the Mini 5 Pro. Here is the answer:") +
            specs_table(
                ["Feature", "UHS-I", "UHS-II", "Does Mini 5 Pro Use It?"],
                [
                    ["<strong>Max Bus Speed</strong>", "104 MB/s", "312 MB/s", "No — only UHS-I"],
                    ["<strong>Typical Write Speed</strong>", "60-95 MB/s", "150-250+ MB/s", "Limited to UHS-I speeds in drone"],
                    ["<strong>Extra Row of Pins</strong>", "No", "Yes (second row)", "Second row unused in Mini 5 Pro"],
                    ["<strong>Price (128GB)</strong>", "$10-$25", "$25-$50", "—"],
                    ["<strong>Value for Mini 5 Pro</strong>", "Excellent", "Waste of money", "—"],
                ]
            ) +
            p("The DJI Mini 5 Pro only has a UHS-I SD card slot — it does not support the extra speed of UHS-II cards. A UHS-II card will still work in the Mini 5 Pro, but it will only run at UHS-I speeds. You are paying for speed you cannot use inside the drone.") +
            alert("success", "download", "UHS-II helps with transfer speed", "There is one case where UHS-II is worth it: if you transfer footage directly from the card to your computer using a UHS-II card reader, it will be much faster. If you shoot a lot of footage and value fast transfers, a UHS-II card might be worth the premium. But for recording in the drone itself, UHS-I U3/V30 is perfectly sufficient.")
        },
        {
            "id": "recommended-cards",
            "title": "Recommended Cards by Brand & Size",
            "content": p("Here are our top recommended microSD cards for the DJI Mini 5 Pro, organized by brand and size:") +
            specs_table(
                ["Brand & Model", "64GB", "128GB", "256GB", "Speed Rating", "Reliability"],
                [
                    ["<strong>SanDisk Extreme Pro</strong>", "$12-15", "$18-25", "$30-45", "U3 / V30 / A2", "Excellent — gold standard"],
                    ["<strong>SanDisk Extreme</strong>", "$10-13", "$15-20", "$25-35", "U3 / V30 / A2", "Very good — slightly slower"],
                    ["<strong>Samsung EVO Select</strong>", "$8-10", "$12-18", "$22-30", "U3 / V30 / A2", "Very good — great value"],
                    ["<strong>Samsung PRO Endurance</strong>", "$12-15", "$20-28", "$35-50", "U3 / V30", "Excellent — high endurance"],
                    ["<strong>Lexar Professional 1066x</strong>", "$10-14", "$15-22", "$28-40", "U3 / V30 / A2", "Very good — fast"],
                    ["<strong>Kingston Canvas Go! Plus</strong>", "$9-12", "$13-18", "$24-32", "U3 / V30 / A2", "Good — budget option"],
                ]
            ) +
            grid_cards([
                {"title": "SanDisk Extreme Pro", "color": "text-yellow-400", "desc": "The gold standard for drone SD cards. Fast, reliable, widely tested, and available everywhere. SanDisk has a strong reputation and good warranty support. The Extreme Pro model is faster than the regular Extreme, though both work fine. Many professional drone pilots swear by these cards."},
                {"title": "Samsung EVO Select", "color": "text-blue-400", "desc": "The best value pick. Samsung makes excellent NAND flash, and the EVO Select is surprisingly fast and reliable for the price. Great bang for your buck. Available on Amazon in frustration-free packaging. The white/teal color scheme is distinctive."},
                {"title": "Lexar Professional", "color": "text-purple-400", "desc": "Another excellent professional-grade option. Lexar's high-end cards are very fast and durable. The 1066x and 1800x lines are popular with drone pilots. Lexar is a well-established brand in the memory industry."},
                {"title": "Avoid: No-Name Amazon Cards", "color": "text-red-400", "desc": "Cheap cards from unknown brands on Amazon or AliExpress are the #1 cause of corrupted drone footage. They often have fake capacity ratings, slow actual write speeds, and terrible reliability. Losing a card full of amazing footage because you saved $5 is not worth it. Stick with known brands."},
            ], 2)
        },
        {
            "id": "what-size",
            "title": "What Size SD Card Should You Get?",
            "content": p("The right size depends on how much you shoot and how often you offload footage. Here is a guide:") +
            specs_table(
                ["Card Size", "4K 30fps Video", "4K 60fps Video", "48MP Photos", "Best For"],
                [
                    ["<strong>32GB</strong>", "~1.5 hours", "~50 minutes", "~800-1,000", "Casual use, short flights"],
                    ["<strong>64GB</strong>", "~3 hours", "~1.5-2 hours", "~1,600-2,000", "Most casual pilots"],
                    ["<strong>128GB</strong>", "~6-7 hours", "~3-4 hours", "~3,500-4,000", "Sweet spot for most pilots"],
                    ["<strong>256GB</strong>", "~12-15 hours", "~7-9 hours", "~7,000-8,000", "Frequent flyers, professionals"],
                    ["<strong>512GB</strong>", "~25-30 hours", "~15-18 hours", "~15,000+", "Pro shooters, long trips"],
                    ["<strong>1TB</strong>", "~50-60 hours", "~30-35 hours", "~30,000+", "Overkill for most — check compatibility"],
                ]
            ) +
            p("Estimates based on 50-150 Mbps bitrate, which is typical for the Mini 5 Pro. Actual recording time varies based on bitrate, complexity of the scene, and compression settings.") +
            step_grid([
                {"title": "Our Recommendation: 128GB", "desc": "For most people, 128GB is the perfect size. It gives you 3-4 hours of 4K 60fps footage, which is enough for a full day of flying or a weekend trip. It is also the best value per gigabyte — 128GB cards usually cost only slightly more than 64GB, while 256GB is nearly double the price. 128GB also means you will not be devastated if you lose the drone with the card still inside."},
                {"title": "Why Multiple Smaller Cards Are Better", "desc": "Instead of one 512GB card, consider having four 128GB cards. Why? 1) If a card fails or gets corrupted, you only lose part of your footage. 2) If you lose the drone, you only lose one card's worth of footage. 3) You can swap cards and keep flying while offloading. 4) Smaller cards are cheaper to replace. Pro tip: label your cards 1, 2, 3, 4 and use them in order."},
            ], "green") +
            alert("warning", "alert-triangle", "Check maximum supported size", "The DJI Mini 5 Pro supports microSD cards up to at least 512GB, and likely 1TB as well (DJI usually does not publish a hard max but large cards generally work). However, cards must be formatted properly (exFAT or FAT32 depending on size). Very large cards (1TB+) may not be tested or supported by DJI — check recent user reports before buying an ultra-high-capacity card.")
        },
        {
            "id": "reliability-comparison",
            "title": "Card Reliability Comparison",
            "content": p("Reliability is the most important factor in a drone SD card. A fast card is useless if it corrupts your footage. Here is what we know about reliability:") +
            specs_table(
                ["Brand", "Reputation", "Failure Rate (Est.)", "Warranty", "Notes"],
                [
                    ["<strong>SanDisk</strong>", "Excellent", "Low (~1-2%)", "Lifetime limited", "Most widely used/tested by drone community"],
                    ["<strong>Samsung</strong>", "Excellent", "Low (~1-2%)", "10-year limited", "Samsung makes its own NAND — very reliable"],
                    ["<strong>Lexar</strong>", "Very Good", "Low (~2%)", "Lifetime limited", "Professional line is very solid"],
                    ["<strong>Kingston</strong>", "Good", "Low-Med (~2-3%)", "Lifetime limited", "Budget line is decent, higher end better"],
                    ["<strong>PNY</strong>", "Good", "Low-Med (~2-3%)", "Lifetime limited", "Hit or miss — stick to Pro models"],
                    ["<strong>No-name brands</strong>", "Poor", "High (~10%+)", "Often none", "Many counterfeits, high failure rate"],
                ]
            ) +
            p("These failure rate estimates are based on community surveys and anecdotal evidence — your mileage may vary. The most important takeaway: name-brand cards from reputable sellers (Amazon, Best Buy, B&H) are much more reliable than no-name cards or cards from third-party marketplace sellers.") +
            alert("warning", "shopping-bag", "Beware of counterfeit SD cards", "Counterfeit SD cards are a huge problem, especially on Amazon Marketplace and eBay. Fake cards claim to be SanDisk or Samsung but have much lower actual capacity and speed — and they fail frequently. To avoid fakes: buy from Amazon.com (not marketplace sellers), Best Buy, B&H Photo, or other reputable retailers. If the price seems too good to be true, it probably is. Verify the card's actual capacity and speed with a tool like H2testW when you receive it.")
        },
        {
            "id": "how-to-format",
            "title": "How to Format Your SD Card Properly",
            "content": p("Formatting your SD card correctly is important for reliability and performance. Here is how to do it:") +
            step_grid([
                {"title": "Always Format In the Drone First", "desc": "The best way to format a card for your Mini 5 Pro is to format it IN the drone using the DJI Fly app. This ensures the correct file system, cluster size, and DJI-specific folder structure. Go to: Camera view > Settings (three dots) > Storage > Format SD Card. The drone will format the card and create the necessary folders."},
                {"title": "Formatting on Computer", "desc": "If you need to format on a computer: for cards 64GB and larger, use exFAT. For 32GB and smaller, you can use FAT32. On Windows: right-click the drive > Format > File system: exFAT > Quick Format. On Mac: Disk Utility > Select card > Erase > Format: ExFAT > Scheme: Master Boot Record. But after formatting on computer, re-format in the drone to be safe."},
                {"title": "Format Regularly", "desc": "Format your SD card after every few flights or after you have backed up all your footage. Regular formatting keeps the file system clean and reduces the chance of corruption. Always back up your files before formatting — formatting erases everything on the card."},
                {"title": "Do Not Delete Files One by One", "desc": "Avoid deleting individual photos or videos on the card using the drone or your computer. This can cause file system fragmentation and issues over time. Instead, offload all the files you want to keep, then format the entire card. It is faster and more reliable."},
            ], "blue") +
            alert("info", "save", "Backup your footage immediately", "As soon as you get home from flying, copy your footage to your computer or an external drive. SD cards can fail, drones can be lost — the only safe footage is backed-up footage. Follow the 3-2-1 rule: 3 copies of data, on 2 different media, 1 offsite."),
        },
        {
            "id": "common-issues",
            "title": "Common SD Card Issues & Fixes",
            "content": p("Here are the most common SD card problems drone pilots encounter and how to fix them:") +
            specs_table(
                ["Issue", "Possible Cause", "Fix", "Prevent It"],
                [
                    ["<strong>'Card Full' but it is empty</strong>", "File system corruption, hidden files", "Reformat card in drone", "Always format in drone, not computer"],
                    ["<strong>Dropped frames in video</strong>", "Card too slow, counterfeit card", "Use U3/V30 card from reputable brand", "Buy name-brand U3 cards from Amazon/B&H"],
                    ["<strong>'No SD card' error</strong>", "Dirty contacts, bad card, slot issue", "Clean contacts, reinsert, try different card", "Handle card carefully, keep clean"],
                    ["<strong>Corrupted footage</strong>", "Cheap card, fake capacity, heat", "Replace with reliable card, don't shoot in extreme heat", "Use quality cards, let drone cool down"],
                    ["<strong>Slow transfer to computer</strong>", "Slow card reader, USB 2.0 port", "Use USB 3.0+ card reader, UHS-II card for transfer", "Get a good USB 3.2 card reader"],
                    ["<strong>Card not recognized</strong>", "Wrong format, damaged card, dirty pins", "Format properly, clean contacts, replace card", "Eject properly before removing card"],
                ]
            ) +
            alert("critical", "flame", "If a card starts having issues, retire it", "If an SD card starts giving you errors, dropped frames, or corrupted files more than once, do not keep using it. The card is likely failing. SD cards are cheap compared to the footage they hold. Retire problematic cards and use them only for non-critical storage (or throw them away). Do not risk losing irreplaceable footage to save $15.")
        },
    ],
    "faqs": [
        {"q": "What SD card does DJI Mini 5 Pro use?", "a": "The DJI Mini 5 Pro uses microSD cards (microSDHC or microSDXC). DJI recommends UHS-I Speed Grade 3 (U3) or Video Speed Class 30 (V30) cards for reliable 4K video recording. Cards as small as 8GB work for photos and 1080p, but 64GB-256GB U3/V30 cards are the sweet spot. UHS-II cards will work but run at UHS-I speed since the drone only has a UHS-I slot — so UHS-II is not necessary unless you want fast file transfers to your computer."},
        {"q": "What size SD card should I get for Mini 5 Pro?", "a": "For most people, 128GB is the best size. It stores about 3-4 hours of 4K 60fps video or 3,500+ 48MP photos — enough for a full day of flying or a weekend trip. 64GB works if you fly casually and offload footage frequently. 256GB is better if you fly frequently, go on long trips, or do not want to worry about running out of space. We recommend having at least two 128GB cards rather than one 256GB card, so you can swap and reduce the risk of losing all your footage."},
        {"q": "Do I need U3 speed for 4K video?", "a": "Yes — for reliable 4K 60fps recording on the Mini 5 Pro, you should use a U3/V30 rated card. The Mini 5 Pro's 4K 60fps video has a bitrate up to around 150 Mbps, which is about 18.75 MB/s. U3 cards guarantee a minimum sustained write speed of 30 MB/s, which gives plenty of headroom. U1/V10 cards (10 MB/s minimum) might work for 4K 30fps at lower bitrates, but can cause dropped frames or recording stops, especially in high-motion scenes where bitrate spikes."},
        {"q": "Is SanDisk Extreme or Extreme Pro better for drones?", "a": "Both work well for the Mini 5 Pro. The Extreme Pro is faster (up to 200MB/s read vs 160MB/s read for Extreme) and may have slightly better reliability, but both are U3/V30 rated and will record 4K video without issues. The Extreme is better value for money. The Extreme Pro is worth the extra few dollars if you want the absolute best or transfer files directly from the card frequently (it reads faster). Either is fine — both are much better than no-name brands."},
        {"q": "How do I format my SD card for DJI Mini 5 Pro?", "a": "The best way is to format it directly in the drone using the DJI Fly app: Go to the camera view, tap the three dots (Settings), go to Storage, then tap Format SD Card. This ensures the correct file system (exFAT for cards larger than 32GB) and proper DJI folder structure. If you format on a computer first, always re-format in the drone afterward. For 64GB+ cards on computer, use exFAT. Back up your files before formatting — it erases everything."},
        {"q": "Why does my DJI say no SD card?", "a": "The 'No SD card' error on DJI drones usually means: the card is not inserted correctly (try removing and reinserting), the card contacts are dirty (gently clean the gold pins with isopropyl alcohol), the card is not formatted correctly (format it in the drone), or the card is defective or counterfeit. Try a different known-good card to determine if the problem is the card or the drone's card slot. If multiple cards give the same error, the drone's card reader may be faulty and need repair."},
        {"q": "How long does a 128GB SD card record 4K video?", "a": "On the DJI Mini 5 Pro, a 128GB card records approximately 3-4 hours of 4K 60fps video at high bitrate (100-150 Mbps), or 6-8 hours of 4K 30fps at normal bitrate (50-80 Mbps). Actual recording time varies depending on the video settings, bitrate, and scene complexity (high-motion scenes use more data). For photos only, a 128GB card holds roughly 3,500-4,000 48MP RAW+JPEG photos, or 10,000+ JPEG-only photos."},
        {"q": "Are cheap SD cards from Amazon safe to use?", "a": "Generally, no — cheap no-name SD cards are the leading cause of corrupted drone footage and lost data. Many are counterfeit, have fake capacity ratings (claim 128GB but actually hold 16GB), and fail frequently. The $5-10 you save is not worth losing hours of irreplaceable footage. Stick with reputable brands (SanDisk, Samsung, Lexar) sold by Amazon (not third-party marketplace sellers) or other trusted retailers like Best Buy or B&H Photo."},
        {"q": "Can I use a UHS-II card in DJI Mini 5 Pro?", "a": "Yes, a UHS-II microSD card will physically fit and work in the Mini 5 Pro, but the drone only has a UHS-I card slot, so the card will operate at UHS-I speeds (max ~95 MB/s write). You are paying extra for UHS-II speed that you cannot use while recording. However, UHS-II cards do transfer files faster when you use a UHS-II card reader with your computer, so they can still be worth it if you value fast file transfers. For most people, UHS-I U3/V30 cards are the best value."},
        {"q": "How often should I replace my drone SD card?", "a": "SD cards have a limited number of write cycles (usually 1,000-10,000+ depending on the type of flash). For casual drone pilots who fly a few times per month, a good quality SD card should last 3-5 years or more. For heavy users (daily flying), replace cards every 1-2 years or when they start showing issues (errors, corruption, slow speeds). Since SD cards are relatively cheap, it is good practice to rotate between 2-3 cards and replace them proactively every couple of years rather than waiting for one to fail with important footage on it."},
    ],
    "related": drone_related(),
}

PAGES = [page11, page12]

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
