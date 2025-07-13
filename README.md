

# 🏡 Apartment Listing Scout AI

A smart real estate research assistant that uses **Firecrawl** for scraping, **Groq LLMs** for analysis, and **FastAPI** for serving a simple frontend.

Built to help users quickly find and understand the best apartment listings based on custom search queries.

---

## 🚀 Features

- 🔍 Accepts free-text apartment queries (e.g., *"2-bedroom near McGill under $1500 with gym"*)
- 🌐 Scrapes real estate listing websites using Firecrawl
- 🧠 Uses LLMs (Groq or Hugging Face) to analyze and extract:
  - Price
  - Bedrooms
  - Location
  - Amenities
  - Contact info
  - Summary
- 📋 Ranks and displays top 5 listings
- 🖥️ Clean HTML interface via FastAPI and Jinja2

---

## 🧱 Tech Stack

| Layer         | Tech Used                     |
|---------------|-------------------------------|
| LLMs          | Groq (LLaMA 3) or Hugging Face |
| Scraping      | Firecrawl                     |
| Backend       | FastAPI                       |
| Frontend      | HTML + Jinja2                 |
| Orchestration | LangGraph                     |
| Packaging     | Uvicorn, Pydantic, Python 3.10+

---

## 🛠️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/listing-scout-ai.git
cd listing-scout-ai
```
### 2. Create .env

```bash

FIRECRAWL_API_KEY=your_firecrawl_key
GROQ_API_KEY=your_groq_key             #  using Groq

```

## 3. Install dependencies

```bash

pip install -r requirements.txt
Or with uv:
```
```bash

uv pip install -r requirements.txt
Make sure langgraph-checkpoint is also installed.
```
▶️ Run the App
```bash

uvicorn server:app --reload
Visit: http://127.0.0.1:8000

```