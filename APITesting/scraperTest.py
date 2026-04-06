import requests
from bs4 import BeautifulSoup

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
if __name__ == "__main__":
    url = "https://edwarddonner.com/"
    content = scrape_text(url)
    print(content)
