from Day4LLMCalling.messageSeries import mSeries
from openai import OpenAI
from IPython.display import Markdown,display
import os
from dotenv import load_dotenv
load_dotenv(override=True)



class Llms:
    gemini = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/",api_key=os.getenv('GOOGLE_API_KEY'))
    openRouter = OpenAI(base_url="https://openrouter.ai/api/v1",api_key=os.getenv('OPENROUTER_API_KEY'))
    ollama = OpenAI(base_url='http://localhost:11434/v1',api_key='')



    def callOpenRouterModel(message,new=False,system_prompt = '', response_format='text', markdown=False, model= 'qwen/qwen3.6-plus:free'):

        if isinstance(message,str):
            messages = mSeries.openRouterModelSeries(message=[{'role':'user','content':message}],model=model, new=new)
        else:
            messages = mSeries.openRouterModelSeries(message=message,model=model,new=new)
        if system_prompt:
            system_message = {'role':'system','content':system_prompt}
            if mSeries.openRouterModelMessages.get(model):
                mSeries.openRouterModelMessages[model][0] = system_message
            else:
                mSeries.openRouterModelMessages[model] = [system_message]

        response = Llms.openRouter.chat.completions.create(model=model,messages=messages, response_format={"type":response_format}) 
        result = response.choices[0].message.content

        newMessage = [{'role':'assistant','content':result}]
        mSeries.openRouterModelSeries(newMessage,model=model)
        
        if markdown: 
            return Markdown(result)
        return result


    def callOllama(message,new=False,system_prompt = '', response_format='text', markdown=False,  model= 'gemma4:e4b'):

        if isinstance(message,str):
            messages = mSeries.OllamaMessageSeries(message=[{'role':'user','content':message}],new=new, model=model)
        else:
            messages = mSeries.OllamaMessageSeries(message=message,new=new,model=model)
        if system_prompt:
            system_message = {'role':'system','content':system_prompt}
            if mSeries.ollamaMessages.get(model):
                mSeries.ollamaMessages[model][0] = system_message
            else:
                mSeries.ollamaMessages[model] = [system_message]
        response = Llms.ollama.chat.completions.create(model=model,messages=messages, response_format={"type":response_format}) 
        result = response.choices[0].message.content

        newMessage = [{'role':'assistant','content':result}]
        mSeries.OllamaMessageSeries(newMessage,model=model)
        
        print(mSeries.ollamaMessages)

        if markdown: 
            return Markdown(result)
        return result

    def callGemini(message,new=False,system_prompt = '', response_format='text', markdown=False):

        if isinstance(message,str):
            messages = mSeries.GeminiMessageSeries(message=[{'role':'user','content':message}],new=new)
        else:
            messages = mSeries.GeminiMessageSeries(message=message,new=new)
        if system_prompt:
            system_message = {'role':'system','content':system_prompt}
            mSeries.geminiMessages[0] = system_message

        response = Llms.gemini.chat.completions.create(model='gemini-3-flash-preview',messages=messages, response_format={"type":response_format}) 
        result = response.choices[0].message.content

        newMessage = [{'role':'assistant','content':result}]
        mSeries.GeminiMessageSeries(newMessage)

        if markdown: 
            return Markdown(response.choices[0].message.content)
        return result
             

if __name__=='__main__':

    print('This is not supposed to run')
    