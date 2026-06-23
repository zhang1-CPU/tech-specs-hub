#!/usr/bin/env python3
"""
基于调研数据扩展高搜索量页面。
使用数据驱动的模板方法生成分类页面和产品页面。
"""
import os
import json

WORKSPACE = "/workspace"

# ============================================================
# 通用工具函数
# ============================================================

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def get_head_template(depth=2):
    """
    获取页面 head 部分的模板 (从 3d-printers.html 提取模式)
    depth: 相对路径深度 (2 = pages/specs/xxx.html, 1 = pages/xxx.html, 0 = index.html)
    """
    prefix = "../" * depth
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{title}}</title>
  <meta name="description" content="{{description}}">
  <meta name="theme-color" content="#0a1628">
  <!-- Critical Inline CSS: pre-render base styles so first paint is not broken -->
  <style>html,body{{background-color:#0a1628;color:#ffffff;margin:0;padding:0;min-height:100vh;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;line-height:1.5;-webkit-font-smoothing:antialiased}}a{{color:#22d3ee;text-decoration:none}}code,pre{{font-family:ui-monospace,monospace}}</style>

  <!-- Resource Preload Hints -->
  <link rel="preconnect" href="https://cdn.tailwindcss.com">
  <link rel="preconnect" href="https://unpkg.com">
  <link rel="dns-prefetch" href="https://cdn.tailwindcss.com">
  <link rel="dns-prefetch" href="https://unpkg.com">
  <link rel="dns-prefetch" href="https://fonts.gstatic.com">

  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <link rel="canonical" href="{{canonical}}">

  <!-- Open Graph -->
  <meta property="og:title" content="{{title}}">
  <meta property="og:description" content="{{description}}">
  <meta property="og:type" content="WebSite">
  <meta property="og:url" content="{{canonical}}">
  <meta property="og:image" content="https://powerspecshub.com/assets/images/og-default.png">
  <meta property="og:site_name" content="TechSpecsHub">
  <meta property="article:published_time" content="2026-06-23T00:00:00Z">
  <meta property="article:modified_time" content="2026-06-23T00:00:00Z">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{{title}}">
  <meta name="twitter:description" content="{{description}}">
  <meta name="twitter:image" content="https://powerspecshub.com/assets/images/og-default.png">
  <meta name="twitter:site" content="@TechSpecsHub">

  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">

  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
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

  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js" defer></script>
  <link rel="stylesheet" href="{prefix}assets/css/main.css">

  <!-- JSON-LD -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "WebSite",
    "headline": "{{title}}",
    "description": "{{description}}",
    "url": "{{canonical}}",
    "datePublished": "2026-06-23",
    "dateModified": "2026-06-23",
    "publisher": {{
      "@type": "Organization",
      "name": "TechSpecsHub",
      "url": "https://powerspecshub.com/"
    }},
    "mainEntity": {{
      "@type": "WebSite",
      "name": "TechSpecsHub",
      "url": "https://powerspecshub.com/"
    }}
  }}
  </script>

</head>
'''

def get_header_nav(depth=2):
    """获取页头导航"""
    prefix = "../" * depth
    return f'''<body class="bg-navy-950 text-white min-h-screen font-display">

  <!-- HEADER / NAV -->
  <header>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16 gap-4">

        <a href="{prefix}index.html" class="flex items-center gap-2.5 flex-shrink-0">
          <div class="w-9 h-9 bg-gradient-to-br from-electric-400 to-electric-600 rounded-lg flex items-center justify-center shadow-lg shadow-electric-500/20">
            <i data-lucide="cpu" style="width:1.25rem;height:1.25rem;color:#0a1628"></i>
          </div>
          <span class="font-bold text-lg tracking-tight">TechSpecs<span class="gradient-text">Hub</span></span>
        </a>

        <nav class="hidden lg:flex items-center gap-1 text-sm font-medium">
          <div class="nav-dropdown-trigger">
            <button class="flex items-center gap-1.5 px-3 py-2 text-gray-300 hover:text-white rounded-lg hover:bg-white/5 transition-all">
              Categories
              <i data-lucide="chevron-down" style="width:0.875rem;height:0.875rem"></i>
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
              Tools &amp; Data
              <i data-lucide="chevron-down" style="width:0.875rem;height:0.875rem"></i>
            </button>
            <div class="nav-dropdown">
              <p class="nav-dropdown-section-label">Data Resources</p>
              <a href="{prefix}error-code-db.html"><i data-lucide="alert-circle" style="width:1rem;height:1rem;color:#f87171;flex-shrink:0"></i>Error Code Database</a>
              <a href="{prefix}master-specs.html"><i data-lucide="table-2" style="width:1rem;height:1rem;color:#22d3ee;flex-shrink:0"></i>Master Specs Comparison</a>
              <a href="{prefix}brand-index.html"><i data-lucide="building-2" style="width:1rem;height:1rem;color:#22d3ee;flex-shrink:0"></i>Brand Index A&ndash;Z</a>
              <hr class="my-2 border-white/10">
              <p class="nav-dropdown-section-label">Buyer's Guides</p>
              <a href="{prefix}tools/best-multimeters-2026.html"><i data-lucide="wrench" style="width:1rem;height:1rem;color:#fbbf24;flex-shrink:0"></i>Best Multimeters 2026</a>
            </div>
          </div>
          <a href="{prefix}about.html" class="px-3 py-2 text-gray-300 hover:text-white rounded-lg hover:bg-white/5 transition-all">About</a>
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
        <a href="{prefix}error-code-db.html" class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-white/5 text-gray-300 hover:text-white transition-all"><i data-lucide="alert-circle" style="width:1rem;height:1rem;color:#f87171"></i>Error Code Database</a>
        <a href="{prefix}master-specs.html" class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-white/5 text-gray-300 hover:text-white transition-all"><i data-lucide="table-2" style="width:1rem;height:1rem;color:#22d3ee"></i>Master Specs Comparison</a>
        <a href="{prefix}brand-index.html" class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-white/5 text-gray-300 hover:text-white transition-all"><i data-lucide="building-2" style="width:1rem;height:1rem;color:#22d3ee"></i>Brand Index A&ndash;Z</a>
        <a href="{prefix}tools/best-multimeters-2026.html" class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-white/5 text-gray-300 hover:text-white transition-all"><i data-lucide="wrench" style="width:1rem;height:1rem;color:#fbbf24"></i>Best Multimeters 2026</a>
        <hr class="border-white/10 my-2">
        <a href="{prefix}about.html" class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-white/5 text-gray-300 hover:text-white transition-all"><i data-lucide="info" style="width:1rem;height:1rem;color:#22d3ee"></i>About</a>
      </div>
    </div>
  </header>

  <!-- SEARCH MODAL -->
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

def get_footer(depth=2):
    """获取页脚"""
    prefix = "../" * depth
    return f'''
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

  <script src="{prefix}assets/js/main.js" defer></script>

</body>
</html>
'''

def build_breadcrumb(items, depth=2):
    """生成面包屑导航
    items: list of (label, href or None for current)
    """
    prefix = "../" * depth
    parts = []
    for label, href in items:
        if href is None:
            parts.append(f'<span class="breadcrumb-current">{label}</span>')
        else:
            # href 是相对路径，根据 depth 调整
            full_href = href
            parts.append(f'<a href="{full_href}">{label}</a>')
    
    nav_items = ''.join(
        f'{part}<span class="breadcrumb-sep">/</span>' if i < len(parts) - 1 else part
        for i, part in enumerate(parts)
    )
    
    return f'''  <!-- BREADCRUMB -->
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 pb-4">
    <nav class="breadcrumb">
      {nav_items}
    </nav>
  </div>
'''

def build_hero(icon, badge_text, title_highlight, title_rest, description, stats, gradient_pos="left-1/4"):
    """生成 hero 区域
    stats: list of (value, label) tuples, max 4
    """
    stat_cards = "\n".join([f'''        <div class="glass-card p-5">
          <div class="text-2xl font-bold text-electric-400 font-mono">{v}</div>
          <div class="text-xs text-gray-500 mt-1 font-medium">{l}</div>
        </div>''' for v, l in stats])
    
    return f'''  <!-- HERO -->
  <section class="relative pt-6 pb-16">
    <div class="absolute inset-0 pointer-events-none overflow-hidden">
      <div class="absolute top-0 {gradient_pos} w-[400px] h-[400px] bg-electric-500/10 rounded-full blur-3xl"></div>
    </div>
    <div class="relative max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
      <div class="inline-flex items-center gap-2 px-3 py-1.5 bg-electric-500/10 border border-electric-500/30 rounded-full text-xs font-semibold text-electric-400 mb-6 tracking-wide uppercase">
        <i data-lucide="{icon}" style="width:0.85rem;height:0.85rem"></i>
        {badge_text}
      </div>
      <h1 class="font-bold text-4xl md:text-5xl lg:text-6xl mb-6 leading-[1.1] tracking-tight">
        {title_highlight} <span class="gradient-text">{title_rest}</span>
      </h1>
      <p class="text-lg md:text-xl text-gray-400 mb-8 max-w-3xl mx-auto leading-relaxed">
        {description}
      </p>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto mt-10">
{stat_cards}
      </div>
    </div>
  </section>
'''

def build_table_section(title, subtitle, headers, rows, badge_text="OEM Verified"):
    """生成规格对比表
    headers: list of column names
    rows: list of lists (每个子列表是一行数据)
    """
    thead = "".join(f"<th>{h}</th>" for h in headers)
    
    tbody_rows = ""
    for row in rows:
        cells = "".join(f"<td>{c}</td>" for c in row)
        tbody_rows += f"          <tr>{cells}</tr>\n"
    
    return f'''  <!-- TABLE SECTION -->
  <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex items-end justify-between mb-6 flex-wrap gap-3">
      <div>
        <h2 class="font-bold text-2xl md:text-3xl mb-2">{title}</h2>
        <p class="text-gray-400 text-sm">{subtitle}</p>
      </div>
      <span class="badge badge-info"><i data-lucide="check-circle" style="width:0.8rem;height:0.8rem"></i>{badge_text}</span>
    </div>
    <div class="table-scroll">
      <table class="specs-table">
        <thead>
          <tr>
            {thead}
          </tr>
        </thead>
        <tbody>
{tbody_rows.rstrip()}
        </tbody>
      </table>
    </div>
  </section>
'''

