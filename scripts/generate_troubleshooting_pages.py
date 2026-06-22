#!/usr/bin/env python3
"""Generate 20 standalone HTML troubleshooting pages from JSON data."""

import json
import os
import textwrap

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, "troubleshooting_data.json")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "pages", "troubleshooting")

SEVERITY_STYLES = {
    "Critical": "bg-red-500/20 text-red-400 border-red-500/30",
    "Warning": "bg-amber-500/20 text-amber-400 border-amber-500/30",
    "Common": "bg-sky-500/20 text-sky-400 border-sky-500/30",
    "Info": "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
}

DIFFICULTY_STYLES = {
    "Beginner": "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
    "Intermediate": "bg-amber-500/20 text-amber-400 border-amber-500/30",
    "Advanced": "bg-red-500/20 text-red-400 border-red-500/30",
}


def escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def build_breadcrumb_json(page):
    return json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Home",
                    "item": "https://techspecshub.com/",
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "Troubleshooting",
                    "item": "https://techspecshub.com/pages/troubleshooting/",
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": page["code"],
                    "item": page["canonical"],
                },
            ],
        },
        ensure_ascii=False,
    )


def build_howto_json(page):
    steps = []
    for idx, step in enumerate(page["steps"], start=1):
        steps.append(
            {
                "@type": "HowToStep",
                "position": idx,
                "name": f"Step {idx:02d}",
                "text": step,
                "url": f"{page['canonical']}#step-{idx:02d}",
            }
        )
    return json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "HowTo",
            "name": f"How to Fix {page['code']} on {page['device_type']}",
            "description": page["meta_description"],
            "totalTime": f"PT{page['repair_time'].replace(' ', '').upper()}",
            "estimatedCost": {
                "@type": "MonetaryAmount",
                "currency": "USD",
                "value": page["diy_cost"].replace("$", ""),
            },
            "step": steps,
        },
        ensure_ascii=False,
    )


def render_page(page) -> str:
    severity_cls = SEVERITY_STYLES.get(page["severity"], SEVERITY_STYLES["Info"])
    difficulty_cls = DIFFICULTY_STYLES.get(
        page["difficulty"], DIFFICULTY_STYLES["Beginner"]
    )

    symptoms_html = "\n".join(
        f'<li class="flex items-start gap-3"><span class="text-sky-400 mt-1"><i data-lucide="alert-circle" class="w-5 h-5"></i></span><span>{escape_html(s)}</span></li>'
        for s in page["symptoms"]
    )

    tools_html = "\n".join(
        f'<li class="flex items-start gap-3"><span class="text-emerald-400 mt-1"><i data-lucide="wrench" class="w-5 h-5"></i></span><span>{escape_html(t)}</span></li>'
        for t in page["tools"]
    )

    steps_html = "\n".join(
        f'''<li id="step-{i:02d}" class="flex gap-4">
            <span class="flex-shrink-0 w-10 h-10 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center text-sky-400 font-bold">{i:02d}</span>
            <div class="pt-2">{escape_html(step)}</div>
        </li>'''
        for i, step in enumerate(page["steps"], start=1)
    )

    related_html = "\n".join(
        f'<li><a href="{r["href"]}" class="text-sky-400 hover:text-sky-300 underline underline-offset-4">{escape_html(r["text"])}</a></li>'
        for r in page["related"]
    )

    faq_html = "\n".join(
        f'''<details class="group border border-slate-700 rounded-xl bg-slate-800/40 overflow-hidden">
            <summary class="flex items-center justify-between p-4 cursor-pointer hover:bg-slate-800/60 transition-colors">
                <span class="font-semibold text-slate-100 pr-4">{escape_html(qa["q"])}</span>
                <span class="flex-shrink-0 text-sky-400"><i data-lucide="chevron-down" class="w-5 h-5 transition-transform group-open:rotate-180"></i></span>
            </summary>
            <div class="px-4 pb-4 text-slate-300 leading-relaxed">{escape_html(qa["a"])}</div>
        </details>'''
        for qa in page["faq"]
    )

    warnings_html = "\n".join(
        f'<div class="warning-box rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-red-200 flex items-start gap-3"><i data-lucide="alert-triangle" class="w-6 h-6 flex-shrink-0 text-red-400"></i><span>{escape_html(w)}</span></div>'
        for w in page.get("safety_warnings", [])
    )

    cost_table_html = ""
    if page.get("cost_table"):
        cost_table_html = f'''<div class="overflow-x-auto mt-6">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="border-b border-slate-700 text-slate-400 text-sm uppercase tracking-wider">
                        <th class="py-3 pr-4">Repair Type</th>
                        <th class="py-3 pr-4">Estimated Cost</th>
                        <th class="py-3">Notes</th>
                    </tr>
                </thead>
                <tbody class="text-slate-200">
                    <tr class="border-b border-slate-800">
                        <td class="py-3 pr-4 font-medium text-emerald-400">DIY Repair</td>
                        <td class="py-3 pr-4">{escape_html(page["diy_cost"])}</td>
                        <td class="py-3">Requires tools listed above and basic technical skills.</td>
                    </tr>
                    <tr>
                        <td class="py-3 pr-4 font-medium text-amber-400">Dealer / Professional</td>
                        <td class="py-3 pr-4">{escape_html(page["dealer_cost"])}</td>
                        <td class="py-3">Includes labor, diagnostics, and OEM parts where applicable.</td>
                    </tr>
                </tbody>
            </table>
        </div>'''

    html = textwrap.dedent(
        f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape_html(page["title"])}</title>
