import gradio as gr
from Day5CompanyBrochure.BrochureGen import getBrochure



message_input = gr.Textbox(label="Company Name:", info="Enter company name", lines=1)
link = gr.Textbox(label="Link:", info="Enter link", lines =2)
message_output = gr.Markdown(label="Brochure:")


def wrapBrochure(url,company_name):
    yield from getBrochure(url,company_name,source='gemini')

def startBrochureApp():

    view = gr.Interface(
        fn=getBrochure,
        title="Brochure Generator", 
        inputs=[link,message_input], 
        outputs=[message_output], 
        examples=[['https://huggingface.co/',"Hugging Face."], ['https://edwarddonner.com/',"Ed Donner"]], 
        flagging_mode="never",
        theme='soft'
        )
    return view

if __name__ == '__main__':
    print('hi')