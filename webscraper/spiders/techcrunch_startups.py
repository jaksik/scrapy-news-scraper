import scrapy
from datetime import datetime

class TechcrunchAiSpider(scrapy.Spider):
    name = "techcrunch_startups"
    allowed_domains = ["techcrunch.com"]
    start_urls = ["https://techcrunch.com/category/startups/"]
    
    # Define class variables
    search_term = "startups"
    max_articles = 10  # Set the maximum number of articles to scrape
    article_count = 0  # Keep track of articles scraped

    def parse(self, response):
        # Find all article titles by looking for links within H3 elements
        articles = response.xpath('//h3/a')
        
        for article in articles:
            # Stop if we've reached the maximum
            if self.article_count >= self.max_articles:
                self.logger.info(f"Reached maximum of {self.max_articles} articles")
                return
            
            title = article.xpath('string()').get().strip()
            url = article.xpath('@href').get()
            
            # Try to get the publish date using multiple selectors
            date = (
                article.xpath('ancestor::article[1]//time/@datetime').get() or
                article.xpath('..//time/@datetime').get() or
                article.xpath('../..//time/@datetime').get()
            )
            
            # Only yield articles with non-empty title and valid url
            if title and url and len(title.strip()) > 0 and url.startswith('http'):
                self.article_count += 1  # Increment counter
                yield {
                    'title': title,
                    'link': url,
                    'source': 'TechCrunch',
                    'publishedAt': date,
                    'searchTerm': self.search_term,
                    'createdAt': datetime.utcnow().isoformat()
                }