from celery import Celery
from models import NewsArticle, db_session
import spacy

# Initialize Celery
app = Celery('news_processor', broker='redis://localhost:6379/0')

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Define categories
CATEGORIES = {
    "terrorism": "Terrorism / protest / political unrest / riot",
    "natural_disasters": "Natural Disasters",
    "positive": "Positive/Uplifting",
    "others": "Others"
}

def categorize_article(content):
    doc = nlp(content)
    if any(word in doc.text.lower() for word in ["terrorism", "riot", "unrest", "protest"]):
        return CATEGORIES["terrorism"]
    elif any(word in doc.text.lower() for word in ["earthquake", "flood", "storm"]):
        return CATEGORIES["natural_disasters"]
    elif any(word in doc.text.lower() for word in ["good", "happy", "success"]):
        return CATEGORIES["positive"]
    else:
        return CATEGORIES["others"]

@app.task
def process_articles():
    articles = db_session.query(NewsArticle).filter(NewsArticle.category.is_(None)).all()
    for article in articles:
        category = categorize_article(article.content)
        article.category = category
        db_session.commit()
