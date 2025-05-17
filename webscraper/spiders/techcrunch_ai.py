import scrapy
from datetime import datetime

class TechcrunchAiSpider(scrapy.Spider):
    name = "techcrunch_ai"
    allowed_domains = ["techcrunch.com"]
    start_urls = ["https://techcrunch.com/category/artificial-intelligence/"]
    
    # Define search term as class variable
    search_term = "tech crunch ai"

    def parse(self, response):
        # Find all article titles by looking for links within H3 elements
        articles = response.xpath('//h3/a')
        
        for article in articles:
            title = article.xpath('string()').get().strip()
            url = article.xpath('@href').get()
            
            # Try to get the publish date using multiple selectors (from working test)
            date = (
                article.xpath('ancestor::article[1]//time/@datetime').get() or  # Try parent article's time
                article.xpath('..//time/@datetime').get() or                    # Try sibling time
                article.xpath('../..//time/@datetime').get()                    # Try parent's sibling time
            )
            
            # Only yield articles with non-empty title and valid url
            if title and url and len(title.strip()) > 0 and url.startswith('http'):
                yield {
                    'title': title,
                    'link': url,
                    'source': 'Tech Crunch',
                    'publishedAt': date,
                    'searchTerm': self.search_term,
                    'category': '',
                    'createdAt': datetime.utcnow().isoformat()
                }