def build_feature_cards(title, subtitle, features):
    """生成特性卡片网格
    features: list of (icon, title, description)
    """
    cards = ""
    for icon, ft_title, desc in features:
        cards += f'''      <div class="glass-card p-6">
        <div class="w-12 h-12 bg-electric-500/15 rounded-xl flex items-center justify-center mb-4">
          <i data-lucide="{icon}" style="width:1.5rem;height:1.5rem;color:#22d3ee"></i>
        </div>
        <h3 class="text-lg font-semibold mb-2">{ft_title}</h3>
        <p class="text-gray-400 text-sm leading-relaxed">{desc}</p>
      </div>
'''
    
    return f'''  <!-- FEATURE CARDS -->
  <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="max-w-3xl mx-auto mb-10 text-center">
      <h2 class="font-bold text-3xl md:text-4xl mb-4">{title}</h2>
      <p class="text-gray-400">{subtitle}</p>
    </div>
    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
{cards.rstrip()}
    </div>
  </section>
'''

def build_resource_links(title, subtitle, links):
    """生成资源链接卡片
    links: list of (icon, color, title, description, href)
    """
    cards = ""
    for icon, color, lt_title, desc, href in links:
        cards += f'''      <a href="{href}" class="glass-card p-5 hover:bg-white/5 transition-all group">
        <div class="flex items-start gap-4">
          <div class="w-10 h-10 bg-{color}-500/15 rounded-lg flex items-center justify-center flex-shrink-0">
            <i data-lucide="{icon}" style="width:1.2rem;height:1.2rem;color:var(--tw-color)"></i>
          </div>
          <div class="flex-1">
            <h3 class="font-semibold mb-1 group-hover:text-electric-400 transition-colors">{lt_title}</h3>
            <p class="text-sm text-gray-400">{desc}</p>
          </div>
        </div>
      </a>
'''
    
    return f'''  <!-- RESOURCE LINKS -->
  <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="max-w-3xl mx-auto mb-10 text-center">
      <h2 class="font-bold text-3xl md:text-4xl mb-4">{title}</h2>
      <p class="text-gray-400">{subtitle}</p>
    </div>
    <div class="grid md:grid-cols-2 gap-4">
{cards.rstrip()}
    </div>
  </section>
'''

def build_faq_section(title, subtitle, faqs):
    """生成 FAQ 手风琴
    faqs: list of (question, answer)
    """
    items = ""
    for q, a in faqs:
        items += f'''      <details class="glass-card p-5 group">
        <summary class="cursor-pointer font-semibold flex items-center justify-between gap-4">
          <span>{q}</span>
          <i data-lucide="chevron-down" style="width:1rem;height:1rem" class="text-gray-500 group-open:rotate-180 transition-transform flex-shrink-0"></i>
        </summary>
        <p class="mt-3 text-gray-400 text-sm leading-relaxed">{a}</p>
      </details>
'''
    
    return f'''  <!-- FAQ SECTION -->
  <section class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="text-center mb-10">
      <h2 class="font-bold text-3xl md:text-4xl mb-4">{title}</h2>
      <p class="text-gray-400">{subtitle}</p>
    </div>
    <div class="space-y-3">
{items.rstrip()}
    </div>
  </section>
'''

def build_cta(title, description, buttons):
    """生成 CTA 区域
    buttons: list of (text, href, variant) where variant is primary/secondary/ghost
    """
    btn_html = ""
    for text, href, variant in buttons:
        if variant == "primary":
            btn_html += f'        <a href="{href}" class="inline-flex items-center gap-2 px-5 py-2.5 bg-electric-500 hover:bg-electric-400 text-navy-950 font-semibold rounded-lg transition-all">\n          <i data-lucide="file-text" style="width:1rem;height:1rem"></i>\n          {text}\n        </a>\n'
        elif variant == "secondary":
            btn_html += f'        <a href="{href}" class="inline-flex items-center gap-2 px-5 py-2.5 bg-white/5 hover:bg-white/10 text-white font-medium rounded-lg border border-white/10 transition-all">\n          <i data-lucide="wrench" style="width:1rem;height:1rem"></i>\n          {text}\n        </a>\n'
        else:
            btn_html += f'        <a href="{href}" class="inline-flex items-center gap-2 px-5 py-2.5 text-gray-300 hover:text-white font-medium rounded-lg transition-all">\n          <i data-lucide="arrow-right" style="width:1rem;height:1rem"></i>\n          {text}\n        </a>\n'
    
    return f'''  <!-- CTA SECTION -->
  <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="glass-card p-8 md:p-10 text-center">
      <h2 class="font-bold text-2xl md:text-3xl mb-3">{title}</h2>
      <p class="text-gray-400 mb-6 max-w-2xl mx-auto">{description}</p>
      <div class="flex flex-wrap justify-center gap-3">
{btn_html.rstrip()}
      </div>
    </div>
  </section>
'''

# ============================================================
# 1. Outdoor Power Stations 页面
# ============================================================

def generate_outdoor_power():
    depth = 2
    head = get_head_template(depth).replace("{{title}}", "Outdoor Power Station Specs — EcoFlow, Jackery, Bluetti, Anker, Goal Zero | TechSpecsHub")
    head = head.replace("{{description}}", "Complete specs for portable power stations and solar generators from EcoFlow, Jackery, Bluetti, Anker, and Goal Zero. Battery capacity, inverter output, solar input, cycle life, and error codes.")
    head = head.replace("{{canonical}}", "https://powerspecshub.com/pages/specs/outdoor-power.html")
    
    header = get_header_nav(depth)
    breadcrumb = build_breadcrumb([
        ("Home", "../../index.html"),
        ("Specs", "../error-code-db.html"),
        ("Outdoor Power Stations", None)
    ])
    
    hero = build_hero(
        icon="battery-charging",
        badge_text="Portable Power Category · Updated June 2026",
        title_highlight="Outdoor Power Station",
        title_rest="Specifications",
        description="Complete specs for portable power stations and solar generators from EcoFlow, Jackery, Bluetti, Anker, and Goal Zero. Battery capacity, inverter output, solar input, cycle life, and error codes — all cross-referenced against manufacturer data sheets.",
        stats=[("$4.8B", "Market Size (2025)"), ("12+", "Models Listed"), ("5", "Top Brands"), ("6k+", "Cycles (Best)")],
        gradient_pos="left-1/4"
    )
    
    table = build_table_section(
        title="Portable Power Station Comparison",
        subtitle="LiFePO4 and NMC battery power stations. Scroll horizontally on mobile.",
        headers=["Model", "Capacity (Wh)", "Chemistry", "Output (W)", "Surge (W)", "Solar Input (W)", "Charge Time", "Cycles", "Weight", "UPS", "Price"],
        rows=[
            ['<a href="ecoflow-delta-pro-3.html" class="text-electric-400 hover:text-electric-300 transition-colors font-semibold">EcoFlow Delta Pro 3</a>', '4,096', 'LiFePO4', '4,000', '7,000', '1,600 (MPPT)', '~1.2 hrs', '<span class="text-green-400">4,000</span>', '59.5 lbs', '<span class="text-green-400">Yes (0ms)</span>', '$2,399'],
            ['<span class="font-semibold">Bluetti Apex 300</span>', '2,765 (exp to 58kWh)', 'LiFePO4', '3,840', '7,680', '3,000 (MPPT)', '~1.5 hrs', '<span class="text-green-400">6,000</span>', '55 lbs', '<span class="text-green-400">Yes (0ms)</span>', '$1,999'],
            ['<a href="jackery-explorer-2000-plus.html" class="text-electric-400 hover:text-electric-300 transition-colors font-semibold">Jackery Explorer 2000 Plus</a>', '2,042', 'LiFePO4', '3,000', '6,000', '1,200 (MPPT)', '~2 hrs', '<span class="text-green-400">4,000</span>', '50.7 lbs', '<span class="text-yellow-400">Limited</span>', '$899 (sale)'],
            ['<span class="font-semibold">Jackery Explorer 1000 V2</span>', '1,070', 'LiFePO4', '1,500', '3,000', '500 (MPPT)', '~1.7 hrs', '<span class="text-green-400">4,000</span>', '23.8 lbs', '<span class="text-red-400">No</span>', '$429–$499'],
            ['<span class="font-semibold">EcoFlow Delta 3</span>', '1,024', 'LiFePO4', '1,800', '2,700', '500 (MPPT)', '56 min', '<span class="text-green-400">3,500</span>', '23.6 lbs', '<span class="text-green-400">Yes</span>', '$490–$599'],
            ['<span class="font-semibold">Anker Solix C1000</span>', '1,056', 'LiFePO4', '1,800', '2,400', '400 (MPPT)', '58 min', '<span class="text-green-400">3,000</span>', '26.9 lbs', '<span class="text-green-400">Yes</span>', '$430–$499'],
            ['<span class="font-semibold">Bluetti Elite 200 V2</span>', '1,843', 'LiFePO4', '2,400', '4,800', '600 (MPPT)', '~2 hrs', '<span class="text-green-400">6,000</span>', '42 lbs', '<span class="text-green-400">Yes</span>', '$1,099'],
            ['<a href="bluetti-ac200max.html" class="text-electric-400 hover:text-electric-300 transition-colors font-semibold">Bluetti AC200Max</a>', '2,048 (expandable)', 'LiFePO4', '2,200', '4,800', '900 (MPPT)', '~2.5 hrs', '<span class="text-green-400">3,500</span>', '61.7 lbs', '<span class="text-green-400">Yes</span>', '$1,799'],
            ['<span class="font-semibold">EcoFlow River 2 Pro</span>', '768', 'LiFePO4', '800', '1,600', '220 (MPPT)', '70 min', '<span class="text-green-400">3,000</span>', '17.2 lbs', '<span class="text-red-400">No</span>', '$299–$399'],
            ['<span class="font-semibold">Goal Zero Yeti 1500X</span>', '1,516', 'NMC', '2,000', '3,500', '600 (MPPT)', '~2.5 hrs', '<span class="text-yellow-400">500</span>', '36.5 lbs', '<span class="text-yellow-400">Partial</span>', '$1,999'],
        ]
    )
    
    features = build_feature_cards(
        title="How to Choose the Right Power Station",
        subtitle="Five technical specs that actually matter — not marketing language.",
        features=[
            ("battery", "Capacity (Watt-Hours)", "Total energy stored. Calculate daily Wh usage: device watts × hours used. Oversize by 30% for inverter losses. A fridge needs ~1,200 Wh/day."),
            ("zap", "Inverter Output (Watts)", "Maximum continuous power. Check surge rating too — motors draw 2–3x rated watts on startup. Never run above 80% continuous load long-term."),
            ("sun", "Solar Input (MPPT)", "How fast you recharge from solar. MPPT is mandatory — cheap PWM waste 30-40%. Match panel wattage to MPPT rating, not marketing numbers."),
            ("refresh-cw", "Cycle Life (80% DoD)", "Charge-discharge cycles before 80% capacity. LiFePO4 = 3,000–6,000+ cycles. NMC = 500–1,000. Biggest predictor of total cost of ownership."),
            ("plug-zap", "UPS / Transfer Time", "Critical for home backup. 0ms protects sensitive electronics. 10–30ms is fine for appliances but may reboot computers."),
            ("weight", "Portability & Form Factor", "A 2,000 Wh station at 50+ lbs is not truly portable. For frequent moving, look at 700–1,200 Wh class (20–28 lbs). Wheels help but are no substitute."),
        ]
    )
    
    troubleshooting = build_resource_links(
        title="Common Power Station Issues",
        subtitle="Step-by-step diagnostics for the most frequent problems.",
        links=[
            ("power-off", "red", "Power Station Won't Turn On", "Battery reset, firmware recovery, inverter fault diagnosis, and when to contact warranty.", "../troubleshooting/power-station-wont-turn-on.html"),
            ("battery-warning", "yellow", "Not Charging (AC or Solar)", "Charging port issues, MPPT controller faults, cable resistance checks, and adapter replacement.", "../troubleshooting/power-station-not-charging.html"),
            ("alert-triangle", "red", "BMS Error Codes", "Battery Management System fault codes: cell imbalance, over-voltage, over-temperature, and communication errors.", "../troubleshooting/power-station-bms-error.html"),
            ("thermometer", "orange", "Overheating & Thermal Shutdown", "Fan failure, vent obstruction, thermal paste degradation, and high-temperature derating.", "../troubleshooting/power-station-overheating.html"),
            ("sun-dim", "yellow", "Solar Input Not Working", "Panel voltage mismatch, reverse polarity, broken MC4 connectors, and MPPT tracker failure.", "../troubleshooting/power-station-solar-input-not-working.html"),
            ("dollar-sign", "green", "Best Under $500 Comparison", "Mid-range 700–1,100Wh models field-tested for camping, emergency backup, and off-grid projects.", "budget-500w-power-station-comparison.html"),
        ]
    )
    
    faqs = build_faq_section(
        title="Frequently Asked Questions",
        subtitle="The most common questions about portable power stations.",
        faqs=[
            ("How long do portable power stations last?", "Modern LiFePO4 (LFP) power stations last 3,000–6,000 full cycles before dropping to 80% capacity. At one full cycle per week, that's 10+ years. NMC chemistry lasts 500–1,000 cycles (2–5 years). The BMS and inverter electronics typically outlast the battery cells."),
            ("What size do I need to run a fridge?", "A standard fridge uses ~100–200W when running but cycles on/off, totaling ~1,000–1,500 Wh/day. You need at least 1,500 Wh for 24 hours, but 2,000+ Wh is safer (account for inverter losses and temperature). The inverter surge rating must handle compressor startup (3–5x rated watts)."),
            ("LiFePO4 (LFP) vs NMC — which is better?", "LiFePO4 is better for almost every power station use case: 3–6x longer cycle life, better thermal stability (safer), lower cost per cycle, and wider operating temperature range. NMC has slightly higher energy density, but the difference is marginal in sizes most people buy. In 2026, nearly all new stations are LFP."),
            ("Can I leave my power station plugged in all the time?", "Most modern LFP stations with UPS mode are designed for continuous plug-in. The BMS maintains float charge (90–100%) and the station passes through AC. For long-term storage (3+ months), store at 50–60% charge in a cool (50–68°F) location. Never store fully depleted — that permanently damages LFP cells."),
            ("How much solar panel wattage do I need?", "Match panel wattage to your station's MPPT solar input rating. Real-world output is ~70% of panel rating in good sun (angle, temperature, inverter losses). A 500W MPPT with a 500W array gets ~350W real charging, so a 1,000 Wh station takes ~3 hours of good sun to fully charge."),
        ]
    )
    
    cta = build_cta(
        title="More Power Station Resources",
        description="Detailed model deep-dives, error code reference, and off-grid system sizing guides.",
        buttons=[
            ("EcoFlow Delta Pro 3 Full Specs", "ecoflow-delta-pro-3.html", "primary"),
            ("Troubleshooting Guide", "../troubleshooting/power-station-wont-turn-on.html", "secondary"),
            ("Solar System Sizing", "off-grid-solar-system-sizing-guide.html", "ghost"),
        ]
    )
    
    footer = get_footer(depth)
    
    content = head + header + breadcrumb + hero + table + features + troubleshooting + faqs + cta + footer
    write_file(f"{WORKSPACE}/pages/specs/outdoor-power.html", content)
    print("✓ outdoor-power.html 生成完成")


