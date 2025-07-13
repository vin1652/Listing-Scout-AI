from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class ListingAnalysis(BaseModel):
    """Structured output for LLM listing analysis."""
    price: Optional[str] = None
    bedrooms: Optional[str] = None
    location: Optional[str] = None
    amenities: List[str] = []
    contact_info: Optional[str] = None
    description: str = ""

class ListingInfo(BaseModel):
    """Raw + enriched listing information."""
    title: str
    url: str
    description: str
    price: Optional[str] = None
    bedrooms: Optional[str] = None
    location: Optional[str] = None
    amenities: List[str] = []
    contact_info: Optional[str] = None

class ListingResearchState(BaseModel):
    """Tracks the agent’s state during a full listing search + analysis run."""
    query: str
    listings: List[ListingInfo] = []
    search_results: List[Dict[str, Any]] = []
    analysis: Optional[str] = None
