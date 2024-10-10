# Example of exporting data
import csv
from models import db_session, NewsArticle

articles = db_session.query(NewsArticle).all()
with open('news_articles.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Title', 'Content', 'Published', 'Source', 'Category'])
    for article in articles:
        writer.writerow([article.title, article.content, article.published, article.source, article.category])