# ============================================================
# 2. Hybrid & EV Batteries 页面
# ============================================================

def generate_hybrid_cars():
    depth = 2
    head = get_head_template(depth).replace("{{title}}", "Hybrid & EV Battery Specs — Toyota Prius, Camry, Tesla, Honda Insight | TechSpecsHub")
    head = head.replace("{{description}}", "Module-level specs, fault codes, and repair guides for Toyota Prius, Camry Hybrid, RAV4 HV, Tesla LFP, and Honda Insight hybrid battery systems. All data cross-referenced with OEM service manuals.")
    head = head.replace("{{canonical}}", "https://powerspecshub.com/pages/specs/hybrid-cars.html")
    
    header = get_header_nav(depth)
    breadcrumb = build_breadcrumb([
        ("Home", "../../index.html"),
        ("Specs", "../error-code-db.html"),
        ("Hybrid & EV Batteries", None)
    ])
    
    hero = build_hero(
        icon="car",
        badge_text="Hybrid Vehicle Category · Updated June 2026",
        title_highlight="Hybrid & EV Battery",
        title_rest="Specifications",
        description="Module-level specs, fault codes, and repair guides for Toyota Prius, Camry Hybrid, RAV4 HV, Tesla LFP, and Honda Insight hybrid battery systems. All data cross-referenced with OEM service manuals.",
        stats=[("8+", "Models Covered"), ("20+", "Fault Codes"), ("28", "Modules/Pack"), ("8–10y", "Avg Lifespan")],
        gradient_pos="left-1/3"
    )
    
    table = build_table_section(
        title="Hybrid Battery Specifications",
        subtitle="OEM HV battery pack specs by vehicle model. Scroll horizontally on mobile.",
        headers=["Vehicle Model", "Battery Type", "Voltage", "Capacity (Ah)", "Modules/Cells", "Cooling", "Weight", "Warranty", "Replacement Cost"],
        rows=[
            ['<span class="font-semibold">Toyota Prius (Gen 2, 2004–2009)</span>', 'NiMH', '201.6 V', '6.5 Ah', '28 / 168 cells', 'Forced air', '~110 lbs', '8yr / 100k mi', '$1,300–$3,500'],
            ['<span class="font-semibold">Toyota Prius (Gen 3, 2010–2015)</span>', 'NiMH', '201.6 V', '6.5 Ah', '28 / 168 cells', 'Forced air', '~105 lbs', '8yr / 100k mi', '$1,500–$3,800'],
            ['<span class="font-semibold">Toyota Prius (Gen 4, 2016–2022)</span>', 'NiMH / Li-ion', '207.2 V', '6.5 Ah', '28 modules', 'Forced air', '~95 lbs', '8yr / 100k mi', '$2,000–$4,500'],
            ['<span class="font-semibold">Toyota Camry Hybrid (2007–2011)</span>', 'NiMH', '244.8 V', '6.5 Ah', '34 modules', 'Forced air', '~130 lbs', '8yr / 100k mi', '$1,800–$4,000'],
            ['<span class="font-semibold">Toyota RAV4 HV (2016–2018)</span>', 'NiMH', '244.8 V', '6.5 Ah', '34 modules', 'Forced air', '~135 lbs', '8yr / 100k mi', '$2,000–$4,500'],
            ['<span class="font-semibold">Honda Insight (Gen 2, 2009–2014)</span>', 'NiMH', '100.8 V', '5.75 Ah', '14 / 84 cells', 'Natural/forced', '~80 lbs', '8yr / 80k mi', '$1,200–$2,800'],
            ['<span class="font-semibold">Ford Fusion Hybrid (2010–2012)</span>', 'NiMH', '275 V', '5.5 Ah', '~36 modules', 'Forced air', '~140 lbs', '8yr / 100k mi', '$2,000–$4,200'],
            ['<span class="font-semibold">Tesla Model 3 (LFP, 2021+)</span>', 'LiFePO4 (LFP)', '350–400 V', '~150 Ah', '4 modules (CATL)', 'Liquid-cooled', '~1,000 lbs', '8yr / 100k mi', '$5,000–$15,000'],
            ['<span class="font-semibold">Lexus RX 450h (2010–2015)</span>', 'NiMH', '288 V', '6.5 Ah', '40 modules', 'Dual fan forced', '~150 lbs', '8yr / 100k mi', '$2,500–$5,000'],
        ]
    )
    
    troubleshooting = build_resource_links(
        title="Most Common Hybrid Battery Fault Codes",
        subtitle="The diagnostic trouble codes our readers search for most often.",
        links=[
            ("alert-triangle", "red", "P0A80 — Replace Hybrid Battery Pack", "Weak cell failure detected. Most serious hybrid battery code — replacement is needed.", "../troubleshooting/p0a80-replace-hybrid-battery.html"),
            ("battery-warning", "yellow", "P0A7F — Battery Pack Deterioration", "Battery efficiency and capacity have dropped significantly. Often precedes P0A80.", "../troubleshooting/p0a7f-hybrid-battery-deterioration.html"),
            ("cpu", "orange", "P3000 — Battery Control System Fault", "General HV battery control system fault. Communication error between BMS and ECU.", "../troubleshooting/p3000-hybrid-battery-control-module.html"),
            ("gauge", "blue", "P0A7B — Voltage Sensor Circuit", "Voltage sensor circuit fault. Module voltage monitoring is compromised.", "../troubleshooting/p0a7b-hybrid-battery-voltage-sensor.html"),
            ("thermometer", "red", "P0AC4 — Temperature Sensor Fault", "HV battery temperature sensor circuit malfunction. Without temp data, BMS can't properly cool.", "../troubleshooting/p0ac4-hybrid-battery-temperature-sensor.html"),
            ("zap", "purple", "P0A9D — Hybrid Inverter Fault", "Inverter/converter system fault. DC-to-AC conversion failure — limp mode or no start.", "../troubleshooting/p0a9d-hybrid-inverter-fault.html"),
        ]
    )
    
    # 阶段式失效说明
    stages_html = '''  <!-- BATTERY FAILURE STAGES -->
  <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="max-w-3xl mx-auto mb-10 text-center">
      <h2 class="font-bold text-3xl md:text-4xl mb-4">Understanding Hybrid Battery Failure</h2>
      <p class="text-gray-400">What actually happens when a hybrid battery wears out, and what you can do about it.</p>
    </div>

    <div class="grid md:grid-cols-2 gap-8 items-center">
      <div class="space-y-6">
        <div class="flex gap-4">
          <div class="w-8 h-8 bg-electric-500/20 rounded-lg flex items-center justify-center flex-shrink-0 font-bold text-electric-400 text-sm">1</div>
          <div>
            <h3 class="font-semibold mb-1">Cell Imbalance (Early Stage)</h3>
            <p class="text-sm text-gray-400">Individual modules develop slightly different internal resistance. The BMS tries to balance them but can only do so much. You'll notice a small MPG drop — 2–4 mpg.</p>
          </div>
        </div>
        <div class="flex gap-4">
          <div class="w-8 h-8 bg-yellow-500/20 rounded-lg flex items-center justify-center flex-shrink-0 font-bold text-yellow-400 text-sm">2</div>
          <div>
            <h3 class="font-semibold mb-1">Module Weakening (Mid Stage)</h3>
            <p class="text-sm text-gray-400">One or more specific modules can't hold charge like the rest. The battery gauge fluctuates rapidly. Codes like P3011–P3024 appear. MPG drops 5–10 mpg.</p>
          </div>
        </div>
        <div class="flex gap-4">
          <div class="w-8 h-8 bg-orange-500/20 rounded-lg flex items-center justify-center flex-shrink-0 font-bold text-orange-400 text-sm">3</div>
          <div>
            <h3 class="font-semibold mb-1">P0A7F Deterioration (Late Warning)</h3>
            <p class="text-sm text-gray-400">Overall pack capacity has dropped below the BMS threshold. The car still runs but the electric motor is less available.</p>
          </div>
        </div>
        <div class="flex gap-4">
          <div class="w-8 h-8 bg-red-500/20 rounded-lg flex items-center justify-center flex-shrink-0 font-bold text-red-400 text-sm">4</div>
          <div>
            <h3 class="font-semibold mb-1">P0A80 Replace Battery (Failure)</h3>
            <p class="text-sm text-gray-400">Cell failure is confirmed. The vehicle may enter fail-safe mode with limited power. Don't delay — driving with P0A80 can damage the inverter.</p>
          </div>
        </div>
      </div>

      <div class="glass-card p-6">
        <div class="flex items-center gap-3 mb-4">
          <i data-lucide="lightbulb" style="width:1.3rem;height:1.3rem;color:#fbbf24"></i>
          <h3 class="font-semibold text-lg">Replacement Options</h3>
        </div>
        <div class="space-y-4 text-sm">
          <div class="p-3 bg-white/5 rounded-lg">
            <div class="font-semibold text-green-400 mb-1">Remanufactured Pack ($1,300–$2,500)</div>
            <p class="text-gray-400">Best value. New matched cells, tested BMS, 2–3 year warranty. Installed by specialty hybrid shops.</p>
          </div>
          <div class="p-3 bg-white/5 rounded-lg">
            <div class="font-semibold text-electric-400 mb-1">OEM Dealer Pack ($3,000–$8,000)</div>
            <p class="text-gray-400">Factory new, perfect fit, longest warranty (8yr). Premium pricing — often more than the car is worth on older models.</p>
          </div>
          <div class="p-3 bg-white/5 rounded-lg">
            <div class="font-semibold text-yellow-400 mb-1">Module Replacement ($800–$1,500)</div>
            <p class="text-gray-400">Replace only the bad modules. Cheaper short-term but the rest of the pack continues aging.</p>
          </div>
          <div class="p-3 bg-white/5 rounded-lg">
            <div class="font-semibold text-red-400 mb-1">Used / Junkyard Pack ($500–$1,200)</div>
            <p class="text-gray-400">High risk. You don't know the pack's history or health. May fail in months. Not recommended.</p>
          </div>
        </div>
      </div>
    </div>
  </section>
'''
    
    faqs = build_faq_section(
        title="Frequently Asked Questions",
        subtitle="Common questions about hybrid battery maintenance and replacement.",
        faqs=[
            ("How long does a Toyota Prius hybrid battery really last?", "In moderate climates, 150,000–200,000 miles (10–14 years) is typical for the original NiMH pack. In very hot climates, 100,000–130,000 miles is more common due to heat accelerating cell degradation. The 8-year / 100k-mile factory warranty covers early failures."),
            ("Can I drive with a P0A80 code?", "Technically yes — the vehicle enters fail-safe mode and runs primarily on gas. But it's risky: the inverter must work harder to compensate for weak cells, and a complete pack failure can leave you stranded. If the 'Check Hybrid System' light is on with P0A80, get it diagnosed within a week or two."),
            ("Should I replace just the bad modules or the whole pack?", "Replacing only weak modules costs less upfront but is usually a false economy. Hybrid battery cells age together — if one or two have failed, the rest are close behind. A remanufactured pack with all-new matched cells and a 2–3 year warranty is almost always better value."),
            ("What is Dr. Prius and is it accurate?", "Dr. Prius is a mobile app that reads Toyota hybrid battery data through a Bluetooth OBD-II adapter. It shows individual module voltages and can estimate pack health. It's reasonably accurate for identifying which modules are weak, but don't treat its 'battery life remaining' percentage as gospel."),
            ("How do I clean the hybrid battery cooling fan?", "The HV battery cooling fan intake is usually in the rear parcel shelf or side panel. Locate the intake grille, gently vacuum dust from the surface, then use low-pressure compressed air to blow out dust from the fan housing. Do this every 10,000–15,000 miles. A clogged fan causes the battery to run hot and shortens life significantly."),
        ]
    )
    
    cta = build_cta(
        title="Got a hybrid battery code?",
        description="Start with the most common fault code and work through diagnostics step by step.",
        buttons=[
            ("P0A80 Diagnostic Guide", "../troubleshooting/p0a80-replace-hybrid-battery.html", "primary"),
            ("P0A7F Early Warning", "../troubleshooting/p0a7f-hybrid-battery-deterioration.html", "secondary"),
            ("Browse All Codes", "../error-code-db.html", "ghost"),
        ]
    )
    
    footer = get_footer(depth)
    
    content = head + header + breadcrumb + hero + table + troubleshooting + stages_html + faqs + cta + footer
    write_file(f"{WORKSPACE}/pages/specs/hybrid-cars.html", content)
    print("✓ hybrid-cars.html 生成完成")


