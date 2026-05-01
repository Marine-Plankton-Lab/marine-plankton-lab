import re
from bs4 import BeautifulSoup

def clean_and_rebuild(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    
    pubs = []
    
    for item in soup.find_all('div', class_='pub-item'):
        topic = item.get('data-topic', '')
        
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
        
    # Sort
    pubs.sort(key=lambda x: x['year'], reverse=True)
    
    # Re-group by year
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
    
    # Find insertion point
    filter_bar_pattern = r'(<div class="pub-filter-bar">.*?</div>\s*)'
    filter_match = re.search(filter_bar_pattern, html, re.DOTALL)
    if not filter_match:
        print("Could not find filter bar in", filepath)
        return
        
    start_idx = filter_match.end()
    
    end_idx = html.find('</main>', start_idx)
    end_idx = html.rfind('</div>', start_idx, end_idx) 
    
    new_content = html[:start_idx] + "\n" + final_html + "\n    " + html[end_idx:]
    
    total_count = item_counter - 1
    new_content = re.sub(r'\(44\)', f'({total_count})', new_content)
    new_content = re.sub(r'44편 논문', f'{total_count}편 논문', new_content)
    new_content = re.sub(r'44 papers', f'{total_count} papers', new_content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print(f"Successfully rebuilt {filepath} with {total_count} items.")

clean_and_rebuild('c:/Users/JO/Desktop/marine-planktonology-lab/pages/publications.html')
clean_and_rebuild('c:/Users/JO/Desktop/marine-planktonology-lab/pages/publications_en.html')
