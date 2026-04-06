import os
from openai import OpenAI
from dotenv import load_dotenv
from getMessage import message_for
from IPython.display import Markdown, display
load_dotenv(override=True)

GEMINI_BASE_URL ="https://generativelanguage.googleapis.com/v1beta/openai/"
api_key = os.getenv("GOOGLE_API_KEY")

gemini = OpenAI(base_url=GEMINI_BASE_URL,api_key=api_key)

def get_gemini_response(url,system_prompt = '',user_prompt_prefix = ''):
    message = message_for(url,system_prompt,user_prompt_prefix)
    response = gemini.chat.completions.create(model="gemini-3-flash-preview",messages=message)
    display(Markdown(response.choices[0].message.content))

     