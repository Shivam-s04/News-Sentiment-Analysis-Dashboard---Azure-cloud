import os
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.news_service import NewsService
from core.ai_service import AIService
from core.data_service import DataService # <-- NEW IMPORT

def run_pipeline_test():
    print("--- Starting End-to-End Architecture Test ---")
    
    settings_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'local.settings.json')
    try:
        with open(settings_path) as f:
            settings = json.load(f)
            os.environ["NEWS_API_KEY"] = settings["Values"]["NEWS_API_KEY"]
    except FileNotFoundError:
        print("Error: local.settings.json not found.")
        return

    # 1. Boot up the Microservices
    try:
        news_service = NewsService()
        ai_service = AIService()
        db_service = DataService() # <-- INITIALIZE DB
    except ValueError as e:
        print(e)
        return

    # 2. Execute the Pipeline
    test_keyword = "Electric Vehicles"
    print(f"\n[1] Fetching news for: '{test_keyword}'...")
    articles = news_service.fetch_recent_news(search_term=test_keyword, limit=3)
    
    if not articles:
        print("Test Failed.")
        return
        
    print(f"[2] Sent to AI Brain...")
    final_result = ai_service.analyze_sentiment(search_term=test_keyword, articles=articles)
    
    print(f"[3] Persisting to Database...")
    success = db_service.save_summary(final_result) # <-- SAVE COMMAND
    
    if success:
        print("\nSUCCESS! Pipeline executed and data saved. Check 'local_database.json'!")
            
if __name__ == "__main__":
    run_pipeline_test()