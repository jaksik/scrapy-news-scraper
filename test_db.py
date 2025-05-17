from dotenv import load_dotenv
import os
import datetime
from mongoengine import connect, disconnect
from webscraper.models import Article

def test_mongodb():
    # Load environment variables
    load_dotenv()
    
    # Get MongoDB URI
    mongodb_uri = os.getenv('MONGODB_URI')
    if not mongodb_uri:
        print("Error: MONGODB_URI environment variable not set")
        return False
    
    try:
        # Ensure no existing connections
        disconnect()
        
        # Connect to MongoDB with explicit database name
        connect(db='dashboard_data', host=mongodb_uri, retryWrites=True)
        print("Successfully connected to MongoDB dashboard_data database")
        
        # Create test articles with new content
        test_articles = [
               {
                "title": "New AI Language Model Achieves Human-Level Performance in Medical Diagnosis",
                "link": "https://techcrunch.com/2025/05/13/ai-medical-diagnosis",  # Changed from 'url' to 'link'
                "source": "TechCrunch",
                "publishedAt": datetime.datetime.utcnow(),
                "searchTerm": "Startups",
                "category": "Artificial Intelligence",
                "createdAt": datetime.datetime.utcnow()
            },
            {
                "title": "AI-Powered Chatbots Revolutionize Customer Service",
                "link": "https://techcrunch.com/2025/05/14/ai-chatbots-customer-service",  # Changed from 'url' to 'link'
                "source": "TechCrunch",
                "publishedAt": datetime.datetime.utcnow(),
                "searchTerm": "Startups",
                "category": "Artificial Intelligence",
                "createdAt": datetime.datetime.utcnow()
            },
            {
                "title": "New AI Model Predicts Stock Market Trends with High Accuracy",
                "link": "https://techcrunch.com/2025/05/15/ai-stock-market-prediction",  # Changed from 'url' to 'link'
                "source": "TechCrunch",
                "publishedAt": datetime.datetime.utcnow(),
                "searchTerm": "Startups",
                "category": "Artificial Intelligence",
                "createdAt": datetime.datetime.utcnow()
            }
            # Add more articles as needed
        ]
        
        # Save articles
        for article_data in test_articles:
            # Check if article already exists
            existing = Article.objects(link=article_data['link']).first()  # Changed from 'url' to 'link'
            if not existing:
                article = Article(**article_data)
                article.save()
                print(f"Added article: {article.title}")
            else:
                print(f"Article already exists: {article_data['title']}")
        
        # Verify articles in database
        all_articles = Article.objects()
        print(f"\nTotal articles in database: {len(all_articles)}")
        for article in all_articles:
            print(f"- {article.title}")
        
        print("\nDatabase connection test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    finally:
        disconnect()

if __name__ == "__main__":
    test_mongodb()