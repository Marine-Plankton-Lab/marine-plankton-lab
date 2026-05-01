import re

html_path = 'c:/Users/JO/Desktop/marine-planktonology-lab/pages/publications.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    (r'<a href="https://doi.org/10.7837/kosomes.2025.31.1.043"[^>]*>(.*?)</a>',
     r'<a href="https://doi.org/10.7837/kosomes.2025.31.1.043" target="_blank" rel="noopener">부산 연안에서 분리한 해양 규조류 <em>Chaetoceros constrictus</em>(MPL-Cc01)의 수온과 pH 변화에 따른 성장 반응</a>'),
     
    (r'<a href="https://doi.org/10.11626/KJEB.2021.39.4.573"[^>]*>(.*?)</a>',
     r'<a href="https://doi.org/10.11626/KJEB.2021.39.4.573" target="_blank" rel="noopener">한국 기수 및 연안 해역에서 채집된 무각 및 박막 와편모조류 5종의 신기록</a>'),
     
    (r'<a href="https://doi.org/10.11626/KJEB.2021.39.2.236"[^>]*>(.*?)</a>',
     r'<a href="https://doi.org/10.11626/KJEB.2021.39.2.236" target="_blank" rel="noopener">한국 기수 및 연안에서 새로 기록된 Kareniaceae과(Gymnodiniales, Dinophyceae)의 무각 와편모류</a>'),

    (r'<a href="https://doi.org/10.11626/KJEB.2020.38.4.567"[^>]*>(.*?)</a>',
     r'<a href="https://doi.org/10.11626/KJEB.2020.38.4.567" target="_blank" rel="noopener">한국 용호만에서 채집한 해양 규조류 <em>Coscinodiscus wailesii</em>(Bacillariophyceae)에 대한 기생성 나노편모류 <em>Pirsonia diadema</em>(Stramenopiles)의 감염</a>'),

    (r'<a href="https://doi.org/10.7850/jkso.2019.24.2.236"[^>]*>(.*?)</a>',
     r'<a href="https://doi.org/10.7850/jkso.2019.24.2.236" target="_blank" rel="noopener">춘계 제주 연안에서 유독 저서성 와편모류 <em>Ostreopsis</em> sp.의 분포와 분자계통학적 위치</a>'),

    (r'<a href="https://doi.org/10.7850/jkso.2018.23.1.20"[^>]*>(.*?)</a>',
     r'<a href="https://doi.org/10.7850/jkso.2018.23.1.20" target="_blank" rel="noopener">유해 적조생물 <em>Akashiwo sanguinea</em>를 감염시키는 포식성 기생생물 <em>Amoebophrya</em> sp.의 감염력에 대한 수온의 영향</a>'),

    (r'<a href="https://doi.org/10.7850/jkso.2015.20.4.216"[^>]*>(.*?)</a>',
     r'<a href="https://doi.org/10.7850/jkso.2015.20.4.216" target="_blank" rel="noopener">한국 연안 해역 무각 와편모류의 다양성과 분자계통학적 위치</a>'),

    (r'<a href="https://doi.org/10.4217/OPR.2015.37.3.201"[^>]*>(.*?)</a>',
     r'<a href="javascript:void(0)" target="_blank" rel="noopener">마산만의 와편모류 <em>Dinophysis acuminata</em>와 혼합영양 섬모충 <em>Mesodinium rubrum</em> 개체군의 반일주기 변동</a>'),

    (r'<a href="https://doi.org/10.7850/jkso.2014.19.3.183"[^>]*>(.*?)</a>',
     r'<a href="https://doi.org/10.7850/jkso.2014.19.3.183" target="_blank" rel="noopener">기생성 와편모류 <em>Amoebophrya</em> sp.의 시공간적 분포</a>'),

    (r'<a href="https://doi.org/10.7850/jkso.2013.18.2.101"[^>]*>(.*?)</a>',
     r'<a href="https://doi.org/10.7850/jkso.2013.18.2.101" target="_blank" rel="noopener">2011년 한국 시화호의 적조</a>')
]

for old, new in replacements:
    content, count = re.subn(old, new, content, flags=re.DOTALL)
    print(f'Replaced {count} occurrences for {new[-20:]}')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
