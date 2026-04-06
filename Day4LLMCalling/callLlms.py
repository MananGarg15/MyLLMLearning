from Day4LLMCalling.messageSeries import mSeries
from openai import OpenAI
from IPython.display import Markdown,display
import os
from dotenv import load_dotenv
load_dotenv(override=True)



class Llms:
    llama = OpenAI(base_url='http://localhost:11434/v1',api_key='')
    gpt_oss = OpenAI(base_url='http://localhost:11434/v1',api_key='')
    gemini = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/",api_key=os.getenv('GOOGLE_API_KEY'))
    qwen = OpenAI(base_url="https://openrouter.ai/api/v1",api_key=os.getenv('OPENROUTER_API_KEY'))

    def callLlama(message,new=False,system_prompt = '', response_format='text'):

        if isinstance(message,str):
            messages = mSeries.LlamaMessageSeries(message=[{'role':'user','content':message}],new=new)
        else:
            messages = mSeries.LlamaMessageSeries(message=message,new=new)
        if system_prompt:
            system_message = {'role':'system','content':system_prompt}
            mSeries.LlamaMessages[0] = system_message

        response = Llms.llama.chat.completions.create(model='llama3.2',messages=messages, response_format={"type":response_format}) 
        newMessage = [{'role':'assistant','content':response.choices[0].message.content}]
        mSeries.LlamaMessageSeries(newMessage)
        display(Markdown(response.choices[0].message.content)) 
        return response.choices[0].message.content

    def callGemini(message,new=False,system_prompt = '', response_format='text'):

        if isinstance(message,str):
            messages = mSeries.GeminiMessageSeries(message=[{'role':'user','content':message}],new=new)
        else:
            messages = mSeries.GeminiMessageSeries(message=message,new=new)
        if system_prompt:
            system_message = {'role':'system','content':system_prompt}
            mSeries.geminiMessages[0] = system_message

        response = Llms.gemini.chat.completions.create(model='gemini-3-flash-preview',messages=messages, response_format={"type":response_format}) 
        newMessage = [{'role':'assistant','content':response.choices[0].message.content}]
        mSeries.GeminiMessageSeries(newMessage)
        display(Markdown(response.choices[0].message.content)) 
        return response.choices[0].message.content

    def callQwen(message,new=False,system_prompt = '', response_format='text'):

        if isinstance(message,str):
            messages = mSeries.QwenMessageSeries(message=[{'role':'user','content':message}],new=new)
        else:
            messages = mSeries.QwenMessageSeries(message=message,new=new)
        if system_prompt:
            system_message = {'role':'system','content':system_prompt}
            mSeries.qwenMessages[0] = system_message

        response = Llms.qwen.chat.completions.create(model='qwen/qwen3.6-plus:free',messages=messages, response_format={"type":response_format}) 
        newMessage = [{'role':'assistant','content':response.choices[0].message.content}]
        mSeries.QwenMessageSeries(newMessage)
        display(Markdown(response.choices[0].message.content)) 
        return response.choices[0].message.content

    def callGPT_OSS(message,new=False,system_prompt = '', response_format='text'):

        if isinstance(message,str):
            messages = mSeries.GPT_OSSMessageSeries(message=[{'role':'user','content':message}],new=new)
        else:
            messages = mSeries.GPT_OSSMessageSeries(message=message,new=new)
        if system_prompt:
            system_message = {'role':'system','content':system_prompt}
            mSeries.gpt_ossMessages[0] = system_message

        response = Llms.gpt_oss.chat.completions.create(model='gpt-oss',messages=messages, response_format={"type":response_format}) 
        newMessage = [{'role':'assistant','content':response.choices[0].message.content}]
        mSeries.GPT_OSSMessageSeries(newMessage)
        display(Markdown(response.choices[0].message.content)) 
        return response.choices[0].message.content

   

if __name__=='__main__':

    print('This is not supposed to run')