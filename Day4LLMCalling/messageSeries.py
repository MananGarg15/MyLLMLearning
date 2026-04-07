class mSeries:
    promptList = {}

    @staticmethod
    def addToPromptList(message,model,new = False):
        if(new or not mSeries.promptList.get(model) ):
            initial_message = [{'role':'system','content':''}]
            
            mSeries.promptList[model] = initial_message + message
            return mSeries.promptList[model]
        else:
            mSeries.promptList[model].extend(message)
            return mSeries.promptList[model]


if __name__ == '__main__':
    print(mSeries.LlamaMessageSeries([{'role':'user','content':'Hi there'}]))
    print(mSeries.GeminiMessageSeries([{'role':'user','content':'Hi there'}]))
    print(mSeries.LlamaMessageSeries([{'role':'user','content':'Hi there'}]))