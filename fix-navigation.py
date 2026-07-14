#!/usr/bin/env python3
import os

NAV_FILES = {
    "/workspace/pages/master-specs.html": {
        "active": "master-specs.html",
        "active_text": "Compare"
    },
    "/workspace/pages/brand-index.html": {
        "active": "brand-index.html",
        "active_text": "Brands"
    },
    "/workspace/pages/about.html": {
        "active": "about.html",
        "active_text": "About"
    },
    "/workspace/pages/contact.html": {
        "active": "contact.html",
        "active_text": "Contact"
    },
    "/workspace/pages/privacy-policy.html": {
        "active": "privacy-policy.html",
        "active_text": "Privacy"
    }
}

def create_new_nav(active_page, active_text):
    return f"""          <div class="nav-dropdown-trigger">
            <button class="flex items-center gap-1.5 px-3 py-2 text-gray-300 hover:text-white rounded-lg hover:bg-white/5 transition-all">
              Tools & Data
              <i data-lucide="chevron-down" style="width:0.875rem;height:0.875rem"></i>
            </button>
            <div class="nav-dropdown">
              <p class="nav-dropdown-section-label">Data Resources</p>
              <a href="error-code-db.html"><i data-lucide="alert-circle" style="width:1rem;height:1rem;color:#f87171;flex-shrink:0"></i>Error Code Database</a>
              <a href="master-specs.html"><i data-lucide="table-2" style="width:1rem;height:1rem;color:#22d3ee;flex-shrink:0"></i>Master Specs Comparison</a>
              <a href="brand-index.html"><i data-lucide="building-2" style="width:1rem;height:1rem;color:#22d3ee;flex-shrink:0"></i>Brand Index A&ndash;Z</a>
              <hr class="my-2 border-white/10">
              <p class="nav-dropdown-section-label">Calculators & Guides</p>
              <a href="tools/best-multimeters-2026.html"><i data-lucide="wrench" style="width:1rem;height:1rem;color:#fbbf24;flex-shrink:0"></i>Best Multimeters 2026</a>
              <a href="tools/power-station-runtime-calculator.html"><i data-lucide="timer" style="width:1rem;height:1rem;color:#22d3ee;flex-shrink:0"></i>Runtime Calculator</a>
              <a href="tools/solar-panel-needs-calculator.html"><i data-lucide="sun" style="width:1rem;height:1rem;color:#fbbf24;flex-shrink:0"></i>Solar Calculator</a>
              <a href="tools/appliance-wattage-calculator.html"><i data-lucide="zap" style="width:1rem;height:1rem;color:#22d3ee;flex-shrink:0"></i>Wattage Calculator</a>
              <a href="tools/camping-power-calculator.html"><i data-lucide="tent" style="width:1rem;height:1rem;color:#22d3ee;flex-shrink:0"></i>Camping Calculator</a>
              <a href="tools/cpap-battery-calculator.html"><i data-lucide="heart-pulse" style="width:1rem;height:1rem;color:#f87171;flex-shrink:0"></i>CPAP Calculator</a>
              <a href="tools/drone-flight-time-calculator.html"><i data-lucide="plane" style="width:1rem;height:1rem;color:#22d3ee;flex-shrink:0"></i>Drone Flight Time</a>
            </div>
          </div>
          <a href="about.html" class="px-3 py-2 {'text-white rounded-lg bg-white/5' if active_page == 'about.html' else 'text-gray-300 hover:text-white rounded-lg hover:bg-white/5'} transition-all">About</a>"""

for filepath, config in NAV_FILES.items():
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
    
    if "Tools & Data" in html:
        print(f"Skipping (already has Tools & Data): {filepath}")
        continue
    
    pattern = r'<a href="error-code-db\.html"[^>]*>Error Codes</a>\s*<a href="master-specs\.html"[^>]*>Compare</a>\s*<a href="brand-index\.html"[^>]*>Brands</a>\s*<a href="about\.html"[^>]*>About</a>'
    
    import re
    match = re.search(pattern, html, re.DOTALL)
    
    if match:
        new_nav = create_new_nav(config["active"], config["active_text"])
        html = html[:match.start()] + new_nav + html[match.end():]
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Updated navigation: {filepath}")
    else:
        print(f"Skipping (no match): {filepath}")

if __name__ == "__main__":
    pass
