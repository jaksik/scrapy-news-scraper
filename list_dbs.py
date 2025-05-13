from pymongo import MongoClient
from dotenv import load_dotenv
import os

def list_databases():
    # Load environment variables
    load_dotenv()
    
    # Get MongoDB URI from environment
    mongodb_uri = os.getenv('MONGODB_URI')
    
    if not mongodb_uri:
        print("Error: MONGODB_URI environment variable not set")
        return
    
    try:
        # Connect to MongoDB
        client = MongoClient(mongodb_uri)
        
        # List all databases
        print("\nAvailable databases:")
        for db in client.list_databases():
            print(f"- {db['name']}")
            
        # Show collections in dashboard_data
        db = client['dashboard_data']
        print("\nCollections in 'dashboard_data':")
        for collection in db.list_collection_names():
            print(f"- {collection}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    list_databases()