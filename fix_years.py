import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the filter bar end
    filter_bar_pattern = r'(<div class="pub-filter-bar">.*?</div>\s*)'
    filter_match = re.search(filter_bar_pattern, content, re.DOTALL)
    if not filter_match:
        print("Could not find filter bar in", filepath)
        return
        
    start_idx = filter_match.end()
    
    # Find the end of the page-inner block
    end_idx = content.find('</main>', start_idx)
    end_idx = content.rfind('</div>', start_idx, end_idx) 
    
    pubs_content = content[start_idx:end_idx]
    
    parsed_items = []
    
    parts = pubs_content.split('<div class="pub-item"')
    for p in parts[1:]:
        block = '<div class="pub-item"' + p
        block = re.sub(r'</div>\s*$', '', block).strip()
        
        divs = 0
        end_cut = 0
        for m in re.finditer(r'<div|</div', block):
            if m.group(0) == '<div':
                divs += 1
            else:
                divs -= 1
            if divs == 0:
                end_cut = m.end() + 1
                break
        
        if end_cut > 0:
            block = block[:end_cut].strip()
            
        # extract year robustly from journal div
        journal_match = re.search(r'<div class="pub-item-journal">(.*?)</div>', block, re.DOTALL)
        year = 0
        if journal_match:
            journal_text = journal_match.group(1)
            # Find the first 4-digit number that looks like a year (e.g. 2000-2030)
            years = re.findall(r'\b(20[0-2]\d)\b', journal_text)
            if years:
                year = int(years[-1]) # Usually the last 4 digit number is the year
        
        parsed_items.append({
            'year': year,
            'html': block
        })
        
    parsed_items.sort(key=lambda x: x['year'], reverse=True)
    
    final_html = ""
    current_year = 0
    item_counter = 1
    
    for item in parsed_items:
        if item['year'] != current_year:
            if current_year != 0:
                final_html += "      </div>\n\n"
            current_year = item['year']
            final_html += f"      <!-- {current_year} -->\n"
            final_html += f"      <div class=\"pub-year-group fade-in\" data-y=\"{current_year}\">\n"
            final_html += f"        <div class=\"pub-year-header\">{current_year}</div>\n\n"
            
        block = item['html']
        block = re.sub(r'>\[\d+\]</span>', f'>[{item_counter}]</span>', block)
        final_html += block + "\n\n"
        item_counter += 1
        
    final_html += "      </div>\n" 
    
    new_content = content[:start_idx] + "\n" + final_html + "\n    " + content[end_idx:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print(f"Updated {filepath} with {item_counter - 1} items.")

process_file('c:/Users/JO/Desktop/marine-planktonology-lab/pages/publications.html')
process_file('c:/Users/JO/Desktop/marine-planktonology-lab/pages/publications_en.html')
