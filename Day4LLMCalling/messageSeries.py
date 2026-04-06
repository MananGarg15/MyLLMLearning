class mSeries:
    LlamaMessages = [{'role':'system','content':''}]
    geminiMessages = [{'role':'system','content':''}]
    qwenMessages = [{'role':'system','content':''}]
    gpt_ossMessages = [{'role':'system','content':''}]

    @staticmethod
    def LlamaMessageSeries(message,new = False):
        if(new):
            initial_message = [{'role':'system','content':''}]
            mSeries.LlamaMessages = initial_message + message
            return mSeries.LlamaMessages
        else:
            mSeries.LlamaMessages.extend(message)
            return mSeries.LlamaMessages

    @staticmethod
    def GPT_OSSMessageSeries(message,new = False):
        if(new):
            initial_message = [{'role':'system','content':''}]
            mSeries.gpt_ossMessages = initial_message + message
            return mSeries.gpt_ossMessages
        else:
            mSeries.gpt_ossMessages.extend(message)
            return mSeries.gpt_ossMessages

    def GeminiMessageSeries(message,new = False):
        if(new):
            initial_message = [{'role':'system','content':''}]
            mSeries.geminiMessages = initial_message + message
            return mSeries.geminiMessages
        else:
            mSeries.geminiMessages.extend(message)
            return mSeries.geminiMessages
    
    def QwenMessageSeries(message,new = False):
        if(new):
            initial_message = [{'role':'system','content':''}]
            mSeries.qwenMessages = initial_message + message
            return mSeries.qwenMessages
        else:
            mSeries.qwenMessages.extend(message)
            return mSeries.qwenMessages


if __name__ == '__main__':
    print(mSeries.LlamaMessageSeries([{'role':'user','content':'Hi there'}]))
    print(mSeries.GeminiMessageSeries([{'role':'user','content':'Hi there'}]))
    print(mSeries.LlamaMessageSeries([{'role':'user','content':'Hi there'}]))