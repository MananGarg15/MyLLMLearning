from Day4LLMCalling.messageSeries import mSeries
from openai import OpenAI
from IPython.display import Markdown,display, update_display
import os
from dotenv import load_dotenv
load_dotenv(override=True)



class Llms:
    gemini = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/",api_key=os.getenv('GOOGLE_API_KEY'))
    openRouter = OpenAI(base_url="https://openrouter.ai/api/v1",api_key=os.getenv('OPENROUTER_API_KEY'))
    ollama = OpenAI(base_url='http://localhost:11434/v1',api_key='')



    def callOpenRouterModel(message,new=False,system_prompt = '', response_format='text', markdown=False, model= 'openai/gpt-oss-120b:free', stream=False):

        if isinstance(message,str):
            messages = mSeries.addToPromptList(message=[{'role':'user','content':message}],model=model, new=new)
        else:
            messages = mSeries.addToPromptList(message=message,model=model,new=new)
        if system_prompt:
            system_message = {'role':'system','content':system_prompt}
            if mSeries.promptList.get(model):
                mSeries.promptList[model][0] = system_message
            else:
                mSeries.promptList[model] = [system_message]

        response = Llms.openRouter.chat.completions.create(model=model,messages=messages, response_format={"type":response_format}, stream=stream) 

        
        if stream:
            display_handle = display(Markdown(''), display_id=True)
            rsp = ''
            for chunk in response:
                rsp+= chunk.choices[0].delta.content or ''
                update_display(Markdown(rsp),display_id=display_handle.display_id)

            newMessage = [{'role':'assistant','content':rsp}]
            mSeries.addToPromptList(newMessage,model=model)
            return rsp

        else:
            result = response.choices[0].message.content

            newMessage = [{'role':'assistant','content':result}]
            mSeries.addToPromptList(newMessage,model=model)
            
            if markdown: 
                return Markdown(result)
            return result

    def callOllama(message,new=False,system_prompt = '', response_format='text', markdown=False,  model= 'gemma4:e4b', stream=False):

        if isinstance(message,str):
            messages = mSeries.addToPromptList(message=[{'role':'user','content':message}],new=new, model=model)
        else:
            messages = mSeries.addToPromptList(message=message,new=new,model=model)
        if system_prompt:
            system_message = {'role':'system','content':system_prompt}
            if mSeries.promptList.get(model):
                mSeries.promptList[model][0] = system_message
            else:
                mSeries.promptList[model] = [system_message]
                
        response = Llms.ollama.chat.completions.create(model=model,messages=messages, response_format={"type":response_format},stream=stream) 

        if stream:
            display_handle = display(Markdown(''), display_id=True)
            rsp = ''
            for chunk in response:
                rsp+= chunk.choices[0].delta.content  or ''
                update_display(Markdown(rsp),display_id=display_handle.display_id)

            newMessage = [{'role':'assistant','content':rsp}]
            mSeries.addToPromptList(newMessage,model=model)
            return rsp
        else:
            result = response.choices[0].message.content

            newMessage = [{'role':'assistant','content':result}]
            mSeries.addToPromptList(newMessage,model=model)
            
            if markdown: 
                return Markdown(result)
            return result

    def callGemini(message,new=False,system_prompt = '', response_format='text', markdown=False, model='gemini-3-flash-preview', stream=False):

        if isinstance(message,str):
            messages = mSeries.addToPromptList(message=[{'role':'user','content':message}],new=new, model = model)
        else:
            messages = mSeries.addToPromptList(message=message,new=new, model=model)
        if system_prompt:
            system_message = {'role':'system','content':system_prompt}
            if mSeries.promptList.get(model):
                mSeries.promptList[model][0] = system_message
            else:
                mSeries.promptList[model] = [system_message]

        response = Llms.gemini.chat.completions.create(model=model,messages=messages, response_format={"type":response_format}, stream=stream) 

        if stream:
            display_handle = display(Markdown(''), display_id=True)
            rsp = ''
            for chunk in response:
                rsp+= chunk.choices[0].delta.content  or ''
                update_display(Markdown(rsp),display_id=display_handle.display_id)

            newMessage = [{'role':'assistant','content':rsp}]
            mSeries.addToPromptList(newMessage,model=model)
            return rsp

        else:
            result = response.choices[0].message.content

            newMessage = [{'role':'assistant','content':result}]
            mSeries.addToPromptList(newMessage,model=model)
            
            if markdown: 
                return Markdown(result)
            return result
             

if __name__=='__main__':

    print('This is not supposed to run')
    