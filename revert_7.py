import re

file = 'c:/Users/JO/Desktop/marine-planktonology-lab/pages/publications.html'

with open(file, 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(
    r'<a href="https://doi.org/10.7837/kosomes.2025.31.1.043"[^>]*>.*?</a>',
    r'<a href="https://doi.org/10.7837/kosomes.2025.31.1.043" target="_blank" rel="noopener">Temperature and pH-dependent Growth Response of the marine diatom <em>Chaetoceros constrictus</em> (MPL-Cc01) isolated from the Yongho Bay, Busan</a>',
    content
)

with open(file, 'w', encoding='utf-8') as f:
    f.write(content)
