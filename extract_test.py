import re

with open('c:/Users/JO/Desktop/marine-planktonology-lab/pages/publications.html', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'<div class="pub-item" data-topic="([^"]+)".*?<div class="pub-item-title"><a href="([^"]+)"[^>]*>(.*?)</a></div>\s*<div class="pub-item-authors">(.*?)</div>\s*<div class="pub-item-journal">(.*?)(?=<div class="pub-item"|</main>|</div>\s*</main>)'
items = re.findall(pattern, content, re.DOTALL)

print(len(items))
for topic, href, title, authors, journal in items:
    print("Found:", title[:30])