# ============================================================
# 3. Drones 页面
# ============================================================

def generate_drones():
    depth = 2
    head = get_head_template(depth).replace("{{title}}", "Drone & UAV Specs — DJI Mavic, Air, Mini Series Camera & Flight Parameters | TechSpecsHub")
    head = head.replace("{{description}}", "Camera specs, flight parameters, gimbal error codes, and battery data for DJI Mavic, Air, and Mini series drones. All specs verified against official DJI documentation and real-world testing.")
    head = head.replace("{{canonical}}", "https://powerspecshub.com/pages/specs/drones.html")
    
    header = get_header_nav(depth)
    breadcrumb = build_breadcrumb([
        ("Home", "../../index.html"),
        ("Specs", "../error-code-db.html"),
        ("Drones & UAV", None)
    ])
    
    hero = build_hero(
        icon="plane",
        badge_text="Drone Category · Updated June 2026",
        title_highlight="Drone & UAV",
        title_rest="Specifications",
        description="Camera specs, flight parameters, gimbal error codes, and battery data for DJI Mavic, Air, and Mini series drones. All specs verified against official DJI documentation and real-world testing.",
        stats=[("10+", "DJI Models"), ("15+", "Error Patterns"), ("249g", "Sub-250g Lineup"), ("52 min", "Longest Flight")],
        gradient_pos="right-1/4"
    )
    
    table = build_table_section(
        title="DJI Drone Comparison",
        subtitle="Consumer and prosumer drone specs from the 2026 lineup. Scroll horizontally on mobile.",
        headers=["Model", "Weight", "Camera Sensor", "Max Video", "Flight Time", "Transmission", "Obstacle Sensing", "Gimbal", "Price"],
        rows=[
            ['<span class="font-semibold">DJI Mini 5 Pro</span>', '<span class="text-green-400">249g</span>', '1-inch CMOS', '4K/120fps HDR', '<span class="text-green-400">52 min</span>', 'O4 (20 km)', '<span class="text-green-400">Omnidirectional</span>', '3-axis, 225° tilt', '$799'],
            ['<span class="font-semibold">DJI Mini 4 Pro</span>', '<span class="text-green-400">249g</span>', '1/1.3-inch CMOS', '4K/60fps HDR', '34 min (45 w/ Plus)', 'O4 (20 km)', '<span class="text-green-400">Omnidirectional</span>', '3-axis mechanical', '$759'],
            ['<span class="font-semibold">DJI Mini 3</span>', '<span class="text-green-400">249g</span>', '1/1.3-inch CMOS', '4K/30fps HDR', '38 min', 'O2 (10 km)', '<span class="text-yellow-400">Downward only</span>', '3-axis mechanical', '$469'],
            ['<span class="font-semibold">DJI Mini 4K</span>', '<span class="text-green-400">249g</span>', '1/2.3-inch CMOS', '4K/30fps', '31 min', 'O2 (10 km)', '<span class="text-yellow-400">Downward only</span>', '3-axis mechanical', '$299'],
            ['<span class="font-semibold">DJI Air 3S</span>', '695 g', '1-inch CMOS', '4K/60fps HDR', '45 min', 'O4 (20 km)', '<span class="text-green-400">Omni Nightscape</span>', '3-axis', '$1,099'],
            ['<span class="font-semibold">DJI Mavic 4 Pro</span>', '~895 g', '4/3" Hasselblad', '6K/60fps HDR', '51 min', 'O4+ (30 km)', '<span class="text-green-400">Omni (0.1-Lux)</span>', '3-axis Hasselblad', '$2,849'],
            ['<span class="font-semibold">DJI Flip</span>', '<span class="text-green-400">249g</span>', '1/1.3-inch CMOS', '4K/60fps HDR', '31 min', 'O3 (13 km)', '<span class="text-yellow-400">Forward + Down</span>', '3-axis (guards)', '$439'],
            ['<span class="font-semibold">DJI Neo 2</span>', '149 g', '1/2-inch CMOS', '4K/60fps', '~22 min', 'O2 (10 km)', '<span class="text-yellow-400">Downward + Track</span>', '2-axis + EIS', '$199'],
            ['<span class="font-semibold">DJI Avata 2</span>', '410 g', '1/1.3-inch CMOS', '4K/60fps', '23 min', 'O3 (20 km)', '<span class="text-red-400">None (FPV)</span>', '1-axis (155° FOV)', '$999 (Fly More)'],
        ]
    )
    
    features = build_feature_cards(
        title="Choosing the Right Drone",
        subtitle="Six spec categories that determine which drone is right for you.",
        features=[
            ("camera", "Camera Sensor Size", "Bigger sensors capture more light and produce better image quality, especially in low light. 1-inch is the sweet spot for travel photography. 4/3-inch Hasselblad sensors are for professional work."),
            ("gauge", "Flight Time & Battery Life", "Rated flight times are in ideal conditions (no wind, slow flight). Subtract 20–30% for real-world use. Always buy a Fly More Combo (3 batteries) — one battery barely gets you set up."),
            ("shield", "Obstacle Avoidance", "Omnidirectional sensing is not a gimmick — it's the #1 feature that prevents crashes. Forward-only sensing misses obstacles to the side and rear when you're focusing on composition."),
            ("wifi", "Video Transmission", "O4 (20 km range) is dramatically better than O2 (10 km) — not because you'll fly 20km, but because the signal stays rock-solid at 2–3 km in urban areas with interference."),
            ("scale", "Weight & Registration", "Drones under 250g don't require FAA registration for recreational use in the US (you still need TRUST). This is a huge advantage in convenience and cost."),
            ("zap", "Gimbal Stabilization", "3-axis mechanical gimbal is non-negotiable for usable video. 2-axis or pure EIS causes rolling shutter and cropped footage. The gimbal is also the most fragile component."),
        ]
    )
    
    troubleshooting = build_resource_links(
        title="Common DJI Drone Issues",
        subtitle="Step-by-step fixes for the most frequent drone problems.",
        links=[
            ("alert-circle", "red", "Gimbal Error Codes", "Gimbal motor stuck, overload, IMU calibration — all the common DJI gimbal faults with actual fixes.", "../troubleshooting/dji-gimbal-error-codes.html"),
            ("compass", "yellow", "Compass Error / Calibration", "Compass interference, calibration failures, and IMU drift. How to properly calibrate in the field.", "../troubleshooting/dji-compass-error.html"),
            ("activity", "orange", "IMU Calibration Error", "IMU initialization failures, abnormal gyro data, and accelerometer calibration procedures.", "../troubleshooting/dji-imu-calibration-error.html"),
            ("battery-warning", "yellow", "Battery Not Charging", "Battery charging port issues, charging hub faults, battery management problems, and firmware update stuck.", "../troubleshooting/dji-battery-not-charging.html"),
            ("eye", "blue", "Vision Positioning Error", "Downward vision sensor failure, VPS calibration issues, and landing protection malfunction.", "../troubleshooting/dji-vision-positioning-error.html"),
        ]
    )
    
    faqs = build_faq_section(
        title="Frequently Asked Questions",
        subtitle="Common questions about DJI drones and drone photography.",
        faqs=[
            ("Is the DJI Mini 5 Pro worth upgrading from the Mini 4 Pro?", "If you shoot a lot of low-light or want the 225° gimbal tilt angle, yes — the 1-inch sensor is a noticeable step up. But if you mainly shoot in good daylight with the Mini 4 Pro, the upgrade is marginal. The 52-minute flight time (vs 34/45) is also a meaningful improvement for longer shoots."),
            ("Do I need to register a sub-250g drone?", "In the US, recreational users do NOT need to register drones under 250g with the FAA. However, you still need to pass the TRUST test (free online), follow all airspace rules, and can't fly recklessly. Commercial use requires a Part 107 certificate regardless of weight."),
            ("How important is obstacle avoidance?", "Extremely important. It's the feature that most prevents expensive crashes. Even experienced pilots hit obstacles when they're focused on composition and lose spatial awareness. Omnidirectional is far better than forward-only — most crashes happen from the side or rear during backward/sideways flight."),
            ("What's the difference between O2, O3, and O4 transmission?", "These are DJI's video transmission generations. O2 = 10km range / 1080p. O3 = 12–15km / 1080p. O4 = 20km / 1080p/60fps with better anti-interference. The real-world difference is signal stability in cluttered environments — O4 stays rock-solid where O2 starts dropping frames."),
            ("How long do drone batteries last?", "DJI Intelligent Flight batteries are rated for ~300 charge cycles before capacity drops below 80%. At 2–3 flights per week, that's 2–3 years. To maximize lifespan: store at 40–60% charge for long periods, avoid full discharges, and don't charge immediately after a hot flight (let the battery cool first)."),
        ]
    )
    
    cta = build_cta(
        title="More Drone Resources",
        description="Gimbal error guides, battery troubleshooting, and detailed model specs.",
        buttons=[
            ("Gimbal Error Code Guide", "../troubleshooting/dji-gimbal-error-codes.html", "primary"),
            ("Battery Troubleshooting", "../troubleshooting/dji-battery-not-charging.html", "secondary"),
            ("Mini 5 Pro Specs", "#", "ghost"),
        ]
    )
    
    footer = get_footer(depth)
    
    content = head + header + breadcrumb + hero + table + features + troubleshooting + faqs + cta + footer
    write_file(f"{WORKSPACE}/pages/specs/drones.html", content)
    print("✓ drones.html 生成完成")


