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
    title = StringField(required=True, index=True)
    link = StringField(required=True, unique=True)  # Changed from url to link
    source = StringField(required=True)
    image = StringField(default=None)
    publishedAt = DateTimeField(required=True)
    articleType = StringField(default='news')
    searchTerm = StringField(required=True)
    category = StringField(default='')
    tags = ListField(StringField(), default=list)
    used = BooleanField(default=False)
    usedAt = DateTimeField(default=None)
    createdAt = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'articles',
        'indexes': [
            {'fields': ['link'], 'unique': True}
        ]
    }