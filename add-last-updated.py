#!/usr/bin/env python3
import os

specs_dir = "/workspace/pages/specs"
tools_dir = "/workspace/pages/tools"
troubleshooting_dir = "/workspace/pages/troubleshooting"

all_files = []
for root, dirs, files in os.walk(specs_dir):
    for f in files:
        if f.endswith(".html"):
            all_files.append(os.path.join(root, f))

for root, dirs, files in os.walk(tools_dir):
    for f in files:
        if f.endswith(".html"):
            all_files.append(os.path.join(root, f))

for root, dirs, files in os.walk(troubleshooting_dir):
    for f in files:
        if f.endswith(".html"):
            all_files.append(os.path.join(root, f))

last_updated_html = '<div class="flex items-center gap-2 text-xs text-gray-500 mb-4"><i data-lucide="calendar" style="width:0.75rem;height:0.75rem"></i><span>Last Updated: July 14, 2026</span></div>'

updated_count = 0
skipped_count = 0

for filepath in all_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "Last Updated" in content or "last-updated" in content.lower():
        skipped_count += 1
        continue
    
    import re
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    
    if h1_match:
        insert_pos = h1_match.end()
        content = content[:insert_pos] + "\n" + last_updated_html + content[insert_pos:]
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        updated_count += 1
        print(f"Added last updated date: {os.path.basename(filepath)}")
    else:
        skipped_count += 1
        print(f"Could not find h1: {os.path.basename(filepath)}")

print(f"\nTotal updated: {updated_count}")
print(f"Total skipped: {skipped_count}")
