import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('c:/Users/JO/Desktop/marine-planktonology-lab/pages/publications.html', 'r', encoding='utf-8') as f:
    content = f.read()

titles = re.findall(r'<div class="pub-item-title">(.*?)</div>', content, re.DOTALL)
print('Current HTML titles count:', len(titles))
for i, t in enumerate(titles[-20:]):
    print(f'{len(titles)-20+i+1}: {re.sub(r"<[^>]+>", "", t).strip()}')