# ============================================================
# 4. Smart Home 页面
# ============================================================

def generate_smart_home():
    depth = 2
    head = get_head_template(depth).replace("{{title}}", "Smart Home Device Specs — Robot Vacuums, Smart Displays, Wi-Fi Routers | TechSpecsHub")
    head = head.replace("{{description}}", "Complete technical specs for smart home devices: robot vacuums, smart displays, Wi-Fi routers, smart speakers, and home security. All data verified against OEM specifications.")
    head = head.replace("{{canonical}}", "https://powerspecshub.com/pages/specs/smart-home.html")
    
    header = get_header_nav(depth)
    breadcrumb = build_breadcrumb([
        ("Home", "../../index.html"),
        ("Specs", "../error-code-db.html"),
        ("Smart Home Devices", None)
    ])
    
    hero = build_hero(
        icon="home",
        badge_text="Smart Home Category · Updated June 2026",
        title_highlight="Smart Home Device",
        title_rest="Specifications",
        description="Complete technical specs for smart home devices: robot vacuums, smart displays, Wi-Fi routers, smart speakers, and home security. All data verified against OEM specifications.",
        stats=[("15+", "Models Listed"), ("5+", "Device Types"), ("10+", "Troubleshooting Guides"), ("WiFi 7", "Latest Standard")],
        gradient_pos="right-1/3"
    )
    
    table = build_table_section(
        title="Smart Speaker & Display Comparison",
        subtitle="Smart speakers and displays from Amazon, Google, and Apple. Scroll horizontally on mobile.",
        headers=["Model", "Display", "Speakers", "Microphones", "Voice Assistant", "Connectivity", "Smart Home Hub", "Price"],
        rows=[
            ['<span class="font-semibold">Amazon Echo Show 15</span>', '15.6" FHD (1920×1080)', '2x 1.6" + 1x passiv', '8-mic array', 'Alexa', 'Wi-Fi 6, BT 5.0', '<span class="text-green-400">Zigbee + Matter</span>', '$279.99'],
            ['<span class="font-semibold">Google Nest Hub (2nd Gen)</span>', '7" HD (1024×600)', 'Full-range speaker', '3-mic array', 'Google Assistant', 'Wi-Fi 5, BT 5.0', '<span class="text-green-400">Thread + Matter</span>', '$99.99'],
            ['<span class="font-semibold">Amazon Echo (4th Gen)</span>', '—', '3" woofer + 2x tweeters', '7-mic array', 'Alexa', 'Wi-Fi 5, BT 5.0', '<span class="text-green-400">Zigbee</span>', '$99.99'],
            ['<span class="font-semibold">Google Nest Audio</span>', '—', '75mm mid + tweeter', '3-mic array', 'Google Assistant', 'Wi-Fi 5, BT 5.0', '<span class="text-yellow-400">Thread only</span>', '$99.99'],
            ['<span class="font-semibold">Apple HomePod (2nd Gen)</span>', '—', '4" woofer + 5x tweeters', '6-mic array', 'Siri', 'Wi-Fi 5, BT 5.0', '<span class="text-green-400">Thread + Matter</span>', '$299.00'],
            ['<span class="font-semibold">Amazon Echo Dot (5th Gen)</span>', '—', '1.73" front-firing', '4-mic array', 'Alexa', 'Wi-Fi 5, BT 5.2', '<span class="text-red-400">No</span>', '$49.99'],
            ['<span class="font-semibold">Apple HomePod mini</span>', '—', 'Full-range driver + passive', '4-mic array', 'Siri', 'Wi-Fi 5, BT 5.0', '<span class="text-green-400">Thread + Matter</span>', '$99.00'],
        ]
    )
    
    # Robot Vacuum Table
    vac_table = build_table_section(
        title="Robot Vacuum Comparison",
        subtitle="Robot vacuum and mop specs from iRobot, Roborock, Ecovacs, and more.",
        headers=["Model", "Suction (Pa)", "Mopping", "Navigation", "Battery", "Dustbin", "Self-Empty", "Price"],
        rows=[
            ['<span class="font-semibold">Roborock S8 MaxV Ultra</span>', '<span class="text-green-400">10,000 Pa</span>', 'VibraRise 3.0 (3000rpm)', 'Reactive AI 2.0 + 3D', '5200 mAh', '350 ml', '<span class="text-green-400">Yes (Dock)</span>', '$1,599'],
            ['<span class="font-semibold">Ecovacs Deebot T30 Omni</span>', '<span class="text-green-400">11,000 Pa</span>', 'OZMO Turbo 2.0', 'TrueDetect 3.0 + AI', '5200 mAh', '380 ml', '<span class="text-green-400">Yes (Dock)</span>', '$1,099'],
            ['<span class="font-semibold">iRobot Roomba j9+</span>', '— (undisclosed)', 'Dual Rubber Brushes', 'vSLAM 3.0', '—', '~350 ml', '<span class="text-green-400">Yes (Clean Base)</span>', '$899'],
            ['<span class="font-semibold">Roborock Q8 Max+</span>', '5,500 Pa', 'Dual SpinBrush', 'Reactive Tech', '5200 mAh', '470 ml', '<span class="text-green-400">Yes</span>', '$699'],
            ['<span class="font-semibold">Ecovacs Deebot N8 Pro+</span>', '2,600 Pa', 'OZMO Pro', 'dToF LiDAR', '3200 mAh', '400 ml', '<span class="text-green-400">Yes</span>', '$499'],
            ['<span class="font-semibold">iRobot Roomba 692</span>', '— (budget)', 'No', 'Adaptive Navigation', '—', '300 ml', '<span class="text-red-400">No</span>', '$299'],
        ]
    )
    
    troubleshooting = build_resource_links(
        title="Common Smart Home Issues",
        subtitle="Step-by-step diagnostics for the most frequent smart home problems.",
        links=[
            ("wifi-off", "red", "Smart Home Device Offline", "Wi-Fi connectivity issues, router compatibility, 2.4GHz vs 5GHz, and factory reset procedures.", "../troubleshooting/smart-home-device-offline.html"),
            ("mic", "orange", "Smart Speaker Not Responding", "Microphone problems, voice recognition failures, mute button glitches, and wake word detection issues.", "../troubleshooting/smart-speaker-not-responding.html"),
        ]
    )
    
    faqs = build_faq_section(
        title="Frequently Asked Questions",
        subtitle="Common questions about smart home devices and ecosystems.",
        faqs=[
            ("Alexa vs Google Assistant vs Siri — which is best?", "Alexa has the widest smart home device support and best routines. Google Assistant is better at search and answers questions more accurately. Siri has the best privacy and deepest Apple ecosystem integration. For most people, Alexa or Google Assistant is the practical choice for smart home control."),
            ("What is Matter and why does it matter?", "Matter is a universal smart home standard backed by Apple, Google, Amazon, and Samsung. Devices that support Matter work across all ecosystems — you can control a Matter device with Alexa, Google Home, and Apple Home simultaneously without needing bridges or hubs."),
            ("Do I need a smart home hub?", "Not always — many Wi-Fi devices connect directly to your router. But Zigbee and Thread devices need a hub (or a speaker/display with built-in hub). Hubs also improve reliability with local control (works when internet is down) and faster response times."),
            ("How much suction do I need in a robot vacuum?", "For hard floors, 2,000–3,000 Pa is fine. For carpets, look for 5,000+ Pa. But suction numbers alone don't tell the whole story — brushroll design, airflow, and navigation matter more than raw Pa. Don't chase the highest number blindly."),
            ("Can smart speakers spy on me?", "Smart speakers only listen for the wake word — they don't continuously record everything. However, voice clips may be sent to the cloud for processing and can be stored (often anonymized). You can review and delete your voice history in the app settings. For maximum privacy, use the physical mute button when not in use."),
        ]
    )
    
    cta = build_cta(
        title="More Smart Home Resources",
        description="Troubleshooting guides and complete device specifications.",
        buttons=[
            ("Offline Troubleshooting", "../troubleshooting/smart-home-device-offline.html", "primary"),
            ("Smart Speaker Fixes", "../troubleshooting/smart-speaker-not-responding.html", "secondary"),
        ]
    )
    
    footer = get_footer(depth)
    
    content = head + header + breadcrumb + hero + table + vac_table + troubleshooting + faqs + cta + footer
    write_file(f"{WORKSPACE}/pages/specs/smart-home.html", content)
    print("✓ smart-home.html 生成完成")


