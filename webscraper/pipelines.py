import logging
import os
from datetime import datetime
from mongoengine import connect, disconnect
from .models import Article

class MongoDBPipeline:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def open_spider(self, spider):
        # Ensure clean connection state
        disconnect()
        
        from dotenv import load_dotenv
        load_dotenv()
        
        MONGODB_URI = os.getenv('MONGODB_URI')
        if not MONGODB_URI:
            raise ValueError("MONGODB_URI environment variable not set")
            
        # Connect with alias
        connect(host=MONGODB_URI, alias='default')
        self.logger.info("Connected to MongoDB")

    def close_spider(self, spider):
        disconnect()
        self.logger.info("Disconnected from MongoDB")

    def process_item(self, item, spider):
        try:
            # Create article document
            article = Article(
                title=item['title'],
                link=item['link'],
                source=item['source'],
                publishedAt=datetime.fromisoformat(item['publishedAt']) if item['publishedAt'] else datetime.utcnow(),
                searchTerm=item['searchTerm'],
                category=item['category'],
                createdAt=datetime.fromisoformat(item['createdAt']),
            )
            article.save()
            self.logger.info(f"Saved article: {item['title']}")
            return item
        except Exception as e:
            self.logger.error(f"Error saving article: {str(e)}")
            return item