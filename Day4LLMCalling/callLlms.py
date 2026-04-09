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

             
    def callModel(message,new=False,system_prompt = '', response_format='text', markdown=False, model='gpt-oss:20b', stream=False, source = 'ollama'):
        if isinstance(message,dict):
            messages = mSeries.addToPromptList(message=message,new=new,model=model)
        else:
            messages = mSeries.addToPromptList(message=[{'role':'user','content':message}],new=new, model=model)
        if system_prompt:
            system_message = {'role':'system','content':system_prompt}
            if mSeries.promptList.get(model):
                mSeries.promptList[model][0] = system_message
            else:
                mSeries.promptList[model] = [system_message]

        response = ''

        match source:
            case 'ollama':        
                response = Llms.ollama.chat.completions.create(model=model,messages=messages, response_format={"type":response_format},stream=stream) 
            case 'gemini':
                if model =='gpt-oss:20b':
                    model='gemini-3-flash-preview'
                response = Llms.gemini.chat.completions.create(model=model,messages=messages, response_format={"type":response_format},stream=stream) 
            case 'openRouter':
                if model =='gpt-oss:20b':
                    model='nvidia/nemotron-3-super-120b-a12b:free'            
                response = Llms.openRouter.chat.completions.create(model=model,messages=messages, response_format={"type":response_format},stream=stream) 
            case _:
                print('please select a valid source')
                return

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
    