import re
import urllib.parse
from bs4 import BeautifulSoup

def clean_and_rebuild_with_books(filepath, is_english=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    pubs = []
    
    for item in soup.find_all('div', class_='pub-item'):
        topic = item.get('data-topic', '')
        
        title_tag = item.find('div', class_='pub-item-title')
        if not title_tag: continue
        
        a_tag = title_tag.find('a')
        if a_tag:
            href = a_tag.get('href', '')
            title_html = a_tag.decode_contents().strip()
        else:
            # Maybe there are items without a_tag
            href = ""
            title_html = title_tag.decode_contents().strip()
            
        authors_tag = item.find('div', class_='pub-item-authors')
        authors_html = authors_tag.decode_contents().strip() if authors_tag else ''
        
        journal_tag = item.find('div', class_='pub-item-journal')
        journal_html = journal_tag.decode_contents().strip() if journal_tag else ''
        
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
        
    # Define books
    if is_english:
        new_books = [
            {
                "year": 2021,
                "title": "해양생물학 11 판 Marine biology 11th",
                "authors": "Kang C. et al.",
                "journal": "Life Science Publishing Co., 462pp, 2021 <span class=\"pub-badge non-sci\">Book</span>",
                "topic": "books"
            },
            {
                "year": 2016,
                "title": "Parasitic dinoflagellates",
                "authors": "Kim S., Park M.G.",
                "journal": "In: JK Choi (Eds.), Korean Protists. (in Korean), 2016 <span class=\"pub-badge non-sci\">Book</span>",
                "topic": "books"
            }
        ]
    else:
        new_books = [
            {
                "year": 2021,
                "title": "해양생물학 11 판 Marine biology 11th",
                "authors": "강창근 외",
                "journal": "㈜라이프사이언스, 462pp, 2021 <span class=\"pub-badge non-sci\">Book</span>",
                "topic": "books"
            },
            {
                "year": 2016,
                "title": "Parasitic dinoflagellates",
                "authors": "Kim S., Park M.G.",
                "journal": "In: JK Choi (Eds.), Korean Protists. (in Korean), 2016 <span class=\"pub-badge non-sci\">Book</span>",
                "topic": "books"
            }
        ]

    for b in new_books:
        plain_title = re.sub(r'<[^>]+>', '', b['title'])
        search_query = f"{plain_title} {b['authors'].split(',')[0]}"
        scholar_url = f"https://scholar.google.com/scholar?q={urllib.parse.quote(search_query)}"
        
        pubs.append({
            'topic': b['topic'],
            'href': scholar_url,
            'title_html': b['title'],
            'authors_html': b['authors'],
            'journal_html': b['journal'],
            'year': b['year']
        })
        
    pubs.sort(key=lambda x: x['year'], reverse=True)
    
    # Calculate counts
    counts = {'all': len(pubs)}
    for p in pubs:
        topic_str = p.get('topic', '')
        topics = topic_str.split()
        for t in topics:
            counts[t] = counts.get(t, 0) + 1
            
    final_html = ""
    current_year = 0
    item_counter = 1
    
    for item in pubs:
        if item['year'] != current_year:
            if current_year != 0:
                final_html += "      </div>\n\n"
            current_year = item['year']
            final_html += f"      <!-- {current_year} -->\n"
            final_html += f"      <div class=\"pub-year-group fade-in\" data-y=\"{current_year}\">\n"
            final_html += f"        <div class=\"pub-year-header\">{current_year}</div>\n\n"
            
        final_html += f"""        <div class="pub-item" data-topic="{item['topic']}">
          <span style="color:var(--text-light); font-size:0.78rem; font-family:'Outfit',sans-serif; font-weight:700;">[{item_counter}]</span>
          <div class="pub-item-title"><a href="{item['href']}" target="_blank" rel="noopener">{item['title_html']}</a></div>
          <div class="pub-item-authors">{item['authors_html']}</div>
          <div class="pub-item-journal">{item['journal_html']}</div>
        </div>\n\n"""
        item_counter += 1
        
    final_html += "      </div>\n" 
    
    filter_bar_pattern = r'(<div class="pub-filter-bar">.*?</div>\s*)'
    filter_match = re.search(filter_bar_pattern, html, re.DOTALL)
    if not filter_match:
        print("Could not find filter bar in", filepath)
        return
        
    filter_bar_html = filter_match.group(1)
    
    # Append the "books" button if it doesn't exist
    if 'filterPubs(\'books\'' not in filter_bar_html:
        books_btn_kr = f'<button class="pub-filter-btn" onclick="filterPubs(\'books\', this)">저서 ({counts.get("books", 0)})</button>\n      </div>'
        books_btn_en = f'<button class="pub-filter-btn" onclick="filterPubs(\'books\', this)">Books ({counts.get("books", 0)})</button>\n      </div>'
        
        replacement = books_btn_en if is_english else books_btn_kr
        filter_bar_html = re.sub(r'</div>\s*$', replacement + '\n', filter_bar_html)

    # Update counts in the filter bar
    soup_fb = BeautifulSoup(filter_bar_html, 'html.parser')
    for btn in soup_fb.find_all('button', class_='pub-filter-btn'):
        onclick = btn.get('onclick', '')
        match = re.search(r"filterPubs\('([^']+)'", onclick)
        if match:
            topic = match.group(1)
            count = counts.get(topic, 0)
            
            # get current text without parentheses
            current_text = btn.get_text().strip()
            base_text = re.sub(r'\s*\(\d+\)$', '', current_text)
            
            # update text
            new_text = f"{base_text} ({count})"
            btn.string = new_text

    new_filter_bar = str(soup_fb.find('div', class_='pub-filter-bar'))
    
    start_idx = filter_match.end()
    end_idx = html.find('</main>', start_idx)
    end_idx = html.rfind('</div>', start_idx, end_idx) 
    
    new_content = html[:filter_match.start()] + new_filter_bar + "\n\n" + final_html + "\n    " + html[end_idx:]
    
    total_count = item_counter - 1
    new_content = re.sub(r'총 \d+편 논문', f'총 {total_count}편 논문 및 저서', new_content)
    new_content = re.sub(r'Total \d+ papers', f'Total {total_count} publications', new_content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print(f"Successfully added books and rebuilt {filepath} with {total_count} items.")

clean_and_rebuild_with_books('c:/Users/JO/Desktop/marine-planktonology-lab/pages/publications.html', is_english=False)
clean_and_rebuild_with_books('c:/Users/JO/Desktop/marine-planktonology-lab/pages/publications_en.html', is_english=True)
