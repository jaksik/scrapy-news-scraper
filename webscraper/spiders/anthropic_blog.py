import scrapy
from datetime import datetime
import logging  # Add this import

class AnthropicBlogSpider(scrapy.Spider):
    name = "anthropic_blog"
    allowed_domains = ["anthropic.com"]
    start_urls = ["https://www.anthropic.com/news"]    
    search_term = "anthropic blog"

    def __init__(self, *args, **kwargs):
        super(AnthropicBlogSpider, self).__init__(*args, **kwargs)
        self.logger.setLevel(logging.INFO)

    def parse(self, response):
        # Find all article titles by looking for links with the post card class
        articles = response.xpath('//a[contains(@class, "PostCard_post-card__z_Sqq")]')
        
        for article in articles:
            title = article.xpath('.//h3[contains(@class, "PostCard_post-heading__Ob1pu")]/text()').get().strip()
            url = 'https://www.anthropic.com' + article.xpath('@href').get()
            
            # Try to get the publish date using the timestamp class
            date = article.xpath('.//div[contains(@class, "PostList_post-date__djrOA")]/text()').get()
            if date:
                try:
                    date_obj = datetime.strptime(date, '%B %d, %Y')
                    date = date_obj.isoformat()
                except ValueError:
                    date = None
            
            # Only yield articles with non-empty title and valid url
            if title and url and len(title.strip()) > 0 and url.startswith('http'):
                yield {
                    'title': title,
                    'link': url,
                    'source': 'Anthropic',
                    'publishedAt': date,
                    'searchTerm': self.search_term,
                    'category': '',
                    'createdAt': datetime.utcnow().isoformat()
                }