import re

files = [
    'c:/Users/JO/Desktop/marine-planktonology-lab/pages/publications.html',
    'c:/Users/JO/Desktop/marine-planktonology-lab/pages/publications_en.html'
]

# For both files, we do regex replacements
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replacements for BOTH files (fixing DOIs and correcting English titles)

    # [13]
    content = re.sub(
        r'<a href="https://doi.org/10.11626/KJEB.2021.39.4.573"[^>]*>.*?</a>',
        r'<a href="https://doi.org/10.11626/KJEB.2021.39.4.573" target="_blank" rel="noopener">New records of five taxa of unarmored and thin-walled dinoflagellates from brackish and coastal waters of Korea</a>',
        content
    )

    # [15]
    content = re.sub(
        r'<a href="https://doi.org/10.11626/KJEB.2021.39.2.236"[^>]*>.*?</a>',
        r'<a href="https://doi.org/10.11626/KJEB.2021.39.2.236" target="_blank" rel="noopener">Newly recorded unarmored dinoflagellates in the family Kareniaceae (Gymnodiniales, Dinophyceae) in brackish and coastal waters of Korea</a>',
        content
    )

    # [17]
    content = re.sub(
        r'<a href="https://doi.org/10.11626/KJEB.2020.38.4.567"[^>]*>.*?</a>',
        r'<a href="https://doi.org/10.11626/KJEB.2020.38.4.567" target="_blank" rel="noopener">Infection of marine diatom <em>Coscinodiscus wailesii</em> (Bacillariophyceae) by the parasitic nanoflagellate <em>Pirsonia diadema</em> (Stramenopiles) from Yongho Bay in Korea</a>',
        content
    )

    # [19]
    content = re.sub(
        r'<a href="https://doi.org/10.7850/jkso.2019.24.2.236"[^>]*>.*?</a>',
        r'<a href="https://scholar.google.com/scholar?q=Distribution%20and%20molecular%20phylogeny%20of%20the%20toxic%20benthic%20dinoflagellate%20Ostreopsis%20sp.%20in%20the%20coastal%20waters%20off%20Jeju%20Island%2C%20Korea" target="_blank" rel="noopener">Distribution and molecular phylogeny of the toxic benthic dinoflagellate <em>Ostreopsis</em> sp. in the coastal waters off Jeju Island, Korea</a>',
        content
    )

    # [23]
    content = re.sub(
        r'<a href="https://doi.org/10.7850/jkso.2018.23.1.20"[^>]*>.*?</a>',
        r'<a href="https://scholar.google.com/scholar?q=Effect%20of%20water%20temperature%20on%20infectivity%20of%20the%20parasitoid%20Amoebophrya%20sp.%20infecting%20the%20harmful%20bloom-forming%20dinoflagellate%20Akashiwo%20sanguinea" target="_blank" rel="noopener">Effect of water temperature on infectivity of the parasitoid <em>Amoebophrya</em> sp. infecting the harmful bloom-forming dinoflagellate <em>Akashiwo sanguinea</em></a>',
        content
    )

    # [28]
    content = re.sub(
        r'<a href="https://doi.org/10.7850/jkso.2015.20.4.216"[^>]*>.*?</a>',
        r'<a href="https://scholar.google.com/scholar?q=Diversity%20and%20phylogenetic%20position%20of%20unarmored%20dinoflagellates%20from%20the%20coastal%20waters%20of%20Korea" target="_blank" rel="noopener">Diversity and phylogenetic position of unarmored dinoflagellates from the coastal waters of Korea</a>',
        content
    )

    # [29] (This one requires replacing title, DOI, and journal)
    # Search for the pub-item containing this
    # Wait, the easiest way is to just replace the whole pub-item block or just use precise sub.
    # Title link:
    content = re.sub(
        r'<a href="javascript:void\(0\)" target="_blank"[^>]*>마산만의 와편모류 <em>Dinophysis acuminata</em>와 혼합영양 섬모충 <em>Mesodinium rubrum</em> 개체군의 반일주기 변동</a>|<a href="javascript:void\(0\)" target="_blank"[^>]*>Semi-daily variations in populations of the dinoflagellates <em>Dinophysis acuminata</em> and a mixotrophic prey ciliate, <em>Mesodinium rubrum</em></a>|<a href="https://doi.org/10.4217/OPR.2015.37.3.201" target="_blank"[^>]*>Semi-daily variations in populations of the dinoflagellates <em>Dinophysis acuminata</em> and a mixotrophic prey ciliate, <em>Mesodinium rubrum</em></a>',
        r'<a href="https://scholar.google.com/scholar?q=Semi-daily%20Variations%20in%20Populations%20of%20the%20Dinoflagellates%20Dinophysis%20acuminata%20and%20Oxyphysis%20oxytoxoides%20and%20a%20Mixotrophic%20Ciliate%20Prey%20Mesodinium%20rubrum%20in%20Masan%20Bay" target="_blank" rel="noopener">Semi-daily Variations in Populations of the Dinoflagellates <em>Dinophysis acuminata</em> and <em>Oxyphysis oxytoxoides</em> and a Mixotrophic Ciliate Prey <em>Mesodinium rubrum</em> in Masan Bay</a>',
        content
    )
    # Journal metadata for [29]
    content = re.sub(
        r'<em>Ocean and Polar Research</em>, 37\(3\):201–209, 2015',
        r'<em>The Sea (Journal of Korean Society of Oceanography)</em>, 20(3):151–157, 2015',
        content
    )

    # [33]
    content = re.sub(
        r'<a href="https://doi.org/10.1093/plankt/fbu057"[^>]*>The marine tintinnid ciliate <em>Favella ehrenbergii</em></a>',
        r'<a href="javascript:void(0)" target="_blank" rel="noopener">The marine tintinnid ciliate <em>Favella ehrenbergii</em></a>',
        content
    )

    # [35]
    content = re.sub(
        r'<a href="https://doi.org/10.7850/jkso.2014.19.3.183"[^>]*>.*?</a>',
        r'<a href="https://scholar.google.com/scholar?q=Spatio-temporal%20distribution%20of%20the%20parasitic%20dinoflagellate%20Amoebophrya%20sp." target="_blank" rel="noopener">Spatio-temporal distribution of the parasitic dinoflagellate <em>Amoebophrya</em> sp.</a>',
        content
    )

    # [38]
    content = re.sub(
        r'<a href="https://doi.org/10.7850/jkso.2013.18.2.101"[^>]*>.*?</a>',
        r'<a href="https://scholar.google.com/scholar?q=Red%20tides%20in%20Shiwa%20Bay%2C%20Korea%20in%202011" target="_blank" rel="noopener">Red tides in Shiwa Bay, Korea in 2011</a>',
        content
    )

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
