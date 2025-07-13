from app.workflow import ListingWorkflow

def main():
    print("🏡 Welcome to the Apartment Listing Scout Agent!")
    query = input("Enter your apartment search (e.g., '2-bedroom near McGill under $1500 with laundry'): ")

    workflow = ListingWorkflow()
    final_state = workflow.run(query)

    print("\n--- 🧾 TOP RECOMMENDATION ---")
    print(final_state.analysis)

    print("\n--- 📋 MATCHING LISTINGS ---")
    for i, listing in enumerate(final_state.listings[:5]):
        print(f"\n#{i+1}: {listing.title}")
        print(f"URL: {listing.url}")
        print(f"Price: {listing.price}")
        print(f"Bedrooms: {listing.bedrooms}")
        print(f"Location: {listing.location}")
        print(f"Amenities: {', '.join(listing.amenities)}")
        print(f"Contact: {listing.contact_info}")
        print(f"Summary: {listing.description}")

if __name__ == "__main__":
    main()