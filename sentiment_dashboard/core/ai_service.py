import os
from typing import List
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from models.schemas import NewsArticle, SentimentSummary, AnalyzedArticle

class AIService:
    """ function : connect to Azure Cognitive Services API. and send data"""
    
    def __init__(self):
        print("Initializing LIVE Azure AI Language Service...")
        
        endpoint = os.environ.get("AZURE_LANGUAGE_ENDPOINT")
        key = os.environ.get("AZURE_LANGUAGE_KEY")
        
        if not endpoint or not key:
            raise ValueError("ERROR: Missing Azure AI credentials in local.settings.json")
            
        # Microsoft Client connection
        self.client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    def analyze_sentiment(self, search_term: str, articles: List[NewsArticle]) -> SentimentSummary:
        if not articles:
            return SentimentSummary(
                search_term=search_term, average_score=0.0, 
                positive_score=0.0, neutral_score=0.0, negative_score=0.0, 
                label="Neutral", articles=[]
            )

        analyzed_articles = []
        total_pos = total_neu = total_neg = 0.0

        
        for i in range(0, len(articles), 10):
            batch = articles[i:i+10]
            documents = [article.title for article in batch]
            
            try:
                # azure connection to the AI
                results = self.client.analyze_sentiment(documents=documents)
                
                for idx, result in enumerate(results):
                    if not result.is_error:
                        # returned decimals so convert to percent
                        pos = result.confidence_scores.positive * 100
                        neu = result.confidence_scores.neutral * 100
                        neg = result.confidence_scores.negative * 100
                        
                        
                         
                        label = result.sentiment.capitalize()
                        if label == "Mixed":
                            label = "Neutral" # returns mixed instead of neutral so fixed it
                            
                        actual_confidence = max(pos, neu, neg)
                            
                        
                        analyzed_articles.append(AnalyzedArticle(
                            title=batch[idx].title,
                            source=batch[idx].source,
                            url=batch[idx].url,
                            score=round(actual_confidence, 2), 
                            label=label
                        ))
                        
                        total_pos += pos
                        total_neu += neu
                        total_neg += neg
                    else:
                        print(f"[Error] Document {idx} failed: {result.error}") #type: ignore
            except Exception as e:
                print(f"[ERROR] Azure API Call Failed: {e}")

        
        num_articles = len(analyzed_articles)
        if num_articles == 0: 
            return SentimentSummary(search_term=search_term, average_score=0, positive_score=0, neutral_score=0, negative_score=0, label="Neutral", articles=[])

        # Calculate Dashboard Averages
        avg_pos = round(total_pos / num_articles, 2)
        avg_neu = round(total_neu / num_articles, 2)
        avg_neg = round(total_neg / num_articles, 2)
        
        
        if avg_neg >= 40.0:
            overall_label = "Negative"
            final_main_score = avg_neg
        elif avg_pos >= 50.0:
            overall_label = "Positive"
            final_main_score = avg_pos
        else:
            overall_label = "Neutral" 
            final_main_score = avg_neu
            
        return SentimentSummary(
            search_term=search_term,
            average_score=final_main_score,
            positive_score=avg_pos,
            neutral_score=avg_neu,
            negative_score=avg_neg,
            label=overall_label,
            articles=analyzed_articles
        )