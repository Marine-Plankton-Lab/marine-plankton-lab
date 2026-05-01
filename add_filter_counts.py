import re
from bs4 import BeautifulSoup

def update_counts_and_js(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    
    # Calculate counts
    counts = {'all': 0}
    
    for item in soup.find_all('div', class_='pub-item'):
        counts['all'] += 1
        topic_str = item.get('data-topic', '')
        topics = topic_str.split()
        for t in topics:
            counts[t] = counts.get(t, 0) + 1
            
    # Now update the buttons
    for btn in soup.find_all('button', class_='pub-filter-btn'):
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

    # Convert back to HTML
    # We only want to replace the filter bar to avoid messing up formatting
    new_filter_bar = str(soup.find('div', class_='pub-filter-bar'))
    
    # Find original filter bar in HTML
    pattern = r'<div class="pub-filter-bar">.*?</div>'
    html = re.sub(pattern, new_filter_bar, html, flags=re.DOTALL)
    
    # Remove the JS update count logic
    js_pattern = r'\s*// update count.*?\(\s*visible\s*\)\s*`;'
    html = re.sub(js_pattern, '', html, flags=re.DOTALL)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"Updated {filepath} with static counts.")

update_counts_and_js('c:/Users/JO/Desktop/marine-planktonology-lab/pages/publications.html')
update_counts_and_js('c:/Users/JO/Desktop/marine-planktonology-lab/pages/publications_en.html')
