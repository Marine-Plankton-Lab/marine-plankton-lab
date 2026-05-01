import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

html_path = 'c:/Users/JO/Desktop/marine-planktonology-lab/pages/publications.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

items = content.split('<div class="pub-item"')
for item in items[1:]:
    if '<span class="pub-badge">SCI</span>' not in item:
        num_match = re.search(r'>\[(\d+)\]<', item)
        if num_match:
            num = num_match.group(1)
            title_match = re.search(r'<div class="pub-item-title"><a href="(.*?)".*?>(.*?)</a></div>', item, re.DOTALL)
            if title_match:
                url = title_match.group(1)
                title = re.sub(r'<[^>]+>', '', title_match.group(2)).strip()
                title = re.sub(r'\s+', ' ', title)
                journal_match = re.search(r'<div class="pub-item-journal">(.*?)</div>', item, re.DOTALL)
                journal = re.sub(r'<[^>]+>', '', journal_match.group(1)).strip() if journal_match else ''
                journal = re.sub(r'\s+', ' ', journal)
                print(f'[{num}] {title}')
                print(f'   URL: {url}')
                print(f'   Journal: {journal}')