# ============================================================
# 5. EcoFlow Delta Pro 3 产品详情页（扩展）
# ============================================================

def generate_ecoflow_delta_pro_3():
    depth = 2
    head = get_head_template(depth).replace("{{title}}", "EcoFlow Delta Pro 3 Full Spec Sheet — 4,096Wh LFP, 4,000W Inverter, 1,600W Solar | TechSpecsHub")
    head = head.replace("{{description}}", "Complete EcoFlow Delta Pro 3 specifications: 4,096 Wh LFP battery, 4,000W continuous inverter, 1,600W MPPT solar input, idle drain, charge efficiency, cycle life, and the complete error code list.")
    head = head.replace("{{canonical}}", "https://powerspecshub.com/pages/specs/ecoflow-delta-pro-3.html")
    
    header = get_header_nav(depth)
    breadcrumb = build_breadcrumb([
        ("Home", "../../index.html"),
        ("Specs", "../error-code-db.html"),
        ("Outdoor Power", "outdoor-power.html"),
        ("EcoFlow Delta Pro 3", None)
    ])
    
    # 产品 hero
    hero_html = f'''  <!-- PRODUCT HERO -->
  <section class="relative pt-6 pb-16">
    <div class="absolute inset-0 pointer-events-none overflow-hidden">
      <div class="absolute top-0 left-1/3 w-[400px] h-[400px] bg-electric-500/10 rounded-full blur-3xl"></div>
    </div>
    <div class="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid md:grid-cols-2 gap-10 items-center">
        <div>
          <div class="inline-flex items-center gap-2 px-3 py-1.5 bg-green-500/10 border border-green-500/30 rounded-full text-xs font-semibold text-green-400 mb-4 tracking-wide uppercase">
            <i data-lucide="award" style="width:0.85rem;height:0.85rem"></i>
            Best Whole-Home Backup · 2026
          </div>
          <h1 class="font-bold text-4xl md:text-5xl mb-4 leading-[1.1] tracking-tight">
            EcoFlow Delta Pro 3
          </h1>
          <p class="text-lg text-gray-400 mb-6 leading-relaxed">
            4,096 Wh LFP portable power station with 4,000W continuous inverter output, 1,600W MPPT solar input, 0ms UPS mode, and expandable architecture up to 24 kWh.
          </p>
          <div class="grid grid-cols-2 gap-3 mb-6">
            <div class="glass-card p-4">
              <div class="text-2xl font-bold text-electric-400 font-mono">4,096 Wh</div>
              <div class="text-xs text-gray-500 mt-1">Capacity (LFP)</div>
            </div>
            <div class="glass-card p-4">
              <div class="text-2xl font-bold text-electric-400 font-mono">4,000 W</div>
              <div class="text-xs text-gray-500 mt-1">Continuous Output</div>
            </div>
            <div class="glass-card p-4">
              <div class="text-2xl font-bold text-electric-400 font-mono">1,600 W</div>
              <div class="text-xs text-gray-500 mt-1">Solar (MPPT)</div>
            </div>
            <div class="glass-card p-4">
              <div class="text-2xl font-bold text-electric-400 font-mono">4,000</div>
              <div class="text-xs text-gray-500 mt-1">Cycles to 80%</div>
            </div>
          </div>
          <div class="flex flex-wrap gap-3">
            <span class="px-3 py-1 bg-white/5 rounded-full text-xs text-gray-300">LiFePO4 Battery</span>
            <span class="px-3 py-1 bg-white/5 rounded-full text-xs text-gray-300">0ms UPS</span>
            <span class="px-3 py-1 bg-white/5 rounded-full text-xs text-gray-300">App Control</span>
            <span class="px-3 py-1 bg-white/5 rounded-full text-xs text-gray-300">Expandable</span>
          </div>
        </div>
        <div class="glass-card p-6 text-center">
          <div class="text-6xl font-bold text-electric-400/20 mb-2">⚡</div>
          <div class="text-sm text-gray-500 mb-1">Est. Street Price (June 2026)</div>
          <div class="text-4xl font-bold text-white font-mono">$2,399</div>
          <div class="text-sm text-gray-400 mt-2">Price varies by retailer and promotions</div>
        </div>
      </div>
    </div>
  </section>
'''
    
    spec_table = build_table_section(
        title="Full Specifications",
        subtitle="Complete technical specifications for the EcoFlow Delta Pro 3.",
        headers=["Category", "Specification"],
        rows=[
            ['<span class="font-semibold">Battery Capacity</span>', '4,096 Wh (128 V × 32 Ah)'],
            ['<span class="font-semibold">Battery Chemistry</span>', 'LiFePO4 (Lithium Iron Phosphate)'],
            ['<span class="font-semibold">Cycle Life</span>', '4,000 cycles to 80% capacity (0.5C charge/discharge, 25°C)'],
            ['<span class="font-semibold">Battery Management</span>', 'Smart BMS with over-voltage, under-voltage, over-current, over-temperature, short-circuit protection'],
            ['<span class="font-semibold">Inverter Type</span>', 'Pure sine wave'],
            ['<span class="font-semibold">Continuous Output</span>', '4,000 W (total, all outlets combined)'],
            ['<span class="font-semibold">Surge Output</span>', '7,000 W (peak, <1s)'],
            ['<span class="font-semibold">X-Boost</span>', 'Yes — runs resistive loads up to 4,500W with power factor correction'],
            ['<span class="font-semibold">AC Outlets</span>', '5 × NEMA 5-15R (120V, 60Hz)'],
            ['<span class="font-semibold">USB-C</span>', '1 × 100W PD (5–20V)'],
            ['<span class="font-semibold">USB-A</span>', '2 × USB-A QC3.0 (18W each)'],
            ['<span class="font-semibold">Car Port</span>', '1 × 12V/30A regulated'],
            ['<span class="font-semibold">DC5521</span>', '2 × 12V/5A'],
            ['<span class="font-semibold">UPS Mode</span>', 'Yes, 0ms transfer time (online double-conversion)'],
            ['<span class="font-semibold">Solar Input</span>', '2 × XT60 ports (combined max 1,600W)'],
            ['<span class="font-semibold">MPPT Voltage Range</span>', '12–120V DC, 15A max per port'],
            ['<span class="font-semibold">AC Charge Speed</span>', '80% in ~50 minutes, 100% in ~1.2 hours (with AC+Solar simultaneously)'],
            ['<span class="font-semibold">Charging Modes</span>', 'Silent / Standard / Turbo / Custom'],
            ['<span class="font-semibold">Display</span>', 'Full-color LCD touchscreen with real-time monitoring'],
            ['<span class="font-semibold">App Connectivity</span>', 'Wi-Fi (2.4 GHz) + Bluetooth, EcoFlow app (iOS/Android)'],
            ['<span class="font-semibold">Weight</span>', '59.5 lbs (27 kg)'],
            ['<span class="font-semibold">Dimensions</span>', '19.6 × 10.4 × 15.0 in (50 × 26.5 × 38 cm)'],
            ['<span class="font-semibold">Operating Temperature</span>', '–4°F to 104°F (–20°C to 40°C)'],
            ['<span class="font-semibold">Charging Temperature</span>', '32°F to 113°F (0°C to 45°C)'],
            ['<span class="font-semibold">Noise Level</span>', '<30 dB at 3.3 ft (1 m) in Silent mode'],
            ['<span class="font-semibold">Warranty</span>', '5 years (with optional extended warranty)'],
            ['<span class="font-semibold">Expandability</span>', 'Up to 2 × Extra Battery (Max 12,288 Wh)'],
        ]
    )
    
    # Performance 部分
    perf_html = '''  <!-- PERFORMANCE SECTION -->
  <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="max-w-3xl mx-auto mb-10 text-center">
      <h2 class="font-bold text-3xl md:text-4xl mb-4">Real-World Performance</h2>
      <p class="text-gray-400">What the Delta Pro 3 can actually power, and for how long.</p>
    </div>

    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div class="glass-card p-6">
        <div class="w-12 h-12 bg-blue-500/15 rounded-xl flex items-center justify-center mb-4">
          <i data-lucide="refrigerator" style="width:1.5rem;height:1.5rem;color:#60a5fa"></i>
        </div>
        <h3 class="text-lg font-semibold mb-2">Full-Size Fridge</h3>
        <p class="text-gray-400 text-sm mb-4">~100–150W continuous, cycling on/off.</p>
        <div class="text-3xl font-bold text-electric-400 font-mono">24–32 hrs</div>
        <div class="text-xs text-gray-500 mt-1">Estimated runtime</div>
      </div>

      <div class="glass-card p-6">
        <div class="w-12 h-12 bg-yellow-500/15 rounded-xl flex items-center justify-center mb-4">
          <i data-lucide="microwave" style="width:1.5rem;height:1.5rem;color:#fbbf24"></i>
        </div>
        <h3 class="text-lg font-semibold mb-2">Microwave (1,000W)</h3>
        <p class="text-gray-400 text-sm mb-4">Sustained 1,000W draw with inverter surge.</p>
        <div class="text-3xl font-bold text-electric-400 font-mono">~3.5 hrs</div>
        <div class="text-xs text-gray-500 mt-1">Continuous use</div>
      </div>

      <div class="glass-card p-6">
        <div class="w-12 h-12 bg-green-500/15 rounded-xl flex items-center justify-center mb-4">
          <i data-lucide="lamp" style="width:1.5rem;height:1.5rem;color:#4ade80"></i>
        </div>
        <h3 class="text-lg font-semibold mb-2">LED Lighting</h3>
        <p class="text-gray-400 text-sm mb-4">10 × 10W LED bulbs = 100W total.</p>
        <div class="text-3xl font-bold text-electric-400 font-mono">35–40 hrs</div>
        <div class="text-xs text-gray-500 mt-1">All lights on</div>
      </div>

      <div class="glass-card p-6">
        <div class="w-12 h-12 bg-purple-500/15 rounded-xl flex items-center justify-center mb-4">
          <i data-lucide="laptop" style="width:1.5rem;height:1.5rem;color:#c084fc"></i>
        </div>
        <h3 class="text-lg font-semibold mb-2">Laptop + Router + Modem</h3>
        <p class="text-gray-400 text-sm mb-4">Home office / remote work setup.</p>
        <div class="text-3xl font-bold text-electric-400 font-mono">15–20 hrs</div>
        <div class="text-xs text-gray-500 mt-1">Full workday</div>
      </div>

      <div class="glass-card p-6">
        <div class="w-12 h-12 bg-orange-500/15 rounded-xl flex items-center justify-center mb-4">
          <i data-lucide="tv" style="width:1.5rem;height:1.5rem;color:#fb923c"></i>
        </div>
        <h3 class="text-lg font-semibold mb-2">55" LED TV + Streaming</h3>
        <p class="text-gray-400 text-sm mb-4">~80–120W TV + streaming device.</p>
        <div class="text-3xl font-bold text-electric-400 font-mono">30–40 hrs</div>
        <div class="text-xs text-gray-500 mt-1">Binge-watch ready</div>
      </div>

      <div class="glass-card p-6">
        <div class="w-12 h-12 bg-red-500/15 rounded-xl flex items-center justify-center mb-4">
          <i data-lucide="wind" style="width:1.5rem;height:1.5rem;color:#f87171"></i>
        </div>
        <h3 class="text-lg font-semibold mb-2">Window AC Unit</h3>
        <p class="text-gray-400 text-sm mb-4">5,000 BTU window AC (~600W continuous).</p>
        <div class="text-3xl font-bold text-electric-400 font-mono">5–7 hrs</div>
        <div class="text-xs text-gray-500 mt-1">Duty cycling</div>
      </div>
    </div>
  </section>
'''
    
    faqs = build_faq_section(
        title="Frequently Asked Questions",
        subtitle="Common questions about the EcoFlow Delta Pro 3.",
        faqs=[
            ("How many solar panels can I connect to the Delta Pro 3?", "The Delta Pro 3 supports up to 1,600W of solar input across two XT60 ports. Each port handles up to 800W with a voltage range of 12–120V. Most users pair it with 2–4 × 400W panels in series. Remember: real-world output is ~70% of panel rating in good sun."),
            ("Can I use the Delta Pro 3 as a whole-home backup?", "It can power critical circuits during an outage — fridge, lights, internet, TV, a few small appliances. But it's not a whole-home system. For that, you'd need the expanded version (up to 24 kWh with extra batteries) paired with a transfer switch connected to essential circuits. A 4,096 Wh unit alone will run essential loads for 1–2 days."),
            ("How long does the battery really last?", "EcoFlow rates the LFP battery at 4,000 cycles to 80% capacity. If you use one full charge per week (common for backup/camping), that's roughly 77 years. Even with daily use, it's 11+ years. Realistically, the inverter or BMS electronics will likely fail before the battery cells in most use cases."),
            ("Is the UPS mode really 0ms transfer?", "Yes — EcoFlow uses an online double-conversion topology in UPS mode, meaning the inverter is always running and there is zero transfer time when grid power fails. This protects sensitive electronics like computers, gaming consoles, and medical equipment. Most competitors use a standby topology with 10–30ms transfer."),
            ("Can I expand the Delta Pro 3 with extra batteries?", "Yes — you can add up to 2 EcoFlow Extra Batteries (each 4,096 Wh) for a total of 12,288 Wh. They connect in series via a dedicated port. You can also use the EcoFlow Double Voltage Hub to connect two Delta Pro 3 units for 240V output at up to 8,000W."),
        ]
    )
    
    cta = build_cta(
        title="More EcoFlow Delta Pro 3 Resources",
        description="Error code reference, troubleshooting guides, and power station comparisons.",
        buttons=[
            ("Power Station Comparison", "outdoor-power.html", "primary"),
            ("Troubleshooting Guide", "../troubleshooting/power-station-wont-turn-on.html", "secondary"),
            ("BMS Error Codes", "../troubleshooting/power-station-bms-error.html", "ghost"),
        ]
    )
    
    footer = get_footer(depth)
    
    content = head + header + breadcrumb + hero_html + spec_table + perf_html + faqs + cta + footer
    write_file(f"{WORKSPACE}/pages/specs/ecoflow-delta-pro-3.html", content)
    print("✓ ecoflow-delta-pro-3.html 生成完成")


