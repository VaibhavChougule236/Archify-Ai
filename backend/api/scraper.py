import requests
from bs4 import BeautifulSoup
from readability import Document

def scrape_page(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        doc = Document(response.text)
        html = doc.summary()

        soup = BeautifulSoup(html, "html.parser")

        # Remove scripts/styles
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=" ")
        cleaned = " ".join(text.split())

        return cleaned[:6000]  # limit to avoid overload

    except Exception as e:
        return ""
    
def scrape_multiple(links: list[str]) -> str:
    content = []

    for link in links:
        page_text = scrape_page(link)
        if page_text:
            content.append(page_text)

    return "\n\n".join(content)