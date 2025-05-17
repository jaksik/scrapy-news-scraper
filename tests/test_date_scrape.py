from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals
import scrapy
from datetime import datetime

class TechcrunchAiSpider(scrapy.Spider):
    name = "techcrunch_ai"
    allowed_domains = ["techcrunch.com"]
    start_urls = ["https://techcrunch.com/category/artificial-intelligence/"]

    def parse(self, response):
        # Find all article titles by looking for links within H3 elements
        articles = response.xpath('//h3/a')
        
        for article in articles:
            title = article.xpath('string()').get().strip()
            url = article.xpath('@href').get()
            
            # Try to get the publish date using multiple selectors
            date = (
                article.xpath('ancestor::article[1]//time/@datetime').get() or  # Try parent article's time
                article.xpath('..//time/@datetime').get() or                    # Try sibling time
                article.xpath('../..//time/@datetime').get()                    # Try parent's sibling time
            )
            
            # Only yield articles with non-empty title and valid url
            if title and url and len(title.strip()) > 0 and url.startswith('http'):
                yield {
                    'title': title,
                    'url': url,
                    'publishedAt': date
                }

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
        print(f"URL: {item['url']}")
        print(f"Published Date: {item['publishedAt']}")
        print("-" * 80)
    
    # Set up the crawler
    crawler = process.create_crawler(TechcrunchAiSpider)
    crawler.signals.connect(handle_item, signal=signals.item_scraped)
    
    # Run the spider
    process.crawl(crawler)
    process.start()
    
    # Print summary
    print(f"\nTotal articles found: {len(items)}")

if __name__ == "__main__":
    test_scrape()
