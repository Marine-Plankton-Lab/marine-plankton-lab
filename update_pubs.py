import re
import urllib.parse
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

new_papers = [
    {
        "year": 2015,
        "title": "Occurrence and molecular phylogenetic characteristics of benthic sand-dwelling dinoflagellates in intertidal flat of Dongho, west coast of Korea",
        "authors": "Kim S., Yoon J., Park M.G.",
        "journal": "<em>The Sea</em>, 2015 <span class=\"pub-badge non-sci\">KCI</span>",
        "topic": "molecular dino"
    },
    {
        "year": 2012,
        "title": "The marine dinoflagellate genus <em>Dinophysis</em> can retain plastids of multiple algal origins at the same time",
        "authors": "Kim M., Kim S., Yih W., Park M.G.",
        "journal": "<em>Harmful Algae</em>, 2012 <span class=\"pub-badge\">SCI</span>",
        "topic": "ecology dino"
    },
    {
        "year": 2009,
        "title": "Phylogeny of four dinophysiacean genera (Dinophyceae, Dinophysiales) based on rDNA sequences from single cells and environmental samples",
        "authors": "Handy S.M., Bachvaroff T.R., Timme R., Coats D.W., Kim S., Delwiche C.F.",
        "journal": "<em>Journal of Phycology</em>, 2009 <span class=\"pub-badge\">SCI</span>",
        "topic": "molecular dino"
    },
    {
        "year": 2009,
        "title": "Dinoflagellate host-parasite sterol profiles dictate karlotoxin sensitivity",
        "authors": "Place A., Bai X., Kim S., Sengco M., Coats D.W.",
        "journal": "<em>Journal of Phycology</em>, 2009 <span class=\"pub-badge\">SCI</span>",
        "topic": "parasites ecology dino"
    },
    {
        "year": 2008,
        "title": "Prevalence and phylogeny of parasitic dinoflagellates (Genus <em>Blastodinium</em>) infecting copepods in the Gulf of California",
        "authors": "Coats D.W., Bachvaroff T., Handy S.M., Kim S., Garate-Lizarraga I., Delwiche C.F.",
        "journal": "<em>CICIMAR Oceánides</em>, 2008 <span class=\"pub-badge non-sci\">Non-SCI</span>",
        "topic": "parasites molecular dino"
    },
    {
        "year": 2008,
        "title": "Genetic diversity of the parasitic dinoflagellate in the genus <em>Amoebophrya</em> and its relationship to parasite biology and biogeography",
        "authors": "Kim S., Park M.G., Kim K.Y., Kim C.H., Yih W., Park J.S., Coats D.W.",
        "journal": "<em>Journal of Eukaryotic Microbiology</em>, 2008 <span class=\"pub-badge\">SCI</span>",
        "topic": "parasites molecular"
    },
    {
        "year": 2008,
        "title": "Growth and grazing responses of the mixotrophic dinoflagellate <em>Dinophysis acuminata</em> as functions of light intensity and prey concentration",
        "authors": "Kim S., Park M.G., Kang Y.G., Kim H.S., Yih W.",
        "journal": "<em>Aquatic Microbial Ecology</em>, 2008 <span class=\"pub-badge\">SCI</span>",
        "topic": "ecology dino"
    },
    {
        "year": 2007,
        "title": "Seasonal variations in phytoplankton growth and microzooplankton grazing in a temperate coastal embayment, Korea",
        "authors": "Kim S., Park M.G., Moon C., Shin K., Chang M.",
        "journal": "<em>Estuarine, Coastal and Shelf Science</em>, 2007 <span class=\"pub-badge\">SCI</span>",
        "topic": "ecology"
    },
    {
        "year": 2006,
        "title": "Patterns in host range for two strains of <em>Amoebophrya</em> (Dinophyta) infecting the thecate dinoflagellates <em>Alexandrium affine</em> and <em>Gonyaulax polygramma</em>",
        "authors": "Kim S.",
        "journal": "<em>Journal of Phycology</em>, 2006 <span class=\"pub-badge\">SCI</span>",
        "topic": "parasites ecology dino"
    },
    {
        "year": 2004,
        "title": "Infection of the bloom-forming thecate dinoflagellates <em>Alexandrium affine</em> and <em>Gonyaulax polygramma</em> by two strain <em>Amoebophrya</em> (Dinophyta)",
        "authors": "Kim S., Park M.G., Yih W., Coats D.W.",
        "journal": "<em>Journal of Phycology</em>, 2004 <span class=\"pub-badge\">SCI</span>",
        "topic": "parasites ecology dino"
    },
    {
        "year": 2003,
        "title": "Effects of benzo[a]pyrene on growth and photosynthetic performance of phytoplankton",
        "authors": "Kim S., Shin K., Moon C., Chang M.",
        "journal": "<em>Korean Journal of Environmental Biology</em>, 2003 <span class=\"pub-badge non-sci\">KCI</span>",
        "topic": "ecology"
    }
]