<meta name="description" content="{escape_html(page["meta_description"])}">
<link rel="canonical" href="{escape_html(page["canonical"])}">
<meta property="og:title" content="{escape_html(page["title"])}">
<meta property="og:description" content="{escape_html(page["meta_description"])}">
<meta property="og:url" content="{escape_html(page["canonical"])}">
<meta property="og:type" content="article">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape_html(page["title"])}">
<meta name="twitter:description" content="{escape_html(page["meta_description"])}">
<script type="application/ld+json">{build_breadcrumb_json(page)}</script>
<script type="application/ld+json">{build_howto_json(page)}</script>
<script src="https://cdn.tailwindcss.com"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<script src="https://unpkg.com/lucide@latest"></script>
<style>
    body {{ font-family: 'Inter', sans-serif; background: #0b1120; color: #e2e8f0; }}
    .glass {{ background: rgba(30, 41, 59, 0.6); backdrop-filter: blur(12px); border: 1px solid rgba(148, 163, 184, 0.1); }}
    .gradient-text {{ background: linear-gradient(135deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
    .warning-box {{ background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); color: #fecaca; }}
</style>
</head>
<body class="min-h-screen antialiased">
<header class="border-b border-slate-800/60 bg-slate-900/50 backdrop-blur">
    <div class="max-w-5xl mx-auto px-4 py-6">
        <nav aria-label="Breadcrumb" class="text-sm text-slate-400 mb-4">
            <ol class="flex flex-wrap items-center gap-2">
                <li><a href="../index.html" class="hover:text-sky-400 transition-colors">Home</a></li>
                <li><i data-lucide="chevron-right" class="w-4 h-4"></i></li>
                <li><a href="../troubleshooting/" class="hover:text-sky-400 transition-colors">Troubleshooting</a></li>
                <li><i data-lucide="chevron-right" class="w-4 h-4"></i></li>
                <li class="text-slate-200" aria-current="page">{escape_html(page["code"])}</li>
            </ol>
        </nav>
        <h1 class="text-3xl md:text-4xl font-extrabold tracking-tight gradient-text">{escape_html(page["h1"])}</h1>
    </div>
</header>

<main class="max-w-5xl mx-auto px-4 py-8 space-y-10">

    <!-- Meta badges -->
    <section class="flex flex-wrap gap-3">
        <span class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-semibold border {severity_cls}">
            <i data-lucide="shield-alert" class="w-4 h-4"></i> Severity: {escape_html(page["severity"])}
        </span>
        <span class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-semibold border {difficulty_cls}">
            <i data-lucide="gauge" class="w-4 h-4"></i> Difficulty: {escape_html(page["difficulty"])}
        </span>
        <span class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-semibold border bg-slate-800 text-slate-300 border-slate-700">
            <i data-lucide="clock" class="w-4 h-4"></i> {escape_html(page["repair_time"])}
        </span>
        <span class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-semibold border bg-slate-800 text-slate-300 border-slate-700">
            <i data-lucide="wallet" class="w-4 h-4"></i> DIY {escape_html(page["diy_cost"])}
        </span>
        <span class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-semibold border bg-slate-800 text-slate-300 border-slate-700">
            <i data-lucide="briefcase" class="w-4 h-4"></i> Dealer {escape_html(page["dealer_cost"])}
        </span>
    </section>

    {warnings_html}

    <!-- What is -->
    <section class="glass rounded-2xl p-6 md:p-8">
        <h2 class="text-2xl font-bold mb-4 flex items-center gap-3">
            <span class="w-8 h-8 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center text-sky-400"><i data-lucide="info" class="w-5 h-5"></i></span>
            What is {escape_html(page["code"])}?
        </h2>
        <div class="prose prose-invert max-w-none text-slate-300 leading-relaxed">
            <p>{escape_html(page["what_is"])}</p>
        </div>
        {cost_table_html}
    </section>

    <!-- Symptoms -->
    <section class="glass rounded-2xl p-6 md:p-8">
        <h2 class="text-2xl font-bold mb-4 flex items-center gap-3">
            <span class="w-8 h-8 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center text-sky-400"><i data-lucide="activity" class="w-5 h-5"></i></span>
            Common Symptoms
        </h2>
        <ul class="space-y-3 text-slate-300">
            {symptoms_html}
        </ul>
    </section>

    <!-- Tools -->
    <section class="glass rounded-2xl p-6 md:p-8">
        <h2 class="text-2xl font-bold mb-4 flex items-center gap-3">
            <span class="w-8 h-8 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center text-sky-400"><i data-lucide="tool" class="w-5 h-5"></i></span>
            Tools You'll Need
        </h2>
        <ul class="grid sm:grid-cols-2 gap-3 text-slate-300">
            {tools_html}
        </ul>
    </section>

    <!-- Steps -->
    <section class="glass rounded-2xl p-6 md:p-8">
        <h2 class="text-2xl font-bold mb-6 flex items-center gap-3">
            <span class="w-8 h-8 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center text-sky-400"><i data-lucide="list-ordered" class="w-5 h-5"></i></span>
            Step-by-Step Fix
        </h2>
        <ol class="space-y-6 text-slate-300">
            {steps_html}
        </ol>
    </section>

    <!-- Professional -->
    <section class="glass rounded-2xl p-6 md:p-8">
        <h2 class="text-2xl font-bold mb-4 flex items-center gap-3">
            <span class="w-8 h-8 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center text-sky-400"><i data-lucide="phone" class="w-5 h-5"></i></span>
            When to Call a Professional
        </h2>
        <p class="text-slate-300 leading-relaxed">{escape_html(page["professional_when"])}</p>
    </section>

    <!-- Related -->
    <section class="glass rounded-2xl p-6 md:p-8">
        <h2 class="text-2xl font-bold mb-4 flex items-center gap-3">
            <span class="w-8 h-8 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center text-sky-400"><i data-lucide="link" class="w-5 h-5"></i></span>
            Related Codes
        </h2>
        <ul class="space-y-2">
            {related_html}
        </ul>
        <div class="mt-6 flex flex-wrap gap-4 text-sm">
            <a href="../master-specs.html" class="inline-flex items-center gap-2 text-sky-400 hover:text-sky-300 underline underline-offset-4"><i data-lucide="book-open" class="w-4 h-4"></i> Master Specs</a>
            <a href="../error-code-db.html" class="inline-flex items-center gap-2 text-sky-400 hover:text-sky-300 underline underline-offset-4"><i data-lucide="database" class="w-4 h-4"></i> Error Code Database</a>
        </div>
    </section>

    <!-- FAQ -->
    <section class="glass rounded-2xl p-6 md:p-8">
        <h2 class="text-2xl font-bold mb-6 flex items-center gap-3">
            <span class="w-8 h-8 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center text-sky-400"><i data-lucide="help-circle" class="w-5 h-5"></i></span>
            Frequently Asked Questions
        </h2>
        <div class="space-y-4">
            {faq_html}
        </div>
    </section>

    <!-- Disclaimer -->
    <section class="rounded-2xl border border-slate-700 bg-slate-900/40 p-6 text-sm text-slate-400 leading-relaxed">
        <strong class="text-slate-200">Disclaimer:</strong> The information provided on this page is for educational and troubleshooting purposes only. Always consult your device's official manual and follow manufacturer safety guidelines. High-voltage repairs, lithium battery servicing, and drone maintenance carry inherent risks. TechSpecsHub is not liable for injury, damage, or warranty voidance resulting from DIY repairs.
    </section>

</main>

<footer class="border-t border-slate-800/60 mt-12">
    <div class="max-w-5xl mx-auto px-4 py-8 text-sm text-slate-500 flex flex-col sm:flex-row items-center justify-between gap-4">
        <span>&copy; TechSpecsHub. All rights reserved.</span>
        <div class="flex items-center gap-4">
            <a href="../master-specs.html" class="hover:text-sky-400 transition-colors">Master Specs</a>
            <a href="../error-code-db.html" class="hover:text-sky-400 transition-colors">Error Code DB</a>
        </div>
    </div>
</footer>

<script>lucide.createIcons();</script>
</body>
</html>'''
    )
    return html


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        pages = json.load(f)

    if len(pages) != 20:
        raise ValueError(f"Expected 20 pages, got {len(pages)}")

    generated = []
    for page in pages:
        html = render_page(page)
        out_path = os.path.join(OUTPUT_DIR, page["filename"])
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        generated.append(page["filename"])
        print(f"Generated: {out_path}")

    print(f"\nDone. {len(generated)} files written to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
