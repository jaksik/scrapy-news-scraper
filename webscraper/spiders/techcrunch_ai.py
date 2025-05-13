import scrapy


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
            
            # Only yield articles with non-empty title and valid url
            if title and url and len(title.strip()) > 0 and url.startswith('http'):
                yield {
                    'title': title,
                    'url': url
                }
