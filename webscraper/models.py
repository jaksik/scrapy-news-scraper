import os
from mongoengine import connect, Document, StringField, DateTimeField, URLField
from datetime import datetime

# Initialize MongoDB connection
connect(
    db='dashboard_data',
    host=os.getenv('MONGODB_URI')
)

class Article(Document):
    title = StringField(required=True)
    url = StringField(required=True, unique=True)  # Change to StringField to avoid validation issues
    source = StringField(default='TechCrunch')
    category = StringField(default='Artificial Intelligence')
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'articles',
        'indexes': [
            {'fields': ['url'], 'unique': True, 'sparse': True}  # Add sparse index to handle nulls better
        ]
    }