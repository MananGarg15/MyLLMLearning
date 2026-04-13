class mSeries:

    promptList = [{}]

    @staticmethod
    def addToPromptList(message,model,new = False, chat_no=0):
        if chat_no>= len(mSeries.promptList) :
            mSeries.promptList.extend([{}])

        if(new or not mSeries.promptList[chat_no].get(model) ):
            initial_message = [{'role':'system','content':''}]
            
            mSeries.promptList[chat_no][model] = initial_message + message
            return mSeries.promptList[chat_no][model]
        else:
            mSeries.promptList[chat_no][model].extend(message)
            return mSeries.promptList[chat_no][model]


if __name__ == '__main__':
    print(mSeries.LlamaMessageSeries([{'role':'user','content':'Hi there'}]))
    print(mSeries.GeminiMessageSeries([{'role':'user','content':'Hi there'}]))
    print(mSeries.LlamaMessageSeries([{'role':'user','content':'Hi there'}]))