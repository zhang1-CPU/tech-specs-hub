#!/usr/bin/env python3
import os

pages_dir = "/workspace/pages"
root_files = ["/workspace/index.html", "/workspace/404.html"]

all_files = []
for f in root_files:
    all_files.append(f)

for root, dirs, files in os.walk(pages_dir):
    for f in files:
        if f.endswith(".html"):
            all_files.append(os.path.join(root, f))

ga4_script = """  <!-- GA4 Consent Mode v2 -->
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('consent', 'default', {
      'analytics_storage': 'granted',
      'ad_storage': 'denied',
      'ad_user_data': 'denied',
      'ad_personalization': 'denied'
    });
  </script>
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-MEQ0R6DSNQ"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-MEQ0R6DSNQ', {
      'send_page_view': true,
      'storage': 'granted',
      'client_storage': 'granted'
    });
  </script>
"""

updated_count = 0
skipped_count = 0

for filepath in all_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "G-MEQ0R6DSNQ" in content:
        if "gtag('consent'" in content:
            skipped_count += 1
            continue
        
        content = content.replace(
            '<script async src="https://www.googletagmanager.com/gtag/js?id=G-MEQ0R6DSNQ"></script>',
            ga4_script
        )
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        updated_count += 1
        print(f"Updated GA4 Consent Mode v2: {os.path.basename(filepath)}")
    else:
        insert_pos = content.find('</head>')
        if insert_pos != -1:
            content = content[:insert_pos] + ga4_script + content[insert_pos:]
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            updated_count += 1
            print(f"Added GA4 Consent Mode v2: {os.path.basename(filepath)}")
        else:
            skipped_count += 1

print(f"\nTotal updated: {updated_count}")
print(f"Total skipped: {skipped_count}")
