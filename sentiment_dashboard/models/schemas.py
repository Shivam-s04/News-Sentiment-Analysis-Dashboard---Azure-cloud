from dataclasses import dataclass, field
from typing import List
from datetime import datetime, timezone

@dataclass
class NewsArticle:
    """Represents a single news article fetched from the API."""
    title: str
    source: str
    url: str

@dataclass
class AnalyzedArticle:
    """Combines news metadata with specific AI sentiment results."""
    title: str
    source: str
    url: str
    score: float
    label: str

@dataclass
class SentimentSummary:
    search_term: str
    average_score: float
    # These remain for the "Overall" charts
    positive_score: float
    neutral_score: float
    negative_score: float
    label: str
    # CHANGED: Now we return a list of ANALYZED articles
    articles: List[AnalyzedArticle] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())