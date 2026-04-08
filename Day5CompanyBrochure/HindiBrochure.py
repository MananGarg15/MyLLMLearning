from Day5CompanyBrochure.Brochure import getBrochure
from Day4LLMCalling.callLlms import Llms
from IPython.display import display,Markdown, update_display

def hindiBrochure(url,company_name, source='ollama'):
    brochure = getBrochure(url,company_name,False, source=source)

    print('Translating brochure in Hindi...')

    system_prompt = """
    You will be given the contents of a company brochure. You have to translate it in Hindi and give the output in markdown.
    """

    response = Llms.callModel(brochure.data,system_prompt=system_prompt,stream=True)
    return response


        
    