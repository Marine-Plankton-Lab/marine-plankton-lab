import re
import urllib.request
import json
from bs4 import BeautifulSoup

html_path = 'c:/Users/JO/Desktop/marine-planktonology-lab/pages/publications.html'
with open(html_path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

items = soup.find_all('div', class_='pub-item')
for idx, item in enumerate(items):
    span = item.find('span')
    if not span:
        continue
    num_match = re.search(r'\[(\d+)\]', span.text)
    if not num_match:
        continue
    num = int(num_match.group(1))
    
    if num >= 19:
        title_div = item.find('div', class_='pub-item-title')
        a_tag = title_div.find('a') if title_div else None
        url = a_tag['href'] if a_tag else 'NO_URL'
        title_text = title_div.text.strip() if title_div else ''
        
        author_div = item.find('div', class_='pub-item-authors')
        author_text = author_div.text.strip() if author_div else ''
        
        journal_div = item.find('div', class_='pub-item-journal')
        journal_text = journal_div.text.strip() if journal_div else ''
        
        print(f'[{num}] URL: {url}')
        print(f'   HTML Title: {title_text}')
        print(f'   HTML Authors: {author_text}')
        
        if 'doi.org/' in url:
            doi = url.split('doi.org/')[1]
            api_url = f'https://api.crossref.org/works/{doi}'
            try:
                req = urllib.request.Request(api_url, headers={'User-Agent': 'mailto:test@example.com'})
                resp = urllib.request.urlopen(req, timeout=5)
                data = json.loads(resp.read())
                actual_title = data['message'].get('title', [''])[0]
                authors_list = data['message'].get('author', [])
                actual_authors = ', '.join([a.get('family', '') + ' ' + a.get('given', '') for a in authors_list])
                print(f'   Real Title: {actual_title}')
                print(f'   Real Authors: {actual_authors}')
            except Exception as e:
                print(f'   Crossref Error: {e}')
        print('-'*40)
