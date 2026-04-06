import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_text(url):
    try:
        # Send HTTP request
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad status codes

        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove script and style elements
        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()

        # Extract text
        text = soup.get_text(separator=' ', strip=True)

        return text

    except requests.exceptions.RequestException as e:
        return f"Error fetching {url}: {e}"

# Example usage:
# if __name__ == "__main__":
#     url = "https://edwarddonner.com/"
#     content = scrape_text(url)
#     print(content)



def get_all_links(url):
    """
    Fetches all unique anchor links from a given webpage.
    """
    try:
        # 1. Send a GET request to the URL
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Check for HTTP errors
        
        # 2. Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 3. Extract all 'href' attributes from <a> tags
        links = set()  # Use a set to avoid duplicates
        for anchor in soup.find_all('a', href=True):
            href = anchor['href']
            # Convert relative paths to absolute URLs
            absolute_url = urljoin(url, href)
            links.add(absolute_url)
            
        return list(links)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

# Example Usage:
if __name__ == "__main__":
    target_site = "https://www.google.com"
    all_links = get_all_links(target_site)
    
    print(f"Found {len(all_links)} links:")
    for link in all_links:
        print(link)