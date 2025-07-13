class ListingPrompts:
    """Prompt templates for extracting and analyzing apartment listings."""

    # SYSTEM prompt to extract key info from a listing
    LISTING_ANALYSIS_SYSTEM = """You are a real estate assistant helping users analyze apartment rental listings.
Focus on identifying price, number of bedrooms, location, amenities (e.g., gym, laundry, pet-friendly), and contact information.
Your goal is to extract this information in a structured way from the text."""

    @staticmethod
    def listing_analysis_user(listing_title: str, content: str) -> str:
        return f"""Listing Title: {listing_title}
    Content: {content[:2500]}

    Extract the following as a JSON object:
    - price (e.g., "$1400/month")
    - bedrooms (e.g., "1-bedroom", "studio", "2 bedrooms")
    - location (e.g., "Downtown Montreal", "McGill Ghetto")
    - amenities (list like ["laundry", "gym", "pet-friendly"])
    - contact_info (email, phone, or other contact)
    - description (1-sentence summary of the apartment)

    Respond ONLY with valid JSON like this:
    {{
    "price": "$1400/month",
    "bedrooms": "2-bedroom",
    "location": "Mile End, Montreal",
    "amenities": ["balcony", "laundry", "pet-friendly"],
    "contact_info": "call 514-123-4567",
    "description": "Spacious 2-bedroom apartment near Peel street with a gym and balcony."
    }}
    """

    # SYSTEM prompt to recommend top listings
    RECOMMENDATIONS_SYSTEM = """You are a smart apartment matchmaker. Based on the user's needs and the listings analyzed,
recommend the best matches clearly and concisely in under 4 sentences."""

    @staticmethod
    def recommendations_user(query: str, listing_data: str) -> str:
        return f"""User Query: {query}
Listings:
{listing_data}

Based on the user’s query, briefly recommend the top 1–3 apartments. Highlight:
- Why each one is a good fit
- Price or location match
- Any key amenities (e.g., laundry, balcony, pet-friendly)

Keep it short, helpful, and user-friendly."""
