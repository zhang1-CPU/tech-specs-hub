#!/usr/bin/env python3
import os

pages_dir = "/workspace/pages"

all_files = []
for root, dirs, files in os.walk(pages_dir):
    for f in files:
        if f.endswith(".html"):
            all_files.append(os.path.join(root, f))

report_error_html = """  <!-- REPORT ERROR SECTION -->
  <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div class="text-center text-sm text-gray-500">
      <a href="../contact.html" class="inline-flex items-center gap-1.5 text-electric-400 hover:text-electric-300 transition-colors">
        <i data-lucide="alert-circle" style="width:0.75rem;height:0.75rem"></i>
        Report an error or suggest an update
      </a>
      <span class="mx-2">|</span>
      <a href="../about.html" class="text-gray-400 hover:text-white transition-colors">Editorial standards</a>
    </div>
  </section>
"""

updated_count = 0
skipped_count = 0

for filepath in all_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "Report an error" in content:
        skipped_count += 1
        continue
    
    insert_pos = content.find('<!-- FOOTER -->')
    if insert_pos == -1:
        insert_pos = content.find('<footer class="border-t')
    
    if insert_pos != -1:
        content = content[:insert_pos] + report_error_html + content[insert_pos:]
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        updated_count += 1
        print(f"Added report error link: {os.path.basename(filepath)}")
    else:
        skipped_count += 1
        print(f"Could not find FOOTER section: {os.path.basename(filepath)}")

print(f"\nTotal updated: {updated_count}")
print(f"Total skipped: {skipped_count}")
