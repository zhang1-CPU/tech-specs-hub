#!/usr/bin/env python3
import os
import re

def update_html_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
    
    tailwind_script = '<script src="https://cdn.tailwindcss.com" defer></script>'
    tailwind_config_start = '<script>\n    tailwind.config = {'
    tailwind_config_end = '    }\n  </script>'
    
    if tailwind_script in html and tailwind_config_start in html:
        html = html.replace(tailwind_script, '')
        
        config_start_idx = html.find(tailwind_config_start)
        config_end_idx = html.find(tailwind_config_end, config_start_idx)
        if config_start_idx != -1 and config_end_idx != -1:
            html = html[:config_start_idx] + html[config_end_idx + len(tailwind_config_end):]
        
        html = html.replace('rel="preconnect" href="https://cdn.tailwindcss.com"', '')
        html = html.replace('rel="dns-prefetch" href="https://cdn.tailwindcss.com"', '')
        
        css_link = '<link rel="stylesheet" href="assets/css/main.css">'
        if css_link in html:
            html = html.replace(css_link, '<link rel="stylesheet" href="assets/css/tailwind-compiled.css">\n  <link rel="stylesheet" href="assets/css/main.css">')
        else:
            css_link_rel = '<link rel="stylesheet" href="../assets/css/main.css">'
            if css_link_rel in html:
                html = html.replace(css_link_rel, '<link rel="stylesheet" href="../assets/css/tailwind-compiled.css">\n  <link rel="stylesheet" href="../assets/css/main.css">')
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Updated: {filepath}")
    else:
        print(f"Skipping (no Tailwind CDN): {filepath}")

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                update_html_file(filepath)

if __name__ == "__main__":
    update_html_file("/workspace/index.html")
    update_html_file("/workspace/404.html")
    process_directory("/workspace/pages")
