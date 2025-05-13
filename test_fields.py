from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals
from webscraper.spiders.techcrunch_ai import TechcrunchAiSpider

def test_scrape():
    # Initialize the crawler process
    settings = get_project_settings()
    settings['ITEM_PIPELINES'] = {}  # Disable pipelines for testing
    process = CrawlerProcess(settings)
    
    # Store scraped items
    items = []
    
    def handle_item(item, response, spider):
        items.append(item)
        print("\nArticle found:")
        print(f"Title: {item['title']}")
        print(f"Link: {item['link']}")
        print(f"Source: {item['source']}")
        print(f"Published Date: {item['publishedAt']}")
        print(f"Search Term: {item['searchTerm']}")
        print(f"Created At: {item['createdAt']}")
        print("-" * 80)
    
    # Set up the crawler
    crawler = process.create_crawler(TechcrunchAiSpider)
    crawler.signals.connect(handle_item, signal=signals.item_scraped)
    
    # Run the spider
    process.crawl(crawler)
    process.start()
    
    # Print summary
    print(f"\nTotal articles found: {len(items)}")
    
    # Verify all required fields are present
    if items:
        print("\nVerifying required fields...")
        required_fields = ['title', 'link', 'source', 'publishedAt', 'searchTerm', 'createdAt']
        sample_item = items[0]
        for field in required_fields:
            print(f"{field}: {'✓' if field in sample_item else '✗'}")

if __name__ == "__main__":
    test_scrape()
