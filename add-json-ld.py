#!/usr/bin/env python3
import os
import re
from html.parser import HTMLParser

class FAQParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.faqs = []
        self.in_details = False
        self.in_summary = False
        self.in_p = False
        self.current_question = ""
        self.current_answer = ""

    def handle_starttag(self, tag, attrs):
        if tag == "details":
            self.in_details = True
        elif tag == "summary" and self.in_details:
            self.in_summary = True
        elif tag == "p" and self.in_details:
            self.in_p = True

    def handle_endtag(self, tag):
        if tag == "details":
            if self.current_question and self.current_answer:
                self.faqs.append({
                    "question": self.current_question.strip(),
                    "answer": self.current_answer.strip()
                })
            self.in_details = False
            self.current_question = ""
            self.current_answer = ""
        elif tag == "summary":
            self.in_summary = False
        elif tag == "p":
            self.in_p = False

    def handle_data(self, data):
        if self.in_summary:
            self.current_question += data
        elif self.in_p:
            self.current_answer += data

def extract_breadcrumb(html):
    match = re.search(r'<nav\s+class="breadcrumb"[^>]*>(.*?)</nav>', html, re.DOTALL)
    if not match:
        return None
    
    breadcrumb_html = match.group(1)
    items = []
    
    link_pattern = re.compile(r'<a\s+href="([^"]+)">([^<]+)</a>')
    span_pattern = re.compile(r'<span[^>]*>([^<]+)</span>')
    
    parts = re.split(r'<span\s+class="breadcrumb-sep">/', breadcrumb_html)
    
    for part in parts:
        part = part.strip()
        link_match = link_pattern.search(part)
        if link_match:
            href = link_match.group(1)
            text = link_match.group(2).strip()
            if href.startswith("../../"):
                href = href.replace("../../", "https://powerspecshub.com/")
            elif href.startswith("../"):
                href = href.replace("../", "https://powerspecshub.com/pages/")
            elif href.startswith("./"):
                href = href.replace("./", "")
            elif not href.startswith("http"):
                href = "https://powerspecshub.com/pages/specs/" + href
            items.append({"name": text, "url": href})
        else:
            span_match = span_pattern.search(part)
            if span_match:
                text = span_match.group(1).strip()
                items.append({"name": text})
    
    return items

def generate_faq_json_ld(faqs):
    if not faqs:
        return ""
    
    questions = []
    for i, faq in enumerate(faqs):
        questions.append({
            "@type": "Question",
            "name": faq["question"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["answer"]
            }
        })
    
    json_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": questions
    }
    
    import json
    return "<script type=\"application/ld+json\">" + json.dumps(json_ld, indent=2) + "</script>"

def generate_breadcrumb_json_ld(items):
    if not items or len(items) < 2:
        return ""
    
    breadcrumb_items = []
    for i, item in enumerate(items):
        breadcrumb_item = {
            "@type": "ListItem",
            "position": i + 1,
            "name": item["name"]
        }
        if "url" in item:
            breadcrumb_item["item"] = item["url"]
        breadcrumb_items.append(breadcrumb_item)
    
    json_ld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": breadcrumb_items
    }
    
    import json
    return "<script type=\"application/ld+json\">" + json.dumps(json_ld, indent=2) + "</script>"

def process_html_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
    
    if "FAQPage" in html and "BreadcrumbList" in html:
        print(f"Skipping (already has JSON-LD): {filepath}")
        return
    
    parser = FAQParser()
    parser.feed(html)
    
    breadcrumb_items = extract_breadcrumb(html)
    
    faq_json_ld = generate_faq_json_ld(parser.faqs)
    breadcrumb_json_ld = generate_breadcrumb_json_ld(breadcrumb_items) if breadcrumb_items else ""
    
    insert_point = html.find("</head>")
    if insert_point == -1:
        print(f"Warning: No </head> found in {filepath}")
        return
    
    new_html = html[:insert_point]
    
    if faq_json_ld:
        new_html += "\n  " + faq_json_ld + "\n"
    if breadcrumb_json_ld:
        new_html += "\n  " + breadcrumb_json_ld + "\n"
    
    new_html += html[insert_point:]
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_html)
    
    print(f"Updated: {filepath}")
    print(f"  - FAQs: {len(parser.faqs)}")
    print(f"  - Breadcrumb items: {len(breadcrumb_items) if breadcrumb_items else 0}")

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                process_html_file(filepath)

if __name__ == "__main__":
    process_directory("/workspace/pages")
    process_html_file("/workspace/index.html")
    process_html_file("/workspace/404.html")
