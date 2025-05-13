# TechCrunch AI News Scraper

A simple web scraper that collects AI-related news articles from TechCrunch.

## Setup

1. Create and activate a Python virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install required packages:
```bash
pip install scrapy
```

## Running the Scraper

To run the scraper and save results to a JSON file:
```bash
scrapy crawl techcrunch_ai -O techcrunch_ai_results.json
```

The scraper will collect article titles and URLs from TechCrunch's AI category and save them to `techcrunch_ai_results.json`.

## Output Format

The results will be saved in JSON format with each article containing:
- `title`: The article title
- `url`: The article URL