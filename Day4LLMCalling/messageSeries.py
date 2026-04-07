class mSeries:
    geminiMessages = [{'role':'system','content':''}]
    openRouterModelMessages = {}
    ollamaMessages = {}

    @staticmethod
    def openRouterModelSeries(message,model,new = False):
        if(new or not mSeries.openRouterModelMessages.get(model) ):
            initial_message = [{'role':'system','content':''}]
            
            mSeries.openRouterModelMessages[model] = initial_message + message
            return mSeries.openRouterModelMessages[model]
        else:
            mSeries.openRouterModelMessages[model].extend(message)
            return mSeries.openRouterModelMessages[model]

    @staticmethod
    def OllamaMessageSeries(message,model,new = False):
        if(new or not mSeries.ollamaMessages.get(model) ):
            initial_message = [{'role':'system','content':''}]
            
            mSeries.ollamaMessages[model] = initial_message + message
            return mSeries.ollamaMessages[model]
        else:
            mSeries.ollamaMessages[model].extend(message)
            return mSeries.ollamaMessages[model]

    def GeminiMessageSeries(message,new = False):
        if(new):
            initial_message = [{'role':'system','content':''}]
            mSeries.geminiMessages = initial_message + message
            return mSeries.geminiMessages
        else:
            mSeries.geminiMessages.extend(message)
            return mSeries.geminiMessages


if __name__ == '__main__':
    print(mSeries.LlamaMessageSeries([{'role':'user','content':'Hi there'}]))
    print(mSeries.GeminiMessageSeries([{'role':'user','content':'Hi there'}]))
    print(mSeries.LlamaMessageSeries([{'role':'user','content':'Hi there'}]))