import re

html_path = 'c:/Users/JO/Desktop/marine-planktonology-lab/pages/publications_en.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    (r'<a href="https://doi.org/10.4217/OPR.2015.37.3.201"[^>]*>(.*?)</a>',
     r'<a href="javascript:void(0)" target="_blank" rel="noopener">\1</a>'),
]

for old, new in replacements:
    content, count = re.subn(old, new, content, flags=re.DOTALL)
    print(f'Replaced {count} occurrences for {new[-20:]}')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
