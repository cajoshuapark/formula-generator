import requests
from bs4 import BeautifulSoup
from models import db, WebsiteContent

def scrape_website(url):
    """Scrape a website and store content in the database."""
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return f"Failed to fetch {url}, status code: {response.status_code}"

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract readable text from paragraphs and headers
        website_text = " ".join([p.get_text() for p in soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6"])])
        
        # Limit text to avoid excessive database storage
        trimmed_text = website_text[:5000]


        # Save or update website content
        website_entry = WebsiteContent.query.first()

        if website_entry:
            website_entry.content = trimmed_text  # Update existing content
        else:
            db.session.add(WebsiteContent(content=trimmed_text))  # Add new content if empty

        db.session.commit()
        return f"Website content scraped and updated successfully."

    except Exception as e:
        return f"Error scraping {url}: {e}"
        return f"Error scraping {url}: {e}"
