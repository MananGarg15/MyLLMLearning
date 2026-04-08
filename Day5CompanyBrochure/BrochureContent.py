from Day5CompanyBrochure.RelevantLinks import getRelevantLinks
from Day5CompanyBrochure.WebsiteContent import getWebsiteContent


def getBrochureContent(url, source = 'ollama'):
    content = getWebsiteContent(url)
    links = getRelevantLinks(url, source = source)

    brochureContent = f"""
    \n\n{content}\n\n
    """

    for link in links['links']:
        brochureContent += link['url'] + '\n\n' 
        brochureContent += getWebsiteContent(link['url']) + '\n\n'

    print('Generated Brochure Content.')

    return brochureContent