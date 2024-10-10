import feedparser
from datetime import datetime
from models import NewsArticle, db_session
from sqlalchemy.exc import IntegrityError
from tasks import process_articles
import logger

RSS_FEEDS = [
    'http://qz.com/feed',
    'http://feeds.foxnews.com/foxnews/politics',
    'http://feeds.reuters.com/reuters/businessNews',
    'http://feeds.feedburner.com/NewshourWorld',
    'https://feeds.bbci.co.uk/news/world/asia/india/rss.xml'
]

def parse_feed():
    articles = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            logger.log_event(entry.summary)
            logger.log_event(entry.keys())
            article = {
                'title': entry.title,
                'content': entry.summary,
                'published': entry.published if 'published' in entry else datetime.now().isoformat(),
                'source': url
            }
            articles.append(article)
    return articles

def save_articles(articles):
    for article in articles:
        news_article = NewsArticle(
            title=article['title'],
            content=article['content'],
            published=article['published'],
            source=article['source']
        )
        try:
            db_session.add(news_article)
            db_session.commit()
        except IntegrityError:
            db_session.rollback()  # Avoid inserting duplicate articles

if __name__ == "__main__":
    articles = parse_feed()
    save_articles(articles)
    
