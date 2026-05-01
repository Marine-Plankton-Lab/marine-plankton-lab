import re
import urllib.parse
from bs4 import BeautifulSoup

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

title_translations = {
    "한국 연안 및 기수역 출현 무갑옷 및 박막갑옷와편모조류 5 분류군 미기록종 보고": "New records of five taxa of unarmored and thin-walled dinoflagellates from brackish and coastal waters of Korea",
    "한국 연안 및 기수역 카레니아과 (알몸와편모조류목, 와편모조류강)의 미기록 알몸와편모조류": "Newly recorded unarmored dinoflagellates in the family Kareniaceae (Gymnodiniales, Dinophyceae) in brackish and coastal waters of Korea",
    "부산 용호만에서 기생성 진핵생물 Pirsonia diadema (대롱편모조류)에 의한 규조류 Coscinodiscus wailesii (규조강) 감염": "Infection of marine diatom <em>Coscinodiscus wailesii</em> (Bacillariophyceae) by the parasitic nanoflagellate <em>Pirsonia diadema</em> (Stramenopiles) from Yongho Bay in Korea",
    "제주연안 해역에 출현하는 유독 저서성 와편모조류 Ostreopsis 속의 분포 및 분자계통학적 특성": "Distribution and molecular phylogeny of the toxic benthic dinoflagellate <em>Ostreopsis</em> sp. in the coastal waters off Jeju Island, Korea",
    "유해적조원인생물 Akashiwo sanguinea를 감염시키는 기생생물 Amoebophrya sp. 감염력에 대한 수온의 영향": "Effect of water temperature on infectivity of the parasitoid <em>Amoebophrya</em> sp. infecting the harmful bloom-forming dinoflagellate <em>Akashiwo sanguinea</em>",
    "한국 연안 무갑옷와편모조류의 종 다양성 및 분자계통분류학적 위치": "Diversity and phylogenetic position of unarmored dinoflagellates from the coastal waters of Korea",
    "마산만의 와편모조류 Dinophysis acuminata와 혼합영양 섬모충 Mesodinium rubrum 개체군의 반일주기 변화": "Semi-daily Variations in Populations of the Dinoflagellates <em>Dinophysis acuminata</em> and <em>Oxyphysis oxytoxoides</em> and a Mixotrophic Ciliate Prey <em>Mesodinium rubrum</em> in Masan Bay",
    "기생성 와편모조류 Amoebophrya sp.의 시공간적 분포": "Spatio-temporal distribution of the parasitic dinoflagellate <em>Amoebophrya</em> sp.",
    "2011년 시화호 적조발생 특징": "Red tides in Shiwa Bay, Korea in 2011"
}

def format_new_paper(paper):
    plain_title = re.sub(r'<[^>]+>', '', paper['title'])
    search_query = f"{plain_title} {paper['authors'].split(',')[0]}"
    scholar_url = f"https://scholar.google.com/scholar?q={urllib.parse.quote(search_query)}"
    
    return {
        'topic': paper['topic'],
        'href': scholar_url,
        'title_html': paper['title'],
        'authors_html': paper['authors'],
        'journal_html': paper['journal'],
        'year': paper['year']
    }

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
        if a_tag:
            href = a_tag.get('href', '')
            title_html = a_tag.decode_contents()
            plain_title = a_tag.get_text().strip()
        else:
            href = "https://onlinelibrary.wiley.com/doi/full/10.1111/jpy.70160"
            title_html = title_tag.decode_contents().strip()
            plain_title = title_tag.get_text().strip()
            
        if 'Favella ehrenbergii' in plain_title:
            continue
            
        authors_tag = item.find('div', class_='pub-item-authors')
        authors_html = authors_tag.decode_contents().strip() if authors_tag else ''
        
        journal_tag = item.find('div', class_='pub-item-journal')
        journal_html = journal_tag.decode_contents().strip() if journal_tag else ''
        
        # Unveiling paper fixes
        if "Unveiling the phylogenetic position of the type species" in plain_title:
            journal_html = journal_html.replace("In Revision", "SCI")
            
        # Title translations
        for kr, en in title_translations.items():
            # If the plain title contains the korean text or matches closely
            if plain_title.replace(' ', '') == kr.replace(' ', ''):
                title_html = en
                break
                
        # Specific fixes for [29] (Masan Bay)
        if "Masan Bay" in title_html or "마산만의" in plain_title:
            title_html = "Semi-daily Variations in Populations of the Dinoflagellates <em>Dinophysis acuminata</em> and <em>Oxyphysis oxytoxoides</em> and a Mixotrophic Ciliate Prey <em>Mesodinium rubrum</em> in Masan Bay"
            href = "https://scholar.google.com/scholar?q=" + urllib.parse.quote("Semi-daily Variations in Populations of the Dinoflagellates Dinophysis acuminata and Oxyphysis oxytoxoides and a Mixotrophic Ciliate Prey Mesodinium rubrum in Masan Bay")
            journal_html = "<em>The Sea (Journal of Korean Society of Oceanography)</em>, 20(3):151–157, 2015"
            
        # Determine year
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
        
    for p in new_papers:
        pubs.append(format_new_paper(p))
        
    pubs.sort(key=lambda x: x['year'], reverse=True)
    
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
        
    print(f"Successfully processed {filepath} with {total_count} items.")

clean_and_rebuild('c:/Users/JO/Desktop/marine-planktonology-lab/pages/publications.html')
clean_and_rebuild('c:/Users/JO/Desktop/marine-planktonology-lab/pages/publications_en.html')
