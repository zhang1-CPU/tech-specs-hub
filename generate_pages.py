#!/usr/bin/env python3
"""Generate 20 SEO pages for TechSpecsHub."""

import os

OUTPUT_DIR = "/workspace/pages/specs"

def read_template():
    with open(os.path.join(OUTPUT_DIR, "portable-power-station-eco-mode.html"), "r") as f:
        return f.read()

# ===== OUTDOOR POWER PAGES =====

outdoor_power_pages = [
    {
        "filename": "how-to-charge-power-station-without-electricity.html",
        "title": "How to Charge a Portable Power Station Without Electricity (2026)",
        "meta_description": "Learn all the ways to charge a portable power station without grid electricity: solar panels, car charging, generators, wind power, hand cranks, and more. Complete guide for off-grid living.",
        "breadcrumb_current": "Charging Without Electricity",
        "hero_badges": [
            ("OFF-GRID", "green"),
            ("Battery Saving", "info"),
            ("All Brands", "info"),
        ],
        "hero_title": 'How to Charge a Portable Power Station Without Electricity &mdash; <span class="gradient-text">Complete 2026 Guide</span>',
        "hero_intro": "Whether you are camping off-grid, preparing for a long-term power outage, or living a fully off-grid lifestyle, knowing how to charge your power station without access to wall electricity is essential. Solar is the most popular method, but it is far from the only one. This guide covers every charging method available — from rooftop solar to car charging, generators, wind turbines, hand cranks, and even more creative solutions. We break down the pros, cons, costs, and charging speeds of each method so you can build the ultimate off-grid charging setup.",
        "hero_stats": [
            ("Fastest Method", "Generator", "yellow"),
            ("Most Popular", "Solar Panels", "green"),
            ("Slowest Method", "Hand Crank", "red"),
            ("Most Portable", "Car Charging", "electric"),
        ],
        "quick_answer_title": "Quick Answer: How to Charge Without Electricity",
        "quick_answer_text": "The most practical way to charge a portable power station without grid electricity is using solar panels — they are silent, have zero fuel cost, and work anywhere with sunlight. For faster charging, a gas or propane generator fills the battery quickest but requires fuel and makes noise. For short trips or emergencies, car charging via the 12V cigarette lighter port works while you drive. Wind turbines, hand cranks, and fuel cells are niche options for specific use cases.",
        "toc_items": [
            ("solar-charging", "Solar Panel Charging (Most Popular)"),
            ("car-charging", "Car / Vehicle Charging"),
            ("generator-charging", "Gas & Propane Generator Charging"),
            ("wind-charging", "Wind Turbine Charging"),
            ("hand-crank", "Hand Crank & Manual Charging"),
            ("other-methods", "Other Creative Methods"),
            ("comparison", "Method Comparison & Speed Chart"),
            ("off-grid-tips", "Off-Grid Charging Tips"),
            ("pro-tips", "Pro Tips & Best Practices"),
            ("faq", "Frequently Asked Questions"),
            ("related", "Related Guides"),
        ],
        "sections": [
            {
                "id": "solar-charging",
                "title": "Solar Panel Charging (Most Popular Method)",
                "content": [
                    "Solar charging is the most popular and practical way to charge a portable power station off-grid. It is silent, requires no fuel, and with enough panels, you can fully recharge even large stations in a single day of good sun. Every major portable power station brand supports solar charging via an MPPT charge controller built into the unit.",
                    "The basic setup is simple: connect one or more solar panels to the solar input port on your power station using the appropriate cable. The MPPT controller inside the station automatically converts the variable DC output from the panels into the correct voltage to charge the battery. Most stations display real-time solar wattage on the screen or in the app.",
                    "How much solar do you need? It depends on your station's capacity and how fast you want to charge. As a rule of thumb:",
                    [
                        "type": "table",
                        "headers": ["Station Size", "100W Panel", "200W Panel", "400W Panel"],
                        "rows": [
                            ["500Wh", "5-6 hrs full sun", "2.5-3 hrs", "~1.5 hrs"],
                            ["1,000Wh", "10-12 hrs", "5-6 hrs", "2.5-3 hrs"],
                            ["2,000Wh", "20-24 hrs", "10-12 hrs", "5-6 hrs"],
                            ["4,000Wh", "40+ hrs", "20+ hrs", "10-12 hrs"],
                        ],
                    ],
                    "Real-world charging is usually slower than the math suggests due to angle, temperature, shading, and panel inefficiency. Expect 70-80% of the panel's rated wattage in optimal conditions.",
                    [
                        "type": "alert",
                        "class": "alert-info",
                        "icon": "lightbulb",
                        "title": "Pro tip",
                        "text": "To maximize solar charging speed, tilt your panels at roughly your latitude angle, face them directly at the sun, and avoid any shading — even partial shading on one panel cell can drastically reduce output from the entire string.",
                    ],
                ],
            },
            {
                "id": "car-charging",
                "title": "Car / Vehicle Charging (Great for Road Trips)",
                "content": [
                    "Car charging is one of the most underrated off-grid charging methods. If you are driving anyway, you can top up your power station for free using your vehicle's alternator. Most power stations come with a 12V car charger cable that plugs into the cigarette lighter port.",
                    "Charging speed from a car is typically 100-200W — slower than wall charging but steady and free while you drive. A 1,000Wh station takes roughly 5-10 hours of driving to fully charge from a car. This makes it perfect for road trips where you drive during the day and use the power station at camp at night.",
                    "Important considerations for car charging:",
                    [
                        "type": "list",
                        "items": [
                            "Your car must be running to charge at full speed — with the engine off, you risk draining your car battery",
                            "Most cars limit the 12V port to 100-150W even if your station can accept more",
                            "Some power stations support faster charging via direct battery terminal connection (Anderson plugs)",
                            "Charging while driving puts minimal extra load on your alternator — usually not a concern",
                            "Check your car manual for the 12V port wattage limit before using",
                        ],
                    ],
                    [
                        "type": "alert",
                        "class": "alert-warning",
                        "icon": "alert-triangle",
                        "title": "Safety note",
                        "text": "Never charge a power station from your car battery with the engine off for extended periods. You could drain the car battery enough that it will not start. If you need to charge while parked, use a battery isolator or start the engine periodically.",
                    ],
                ],
            },
            {
                "id": "generator-charging",
                "title": "Gas & Propane Generator Charging (Fastest Method)",
                "content": [
                    "When you need the fastest possible charging without grid power, a portable generator is the answer. Generators can charge even the largest power stations in 1-2 hours. They are the go-to option for emergency backup where speed matters more than fuel cost or noise.",
                    "To charge with a generator, simply plug the power station's AC charging cable into the generator's AC outlet, exactly like you would plug into a wall. Most power stations charge at their maximum AC charge rate when connected to a generator — 500W to 3,000W depending on the model.",
                    "Generator sizing: you only need a generator that can output more than your power station's maximum AC charge rate. For example, if your station charges at 1,800W max, a 2,000W generator is sufficient. You do not need a massive generator just for charging.",
                    "Pros and cons of generator charging:",
                    [
                        "type": "grid",
                        "items": [
                            ("Pros", "green", [
                                "Fastest charging speed available",
                                "Works day or night, rain or shine",
                                "Portable — bring it anywhere",
                                "Pair with solar for hybrid off-grid",
                            ]),
                            ("Cons", "red", [
                                "Requires fuel (gas, propane, diesel)",
                                "Noisy — 60-90 dB typical",
                                "Fuel storage and safety concerns",
                                "Ongoing fuel cost per kWh",
                                "Emissions — cannot use indoors",
                            ]),
                        ],
                    ],
                    [
                        "type": "alert",
                        "class": "alert-critical",
                        "icon": "alert-octagon",
                        "title": "Critical safety",
                        "text": "Never run a generator indoors, in a garage, or near open windows. Carbon monoxide poisoning from generators kills hundreds of people every year. Always place generators at least 20 feet from buildings with the exhaust pointed away.",
                    ],
                ],
            },
            {
                "id": "wind-charging",
                "title": "Wind Turbine Charging (Niche but Useful)",
                "content": [
                    "Wind charging is less common than solar for portable power stations but can be useful in certain situations — particularly if you camp in consistently windy areas or need overnight charging. Small portable wind turbines (100-500W) can charge a power station directly, though most require a separate charge controller.",
                    "The biggest advantage of wind over solar is that it works at night and in cloudy weather. If you have consistent wind, a turbine can keep your battery topped up 24/7. The disadvantages are bulk, noise, and the fact that wind is less predictable than solar in most locations.",
                    "What to know about wind charging:",
                    [
                        "type": "list",
                        "items": [
                            "Most portable wind turbines are 100-400W — equivalent to 1-2 solar panels",
                            "Output is highly dependent on wind speed — turbines are rated at specific wind speeds (usually 10-15 m/s)",
                            "Real-world output is often 20-50% of rated power in typical camping wind",
                            "You need a proper charge controller between the turbine and power station",
                            "Turbines must be mounted on a pole or tripod high enough to catch clean wind",
                            "Portability varies — some fold up small, others are quite bulky",
                        ],
                    ],
                    "Wind + solar hybrid systems are the gold standard for long-term off-grid setups. Solar handles daytime charging while wind contributes overnight and on cloudy days. Together they provide much more consistent power than either alone.",
                ],
            },
            {
                "id": "hand-crank",
                "title": "Hand Crank & Manual Charging (Emergency Only)",
                "content": [
                    "Hand crank charging is exactly what it sounds like — turning a crank by hand to generate electricity. While it sounds primitive, it can be a lifesaver in true emergency situations where you have no other options. That said, the amount of power you can generate by hand is surprisingly small.",
                    "A healthy adult cranking vigorously can produce about 50-100W of mechanical power, which translates to roughly 20-50W of electrical power after losses. To put that in perspective: cranking for one hour might add 20-50Wh to your battery, enough for a few phone charges or a few minutes of AC power. It would take 20-50 hours of continuous cranking to charge a 1,000Wh station.",
                    "Hand crank options:",
                    [
                        "type": "list",
                        "items": [
                            "Built-in hand cranks: a few emergency power stations have integrated cranks, usually 10-30W max",
                            "Portable crank generators: separate units that plug into your station, 30-100W output",
                            "Bicycle generators: use a regular bike on a trainer stand to generate power, 50-200W depending on fitness",
                            "Emergency radios with cranks: tiny cranks for radios/phones, not useful for power stations",
                        ],
                    ],
                    [
                        "type": "alert",
                        "class": "alert-warning",
                        "icon": "alert-triangle",
                        "title": "Reality check",
                        "text": "Hand crank charging is an emergency last resort, not a practical daily charging method. If you are considering it for regular use, save your money and buy an extra solar panel instead. You will get far more power with far less effort.",
                    ],
                ],
            },
            {
                "id": "other-methods",
                "title": "Other Creative Charging Methods",
                "content": [
                    "Beyond the main four methods (solar, car, generator, wind), there are several other ways to charge a power station without grid electricity. Some are practical, some are niche, and some are just fun to know about.",
                    "Fuel cell charging: Hydrogen fuel cells are an emerging technology for portable power. They run on hydrogen canisters and produce electricity silently with only water as a byproduct. Current portable fuel cells are expensive and hydrogen is hard to find, but they may become more common in the future.",
                    "Thermoelectric generators: These generate electricity from a temperature difference — typically from a wood stove or campfire. A thermoelectric generator sits on your stove and uses the heat difference between the hot side (stove) and cold side (air or water) to produce power. Output is modest (10-50W) but can be useful if you are running a wood stove anyway.",
                    "Water/hydro charging: Small portable hydro turbines can charge from a stream or river if you camp near moving water. Like wind, hydro works 24/7 if you have consistent flow. Portable hydro turbines for power stations are available but not widely used.",
                    "Battery swapping: Not exactly charging, but you can bring extra fully-charged batteries. Many modular power stations (like EcoFlow Delta Pro or Bluetti AC500) let you swap battery modules. Bring extra charged batteries from home and swap them as needed — zero charging time, just swap and go.",
                ],
            },
            {
                "id": "comparison",
                "title": "Method Comparison — Speed, Cost, and Practicality",
                "content": [
                    "Here is how all the charging methods compare across key factors:",
                    [
                        "type": "table",
                        "headers": ["Method", "Speed", "Cost", "Fuel Cost", "Portability", "Best For"],
                        "rows": [
                            ["Solar Panels", "Slow-Medium", "Medium ($200-800)", "$0", "Good", "Daily off-grid use"],
                            ["Car Charging", "Slow", "Low ($20-50)", "Minimal", "Excellent", "Road trips"],
                            ["Generator", "Very Fast", "Medium ($300-1000)", "High", "Good", "Emergency backup"],
                            ["Wind Turbine", "Slow", "Medium-High", "$0", "Fair", "Windy locations"],
                            ["Hand Crank", "Very Slow", "Low", "$0", "Good", "Emergency only"],
                            ["Fuel Cell", "Medium", "Very High", "High", "Good", "Specialized use"],
                            ["Battery Swap", "Instant", "Very High", "$0", "Fair", "Short trips with prep"],
                        ],
                    ],
                    "The best method for you depends entirely on your situation. For most people, solar + car charging covers 90% of off-grid scenarios. Add a generator if you need fast backup charging for emergencies.",
                ],
            },
            {
                "id": "off-grid-tips",
                "title": "Off-Grid Charging Tips & Strategies",
                "content": [
                    "Whether you are a weekend camper or full-time off-gridder, these strategies will help you get the most out of your off-grid charging setup.",
                    [
                        "type": "grid",
                        "items": [
                            ("Charge During Peak Sun", "yellow", "Solar panels produce the most power between 10 AM and 3 PM. Plan your high-power activities around this window — run appliances, charge devices, and fill up the battery when the sun is strongest."),
                            ("Use a Solar Mount", "green", "Folding panels laid on the ground are convenient but inefficient. Even a simple tilt mount can increase output by 20-30% by getting the panels perpendicular to the sun. For best results, adjust the angle a few times per day."),
                            ("Combine Methods", "electric", "The best off-grid setups use multiple charging methods. Solar for daytime, generator for cloudy days or quick top-ups, car charging on travel days. Having redundancy means you never run out of power."),
                            ("Monitor Usage", "info", "Use your power station's app or display to track usage patterns. Understanding how much power you use each day helps you size your solar array and battery bank correctly."),
                            ("Start with Full Battery", "green", "Always start your trip with a 100% charge from the grid. Think of your battery as a full gas tank — you want to leave home full and only use alternative charging to extend your trip, not start from empty."),
                            ("Minimize Power Use", "yellow", "The easiest way to make your battery last is to use less power. Switch to LED lighting, use efficient appliances, and turn things off when not in use. Every watt you save is a watt you do not need to generate."),
                        ],
                    ],
                ],
            },
            {
                "id": "pro-tips",
                "title": "Pro Tips & Advanced Techniques",
                "content": [
                    "These advanced tips come from experienced off-grid users and can take your charging setup to the next level.",
                    [
                        "type": "grid",
                        "items": [
                            ("String Panels in Series", "electric", "Most MPPT controllers support higher voltage solar inputs. Wiring panels in series (positive to negative) increases voltage and reduces current loss through long cables. Check your station's maximum solar input voltage before wiring."),
                            ("Use Proper Cable Gauge", "yellow", "Thin cables cause voltage drop, especially with solar panels far from the station. Use 12AWG or thicker cables for solar runs longer than 10 feet. The thicker the cable, the more power reaches your battery."),
                            ("Clean Panels Regularly", "green", "Dust, dirt, and bird droppings on solar panels can reduce output by 10-30%. Wipe them down with a soft cloth periodically — especially if you camp in dusty or wooded areas."),
                            ("Charge While You Drive", "info", "On road trips, plug in your power station as soon as you start driving. Even 2-3 hours of driving can add significant charge. Combine with solar at camp and you might never need to plug into the grid."),
                            ("Size for Worst Case", "red", "When planning your off-grid setup, size your solar and battery for the worst conditions — shortest winter days, cloudy weather, higher-than-expected usage. Oversize by 30-50% and you will rarely run into trouble."),
                            ("Use Pass-Through Charging", "electric", "Most modern power stations support pass-through charging — using power while the battery charges. This means you can run devices directly from solar/generator without draining the battery, which is more efficient."),
                        ],
                    ],
                ],
            },
        ],
        "faqs": [
            {
                "question": "What is the fastest way to charge a power station without electricity?",
                "answer": "A gas or propane generator is the fastest way to charge a portable power station off-grid. Most generators can supply enough power to charge a station at its maximum AC charge rate — typically 500-3,000W depending on the model. A 2,000Wh station with 1,800W charging can go from 0-80% in about an hour with a generator.",
            },
            {
                "question": "Can you charge a power station with solar and AC at the same time?",
                "answer": "Yes, most modern portable power stations support simultaneous charging from multiple sources. You can charge from solar panels and AC (wall or generator) at the same time, and many stations also support car charging simultaneously. This is often called dual or multi-source charging and it fills the battery faster than any single source alone.",
            },
            {
                "question": "How long does it take to charge a power station with a 100W solar panel?",
                "answer": "It depends on the station size and sun conditions. A 100W panel produces roughly 60-80W in real use. A 500Wh station takes about 7-9 hours of good sun. A 1,000Wh station takes 14-18 hours. A 2,000Wh station takes 28-36 hours. In practice, you get about 4-6 hours of peak sun per day, so plan accordingly.",
            },
            {
                "question": "Can you charge a power station while it is in use?",
                "answer": "Yes, nearly all modern portable power stations support pass-through charging — you can use the output ports while the battery is charging. Some budget models do not support this, or they limit output while charging, but all major brands (EcoFlow, Jackery, Bluetti, Anker) support full pass-through on their current models.",
            },
            {
                "question": "Will car charging drain my car battery?",
                "answer": "If your engine is running, no — the alternator powers the charging and keeps the car battery topped up. If the engine is off, yes, charging will slowly drain your car battery. Most car ports shut off automatically when the ignition is off, but some do not. To be safe, only charge from your car while the engine is running, or use a battery isolator.",
            },
            {
                "question": "How many solar panels do I need to charge a 2000W power station?",
                "answer": "It depends on how fast you want to charge and how much sun you get. For a full charge in one day (5-6 hours of peak sun), you need roughly 400-500W of solar panels for a 2,000Wh station. For two days, 200-250W works. Always oversize slightly for real-world conditions — panel output is rarely 100% of rated power.",
            },
            {
                "question": "Can you charge a Bluetti/EcoFlow/Jackery with solar panels?",
                "answer": "Yes, all major portable power station brands support solar charging. EcoFlow, Bluetti, Jackery, Anker, and Goal Zero all have built-in MPPT solar charge controllers. Each brand uses its own solar connector, so make sure you get the right cable or adapter for your station.",
            },
            {
                "question": "What is MPPT and why does it matter?",
                "answer": "MPPT (Maximum Power Point Tracking) is a technology that maximizes the power output from solar panels by continuously finding the optimal voltage and current combination. It can increase charging efficiency by 20-30% compared to older PWM charge controllers, especially in partial shading or low-light conditions. All modern power stations use MPPT.",
            },
            {
                "question": "Can I use any solar panel with my power station?",
                "answer": "Generally yes, as long as the panel's voltage is within your station's acceptable input range and you have the right connector. Most stations accept 12-60V or 12-100V solar input. You may need an adapter cable if your panel uses a different connector (MC4, Anderson, XT60, etc.). Check your station's manual for the exact voltage range.",
            },
            {
                "question": "How do I charge my power station during a blackout?",
                "answer": "During a blackout, your options depend on what you have prepared. Solar panels work as long as the sun is out. A generator can charge it anytime. If you have an electric car with vehicle-to-load (V2L), you can use it as a giant power source. The key is to plan ahead — have your charging method ready before the blackout hits.",
            },
        ],
        "related_pages": [
            ("can-portable-power-station-charge-while-in-use.html", "PASS-THROUGH", "All Brands", "Pass-Through Charging Guide", "Can a power station charge and discharge at the same time? How pass-through works and limitations."),
            ("solar-charging-0w-power-station.html", "SOLAR&nbsp;0W", "Universal", "Solar 0W Troubleshooting", "Fix solar charging showing 0 watts — MPPT issues, wiring problems, panel faults."),
            ("portable-power-station-not-charging.html", "CHARGE&nbsp;FAULT", "Universal", "Not Charging Guide", "Troubleshoot AC, solar, and DC charging problems for all major brands."),
            ("lifepo4-vs-lithium-ion-power-station.html", "BATTERY", "Compare", "LiFePO4 vs Lithium-Ion", "Complete comparison of battery chemistries — lifespan, safety, cost, weight."),
            ("off-grid-solar-system-sizing-guide.html", "SOLAR&nbsp;SIZING", "Guide", "Off-Grid Solar Sizing", "Calculate exactly how many solar panels and batteries you need for off-grid."),
            ("outdoor-power.html", "COMPARE", "All Brands", "Power Station Comparison", "Compare all major portable power station models side by side."),
        ],
    },
]

