import gradio as gr
import PyPDF2
from Day4LLMCalling.callLlms import Llms, mSeries
import copy

def wrapLlm(message,file_content,source,model,temperature,chat_no,):
    if file_content:
        message += f'File content: {file_content}'
    
    history = copy.deepcopy(mSeries.promptList.get(chat_no,{}).get(model,[]).copy())
    history.extend([{'role':'user','content':message},{'role':'assistant','content':''}])
    print(history)
    # history[chat_no][model][-1]
    for chunk in Llms.callModelGenerator(message,source=source, model=model, temperature=temperature, chat_no=chat_no):
        history[-1]['content']=chunk
        yield history

def update_chatbox(model,chat_no):
    return mSeries.promptList.get(chat_no,{}).get(model,[])

def create_new_chat(chat_list):
    chat_list.append(f'Chat{len(chat_list)+1}')
    return chat_list, len(chat_list)

def load_chat(chat_num):
    return chat_num

def reset_content():
    return '',''

def getFileContent(file_path):
    # For PDF
    if file_path.name.endswith('.pdf'):
        with open(file_path.name, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            content = ""
            for page in reader.pages:
                content += page.extract_text()
        return content

    if file_path.name.endswith('.txt'):
        with open(file_path.name, 'r') as f:
            content = f.read()
        return content

def startApp():

    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        chat_list = gr.State(['Chat1']) 
        chat_no = gr.State(1)
        source = gr.State('openRouter')
        model_name = gr.State('openrouter/free')
        temperature = gr.State(0)
        file_content = gr.State('')
        
        with gr.Row():
            with gr.Column(scale=1, variant='panel'):

                new_chat_btn = gr.Button('New',variant='huggingface',size='sm')

                @gr.render(inputs=[chat_list])
                def render_chats(chat_list):
                    with gr.Group():
                        for i, chat in enumerate(chat_list) :
                            chat_num = gr.State(i+1)
                            btn = gr.Button(chat,size='lg', variant= 'stop')

                            btn.click(
                                fn=load_chat, 
                                inputs=[chat_num],
                                outputs=[chat_no]
                            ).then(
                                fn=update_chatbox, 
                                inputs=[model_name,chat_no], 
                                outputs=[chat_history] )

                new_chat_btn.click(
                    fn = create_new_chat, 
                    inputs=[chat_list], 
                    outputs=[chat_list,chat_no] )

                
            with gr.Column(scale=4):

                chat_history = gr.Chatbot(label='Chat History')    
                response_box = gr.Markdown(label='Last response')
                    
                with gr.Group():    
                    user_input = gr.Textbox(
                        placeholder='Enter your prompt',
                        show_label=False,
                        scale=8)
                    submit_btn= gr.Button(
                        'enter',
                        size='sm',
                        variant='primary',
                        scale=1)

                submit_btn.click(
                    wrapLlm,
                    inputs=[user_input, file_content,source,model_name,temperature,chat_no], 
                    outputs=[chat_history]
                ).then(
                    fn = reset_content, 
                    outputs=[file_content,user_input] )

                user_input.submit(
                    wrapLlm,
                    inputs=[user_input, file_content,source,model_name,temperature,chat_no], 
                    outputs=[chat_history]
                # ).then(
                #     fn=update_chatbox, 
                #     inputs=[model_name,chat_no], 
                #     outputs=chat_history
                ).then(
                    fn = reset_content,
                    outputs=[file_content,user_input])


            with gr.Column(scale=1):
                with gr.Accordion('Adv_settings'):
                    source_selection = gr.Dropdown(
                        choices=['openRouter','gemini','ollama'],
                        label='Select source-')

                    source_selection.change(
                        fn= lambda source:source, 
                        inputs=[source_selection],
                        outputs= [source])

                    temperature_select = gr.Slider(
                        0,2,value=0,
                        step=0.1,
                        label='temp_slider')
                        
                    with gr.Group():
                        model_name_input = gr.Textbox(
                            placeholder='Enter model name',
                            value='openrouter/free',
                            label='Enter Model name')
                        
                        @gr.render(inputs=model_name)
                        def render_model_name(model_name):
                            model_btn = gr.Button(
                                model_name,
                                size='sm',
                                variant='secondary')
                            model_btn
                        
                    model_name_input.submit(
                        fn = lambda model_name:model_name,
                        inputs=[model_name_input],
                        outputs=[model_name])

                    temperature_select.change(
                        fn = lambda temperature:temperature, 
                        inputs=[temperature_select],
                        outputs=[temperature])

            
                files = gr.File(label='insert file',file_count='single',file_types=['.pdf','.txt'])  
                files.upload(fn = getFileContent, inputs=[files], outputs=[file_content] )

    return demo

if __name__ == '__main__':
    print('hi')