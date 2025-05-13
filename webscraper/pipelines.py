# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
from dotenv import load_dotenv
import logging
from mongoengine import connect, disconnect
from mongoengine.errors import NotUniqueError, ValidationError
from .models import Article


class WebscraperPipeline:
    def process_item(self, item, spider):
        return item


class MongoDBPipeline:
    def __init__(self):
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        self.mongodb_uri = os.getenv('MONGODB_URI')
        if not self.mongodb_uri:
            raise ValueError('MONGODB_URI environment variable not set')

    def open_spider(self, spider):
        # Connect to MongoDB when spider opens
        disconnect()  # Ensure no existing connections
        connect(
            host=self.mongodb_uri,
            retryWrites=True
        )
        self.logger.info("Connected to MongoDB")

    def close_spider(self, spider):
        # Disconnect from MongoDB when spider closes
        disconnect()
        self.logger.info("Disconnected from MongoDB")

    def process_item(self, item, spider):
        try:
            # Create and save article
            article = Article(
                title=item['title'],
                url=item['url']
            )
            article.save()
            return item
        except NotUniqueError:
            self.logger.info(f"Duplicate article URL: {item['url']}")
            return item
        except ValidationError as e:
            self.logger.error(f"Validation error: {str(e)}")
            return item
        except Exception as e:
            self.logger.error(f"Error saving article: {str(e)}")
            return item
