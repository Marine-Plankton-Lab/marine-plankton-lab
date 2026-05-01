import urllib.request
import json
import urllib.parse

titles = {
    '22': 'Revisiting the Parvilucifera infectans / P. sinerae (Alveolata, Perkinsozoa) species complex, two parasitoids of dinoflagellates',
    '23': 'Effect of water temperature on infectivity of the parasitoid Amoebophrya sp. infecting the harmful bloom-forming dinoflagellate Akashiwo sanguinea',
    '24': 'Morphological observations and phylogenetic position of the parasitoid nanoflagellate Pseudopirsonia sp. (Cercozoa) infecting the marine diatom Coscinodiscus wailesii (Bacillariophyta)',
    '28': 'Diversity and phylogenetic position of unarmored dinoflagellates from the coastal waters of Korea',
    '29': 'Semi-daily variations in populations of the dinoflagellates Dinophysis acuminata and a mixotrophic prey ciliate, Mesodinium rubrum',
    '31': 'Phased cell division and facultative mixotrophy of Fragilidium duplocampanaeforme',
    '32': 'The acquisition of plastids/phototrophy in heterotrophic dinoflagellates',
    '33': 'The marine tintinnid ciliate Favella ehrenbergii',
    '34': 'Amoebophrya spp. from the bloom-forming dinoflagellate Cochlodinium polykrikoides',
    '35': 'Spatio-temporal distribution of the parasitic dinoflagellate Amoebophrya sp.',
    '38': 'Red tides in Shiwa Bay, Korea in 2011',
    '39': 'Molecular diversity of the syndinean genus Euduboscquella based on single-cell PCR analysis',
    '40': 'Dynamics of actin evolution in dinoflagellates',
    '41': 'Feeding behavior of the thecate mixotrophic dinoflagellate Oxyphysis oxytoxoides',
    '42': 'Tintinnophagus acutus n. g., n. sp. (Phylum Ciliophora), a Parasite of Tintinnid Ciliates',
    '43': 'Does Dinophysis caudata have permanent plastids?',
    '44': 'First successful culture of the marine dinoflagellate Dinophysis acuminata'
}

for k, title in titles.items():
    query = urllib.parse.quote(title)
    url = f'https://api.crossref.org/works?query.bibliographic={query}&select=DOI,title&rows=1'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'mailto:test@example.com'})
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read())
        items = data['message']['items']
        if items:
            doi = items[0].get("DOI")
            t = items[0].get("title", [""])[0]
            print(f'[{k}] Found DOI: {doi} - Title: {t}')
        else:
            print(f'[{k}] Not found')
    except Exception as e:
        print(f'[{k}] Error: {e}')
