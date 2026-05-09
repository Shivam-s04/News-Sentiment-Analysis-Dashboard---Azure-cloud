# import json
# import os
# import uuid
# from dataclasses import asdict
# from models.schemas import SentimentSummary

# class DataService:
#     """
#     MOCK DATABASE SERVICE - used file to simulate db
#     """
    
#     def __init__(self, db_file: str = "local_database.json"):
#         self.db_file = db_file
        
#         # Initialize the 'database' file if it doesn't exist
#         if not os.path.exists(self.db_file):
#             with open(self.db_file, 'w') as f:
#                 json.dump([], f)
#         print(f"[System] Connected to Local Document DB: {self.db_file}")

#     def save_summary(self, summary: SentimentSummary) -> bool:
#         """
#         Saves the structured sentiment payload into our NoSQL JSON store.
#         """
#         try:
#             with open(self.db_file, 'r') as f:
#                 collection = json.load(f)

#             #  Convert Python Dataclass to a JSON dictionary
#             document = asdict(summary)
            
#            
#             document['id'] = str(uuid.uuid4())
            
#             collection.append(document)
#             with open(self.db_file, 'w') as f:
#                 json.dump(collection, f, indent=4)
                
#             return True
            
#         except Exception as e:
#             print(f"[ERROR] Database write failed: {e}")
#             return False

# Code for local data storing above, removed once nosql cloud storage was enabled. 
import os
import json
import uuid
from datetime import datetime
from azure.cosmos import CosmosClient, exceptions
from models.schemas import SentimentSummary

class DataService:
    """function: Connect to Azure Cosmos DB NoSQL."""
    
    def __init__(self):
        print(" Initializing LIVE Azure Cosmos DB Connection...")
        uri = os.environ.get("COSMOS_URI")
        key = os.environ.get("COSMOS_KEY")
        
        if not uri or not key:
            raise ValueError("CRITICAL: Missing Cosmos DB credentials in local.settings.json")
            
        
        self.client = CosmosClient(uri, credential=key)
        
        
        self.database_name = "SentimentDB"
        self.container_name = "Summaries"
        
        self.database = self.client.get_database_client(self.database_name)
        self.container = self.database.get_container_client(self.container_name)

    def save_summary(self, summary: SentimentSummary):
        summary_dict = json.loads(json.dumps(summary, default=lambda o: o.__dict__))
        
        summary_dict['id'] = str(uuid.uuid4())
        
        summary_dict['timestamp'] = datetime.utcnow().isoformat()
        
        try:
           
            self.container.create_item(body=summary_dict)
            print(f"[Success] Saved '{summary.search_term}' analytics to Cosmos DB!")
        except exceptions.CosmosHttpResponseError as e:
            print(f"[ERROR] Failed to save to Cosmos DB: {e.message}")