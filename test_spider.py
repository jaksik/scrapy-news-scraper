from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals
from webscraper.spiders.techcrunch_ai import TechcrunchAiSpider

def test_spider():
    # Initialize the crawler process with project settings
    settings = get_project_settings()
    
    # Disable MongoDB pipeline for testing
    settings['ITEM_PIPELINES'] = {}
    
    # Create crawler process
    process = CrawlerProcess(settings)
    
    # Create a list to store scraped items
    items = []
    
    def collect_items(item, spider):
        items.append(item)
        print("\nScraped Article:")
        print(f"Title: {item['title']}")
        print(f"Link: {item['link']}")
        print(f"Published: {item['publishedAt']}")
        print("-" * 80)
    
    # Add spider to the process and connect signals
    crawler = process.create_crawler(TechcrunchAiSpider)
    crawler.signals.connect(collect_items, signal=signals.item_scraped)
    
    # Run the spider
    process.crawl(crawler)
    process.start()
    
    # Print summary
    print(f"\nTotal articles scraped: {len(items)}")

if __name__ == "__main__":
    test_spider()