def format_new_paper(paper):
    plain_title = re.sub(r'<[^>]+>', '', paper['title'])
    search_query = f"{plain_title} {paper['authors'].split(',')[0]}"
    scholar_url = f"https://scholar.google.com/scholar?q={urllib.parse.quote(search_query)}"
    
    html = f"""        <div class="pub-item" data-topic="{paper['topic']}">
          <span style="color:var(--text-light); font-size:0.78rem; font-family:'Outfit',sans-serif; font-weight:700;">[X]</span>
          <div class="pub-item-title"><a href="{scholar_url}" target="_blank" rel="noopener">{paper['title']}</a></div>
          <div class="pub-item-authors">{paper['authors']}</div>
          <div class="pub-item-journal">{paper['journal']}</div>
        </div>"""
    return html

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
    end_idx = content.rfind('</div>', start_idx, end_idx) # The closing div of page-inner
    
    pubs_content = content[start_idx:end_idx]
    
    parsed_items = []
    
    # Extract existing pub items
    # They look like: <div class="pub-item" data-topic="...">...</div>
    pub_items = re.findall(r'<div class="pub-item".*?</div>\s*(?=</div>|\s*<div class="pub-item"|\s*<div class="pub-year-group"|\Z)', pubs_content, re.DOTALL)
    # This regex is tricky. Better to split by '<div class="pub-item"'
    parts = pubs_content.split('<div class="pub-item"')
    for p in parts[1:]:
        # Find where it ends
        # It typically has 3 child divs, so let's match till we have matched all opening/closing tags.
        # Or simpler: cut at the first <div class="pub-year-group" or just after the last </div> of this item.
        # Since we just want the item HTML, we can just find the year.
        block = '<div class="pub-item"' + p
        # trim any trailing `      </div>` that closes pub-year-group
        block = re.sub(r'</div>\s*$', '', block).strip()
        # sometimes it ends with another </div> which belonged to pub-year-group
        # let's balance the divs
        
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
            
        title_match = re.search(r'<div class="pub-item-title"><a[^>]*>(.*?)</a></div>', block, re.DOTALL)
        if not title_match:
            continue
            
        title = title_match.group(1).strip()
        plain_title = re.sub(r'<[^>]+>', '', title)
        
        if "Favella ehrenbergii" in plain_title:
            continue # Skip Favella
            
        year_match = re.search(r'</div>\s*(?:<em>.*?</em>)?.*?,\s*(\d{4})', block)
        year = 0
        if year_match:
            year = int(year_match.group(1))
        else:
            year_match2 = re.search(r'(\d{4})\s*<span class="pub-badge', block)
            if year_match2:
                year = int(year_match2.group(1))
                
        parsed_items.append({
            'year': year,
            'title': plain_title,
            'html': block,
            'is_new': False
        })

    # Add new items
    for p in new_papers:
        parsed_items.append({
            'year': p['year'],
            'title': re.sub(r'<[^>]+>', '', p['title']),
            'html': format_new_paper(p),
            'is_new': True
        })
        
    # Sort
    parsed_items.sort(key=lambda x: x['year'], reverse=True)
    
    # Re-group by year
    final_html = ""
    current_year = 0
    item_counter = 1
    
    for item in parsed_items:
        if item['year'] != current_year:
            if current_year != 0:
                final_html += "      </div>\n\n" # close previous year
            current_year = item['year']
            final_html += f"      <!-- {current_year} -->\n"
            final_html += f"      <div class=\"pub-year-group fade-in\" data-y=\"{current_year}\">\n"
            final_html += f"        <div class=\"pub-year-header\">{current_year}</div>\n\n"
            
        block = item['html']
        block = re.sub(r'>\[\d+\]</span>', f'>[{item_counter}]</span>', block)
        block = re.sub(r'>\[X\]</span>', f'>[{item_counter}]</span>', block)
        final_html += block + "\n\n"
        item_counter += 1
        
    final_html += "      </div>\n" # close last year
    
    # Replace in file
    new_content = content[:start_idx] + "\n" + final_html + "\n    " + content[end_idx:]
    
    # Replace counts
    total_count = item_counter - 1
    new_content = re.sub(r'\(44\)', f'({total_count})', new_content)
    new_content = re.sub(r'44편 논문', f'{total_count}편 논문', new_content)
    new_content = re.sub(r'44 papers', f'{total_count} papers', new_content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print(f"Updated {filepath} with {total_count} items.")

process_file('c:/Users/JO/Desktop/marine-planktonology-lab/pages/publications.html')
process_file('c:/Users/JO/Desktop/marine-planktonology-lab/pages/publications_en.html')
