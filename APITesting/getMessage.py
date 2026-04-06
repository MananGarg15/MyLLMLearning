from scraperTest import scrape_text

system_prompt = "You are a stand-up comedian. You have to entertain the audience with whatever you are given. Make your response in markdown."
user_prompt_prefix = """Here is the text of a website. 

"""

def message_for(url,system_prompt = system_prompt,user_prompt_prefix = user_prompt_prefix):
    text = scrape_text(url) 
    message = [{'role':'system','content':system_prompt},{'role':'user','content':user_prompt_prefix + text}]
    return message

if __name__ == "__main__":
    url = "https://www.octoparse.com/blog/top-10-most-scraped-websites"
    message = message_for(url)
    print(message)