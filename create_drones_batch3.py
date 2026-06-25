#!/usr/bin/env python3
"""Generate drone pages batch 3: photo transfer, FAA license, battery swelling."""

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
        {"href": "dji-drone-battery-swelling-what-to-do.html", "badge": "SAFETY", "badge_class": "bg-red-500/20 text-red-400", "border_class": "border-red-500/30", "badge2": "Safety", "title": "Battery Swelling", "desc": "What causes DJI drone battery swelling, is it safe, and what to do with swollen batteries."},
        {"href": "dji-drone-atti-mode-how-to-get-out.html", "badge": "ATTI&nbsp;MODE", "badge_class": "bg-purple-500/20 text-purple-400", "border_class": "border-purple-500/30", "badge2": "Troubleshoot", "title": "ATTI Mode Guide", "desc": "What is ATTI mode, why drones enter it, and how to fix GPS issues and land safely."},
        {"href": "drones.html", "badge": "ALL&nbsp;GUIDES", "badge_class": "bg-electric-500/20 text-electric-400", "border_class": "border-electric-500/30", "badge2": "Category", "title": "Drone Hub", "desc": "Browse all drone guides, comparisons, specs, and troubleshooting resources."},
    ]

# =================== PAGE 15: TRANSFER PHOTOS TO PHONE ===================

