import os
from mongoengine import connect, Document, StringField, DateTimeField, URLField, BooleanField, ListField
from datetime import datetime

# Initialize MongoDB connection
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load environment variables from .env file
    
    MONGODB_URI = os.getenv('MONGODB_URI')
    if not MONGODB_URI:
        raise ValueError("MONGODB_URI environment variable not set")
        
    connect(
        host=MONGODB_URI,
        tz_aware=True
    )
    print("Successfully connected to MongoDB")
except Exception as e:
    print(f"Error connecting to MongoDB: {str(e)}")

class Article(Document):
    title = StringField(required=True)
    link = StringField(required=True, unique=True)
    source = StringField(required=True)
    publishedAt = DateTimeField(required=False)
    searchTerm = StringField(required=False)
    category = StringField(default='')
    createdAt = DateTimeField(required=True)

    meta = {
        'collection': 'test_four',
        'indexes': [
            {'fields': ['link'], 'unique': True}
        ]
    }