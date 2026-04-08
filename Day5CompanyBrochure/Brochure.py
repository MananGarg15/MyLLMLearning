from re import L
from Day5CompanyBrochure.BrochureContent import getBrochureContent
from Day4LLMCalling.callLlms import Llms

def getBrochure(url, company_name = '', stream=True, source = 'ollama'):
    brochure_system_prompt = """
    You are a professional business writer. Your goal is to analyze the provided company website content and summarize
     it into a short brochure for customers, investors, and potential recruits.

Instructions:

Tone: Professional and engaging.

Structure: Use clear sections for "Company Overview," "Products & Services," "Investor Highlights," "Careers & Culture," or any other titles you may find relevant

Formatting: Use Markdown with bold headers and bullet points. Do not use code blocks.

Constraint: Keep the total length concise (around 800-1000 words).
    """

    brochure_user_prompt = f"""
    The name of the company is {company_name}. Here are the contents - 

    """
    contents = getBrochureContent(url, source=source)[:5000]
    brochure_user_prompt += contents
    

    print(f'Creating brochure for {company_name}...')
    response = Llms.callModel(brochure_user_prompt,system_prompt=brochure_system_prompt,markdown=True,stream=stream)
    print(f'Brochure generated!')

    return response
