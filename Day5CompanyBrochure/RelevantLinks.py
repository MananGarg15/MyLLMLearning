from Utils.Scraper import get_all_links
from Day4LLMCalling.callLlms import Llms
import json

def getRelevantLinks(url):
    links_system_prompt = """
You will be provided with a set of links from a website. You have to correctly identify the links most relevant to be included in the brochure
 of the company and provide them in as a JSON object, specifying what they are about. Do not include terms of service, email links, but include relavant info
 like linkedin.
Here is an example - 
{
    "links" : [ {"type":"about page","url":"https://fullurl/goes/here/about"},
                {"type":"home page","url":"https://anotherurl/goes/here/home"}
    ]
}

    """
    links = get_all_links(url)

    links_user_prompt = f"""
Here is the list of links in {url} - 

{links}    
    """
    print(f'selecting relevant links from {url}')
    response = Llms.callOpenRouterModel(system_prompt=links_system_prompt,message=links_user_prompt,new=True, response_format = "json_object")
    result =  json.loads(response)
    print(f'Found {len(result['links'])} relevant links')
    return result
