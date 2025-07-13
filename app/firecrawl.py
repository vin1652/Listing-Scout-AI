import os
from firecrawl import FirecrawlApp, ScrapeOptions
from dotenv import load_dotenv

load_dotenv()  # Loads FIRECRAWL_API_KEY from .env file


class FirecrawlService:
    def __init__(self):
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            raise ValueError("Missing FIRECRAWL_API_KEY environment variable")
        self.app = FirecrawlApp(api_key=api_key)

    def search_listings(self, query: str, num_results: int = 5):
        """
        Searches for apartment listings on supported sites.
        You can customize this to target Kijiji, Rentals.ca, Realtor.ca etc.
        """
        try:
            modified_query = f"{query} site:kijiji.ca OR site:rentals.ca OR site:realtor.ca" #f"{query} apartment for rent Montreal" 
            result = self.app.search(
                query=modified_query,
                limit=num_results
            )
            return result
        except Exception as e:
            print(f"[ERROR] search_listings: {e}")
            return []

    def scrape_listing_page(self, url: str):
        """
        Scrapes a full listing page and returns the content.
        """
        try:
            result = self.app.scrape_url(
                url
            )
            return result
        except Exception as e:
            print(f"[ERROR] scrape_listing_page: {e}")
            return None