page15 = {
    "filename": "how-to-transfer-dji-drone-photos-to-phone.html",
    "title": "How to Transfer DJI Drone Photos & Videos to Phone (2026)",
    "headline": "How to Transfer DJI Drone Photos & Videos to Phone (2026)",
    "meta_desc": "How to transfer photos and videos from a DJI drone to your phone. Complete guide covering wireless transfer, USB-C cable, SD card readers, Quick Transfer feature, file formats, and troubleshooting.",
    "category": "Drones",
    "category_link": "drones.html",
    "breadcrumb_title": "Transfer Photos to Phone",
    "hero_blur": "bg-purple-500/5",
    "hero_badges": '''<div class="px-3 py-1.5 bg-purple-500/20 text-purple-400 font-mono font-bold text-sm rounded-md border border-purple-500/30">PHOTO&nbsp;TRANSFER</div>
        <span class="badge badge-info"><i data-lucide="smartphone" style="width:0.75rem;height:0.75rem"></i>iOS + Android</span>
        <span class="badge badge-info"><i data-lucide="folder-down" style="width:0.75rem;height:0.75rem"></i>Quick Transfer</span>''',
    "h1": 'How to Transfer DJI Drone Photos &amp; Videos to Phone &mdash; <span class="gradient-text">Complete Guide 2026</span>',
    "hero_desc": "Getting your drone photos and videos onto your phone lets you edit, share, and post them right away. DJI offers multiple ways to transfer files: wirelessly through the app, with a USB-C cable, using an SD card reader, and via Quick Transfer. Each method has pros and cons — some are fast, some are convenient, some require extra hardware. In this guide, we cover every transfer method, compare speeds, explain file formats, and help you troubleshoot common transfer issues.",
    "hero_stats": f'''<div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="wifi" style="width:0.9rem;height:0.9rem"></i>Wireless</div>
          <div class="font-mono font-bold text-xl text-blue-400">2-10 MB/s</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="usb" style="width:0.9rem;height:0.9rem"></i>USB-C</div>
          <div class="font-bold text-xl text-green-400">20-50 MB/s</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="sd-card" style="width:0.9rem;height:0.9rem"></i>SD Card Reader</div>
          <div class="font-mono font-bold text-xl text-yellow-400">50-100+ MB/s</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="zap" style="width:0.9rem;height:0.9rem"></i>Quick Transfer</div>
          <div class="font-bold text-xl text-purple-400">Fastest wireless</div>
        </div>''',
    "qa_gradient": "from-purple-950/20 to-navy-900 border-purple-500/20",
    "qa_icon_color": "#c084fc",
    "qa_title": "Best Way to Transfer Photos",
    "qa_text": '<strong class="text-white">The fastest way to transfer DJI photos and videos to your phone is with an SD card reader (Lightning or USB-C), which can transfer full-resolution files at 50-100+ MB/s.</strong> The most convenient way is wireless transfer through the DJI Fly app — no extra hardware needed, just your phone and the drone. For quick sharing of a few photos, the Quick Transfer feature is perfect — it creates a direct Wi-Fi connection between drone and phone without needing the controller. Which method you choose depends on how many files you have, how fast you need them, and what hardware you have. For most people, the built-in download feature in DJI Fly is sufficient and most convenient.',
    "qa_extra": f'''<div class="grid md:grid-cols-2 gap-3 mt-4">
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-green-400 font-semibold mb-1">Fastest</div>
          <p class="text-sm text-gray-300">SD card reader — 1GB in ~10-20 seconds</p>
        </div>
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-blue-400 font-semibold mb-1">Most Convenient</div>
          <p class="text-sm text-gray-300">DJI Fly app download — no extra hardware</p>
        </div>
      </div>''',
    "sections": [
        {
            "id": "wireless-transfer",
            "title": "Wireless Transfer via DJI Fly App",
            "content": p("The most common way to transfer photos and videos is wirelessly through the DJI Fly app. It requires no extra hardware — just your phone connected to the drone via the controller's Wi-Fi.") +
            step_grid([
                {"title": "Step-by-Step: Download from DJI Fly", "desc": "1) Connect your phone to the controller and power on the drone. 2) Open the DJI Fly app and enter the camera view. 3) Tap the media/album icon (looks like a photo thumbnail) in the bottom right. 4) Browse the photos and videos stored on the drone's SD card. 5) Tap 'Select' in the top right, then choose the files you want to download. 6) Tap the download/save icon. 7) Choose whether to download the original file or a compressed version. 8) Wait for the transfer to complete — files are saved to your phone's gallery or DJI album."},
                {"title": "Download Original vs Optimized", "desc": "DJI Fly gives you two download options: 'Original' downloads the full-resolution file exactly as it is on the SD card (larger file size, best quality). 'Optimized' or 'Preview' downloads a smaller, compressed version that is faster to transfer and takes less space on your phone. For sharing to social media, optimized is usually fine. For editing or printing, download the original. Note: RAW photos and 4K video can only be downloaded as original files — optimized versions are lower resolution."},
            ], "blue") +
            specs_table(
                ["File Type", "Original Size (approx)", "Wireless Time", "Optimized Size"],
                [
                    ["<strong>JPEG photo (12MP)</strong>", "3-5 MB", "1-3 seconds", "~0.5-1 MB"],
                    ["<strong>JPEG photo (48MP)</strong>", "10-15 MB", "3-8 seconds", "~1-2 MB"],
                    ["<strong>RAW photo (DNG)</strong>", "20-40 MB", "5-20 seconds", "Not available"],
                    ["<strong>1080p video (1 min)</strong>", "60-120 MB", "10-60 seconds", "~20-40 MB"],
                    ["<strong>4K video (1 min)</strong>", "200-500 MB", "30 seconds - 4 min", "~50-100 MB"],
                ]
            ) +
            p("Wireless transfer speed depends on your phone, the drone model, signal strength, and distance between controller and phone. 2-10 MB/s is typical. The further your phone is from the controller, the slower the transfer. For best speed, keep your phone close to the controller and avoid Wi-Fi interference.") +
            alert("info", "wifi", "Transfer while flying", "You can actually start downloading photos while the drone is still flying — useful if you want to share a shot immediately. However, downloading while flying uses some of the connection bandwidth, which can slightly reduce video feed quality or range. For casual flying it is fine, but be cautious when flying far or in challenging signal conditions.")
        },
        {
            "id": "quick-transfer",
            "title": "Quick Transfer Feature Explained",
            "content": p("Quick Transfer is a DJI feature that lets you transfer photos and videos directly from the drone to your phone without needing the controller. It creates a direct Wi-Fi connection between the drone and your phone.") +
            step_grid([
                {"title": "How to Use Quick Transfer", "desc": "1) Turn on the drone (no controller needed). 2) On your phone, go to Wi-Fi settings and connect to the drone's Wi-Fi network (it will show up as something like 'DJI-Mini3Pro-XXXX'). 3) Open the DJI Fly app. 4) The app will detect the drone and show the Quick Transfer interface. 5) Browse and download photos/videos directly from the drone. 6) When done, disconnect properly. Quick Transfer works best within about 10-30 meters of the drone."},
                {"title": "When to Use Quick Transfer", "desc": "Quick Transfer is perfect for: when you left the controller at home but want to get photos off the drone, when you want to quickly share photos with friends without setting up the whole rig, when the controller battery is dead but the drone has charge, or when you just want a faster direct Wi-Fi connection without the controller in the middle. It is a surprisingly useful feature that many people do not know about."},
            ], "purple") +
            grid_cards([
                {"title": "Quick Transfer Pros", "color": "text-green-400", "desc": "No controller needed, direct connection may be faster than through controller, great for impromptu sharing, works with just drone + phone, easy to use."},
                {"title": "Quick Transfer Cons", "color": "text-red-400", "desc": "Still slower than SD card reader, drains drone battery, limited range (must be close to drone), uses drone Wi-Fi which can drain battery faster, not available on all older DJI models."},
            ], 2) +
            alert("warning", "battery-charging", "Watch your drone battery", "Quick Transfer uses the drone's battery to power the Wi-Fi radio. If you just finished flying and the battery is low, transferring a lot of files might drain it completely. Keep an eye on the battery level during transfer. It is best to do Quick Transfer when the battery still has 20%+ charge."),
        },
        {
            "id": "usb-cable",
            "title": "USB-C Cable Transfer",
            "content": p("You can connect your drone directly to your phone with a USB-C cable for faster wired transfer. This method is less common but works well if you have the right cable.") +
            step_grid([
                {"title": "How to Transfer via USB-C", "desc": "1) Turn on the drone. 2) Connect a USB-C cable from the drone's USB-C port to your phone (you may need an adapter if your phone has Lightning or a different port). 3) On your phone, you may see a prompt to allow the USB connection — tap Allow. 4) The drone's SD card should show up as external storage on your phone. 5) Use your phone's file manager to browse and copy photos/videos to your phone. 6) Eject properly when done before disconnecting the cable."},
                {"title": "What You Need", "desc": "For Android phones with USB-C: a simple USB-C to USB-C cable works. For iPhones with Lightning: you need a Lightning to USB-C camera adapter (Apple's official one or a MFi-certified third-party adapter). The quality of the cable and adapter matters — cheap adapters may not work reliably or may only support USB 2.0 speeds. For best results, use the cable that came with the drone or a high-quality USB 3.x cable."},
            ], "green") +
            specs_table(
                ["Connection Type", "Speed", "Notes"],
                [
                    ["<strong>USB-C to USB-C (Android)</strong>", "20-50 MB/s", "Fast and simple — if both ports support USB 3.x"],
                    ["<strong>Lightning to USB-C (iPhone)</strong>", "10-30 MB/s", "Requires Apple adapter, Lightning is slower than USB-C"],
                    ["<strong>USB 2.0 cable</strong>", "5-10 MB/s", "Slow — similar to wireless, avoid if possible"],
                    ["<strong>USB 3.1/3.2 cable</strong>", "50-100+ MB/s", "Very fast — if both drone and phone support it"],
                ]
            ) +
            alert("info", "cable", "Cable quality matters", "Not all USB-C cables are created equal. Some cheap USB-C cables only support USB 2.0 speeds (480 Mbps = ~60 MB/s theoretical, ~20-40 MB/s real). For fast transfer, make sure you have a cable rated for USB 3.0, 3.1, or 3.2 (5-10+ Gbps). The cable that came with your drone should work — most DJI drones include a decent USB-C cable.")
        },
        {
            "id": "sd-card-reader",
            "title": "SD Card Reader (Fastest Method)",
            "content": p("The absolute fastest way to get photos and videos onto your phone is to take the SD card out of the drone and use a card reader that plugs directly into your phone. This is the professional's choice for transferring large amounts of footage quickly.") +
            step_grid([
                {"title": "How to Use an SD Card Reader", "desc": "1) Turn off the drone and remove the microSD card (push in gently until it clicks, then pull out). 2) Insert the microSD card into the card reader. 3) Plug the card reader into your phone's charging port (Lightning or USB-C). 4) On iPhone: the Photos app should open automatically or you can use the Files app. On Android: use your file manager app. 5) Browse the DCIM folder on the card. 6) Copy or move the files you want to your phone's internal storage. 7) Eject the card properly before removing it, then put it back in the drone."},
                {"title": "Choosing the Right Card Reader", "desc": "For iPhone: get an Apple Lightning to SD Card Camera Reader (the official one works best) or a MFi-certified third-party reader. For Android: any USB-C microSD card reader should work — look for USB 3.0/3.1 for speed. Some card readers have both Lightning and USB-C connectors — these are great if you switch between devices. Avoid the cheapest no-name readers — they can be slow or unreliable. SanDisk, Anker, and other reputable brands make good ones."},
            ], "yellow") +
            specs_table(
                ["Card Reader Type", "Transfer Speed (approx)", "Time for 1GB Video", "Cost"],
                [
                    ["<strong>UHS-I reader (USB 3.0)</strong>", "50-90 MB/s", "12-20 seconds", "$10-$20"],
                    ["<strong>UHS-II reader (USB 3.1)</strong>", "100-200+ MB/s", "5-10 seconds", "$20-$40"],
                    ["<strong>Lightning reader (Apple)</strong>", "30-60 MB/s", "20-35 seconds", "$25-$35"],
                    ["<strong>USB 2.0 reader (avoid)</strong>", "10-20 MB/s", "50-100 seconds", "$5-$10"],
                ]
            ) +
            alert("success", "zap", "SD card readers are worth the investment", "If you transfer files frequently or shoot a lot of 4K video, a good SD card reader is one of the best $15-$30 accessories you can buy. The time savings add up quickly. Instead of waiting 5-10 minutes to transfer a flight's worth of 4K video wirelessly, you can do it in 30-60 seconds with a card reader. Plus, it does not drain the drone's battery.")
        },
        {
            "id": "file-formats",
            "title": "File Formats & What They Mean",
            "content": p("DJI drones shoot photos and videos in several different formats. Understanding these helps you know what to expect when transferring and editing:") +
            specs_table(
                ["Format", "Extension", "Quality", "File Size", "Best For"],
                [
                    ["<strong>JPEG</strong>", ".jpg", "Good (compressed)", "Small (3-15 MB)", "Sharing, social media, quick edits"],
                    ["<strong>RAW / DNG</strong>", ".dng", "Excellent (uncompressed)", "Large (20-50 MB)", "Professional editing, maximum quality"],
                    ["<strong>MP4 (H.264)</strong>", ".mp4", "Good", "Medium", "Most video, easy sharing"],
                    ["<strong>MP4 (H.265/HEVC)</strong>", ".mp4", "Better quality per bit", "Smaller than H.264", "High-quality 4K video"],
                    ["<strong>MOV (ProRes)</strong>", ".mov", "Excellent", "Very large", "Professional video editing"],
                    ["<strong>Slow Motion</strong>", ".mp4/.mov", "Varies", "Large", "Creative slow-mo shots"],
                    ["<strong>Hyperlapse</strong>", ".mp4/.jpg", "Good", "Small-medium", "Time-lapse videos"],
                    ["<strong>Panorama</strong>", ".jpg/.dng", "Good", "Medium", "Wide panoramic shots"],
                ]
            ) +
            grid_cards([
                {"title": "RAW vs JPEG for Photos", "color": "text-yellow-400", "desc": "JPEG files are processed in-camera — they look good right away and are ready to share, but you have less flexibility for editing. RAW (DNG) files contain all the raw sensor data — they look flat and gray straight out of the camera, but you can adjust exposure, white balance, and colors much more aggressively in editing without losing quality. If you edit your photos, shoot RAW. If you just want to share to social media, JPEG is fine."},
                {"title": "Video Codecs Explained", "color": "text-blue-400", "desc": "H.264 is the most common and widely compatible video format — it works on everything. H.265 (HEVC) is newer and more efficient — same quality at about half the file size, or better quality at the same size. H.265 is standard on most newer DJI drones. ProRes is a professional editing format used in higher-end drones (Mavic 3 Pro, Air 3 with certain modes) — it produces huge files but is easier to edit smoothly."},
            ], 2)
        },
        {
            "id": "editing-tips",
            "title": "Editing Tips on Your Phone",
            "content": p("Once your photos and videos are on your phone, you might want to edit them before sharing. Here are the best mobile apps and tips:") +
            specs_table(
                ["App", "Platform", "Best For", "Price"],
                [
                    ["<strong>Lightroom Mobile</strong>", "iOS + Android", "Photo editing (RAW & JPEG)", "Free / $4.99/month premium"],
                    ["<strong>Snapseed</strong>", "iOS + Android", "Powerful free photo editor", "Free"],
                    ["<strong>VSCO</strong>", "iOS + Android", "Filters & film presets", "Free / $19.99/year"],
                    ["<strong>CapCut</strong>", "iOS + Android", "Video editing (free, powerful)", "Free"],
                    ["<strong>DJI Fly editor</strong>", "iOS + Android", "Quick drone video edits", "Free (built-in)"],
                    ["<strong>Adobe Premiere Rush</strong>", "iOS + Android", "Mobile video editing", "Free / $9.99/month"],
                    ["<strong>LumaFusion</strong>", "iOS", "Professional mobile video editing", "$29.99 one-time"],
                ]
            ) +
            step_grid([
                {"title": "Quick Photo Editing Workflow", "desc": "1) Import your photo into Lightroom Mobile or Snapseed. 2) Adjust exposure and contrast to get the brightness right. 3) Tweak white balance if needed (warmer or cooler). 4) Add a little clarity or dehaze to make it pop (subtle is better). 5) Adjust colors (vibrance/saturation) to taste. 6) Crop and straighten for composition. 7) Export at full resolution for sharing. The whole process takes 1-2 minutes with practice."},
                {"title": "Quick Video Editing Tips", "desc": "1) Use CapCut or the DJI Fly built-in editor for quick videos. 2) Trim the boring parts — keep the best 10-30 seconds. 3) Add music (use royalty-free music from the app's library). 4) Add transitions between clips (keep them subtle). 5) Add text overlays if you want. 6) Use filters sparingly — a little goes a long way. 7) Export in 1080p or 4K depending on where you are sharing. The DJI Fly app has templates specifically for drone footage that make it super easy."},
            ], "purple")
        },
        {
            "id": "troubleshooting",
            "title": "Troubleshooting Transfer Issues",
            "content": p("Transfer problems are common. Here are the most frequent issues and how to fix them:") +
            specs_table(
                ["Problem", "Possible Cause", "Fix"],
                [
                    ["<strong>Transfer is very slow</strong>", "Weak Wi-Fi signal, interference, distance", "Move phone closer to controller/drone, use 5GHz Wi-Fi, use SD card reader instead"],
                    ["<strong>Files won't download</strong>", "App glitch, connection issue, corrupt file", "Restart app, reconnect, try different transfer method"],
                    ["<strong>Photos won't save to gallery</strong>", "Permission issue, app setting, storage full", "Check app permissions, check phone storage, save from Files app"],
                    ["<strong>Quick Transfer not working</strong>", "Drone Wi-Fi off, app not updated, Wi-Fi issue", "Restart drone, update app, forget network and reconnect"],
                    ["<strong>SD card not recognized</strong>", "Dirty contacts, wrong format, card reader issue", "Clean contacts, reformat card, try different reader"],
                    ["<strong>Video is choppy on phone</strong>", "Phone too slow, video too high res, codec issue", "Use optimized download, use different video player app"],
                    ["<strong>Missing photos/videos</strong>", "Wrong folder, hidden files, card corruption", "Check DCIM folder, check both internal and SD storage, recover files"],
                ]
            ) +
            step_grid([
                {"title": "General Troubleshooting Steps", "desc": "1) Restart the DJI Fly app. 2) Turn off and on the drone and controller. 3) Turn Wi-Fi off and on on your phone. 4) Forget the drone/controller Wi-Fi network and reconnect. 5) Make sure both DJI Fly and the drone firmware are up to date. 6) Try a different transfer method (e.g., if wireless fails, try SD card reader). 7) Restart your phone. 90% of transfer issues are solved with simple restarts and reconnections."},
            ], "red") +
            alert("warning", "database", "Always back up your files", "Never delete files from the SD card until you have confirmed they are safely transferred and backed up. It is heartbreaking to delete photos only to realize the transfer failed or got corrupted. Keep files on the SD card until you have copied them to at least two locations (phone + computer, or phone + cloud backup). The 3-2-1 backup rule applies to drone footage too: 3 copies, on 2 different media, 1 offsite.")
        },
    ],
    "faqs": [
        {"q": "How do I transfer photos from DJI drone to my phone?", "a": "There are four main ways: 1) Wireless download through the DJI Fly app (most convenient, no extra hardware). 2) Quick Transfer — direct Wi-Fi from drone to phone without the controller. 3) USB-C cable — connect the drone directly to your phone with a cable. 4) SD card reader — remove the SD card and use a card reader that plugs into your phone (fastest method). The best method depends on how many files you have and how fast you need them. For a few quick photos, wireless is fine. For lots of 4K video, use an SD card reader."},
        {"q": "Why is my DJI photo transfer so slow?", "a": "Wireless transfer speed depends on Wi-Fi signal strength, distance between phone and controller/drone, Wi-Fi interference from other devices, and the file size. To speed it up: keep your phone close to the controller, reduce the distance to the drone, switch to 5GHz Wi-Fi if available, avoid areas with lots of Wi-Fi interference, or use a wired method (USB cable or SD card reader) which is much faster. Transferring 4K video wirelessly can be slow — consider using an SD card reader for large video files."},
        {"q": "What is DJI Quick Transfer?", "a": "Quick Transfer is a DJI feature that lets you transfer photos and videos directly from the drone to your phone without needing the remote controller. The drone creates its own Wi-Fi network that your phone connects to directly. It is useful for quickly sharing photos without setting up the whole rig, or when the controller battery is dead. To use it: turn on the drone, connect your phone to the drone's Wi-Fi network, open DJI Fly, and browse the media. It works best within about 10-30 meters."},
        {"q": "Where do DJI photos save on my phone?", "a": "On iPhones: downloaded photos usually save to the Photos app (your camera roll), or you can find them in the Files app under 'DJI Fly' or 'On My iPhone'. On Android: photos typically save to the 'DJI' or 'DJI Fly' folder in your internal storage, and may also appear in your Gallery app. You can change the save location in the DJI Fly app settings on some devices. If you cannot find downloaded photos, check both the DJI app's internal storage and your phone's gallery."},
        {"q": "Can I transfer RAW photos to my phone?", "a": "Yes — you can download RAW (DNG) files to your phone using any transfer method. However, not all phone gallery apps can display RAW photos properly. To view and edit RAW files on your phone, use an app like Adobe Lightroom Mobile, Snapseed, or another RAW-capable photo editor. RAW files are larger (20-50 MB each vs 3-15 MB for JPEG), so they take longer to transfer and use more storage on your phone."},
        {"q": "Why are my drone photos not showing up in my gallery?", "a": "If you downloaded photos from DJI Fly but they do not appear in your phone's gallery, try these fixes: 1) Restart your phone — sometimes the gallery app needs to rescan for new files. 2) Check if the photos saved to the DJI Fly app's internal storage instead of the phone's public storage. 3) Make sure DJI Fly has permission to access your phone's storage/photos. 4) Try downloading again with the 'Save to Album' option enabled. 5) Use your phone's file manager to manually move the files to the DCIM or Pictures folder."},
        {"q": "What is the fastest way to transfer drone videos?", "a": "The fastest way is to remove the microSD card from the drone and use an SD card reader that plugs into your phone. A good UHS-I USB 3.0 card reader can transfer at 50-90 MB/s — a 1GB 4K video takes only 12-20 seconds. UHS-II readers are even faster (100+ MB/s). USB cable transfer is the next fastest (20-50 MB/s), then Quick Transfer, then regular wireless through the controller (2-10 MB/s). For short video clips, wireless is fine. For long 4K videos, definitely use a card reader."},
        {"q": "Do I need internet to transfer DJI photos?", "a": "No — you do not need internet or cellular service to transfer photos from your drone to your phone. All transfer methods (wireless through app, Quick Transfer, USB cable, SD card reader) work completely offline. The DJI Fly app does not need internet to download from the drone — the connection is directly between your phone and the drone/controller. This is great for flying in remote areas with no cell service."},
        {"q": "How do I transfer 4K video to my phone?", "a": "4K video files are large (200-500 MB per minute), so transfer method matters. You can transfer 4K video wirelessly through DJI Fly, but it will be slow (several minutes per minute of video). For faster transfer, use an SD card reader — it is 5-20x faster than wireless. When downloading through the app, make sure to choose 'Original' quality, not 'Optimized', if you want the full 4K resolution. Optimized downloads are lower resolution and smaller file size but not true 4K."},
        {"q": "Can I edit drone photos on my phone?", "a": "Absolutely — modern phones are very capable for photo and video editing. For photos: Adobe Lightroom Mobile is the most powerful (works with RAW files too), Snapseed is excellent and free, VSCO is great for filters. For videos: CapCut is free and surprisingly powerful, the built-in DJI Fly editor is great for quick drone videos, LumaFusion (iOS) is professional-grade. Many drone photographers edit and post entirely from their phone — you do not need a computer anymore."},
    ],
    "related": drone_related(),
}

