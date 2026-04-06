from Utils.Scraper import scrape_text

def getWebsiteContent(url):
    content = scrape_text(url)
    return content

if __name__ == '__main__':
    print(getWebsiteContent('https://huggingface.co/'))