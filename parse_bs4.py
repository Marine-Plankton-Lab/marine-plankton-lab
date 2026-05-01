import re
from bs4 import BeautifulSoup

def clean_and_rebuild(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    
    pubs = []
    
    for item in soup.find_all('div', class_='pub-item'):
        topic = item.get('data-topic', '')
        
        # some items might be malformed, let's carefully extract
        title_tag = item.find('div', class_='pub-item-title')
        if not title_tag: continue
        
        a_tag = title_tag.find('a')
        if not a_tag: continue
        
        href = a_tag.get('href', '')
        title_html = a_tag.decode_contents()
        
        plain_title = a_tag.get_text().strip()
        if 'Favella ehrenbergii' in plain_title:
            continue
            
        authors_tag = item.find('div', class_='pub-item-authors')
        authors_html = authors_tag.decode_contents() if authors_tag else ''
        
        journal_tag = item.find('div', class_='pub-item-journal')
        journal_html = journal_tag.decode_contents() if journal_tag else ''
        
        # determine year
        year = 0
        if journal_html:
            years = re.findall(r'\b(20[0-2]\d)\b', journal_html)
            if years:
                year = int(years[-1])
                
        pubs.append({
            'topic': topic,
            'href': href,
            'title_html': title_html,
            'authors_html': authors_html,
            'journal_html': journal_html,
            'year': year
        })
        
    print(f"{filepath}: Found {len(pubs)} valid publications (excluding Favella).")
    
    return pubs

p1 = clean_and_rebuild('c:/Users/JO/Desktop/marine-planktonology-lab/pages/publications.html')
p2 = clean_and_rebuild('c:/Users/JO/Desktop/marine-planktonology-lab/pages/publications_en.html')

print("P1 count:", len(p1))
print("P2 count:", len(p2))