# =================== PAGE 16: FAA LICENSE / UNDER 250G ===================

page16 = {
    "filename": "dji-mini-drone-under-250g-license-requirements.html",
    "title": "DJI Mini Drone Under 250g: Do I Need a License? (FAA 2026)",
    "headline": "DJI Mini Drone Under 250g: Do I Need a License? (FAA 2026)",
    "meta_desc": "Do you need a license or certification for a DJI Mini drone under 250g? Complete FAA rules guide covering recreational vs commercial use, registration requirements, Remote ID, no-fly zones, and state/local laws.",
    "category": "Drones",
    "category_link": "drones.html",
    "breadcrumb_title": "FAA License Requirements",
    "hero_blur": "bg-blue-500/5",
    "hero_badges": '''<div class="px-3 py-1.5 bg-blue-500/20 text-blue-400 font-mono font-bold text-sm rounded-md border border-blue-500/30">FAA&nbsp;RULES</div>
        <span class="badge badge-info"><i data-lucide="scale" style="width:0.75rem;height:0.75rem"></i>Under 250g</span>
        <span class="badge badge-info"><i data-lucide="file-check" style="width:0.75rem;height:0.75rem"></i>2026 Update</span>''',
    "h1": 'DJI Mini Drone Under 250g: Do I Need a License? &mdash; <span class="gradient-text">FAA Guide 2026</span>',
    "hero_desc": "One of the biggest advantages of DJI Mini drones (under 250 grams) is that they have fewer FAA regulations than heavier drones. But 'fewer' does not mean 'none' — there are still important rules you need to follow. Do you need a license? Do you need to register? What about Remote ID? Can you fly anywhere? In this guide, we break down the exact FAA rules for sub-250g drones in 2026, both recreational and commercial, plus state and local laws, no-fly zones, and international rules.",
    "hero_stats": f'''<div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="gamepad-2" style="width:0.9rem;height:0.9rem"></i>Recreational</div>
          <div class="font-mono font-bold text-xl text-green-400">No Part 107 needed</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="briefcase" style="width:0.9rem;height:0.9rem"></i>Commercial</div>
          <div class="font-bold text-xl text-yellow-400">Part 107 required</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="user" style="width:0.9rem;height:0.9rem"></i>Registration</div>
          <div class="font-mono font-bold text-xl text-blue-400">Recreational: no</div>
        </div>
        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="radio" style="width:0.9rem;height:0.9rem"></i>Remote ID</div>
          <div class="font-bold text-xl text-purple-400">Required (DJI has it)</div>
        </div>''',
    "qa_gradient": "from-blue-950/20 to-navy-900 border-blue-500/20",
    "qa_icon_color": "#60a5fa",
    "qa_title": "Do You Need a License for Under 250g?",
    "qa_text": '<strong class="text-white">For recreational (hobby) use of a drone under 250g: No, you do NOT need a Part 107 Remote Pilot Certificate (drone license) in the United States. You also do NOT need to register your drone with the FAA.</strong> However, you still must follow the FAA\'s recreational flyer rules: fly only for fun, keep the drone within visual line of sight, fly under 400 feet above ground level, yield right of way to manned aircraft, do not fly over people or moving vehicles, do not fly in restricted airspace without authorization, and do not fly under the influence of drugs or alcohol. For commercial use (any flight where you get paid, or that furthers a business), you DO need a Part 107 license AND you must register your drone — even if it is under 250g.',
    "qa_extra": f'''<div class="grid md:grid-cols-2 gap-3 mt-4">
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-green-400 font-semibold mb-1">Recreational (Hobby)</div>
          <p class="text-sm text-gray-300">No license, no registration, must follow safety rules, must have Remote ID</p>
        </div>
        <div class="bg-navy-900/60 border border-white/10 rounded-xl p-4">
          <div class="text-yellow-400 font-semibold mb-1">Commercial (Work)</div>
          <p class="text-sm text-gray-300">Part 107 license required, registration required, all Part 107 rules apply</p>
        </div>
      </div>''',
    "sections": [
        {
            "id": "faa-recreational-rules",
            "title": "FAA Recreational Rules for Sub-250g Drones",
            "content": p("If you fly your Mini drone purely for fun and hobby (recreational use), here are the exact FAA rules as of 2026:") +
            '<div class="space-y-3">' +
            grid_cards([
                {"title": "No Part 107 License Needed", "color": "text-green-400", "desc": "Good news — recreational pilots of sub-250g drones do not need a Remote Pilot Certificate (Part 107 license). You can fly without taking any test or getting any certification from the FAA. This is the biggest benefit of drones under 250g."},
                {"title": "No FAA Registration Required", "color": "text-green-400", "desc": "Drones under 250g flown recreationally do NOT need to be registered with the FAA. You do not need to mark your drone with a registration number. You do not need to pay the $5 registration fee. This is a significant difference from drones weighing 250g or more, which must be registered."},
                {"title": "Remote ID Required", "color": "text-yellow-400", "desc": "Even under-250g recreational drones must have Remote ID as of March 2024 (the final compliance date). The good news: all recent DJI Mini drones (Mini 2 SE, Mini 3, Mini 4 Pro, Mini 5 Pro, etc.) come with built-in Remote ID from the factory, so no extra hardware is needed. Just make sure your firmware is up to date."},
                {"title": "Fly Within Visual Line of Sight", "color": "text-blue-400", "desc": "You must be able to see your drone with your own eyes at all times during flight — no binoculars, no FPV goggles for the whole flight, no flying behind trees or buildings where you cannot see it. This is a safety rule to avoid collisions with manned aircraft and other obstacles."},
                {"title": "Fly Under 400 Feet Above Ground", "color": "text-blue-400", "desc": "Recreational drones must stay below 400 feet above ground level (AGL). This is to stay clear of manned aircraft, which generally fly above 500 feet. If you are flying near a tall structure, you can fly up to 400 feet above that structure as long as you stay within a 400-foot radius of it."},
                {"title": "No Flying in Restricted Airspace", "color": "text-red-400", "desc": "You cannot fly in restricted airspace (near airports, military bases, national parks, etc.) without prior authorization. Use the FAA's B4UFLY app or DJI Fly's geofencing system to check where you can fly. For controlled airspace near airports, you can get quick LAANC authorization through DJI Fly or other apps — it is usually instant."},
                {"title": "Yield to Manned Aircraft", "color": "text-red-400", "desc": "Drones must always yield the right of way to manned aircraft (airplanes, helicopters, gliders, etc.). If you see an aircraft, land immediately or move out of the way. Never fly near airports, helipads, or flight paths. This is both a rule and common sense — a collision could be catastrophic."},
                {"title": "No Flying Over People or Moving Vehicles", "color": "text-red-400", "desc": "Recreational drones (even under 250g) cannot fly over people who are not directly participating in the flight, and cannot fly over moving vehicles. You can fly over your own property and people who are with you and consenting, but not over random bystanders or traffic."},
                {"title": "No Flying Under the Influence", "color": "text-red-400", "desc": "Just like driving, you cannot fly a drone while under the influence of alcohol or drugs. The FAA takes this seriously — impairment affects your judgment and reaction time, making dangerous situations more likely. Save the celebration for after you land safely."},
                {"title": "No Careless or Reckless Operation", "color": "text-red-400", "desc": "This is a catch-all rule: you cannot operate your drone in a careless or reckless manner that endangers people or property. Use common sense. If something seems dangerous or stupid, do not do it. Penalties for reckless operation can be severe — fines, criminal charges, or both."},
            ], 2) +
            "</div>" +
            alert("info", "book-open", "The Recreational UAS Safety Test (TRUST)", "While recreational sub-250g drone pilots are not required to take TRUST (The Recreational UAS Safety Test), the FAA strongly recommends it. TRUST is a free, online test that teaches you the basic safety rules. It takes about 30 minutes and gives you a certificate. It is not required for under-250g, but it is a good idea and is required for recreational pilots of drones 250g and over.")
        },
        {
            "id": "commercial-rules",
            "title": "Commercial Use Rules (Even Under 250g)",
            "content": p("Important: if you use your drone for ANY commercial purpose, different rules apply — even if the drone is under 250g. Commercial use includes anything that makes money or furthers a business.") +
            step_grid([
                {"title": "What Counts as Commercial Use?", "desc": "It is not just getting paid directly to fly. The FAA considers ALL of these commercial use: getting paid to take photos/videos with your drone, real estate photography (even if you are a real estate agent doing your own listings), construction site monitoring for your job, marketing photos for your business, YouTube videos that earn ad revenue, sponsored content, anything you do in connection with your job or business. When in doubt, assume it is commercial and get your Part 107."},
                {"title": "Part 107 License Required", "desc": "For commercial use, you MUST have a Part 107 Remote Pilot Certificate, even for drones under 250g. To get it: you must be at least 16 years old, pass an aeronautical knowledge test at an FAA-approved testing center (or online as of recent rules), pass a TSA security background check, and register with the FAA. The test costs about $175 and is valid for 24 months."},
                {"title": "Registration Required", "desc": "Commercially operated drones MUST be registered with the FAA, regardless of weight — even if they are under 250g. The registration costs $5 per drone and is valid for 3 years. You must mark your drone with your registration number. You also need to carry your registration certificate and Part 107 certificate with you when flying (digital copies are fine)."},
                {"title": "All Part 107 Rules Apply", "desc": "When flying commercially, you must follow all Part 107 rules: fly under 400 feet AGL, visual line of sight, daytime only (or twilight with anti-collision lights), no flying over people (unless you have a waiver and the drone meets Category requirements), no flying from a moving vehicle (unless in a sparsely populated area), maximum ground speed of 100 mph, yield right of way to manned aircraft, and more."},
            ], "yellow") +
            alert("warning", "scale", "Penalties for flying commercially without a license", "Flying a drone commercially without a Part 107 certificate can result in FAA fines of $1,000-$30,000+ per violation, depending on the severity. It is not worth the risk. If you want to make money with your drone — even a little money — get your Part 107. The test is not that hard, the cost is reasonable, and it opens up many opportunities.")
        },
        {
            "id": "remote-id",
            "title": "Remote ID Requirements",
            "content": p("Remote ID is like a digital license plate for drones. It broadcasts the drone's location, the pilot's location, and identification information, so that authorities and others can identify who is flying. Here is what you need to know:") +
            specs_table(
                ["Aspect", "Details"],
                [
                    ["<strong>Compliance Deadline</strong>", "March 16, 2024 — now in effect"],
                    ["<strong>Who needs it?</strong>", "Almost all drones, including sub-250g recreational drones"],
                    ["<strong>What it broadcasts</strong>", "Drone ID, location/altitude of drone, location/altitude of pilot, takeoff point, time, emergency status"],
                    ["<strong>Range</strong>", "Broadcast can be received from ~1-2 miles away by properly equipped receivers"],
                    ["<strong>DJI drones</strong>", "All recent DJI drones have built-in Remote ID via firmware update — no extra hardware needed"],
                    ["<strong>Exceptions</strong>", "Indoor flight, some model aircraft, operations in FRIAs (FAA-Recognized Identification Areas)"],
                ]
            ) +
            step_grid([
                {"title": "DJI Drones & Remote ID", "desc": "Good news: all recent DJI Mini drones (Mini 2, Mini 2 SE, Mini 3, Mini 3 Pro, Mini 4 Pro, Mini 5 Pro, etc.) support Remote ID through a firmware update. DJI started rolling out Remote ID firmware in 2022-2023. As long as your drone's firmware is up to date, it should be broadcasting Remote ID automatically. You do not need to buy any extra modules. You can verify Remote ID is working in the DJI Fly app settings."},
                {"title": "Your Privacy Concerns", "desc": "Remote ID broadcasts the pilot's location (the takeoff point / controller location), which makes some people uncomfortable. However: only authorized parties (law enforcement, FAA) with the right equipment can receive and decode the signal. It does not broadcast your name, phone number, or address — just an ID number. The system is designed for safety, not surveillance. If you have strong privacy concerns, you can fly in FRIA areas where Remote ID is not required, or fly indoors."},
            ], "purple")
        },
        {
            "id": "no-fly-zones",
            "title": "No-Fly Zones & Airspace Restrictions",
            "content": p("Even with a sub-250g drone, you cannot fly everywhere. There are many types of restricted airspace and locations where flying is prohibited or limited:") +
            specs_table(
                ["Restricted Area", "Can You Fly?", "How to Get Permission"],
                [
                    ["<strong>Class B/C/D/E airspace (near airports)</strong>", "Only with authorization", "LAANC (instant via DJI Fly / apps), or FAA DroneZone"],
                    ["<strong>Class G (uncontrolled) airspace</strong>", "Yes — under 400 ft", "No permission needed for recreational"],
                    ["<strong>National Parks</strong>", "Generally no", "Very limited, hard to get permits"],
                    ["<strong>Military bases / restricted areas</strong>", "No", "Very difficult — not recommended"],
                    ["<strong>Washington DC Special Flight Rules Area</strong>", "Strictly no", "Extremely limited — not recreational"],
                    ["<strong>Stadiums / events (large crowds)</strong>", "Temporarily restricted", "Generally no for recreational"],
                    ["<strong>Wildfires / emergency areas</strong>", "No — stay far away", "Absolutely no — you interfere with firefighting"],
                    ["<strong>Over people / moving vehicles</strong>", "Generally no (recreational)", "No easy way for recreational — just avoid"],
                ]
            ) +
            grid_cards([
                {"title": "Using DJI Fly Geofencing", "color": "text-blue-400", "desc": "DJI drones have built-in geofencing (GEO system) that prevents takeoff in restricted areas and warns you about airspace. The DJI Fly app shows you zone boundaries on the map. Green zones = safe to fly. Yellow zones = warning, use caution. Red zones = no fly, takeoff locked. You can unlock some yellow/orange zones through DJI's unlocking system if you have authorization."},
                {"title": "LAANC Authorization", "color": "text-green-400", "desc": "LAANC (Low Altitude Authorization and Notification Capability) lets you get near-instant approval to fly in controlled airspace (around airports). You can request LAANC authorization directly through DJI Fly or other approved apps. For recreational pilots, LAANC is free and usually approved instantly up to certain altitudes (often 200-400 ft depending on the airport)."},
            ], 2) +
            alert("critical", "siren", "Never interfere with emergency response", "If there is a wildfire, hurricane, search and rescue operation, or other emergency — stay far away with your drone. Drones interfere with firefighting aircraft and rescue operations, and can make the situation worse. Flying a drone near an emergency can delay rescue efforts and put lives at risk. It is also illegal and can result in huge fines — up to $20,000+ for interfering with wildfire operations. Just don't do it.")
        },
        {
            "id": "state-local-laws",
            "title": "State & Local Laws",
            "content": p("FAA rules are federal and apply everywhere in the US, but state and local governments can also have their own drone laws. These vary a lot by location.") +
            step_grid([
                {"title": "Common State & Local Restrictions", "desc": "Common state and local drone laws include: no flying over private property without permission (trespassing), no flying in certain city parks or nature reserves, privacy laws (no photographing people without consent in certain situations), local registration requirements (rare, but some cities have them), noise ordinances (drones can be noisy), curfews (no night flying in some areas), drone-free zones at beaches, festivals, etc."},
                {"title": "How to Check Local Laws", "desc": "1) Check your city or county government website for drone ordinances. 2) Check state-level drone laws (many state aviation or transportation departments have summaries). 3) Use the FAA's B4UFLY app or AirMap for information about local restrictions. 4) Check with the specific park or location you want to fly in — many state parks and city parks have their own rules. 5) When in doubt, ask permission or find a different spot."},
                {"title": "Privacy Concerns", "desc": "Privacy is a big issue with drones. Laws vary by state, but as a general rule: do not fly over people's yards and look into their windows. Do not photograph or record people without their consent when they have a reasonable expectation of privacy (their backyard, inside their home, etc.). Just because you can fly somewhere does not mean you should. Be respectful and use common sense. Peeping Toms with drones can face criminal charges in many states."},
            ], "orange") +
            alert("info", "landmark", "Federal vs state — who wins?", "The FAA has authority over all airspace in the United States — this has been repeatedly confirmed by courts. States and cities cannot regulate airspace or create their own aviation rules. However, states CAN make laws about privacy, trespassing, land use, and public safety — and these can effectively restrict where you can take off and land. So even if the FAA says you can fly, a local park ban means you cannot take off from that park.")
        },
        {
            "id": "international-rules",
            "title": "International Rules (Outside the USA)",
            "content": p("If you are not in the United States, the rules are different. Here is a quick overview of how other countries handle sub-250g drones:") +
            specs_table(
                ["Country / Region", "Under 250g Rules", "License Needed?", "Registration?"],
                [
                    ["<strong>Canada (Transport Canada)</strong>", "Basic rules apply, fewer restrictions", "No basic pilot cert if recreational", "Yes — all drones 250g-25kg; sub-250g no"],
                    ["<strong>UK (CAA)</strong>", "Flyer ID required, basic rules", "Flyer ID + Operator ID needed", "Operator ID required"],
                    ["<strong>EU (EASA)</strong>", 'Open category "class" system', "No license for Open category sub-250g", "Some countries require registration"],
                    ["<strong>Australia (CASA)", 'D]', "Basic rules apply", "No license for recreational sub-250g", "Yes — must register all drones"],
                    ["<strong>Japan</strong>", "Some restrictions in populated areas", "No license for sub-200g", "Not required for sub-200g"],
                    ["<strong>China (CAAC)</strong>", "Real-name registration required", "License for commercial/heavy", "Real-name registration for all"],
                ]
            ) +
            p("These are general summaries — always check the specific rules of the country you are flying in before you fly. Rules change frequently, and there can be significant variation even within countries (state/provincial level rules).") +
            alert("warning", "plane", "Traveling with your drone internationally?", "If you are bringing your drone on vacation or a trip abroad: 1) Check the destination country's drone laws — some countries ban drones entirely or require permits. 2) Check airline rules for carrying drones on planes (usually fine in carry-on, batteries must be in carry-on). 3) Check customs — some countries require you to declare drones on arrival. 4) Do not fly near airports, military bases, or government buildings — this is illegal everywhere. 5) Be respectful and follow local rules — do not be the tourist who gives drone pilots a bad name.")
        },
        {
            "id": "fines-penalties",
            "title": "Fines & Penalties for Violations",
            "content": p("Breaking drone rules can have serious consequences. Here is what you could be facing:") +
            specs_table(
                ["Violation", "Potential Penalty", "Severity"],
                [
                    ["<strong>Flying without Part 107 (commercial)</strong>", "$1,000-$30,000+ per violation", "High"],
                    ["<strong>Flying in restricted airspace</strong>", "$1,000-$5,000+ per violation", "Medium-High"],
                    ["<strong>Flying near wildfires / emergencies</strong>", "$10,000-$20,000+", "Very High"],
                    ["<strong>Reckless / dangerous operation</strong>", "Fines + possible criminal charges", "Very High"],
                    ["<strong>Privacy violations</strong>", "Civil lawsuits + criminal charges in some states", "Medium-High"],
                    ["<strong>No Remote ID</strong>", "Warnings, then fines up to $1,000+", "Medium (enforcement ramping up)"],
                    ["<strong>Unregistered drone (250g+)</strong>", "Up to $25,000 civil penalty", "Medium-High"],
                ]
            ) +
            p("In practice, the FAA typically focuses on education and warnings for first-time minor violations, especially with recreational pilots. But serious or repeated violations can result in very large fines. And criminal charges are possible in cases of reckless endangerment or interfering with aircraft.") +
            alert("success", "shield", "How to Stay Out of Trouble", "It is simple: 1) Know the rules — take a few minutes to learn what is allowed. 2) Use apps like B4UFLY or DJI Fly to check airspace before you fly. 3) Fly safely — use common sense and err on the side of caution. 4) Be respectful of others' privacy and property. 5) When in doubt, don't fly. Most drone pilots never have any run-ins with authorities because they follow the rules and use good judgment.")
        },
    ],
    "faqs": [
        {"q": "Do I need a license to fly a DJI Mini under 250g?", "a": "For recreational/hobby use in the United States: No, you do NOT need a Part 107 Remote Pilot Certificate (drone license). You also do not need to register your drone with the FAA. However, you still must follow the FAA's recreational safety rules: keep visual line of sight, fly under 400 feet, yield to manned aircraft, no flying in restricted airspace without permission, no flying over people or moving vehicles, and no reckless operation. For commercial use (any flight for money or business purposes), you DO need a Part 107 license even for sub-250g drones."},
        {"q": "Do I need to register my DJI Mini drone with the FAA?", "a": "If you fly recreationally (only for fun/hobby) and the drone is under 250g: No, you do NOT need to register it with the FAA. This is one of the main benefits of drones under 250g. However, if you use the drone for ANY commercial purpose (work, business, paid photography, YouTube ad revenue, etc.), you MUST register it AND get a Part 107 license, even if it is under 250g. Registration costs $5 and is valid for 3 years."},
        {"q": "What is Remote ID and do I need it for my Mini drone?", "a": "Remote ID is like a digital license plate for drones — it broadcasts the drone's location and ID information. As of March 2024, Remote ID is required for almost all drones in the US, including sub-250g recreational drones. The good news is that all recent DJI Mini drones (Mini 2, Mini 3, Mini 4 Pro, Mini 5 Pro, etc.) have built-in Remote ID support via firmware update. Just make sure your drone's firmware is up to date and it will automatically broadcast Remote ID. No extra hardware is needed."},
        {"q": "Can I fly my Mini drone in a park?", "a": "It depends on the park. National parks: generally no — flying drones in national parks is prohibited by the NPS. State parks: varies — some allow it, some ban it, some require permits. City/county parks: check local ordinances. Even if the FAA says the airspace is fine, the park may have its own rules about taking off and landing on park property. Always check the specific park's rules before flying. When in doubt, ask a park ranger or find a different location."},
        {"q": "How high can I fly a DJI Mini drone?", "a": "For recreational flight, you can fly up to 400 feet above ground level (AGL). If you are flying near a building or structure, you can fly up to 400 feet above the top of that structure as long as you stay within a 400-foot radius of it. For Part 107 commercial flights, the same 400-foot AGL limit applies with the same exception for structures. Always stay well below 500 feet to avoid manned aircraft — that is generally the minimum altitude for planes in most areas."},
        {"q": "Do I need to take the TRUST test for sub-250g drones?", "a": "No — the Recreational UAS Safety Test (TRUST) is required for recreational pilots of drones weighing 250g or more. For drones under 250g flown recreationally, TRUST is not required. However, the FAA strongly recommends it, and it is a good idea anyway. TRUST is free, takes about 30 minutes online, and teaches you the basic safety rules. It never expires once you pass it. Search 'FAA TRUST test' online if you want to take it."},
        {"q": "Can I fly my Mini drone over people?", "a": "Recreational sub-250g drones: generally no, you cannot fly over people who are not participating in the flight or who have not given consent. The FAA's recreational rules prohibit flying over uninvolved people. You can fly over yourself and your friends who are with you and agree to it, but not over random bystanders, crowds, or strangers on the street. For commercial Part 107 operations, flying over people has specific category requirements — even for small drones. When in doubt, just don't fly over people."},
        {"q": "What happens if I get caught flying illegally?", "a": "Consequences depend on the severity of the violation. For minor recreational violations, you will likely get a warning first — the FAA prefers education over punishment for first-time offenders. More serious violations (flying near airports, reckless operation, interfering with aircraft) can result in fines ranging from $1,000 to $30,000+ per violation. In extreme cases of reckless endangerment, there could be criminal charges. Flying near wildfires is especially expensive — fines can be $10,000-$20,000+. Just follow the rules and you will have nothing to worry about."},
        {"q": "Can I fly my Mini drone at night?", "a": "For recreational use: yes, you can fly at night as long as you follow all the other rules (visual line of sight, under 400ft, etc.). However, flying at night is riskier — visibility is worse, obstacles are harder to see, and you might be more likely to lose orientation. Your drone has navigation lights, but they may not be visible from all directions. For Part 107 commercial flights, night flying is allowed as long as you have anti-collision lighting visible for 3 statute miles and you complete the night operations training. Use extra caution when flying at night."},
        {"q": "Is DJI Mini 3/4/5 Pro under 250g?", "a": "The standard DJI Mini 3 (with standard battery) weighs 249g — just under the 250g limit. The Mini 4 Pro with standard battery weighs 249g as well. The Mini 5 Pro with standard battery also comes in at exactly 249g. HOWEVER: if you add accessories (ND filters, propeller guards, landing gear, sticker, etc.), the total weight may exceed 250g. If your drone weighs 250g or more with accessories, the under-250g exceptions no longer apply — you would need to register and follow all rules for 250g+ drones. Be mindful of what you attach."},
    ],
    "related": drone_related(),
}

PAGES = [page15, page16]

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
