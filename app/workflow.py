from typing import Any, Dict
from langgraph.graph import StateGraph, END
import os 
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from .models import ListingResearchState, ListingInfo, ListingAnalysis
from .firecrawl import FirecrawlService
from .prompts import ListingPrompts


class ListingWorkflow:
    def __init__(self):
        self.firecrawl = FirecrawlService()


        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama3-8b-8192",  
            temperature=0.3
        )

        self.prompts = ListingPrompts()
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        graph = StateGraph(ListingResearchState)
        graph.add_node("extract_listings", self._extract_listings_step)
        graph.add_node("analyze_listings", self._analyze_listings_step)
        graph.add_node("recommend_listings", self._recommend_listings_step)
        graph.set_entry_point("extract_listings")
        graph.add_edge("extract_listings", "analyze_listings")
        graph.add_edge("analyze_listings", "recommend_listings")
        graph.add_edge("recommend_listings", END)
        return graph.compile()

    def _extract_listings_step(self, state: ListingResearchState) -> Dict[str, Any]:
        print(f"Searching listings for: {state.query}")
        results = self.firecrawl.search_listings(state.query, num_results=5)

        all_listings = []
        for result in results.data:
            url = result.get("url", "")
            title = result.get("metadata", {}).get("title", "No title")
            scraped = self.firecrawl.scrape_listing_page(url)
            if scraped:
                listing = ListingInfo(
                    title=title,
                    url=url,
                    description=scraped.markdown[:1500]
                )
                all_listings.append(listing)

        return {"listings": all_listings, "search_results": results.data}

    def _analyze_listing_content(self, title: str, content: str) -> ListingAnalysis:
        structured_llm = self.llm.with_structured_output(ListingAnalysis)
        messages = [
            SystemMessage(content=self.prompts.LISTING_ANALYSIS_SYSTEM),
            HumanMessage(content=self.prompts.listing_analysis_user(title, content))
        ]
        try:
            return structured_llm.invoke(messages)
        except Exception as e:
            print(f"[ERROR] analysis failed: {e}")
            return ListingAnalysis(description="Failed to analyze")

    def _analyze_listings_step(self, state: ListingResearchState) -> Dict[str, Any]:
        enriched = []
        for listing in state.listings:
            analysis = self._analyze_listing_content(listing.title, listing.description)
            listing.price = analysis.price
            listing.bedrooms = analysis.bedrooms
            listing.location = analysis.location
            listing.amenities = analysis.amenities
            listing.contact_info = analysis.contact_info
            listing.description = analysis.description
            enriched.append(listing)

        return {"listings": enriched}

    def _recommend_listings_step(self, state: ListingResearchState) -> Dict[str, Any]:
        print("Generating recommendation...")
        listing_data = ",\n".join([listing.json() for listing in state.listings])
        messages = [
            SystemMessage(content=self.prompts.RECOMMENDATIONS_SYSTEM),
            HumanMessage(content=self.prompts.recommendations_user(state.query, listing_data))
        ]
        try:
            response = self.llm.invoke(messages)
            return {"analysis": response.content}
        except Exception as e:
            print(f"[ERROR] recommendation failed: {e}")
            return {"analysis": "Failed to generate recommendations."}

    def run(self, query: str) -> ListingResearchState:
        initial_state = ListingResearchState(query=query)
        final_state = self.workflow.invoke(initial_state)
        return ListingResearchState(**final_state)
