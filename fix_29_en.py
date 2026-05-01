import re

file = 'c:/Users/JO/Desktop/marine-planktonology-lab/pages/publications_en.html'

with open(file, 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(
    r'<a href="javascript:void\(0\)" target="_blank" rel="noopener">Semi-daily variations in populations of the dinoflagellates <em>Dinophysis acuminata</em>\s+and a mixotrophic prey ciliate, <em>Mesodinium rubrum</em></a>',
    r'<a href="https://scholar.google.com/scholar?q=Semi-daily%20Variations%20in%20Populations%20of%20the%20Dinoflagellates%20Dinophysis%20acuminata%20and%20Oxyphysis%20oxytoxoides%20and%20a%20Mixotrophic%20Ciliate%20Prey%20Mesodinium%20rubrum%20in%20Masan%20Bay" target="_blank" rel="noopener">Semi-daily Variations in Populations of the Dinoflagellates <em>Dinophysis acuminata</em> and <em>Oxyphysis oxytoxoides</em> and a Mixotrophic Ciliate Prey <em>Mesodinium rubrum</em> in Masan Bay</a>',
    content
)

with open(file, 'w', encoding='utf-8') as f:
    f.write(content)