# ============================================================
# 6. DJI Mini 5 Pro 产品详情页（新增）
# ============================================================

def generate_dji_mini_5_pro():
    depth = 2
    head = get_head_template(depth).replace("{{title}}", "DJI Mini 5 Pro Spec Sheet — 1-Inch CMOS, 4K/120fps, 52 Min Flight, Omnidirectional Sensing | TechSpecsHub")
    head = head.replace("{{description}}", "Complete DJI Mini 5 Pro specifications: 1-inch CMOS sensor, 4K/120fps HDR video, 52-minute max flight time, omnidirectional obstacle sensing, O4 transmission, sub-249g weight.")
    head = head.replace("{{canonical}}", "https://powerspecshub.com/pages/specs/dji-mini-5-pro.html")
    
    header = get_header_nav(depth)
    breadcrumb = build_breadcrumb([
        ("Home", "../../index.html"),
        ("Specs", "../error-code-db.html"),
        ("Drones & UAV", "drones.html"),
        ("DJI Mini 5 Pro", None)
    ])
    
    hero_html = f'''  <!-- PRODUCT HERO -->
  <section class="relative pt-6 pb-16">
    <div class="absolute inset-0 pointer-events-none overflow-hidden">
      <div class="absolute top-0 right-1/3 w-[400px] h-[400px] bg-electric-500/10 rounded-full blur-3xl"></div>
    </div>
    <div class="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid md:grid-cols-2 gap-10 items-center">
        <div>
          <div class="inline-flex items-center gap-2 px-3 py-1.5 bg-green-500/10 border border-green-500/30 rounded-full text-xs font-semibold text-green-400 mb-4 tracking-wide uppercase">
            <i data-lucide="award" style="width:0.85rem;height:0.85rem"></i>
            Best Sub-250g Drone · 2026
          </div>
          <h1 class="font-bold text-4xl md:text-5xl mb-4 leading-[1.1] tracking-tight">
            DJI Mini 5 Pro
          </h1>
          <p class="text-lg text-gray-400 mb-6 leading-relaxed">
            The first sub-250g drone with a 1-inch CMOS sensor and 4K/120fps HDR video. 52-minute flight time, omnidirectional obstacle sensing, and 225-degree gimbal tilt — all under the 249g FAA registration threshold.
          </p>
          <div class="grid grid-cols-2 gap-3 mb-6">
            <div class="glass-card p-4">
              <div class="text-2xl font-bold text-electric-400 font-mono">1-inch</div>
              <div class="text-xs text-gray-500 mt-1">CMOS Sensor</div>
            </div>
            <div class="glass-card p-4">
              <div class="text-2xl font-bold text-electric-400 font-mono">52 min</div>
              <div class="text-xs text-gray-500 mt-1">Max Flight Time</div>
            </div>
            <div class="glass-card p-4">
              <div class="text-2xl font-bold text-electric-400 font-mono">249g</div>
              <div class="text-xs text-gray-500 mt-1">Weight (under 250g)</div>
            </div>
            <div class="glass-card p-4">
              <div class="text-2xl font-bold text-electric-400 font-mono">Omni</div>
              <div class="text-xs text-gray-500 mt-1">Obstacle Sensing</div>
            </div>
          </div>
          <div class="flex flex-wrap gap-3">
            <span class="px-3 py-1 bg-white/5 rounded-full text-xs text-gray-300">1-Inch CMOS</span>
            <span class="px-3 py-1 bg-white/5 rounded-full text-xs text-gray-300">4K/120fps HDR</span>
            <span class="px-3 py-1 bg-white/5 rounded-full text-xs text-gray-300">O4 Transmission</span>
            <span class="px-3 py-1 bg-white/5 rounded-full text-xs text-gray-300">ActiveTrack 360</span>
          </div>
        </div>
        <div class="glass-card p-6 text-center">
          <div class="text-6xl mb-2">🚁</div>
          <div class="text-sm text-gray-500 mb-1">Fly More Combo Price</div>
          <div class="text-4xl font-bold text-white font-mono">$999</div>
          <div class="text-sm text-gray-400 mt-2">Standard: $799</div>
        </div>
      </div>
    </div>
  </section>
'''
    
    spec_table = build_table_section(
        title="Full Specifications",
        subtitle="Complete technical specifications for the DJI Mini 5 Pro.",
        headers=["Category", "Specification"],
        rows=[
            ['<span class="font-semibold">Weight</span>', '249 g (including battery, gimbal cover, and propellers)'],
            ['<span class="font-semibold">Dimensions (Folded)</span>', '145.5 × 90.8 × 64.5 mm (5.73 × 3.57 × 2.54 in)'],
            ['<span class="font-semibold">Dimensions (Unfolded)</span>', '259.4 × 233.2 × 71 mm (10.21 × 9.18 × 2.80 in)'],
            ['<span class="font-semibold">FAA Registration</span>', '<span class="text-green-400">Not required for recreational use</span> (under 250g)'],
            ['<span class="font-semibold">Camera Sensor</span>', '1-inch CMOS, 50 MP effective pixels'],
            ['<span class="font-semibold">Lens</span>', 'f/2.8 aperture, 24mm equivalent focal length (35mm format)'],
            ['<span class="font-semibold">Photo Resolutions</span>', '50 MP, 24 MP (pixel-binned), 12 MP'],
            ['<span class="font-semibold">Photo Formats</span>', 'JPEG, DNG (RAW), JPEG + DNG'],
            ['<span class="font-semibold">Video Resolutions</span>', '4K: 3840×2160 @ 24/25/30/48/50/60/100/120 fps'],
            ['<span class="font-semibold">Video Formats</span>', 'MP4, MOV (H.264, H.265)'],
            ['<span class="font-semibold">HDR</span>', 'D-Log M, HLG, Normal 10-bit color'],
            ['<span class="font-semibold">Gimbal</span>', '3-axis mechanical gimbal, 225° tilt range'],
            ['<span class="font-semibold">Gimbal Rotation Speed</span>', '120°/s (Tilt), 180°/s (Pan)'],
            ['<span class="font-semibold">Max Flight Time</span>', '52 minutes (no wind, 4.5 m/s constant speed)'],
            ['<span class="font-semibold">Hover Time</span>', '49 minutes'],
            ['<span class="font-semibold">Max Flight Distance</span>', '20 km (O4 transmission range)'],
            ['<span class="font-semibold">Max Speed</span>', '16 m/s (S-mode) / 10 m/s (N-mode)'],
            ['<span class="font-semibold">Max Wind Resistance</span>', '10.7 m/s (Force 6)'],
            ['<span class="font-semibold">Operating Temperature</span>', '-10°C to 40°C (14°F to 104°F)'],
            ['<span class="font-semibold">Battery Capacity</span>', '3,850 mAh, 7.7 V LiPo HV'],
            ['<span class="font-semibold">Charging Time</span>', '~64 minutes (18W USB-C PD)'],
            ['<span class="font-semibold">Obstacle Sensing</span>', 'Omnidirectional (forward, backward, left, right, upward, downward)'],
            ['<span class="font-semibold">Sensing System</span>', 'Stereo vision + infrared (downward)'],
            ['<span class="font-semibold">Video Transmission</span>', 'DJI O4, 20 km max range (FCC), 1080p/60fps'],
            ['<span class="font-semibold">GPS</span>', 'GPS + GLONASS + Galileo + BeiDou'],
            ['<span class="font-semibold">Return to Home</span>', 'Smart RTH, Low Battery RTH, Failsafe RTH'],
            ['<span class="font-semibold">ActiveTrack</span>', 'ActiveTrack 360°, 360° subject tracking with all-direction obstacle avoidance'],
            ['<span class="font-semibold">QuickShots</span>', 'Dronie, Circle, Helix, Rocket, Boomerang, Asteroid'],
            ['<span class="font-semibold">Panoramas</span>', '180° Wide, 360° Sphere, Vertical, Wide'],
            ['<span class="font-semibold">App</span>', 'DJI Fly (iOS 13.0+ / Android 9.0+)'],
            ['<span class="font-semibold">Memory Card Slot</span>', 'microSD (up to 512 GB, UHS-I Speed Grade 3 recommended)'],
            ['<span class="font-semibold">Internal Storage</span>', '12 GB'],
            ['<span class="font-semibold">Warranty</span>', '12 months standard, DJI Care Refresh available'],
        ]
    )
    
    features = build_feature_cards(
        title="Key Features",
        subtitle="What makes the Mini 5 Pro a step up from the Mini 4 Pro.",
        features=[
            ("camera", "1-Inch CMOS Sensor", "The first sub-250g drone with a 1-inch sensor. Dramatically better low-light performance, more dynamic range, and 50MP photos. A genuine leap in image quality for this weight class."),
            ("film", "4K/120fps Slow Motion", "Smooth 120fps footage at 4K resolution for cinematic slow motion. Combined with the 1-inch sensor, low-light slow motion is actually usable — not just a marketing feature."),
            ("shield-alert", "Omnidirectional Sensing", "Full 360° obstacle detection — forward, backward, left, right, upward, and downward. The #1 feature that prevents crashes. Essential for active tracking and cinematic movements."),
            ("gauge", "52-Minute Flight Time", "Unheard of for a sub-250g drone. The previous Mini 4 Pro maxed at 34/45 minutes (standard/Plus). 52 minutes means fewer battery swaps and more shooting time per flight."),
            ("rotate-cw", "225° Gimbal Tilt", "The gimbal can tilt from straight down to 45° upward — a 225° total range. Shoot straight down, straight ahead, or look up at subjects. Great for creative angles."),
            ("wifi", "O4 Video Transmission", "20km range with rock-solid signal stability in cluttered environments. Far better than O2/O3 for urban areas. You'll rarely get video breakup within normal flying distances."),
        ]
    )
    
    faqs = build_faq_section(
        title="Frequently Asked Questions",
        subtitle="Common questions about the DJI Mini 5 Pro.",
        faqs=[
            ("Is the DJI Mini 5 Pro really 249 grams?", "Yes — with the standard battery, gimbal cover, and propellers installed, it weighs exactly 249g. This means no FAA registration for recreational use in the US (you still need the TRUST test and must follow airspace rules). The Fly More Combo includes two additional batteries."),
            ("How does the 1-inch sensor compare to the Mini 4 Pro's 1/1.3-inch?", "The 1-inch sensor has roughly 2.5x the surface area of a 1/1.3-inch sensor. This translates to noticeably better low-light performance (less noise), more dynamic range (better highlights and shadows), and more detailed 50MP photos. The difference is clearly visible when viewing on a large screen."),
            ("Can I use Mini 4 Pro batteries with the Mini 5 Pro?", "No — the Mini 5 Pro uses a new higher-capacity 3,850 mAh battery with a different connector design. The Mini 4 Pro Plus battery was 2,590 mAh (standard) / 3,850 mAh (Plus). Accessories like ND filters and propellers are also different due to the larger camera and redesigned motor arms."),
            ("How good is ActiveTrack 360 on the Mini 5 Pro?", "It's significantly improved over the Mini 4 Pro. The combination of omnidirectional obstacle sensing and the 360° tracking algorithm means the drone can circle around subjects while avoiding obstacles in all directions. It handles trees and complex environments much better than previous generations."),
            ("Is the Mini 5 Pro worth upgrading from the Mini 4 Pro?", "If you primarily shoot in good daylight and the Mini 4 Pro meets your needs, the upgrade is marginal. But if you shoot a lot of low-light footage, want 4K/120fps slow motion, need the extra flight time, or value the 225° gimbal tilt for creative work — yes, it's a meaningful upgrade."),
        ]
    )
    
    cta = build_cta(
        title="More DJI Drone Resources",
        description="Gimbal error guides, battery troubleshooting, and complete drone comparisons.",
        buttons=[
            ("Drone Comparison", "drones.html", "primary"),
            ("Gimbal Error Codes", "../troubleshooting/dji-gimbal-error-codes.html", "secondary"),
            ("Battery Troubleshooting", "../troubleshooting/dji-battery-not-charging.html", "ghost"),
        ]
    )
    
    footer = get_footer(depth)
    
    content = head + header + breadcrumb + hero_html + spec_table + features + faqs + cta + footer
    write_file(f"{WORKSPACE}/pages/specs/dji-mini-5-pro.html", content)
    print("✓ dji-mini-5-pro.html 生成完成 (新增)")


# ============================================================
# 主函数
# ============================================================

def main():
    print("=" * 60)
    print("  扩展高搜索量页面内容")
    print("=" * 60)
    print()
    
    generate_outdoor_power()
    generate_hybrid_cars()
    generate_drones()
    generate_smart_home()
    generate_ecoflow_delta_pro_3()
    generate_dji_mini_5_pro()
    
    print()
    print("=" * 60)
    print("  ✓ 全部生成完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
