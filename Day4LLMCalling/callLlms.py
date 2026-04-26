from Day4LLMCalling.messageSeries import mSeries
from openai import OpenAI
from IPython.display import Markdown,display, update_display
import os
from dotenv import load_dotenv
from Day4LLMCalling.tool_calling import handle_tool_call
load_dotenv(override=True)
import PIL



class Llms:
    openai_api_key = os.getenv('OPENAI_API_KEY')
    gemini = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/",api_key=os.getenv('GOOGLE_API_KEY'))
    openRouter = OpenAI(base_url="https://openrouter.ai/api/v1",api_key=os.getenv('OPENROUTER_API_KEY'))
    ollama = OpenAI(base_url='http://localhost:11434/v1',api_key='')
    openai = OpenAI(api_key=openai_api_key)

             
    def callModel(message,new=False,system_prompt = '', response_format='text', markdown=False, model='gpt-oss:20b', stream=False, source = 'ollama', temperature=1, chat_no=0, tools = '',
     return_tool_arguments=False,max_tokens=640000):

        match source:
            case 'ollama':        
                source = Llms.ollama
            case 'gemini':
                source = Llms.gemini
                if model =='gpt-oss:20b':
                    model='gemini-3-flash-preview'
            case 'openRouter':
                source = Llms.openRouter
                if model =='gpt-oss:20b':
                    model='openrouter/free'     
            case 'openai':
                source = Llms.openRouter
                if model =='gpt-oss:20b':
                    model='gpt-5.4-nano'  
                max_tokens=4096
            case _:
                print('please select a valid source')
                return


        if isinstance(message,dict):
            messages = mSeries.addToPromptList(message=message,new=new,model=model,chat_no=chat_no)
        else:
            messages = mSeries.addToPromptList(message=[{'role':'user','content':message}],new=new, model=model, chat_no=chat_no)
        if system_prompt:
            system_message = {'role':'system','content':system_prompt}
            if mSeries.promptList[chat_no].get(model):
                mSeries.promptList[chat_no][model][0] = system_message
            else:
                mSeries.promptList[chat_no][model] = [system_message]

        if tools:
            stream=False
        
        response = source.chat.completions.create(model=model,messages=messages, response_format={"type":response_format}, stream=stream, temperature = temperature,tools=tools,max_tokens=max_tokens)
        
        tool_arguments = []
        tool_response_obj = None

        while response.choices[0].finish_reason == 'tool_calls':
            tool_request_message = response.choices[0].message
            tool_data_response,tool_argument, tool_response_obj = handle_tool_call(tool_request_message)
            
            message = mSeries.addToPromptList([tool_request_message],model=model,chat_no=chat_no)
            message = mSeries.addToPromptList(tool_data_response,model=model,chat_no=chat_no)
            response = source.chat.completions.create(model=model,messages=messages, response_format={"type":response_format}, stream=stream, temperature = temperature,tools=tools, max_tokens=max_tokens)
            tool_arguments.append(tool_argument)

        if stream:
            display_handle = display(Markdown(''), display_id=True)
            rsp = ''
            for chunk in response:
                rsp+= chunk.choices[0].delta.content  or ''
                update_display(Markdown(rsp),display_id=display_handle.display_id)

            newMessage = [{'role':'assistant','content':rsp}]
            mSeries.addToPromptList(newMessage,model=model,chat_no=chat_no)
            return rsp
        else:
            result = response.choices[0].message.content


            print(f"Input tokens: {response.usage.prompt_tokens}")
            print(f"Output tokens: {response.usage.completion_tokens}")
            print(f"Total tokens: {response.usage.total_tokens}")
            # Define your pricing (example rates per 1M tokens)
            PRICES = {
                "input_per_1m": 0.20,  # Example cost
                "output_per_1m": 1.25  # Example cost
            }

            input_cost = (response.usage.prompt_tokens / 1_000_000) * PRICES["input_per_1m"]
            output_cost = (response.usage.completion_tokens / 1_000_000) * PRICES["output_per_1m"]
            total_cost_cents = (input_cost + output_cost) * 100

            print(f"Total calculated cost: {total_cost_cents:.4f} cents")



            newMessage = [{'role':'assistant','content':result}]
            mSeries.addToPromptList(newMessage,model=model,chat_no=chat_no)
            
            if markdown: 
                return Markdown(result)
            if return_tool_arguments:
                return result,tool_arguments, tool_response_obj
            return result

    def callModelGenerator(message,new=False,system_prompt = '', response_format='text', markdown=False, model='gpt-oss:20b', stream=True, source = 'ollama', temperature=1, chat_no=0,max_tokens=640000):

        match source:
            case 'ollama':        
                source = Llms.ollama
            case 'gemini':
                source = Llms.gemini
                if model =='gpt-oss:20b':
                    model='gemini-3-flash-preview'
            case 'openRouter':
                source = Llms.openRouter
                if model =='gpt-oss:20b':
                    model='openrouter/free'  
            case 'openai':
                source = Llms.openRouter
                if model =='gpt-oss:20b':
                    model='gpt-5.4-nano'  
                max_tokens=4096          
            case _:
                print('please select a valid source')
                return

        if isinstance(message,dict):
            messages = mSeries.addToPromptList(message=message,new=new,model=model, chat_no=chat_no)
        else:
            messages = mSeries.addToPromptList(message=[{'role':'user','content':message}],new=new, model=model, chat_no=chat_no)
        if system_prompt:
            system_message = {'role':'system','content':system_prompt}
            if mSeries.promptList[chat_no].get(model):
                mSeries.promptList[chat_no][model][0] = system_message
            else:
                mSeries.promptList[chat_no][model] = [system_message]

        response = source.chat.completions.create(model=model,messages=messages, response_format={"type":response_format}, stream=stream, temperature = temperature,max_tokens=max_tokens) 

        rsp = ''
        for chunk in response:
            rsp+= chunk.choices[0].delta.content  or ''
            yield rsp

        newMessage = [{'role':'assistant','content':rsp}]
        mSeries.addToPromptList(newMessage,model=model, chat_no=chat_no)

if __name__=='__main__':

    print('This is not supposed to run')
    
