import azure.functions as func
import json
import logging
from core.news_service import NewsService
from core.ai_service import AIService
from core.data_service import DataService
from dataclasses import asdict

# Initialize the Azure Function App with Anonymous access for local testing
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Initialize our microservices globally so they reuse connections (Cold Start optimization)
try:
    news_service = NewsService()
    ai_service = AIService()
    db_service = DataService()
except Exception as e:
    logging.critical(f"Failed to initialize services: {e}")

@app.route(route="analyze", methods=["GET", "POST"])
def analyze_sentiment_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # 1. Extract keyword
    search_term = req.params.get('keyword')
    
    # 2. Extract dynamic limit (Default to 5 if not provided)
    limit_str = req.params.get('limit')
    try:
        limit = int(limit_str) if limit_str else 5
        # Guardrail: Force the limit to be between 1 and 15
        limit = max(1, min(limit, 15))
    except ValueError:
        limit = 5

    if not search_term:
        try:
            req_body = req.get_json()
            search_term = req_body.get('keyword')
            # Extract limit from body if it's a POST request
            if 'limit' in req_body:
                limit = max(1, min(int(req_body.get('limit')), 15))
        except (ValueError, TypeError):
            pass

    if not search_term:
         return func.HttpResponse("Please pass a 'keyword' (e.g., ?keyword=Azure).", status_code=400)

    try:
        logging.info(f"Starting pipeline for keyword: '{search_term}' (Limit: {limit})")
        
        # Pass the dynamic limit to the News API
        articles = news_service.fetch_recent_news(search_term=search_term, limit=limit)
        if not articles:
            return func.HttpResponse(f"No recent news found for '{search_term}'.", status_code=404)
            
        final_summary = ai_service.analyze_sentiment(search_term=search_term, articles=articles)
        db_service.save_summary(final_summary)
        
        return func.HttpResponse(
            body=json.dumps(asdict(final_summary)),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Pipeline Error: {e}")
        return func.HttpResponse(f"Internal Server Error: {str(e)}", status_code=500)