def build_page(data, category="Outdoor Power", category_page="outdoor-power.html"):
    """Build a complete HTML page from structured data."""
    
    # Build hero badges
    badge_html = ""
    for text, color in data["hero_badges"]:
        badge_class = f"badge-{color}"
        icon = "battery-charging" if color == "green" else "info" if color == "info" else "alert-triangle" if color == "yellow" else "alert-circle"
        badge_html += f'        <span class="badge badge-{color}"><i data-lucide="{icon}" style="width:0.75rem;height:0.75rem"></i>{text}</span>\n'
    
    # Build hero stats
    stats_html = ""
    for label, value, color in data["hero_stats"]:
        color_class = f"text-{color}-400" if color != "electric" else "text-electric-400"
        stats_html += f'''        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-4">
          <div class="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide mb-2"><i data-lucide="activity" style="width:0.9rem;height:0.9rem"></i>{label}</div>
          <div class="font-mono font-bold text-xl {color_class}">{value}</div>
        </div>\n'''
    
    # Build TOC
    toc_html = ""
    for i, (anchor, text) in enumerate(data["toc_items"]):
        num = str(i+1).zfill(2)
        toc_html += f'        <a href="#{anchor}" class="flex items-center gap-2 p-2 rounded-lg hover:bg-white/5 text-gray-300 hover:text-white transition-all"><span class="text-electric-400 font-mono">{num}</span>{text}</a>\n'
    
    # Build sections
    sections_html = ""
    for section in data["sections"]:
        section_content = ""
        for item in section["content"]:
            if isinstance(item, str):
                section_content += f'      <p class="text-gray-300 leading-relaxed mb-4">\n        {item}\n      </p>\n'
            elif isinstance(item, dict):
                if item["type"] == "table":
                    table_rows = ""
                    for row in item["rows"]:
                        cells = "".join(f"<td>{cell}</td>" for cell in row)
                        table_rows += f"            <tr>{cells}</tr>\n"
                    headers = "".join(f"<th>{h}</th>" for h in item["headers"])
                    section_content += f'''      <div class="overflow-x-auto mb-6">
        <table class="specs-table w-full text-sm">
          <thead>
            <tr>{headers}</tr>
          </thead>
          <tbody>
{table_rows}          </tbody>
        </table>
      </div>\n'''
                elif item["type"] == "list":
                    list_items = ""
                    for li in item["items"]:
                        list_items += f'            <li>• <strong class="text-white">{li.split(":")[0]}:</strong>{":".join(li.split(":")[1:]) if ":" in li else ""}</li>\n' if ":" in li else f'            <li>• {li}</li>\n'
                    section_content += f'''      <ul class="text-sm text-gray-300 space-y-1 mb-4">
{list_items}      </ul>\n'''
                elif item["type"] == "grid":
                    grid_items = ""
                    for title, color, items in item["items"]:
                        color_class = f"text-{color}-400" if color != "electric" else "text-electric-400"
                        li_items = "".join(f"          <li>• {li}</li>\n" for li in items)
                        grid_items += f'''        <div class="bg-navy-900/80 border border-white/10 rounded-xl p-5">
          <h4 class="font-semibold {color_class} mb-2">{title}</h4>
          <ul class="text-sm text-gray-300 space-y-1">
{li_items}          </ul>
        </div>\n'''
                    section_content += f'''      <div class="grid md:grid-cols-2 gap-4 mb-4">
{grid_items}      </div>\n'''
                elif item["type"] == "alert":
                    section_content += f'''      <div class="mt-4 alert {item["class"]}">
        <i data-lucide="{item["icon"]}" style="width:1rem;height:1rem;flex-shrink:0;margin-top:0.1rem"></i>
        <p class="text-sm"><strong>{item["title"]}:</strong> {item["text"]}</p>
      </div>\n'''
        
        sections_html += f'''  <section id="{section["id"]}" class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <h2 class="font-bold text-3xl mb-5">{section["title"]}</h2>
    <div class="glass-card p-6 md:p-8">
{section_content}    </div>
  </section>\n'''
    
    # Build FAQs
    faq_json = []
    faq_html = ""
    for faq in data["faqs"]:
        faq_json.append({
            "@type": "Question",
            "name": faq["question"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["answer"],
            }
        })
        faq_html += f'''      <details class="glass-card p-5 group">
        <summary class="cursor-pointer font-semibold flex items-center justify-between gap-4">
          <span>{faq["question"]}</span>
          <i data-lucide="chevron-down" style="width:1rem;height:1rem" class="text-gray-500 group-open:rotate-180 transition-transform flex-shrink-0"></i>
        </summary>
        <p class="mt-3 text-gray-400 text-sm leading-relaxed">
          {faq["answer"]}
        </p>
      </details>\n'''
    
    # Build related pages
    related_html = ""
    for page in data["related_pages"]:
        filename, badge_text, badge_label, title, desc = page
        badge_color = "electric" if "ECO" in badge_text or "SOLAR" in badge_text or "PASS" in badge_text else "green" if "STORAGE" in badge_text or "BATTERY" in badge_text else "yellow" if "CHARGE" in badge_text or "FAST" in badge_text else "purple"
        related_html += f'''      <a href="{filename}" class="glass-card p-6 block hover:border-electric-400/50 transition-all group">
        <div class="flex items-start gap-3 mb-3">
          <div class="px-2.5 py-1 bg-{badge_color}-500/20 text-{badge_color}-400 font-mono font-semibold text-sm rounded-md border border-{badge_color}-500/30">{badge_text}</div>
          <span class="badge badge-info">{badge_label}</span>
        </div>
        <h3 class="font-bold text-lg mb-2 group-hover:text-electric-400 transition-colors">{title}</h3>
        <p class="text-sm text-gray-400">{desc}</p>
      </a>\n'''
    
    # JSON-LD
    import json
    article_json = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": data["title"],
        "description": data["meta_description"],
        "url": f"https://powerspecshub.com/pages/specs/{data['filename']}",
        "datePublished": "2026-06-25",
        "dateModified": "2026-06-25",
        "author": {
            "@type": "Organization",
            "name": "TechSpecsHub"
        },
        "publisher": {
            "@type": "Organization",
            "name": "TechSpecsHub",
            "url": "https://powerspecshub.com/"
        },
        "image": {
            "@type": "ImageObject",
            "url": "https://powerspecshub.com/assets/images/og-default.png"
        }
    }
    
    faqpage_json = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_json
    }
    
    breadcrumb_json = {
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
                "item": f"https://powerspecshub.com/pages/specs/{category_page}"
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": data["breadcrumb_current"]
            }
        ]
    }
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{data["title"]} | TechSpecsHub</title>
  <meta name="description" content="{data["meta_description"]}">
  <meta name="theme-color" content="#0a1628">
  <style>html,body{{background-color:#0a1628;color:#ffffff;margin:0;padding:0;min-height:100vh;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;line-height:1.5;-webkit-font-smoothing:antialiased}}a{{color:#22d3ee;text-decoration:none}}code,pre{{font-family:ui-monospace,monospace}}</style>

  <link rel="preconnect" href="https://cdn.tailwindcss.com">
  <link rel="preconnect" href="https://unpkg.com">
  <link rel="dns-prefetch" href="https://cdn.tailwindcss.com">
  <link rel="dns-prefetch" href="https://unpkg.com">
  <link rel="dns-prefetch" href="https://fonts.gstatic.com">

  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <link rel="canonical" href="https://powerspecshub.com/pages/specs/{data['filename']}">

  <meta property="og:title" content="{data["title"]} | TechSpecsHub">
  <meta property="og:description" content="{data["meta_description"]}">
  <meta property="og:type" content="Article">
  <meta property="og:url" content="https://powerspecshub.com/pages/specs/{data['filename']}">
  <meta property="og:image" content="https://powerspecshub.com/assets/images/og-default.png">
  <meta property="og:site_name" content="TechSpecsHub">
  <meta property="article:published_time" content="2026-06-25T00:00:00Z">
  <meta property="article:modified_time" content="2026-06-25T00:00:00Z">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{data["title"]} | TechSpecsHub">
  <meta name="twitter:description" content="{data["meta_description"]}">
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
  {json.dumps(article_json, indent=2)}
  </script>

  <script type="application/ld+json">
  {json.dumps(faqpage_json, indent=2)}
  </script>

  <script type="application/ld+json">
  {json.dumps(breadcrumb_json, indent=2)}
  </script>

</head>
<body class="bg-navy-950 text-white min-h-screen font-display">

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

  <!-- BREADCRUMB -->
  <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 pb-4">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="../../index.html">Home</a>
      <span class="breadcrumb-sep">/</span>
      <a href="{category_page}">{category}</a>
      <span class="breadcrumb-sep">/</span>
      <span class="breadcrumb-current">{data["breadcrumb_current"]}</span>
    </nav>
  </div>

  <!-- HERO -->
  <section class="relative max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-4 pb-6">
    <div class="glass-card p-8 md:p-10 overflow-hidden relative">
      <div class="absolute top-0 right-0 w-[420px] h-[420px] bg-green-500/5 rounded-full blur-3xl pointer-events-none"></div>

      <div class="relative flex flex-wrap items-center gap-3 mb-5">
{badge_html}      </div>

      <h1 class="font-bold text-4xl md:text-5xl mb-4 leading-tight">
        {data["hero_title"]}
      </h1>

      <p class="text-gray-400 text-lg leading-relaxed mb-6 max-w-3xl">
        {data["hero_intro"]}
      </p>

      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8">
{stats_html}      </div>
    </div>
  </section>

  <!-- QUICK ANSWER -->
  <section class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div class="glass-card p-6 md:p-8 bg-gradient-to-br from-green-950/20 to-navy-900 border-green-500/20">
      <h2 class="font-bold text-2xl mb-4 flex items-center gap-2"><i data-lucide="zap" style="width:1.25rem;height:1.25rem;color:#4ade80"></i>{data["quick_answer_title"]}</h2>
      <p class="text-gray-300 leading-relaxed mb-4">
        {data["quick_answer_text"]}
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
      <p class="text-gray-400">Common questions about {data["breadcrumb_current"].lower()}.</p>
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
    
    return html

def generate_page(data, category="Outdoor Power", category_page="outdoor-power.html"):
    filepath = os.path.join(OUTPUT_DIR, data["filename"])
    html = build_page(data, category, category_page)
    with open(filepath, "w") as f:
        f.write(html)
    word_count = len(html.split())
    print(f"Created: {data['filename']} ({word_count} words)")
    return word_count

if __name__ == "__main__":
    # This script will be used by the main generation code
    pass
