from sqlalchemy import create_engine, Column, String, DateTime, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL Database Configuration
# Format: mysql+pymysql://username:password@localhost/db_name
DATABASE_URL = "mysql+pymysql://username:password@localhost/newsdb"

Base = declarative_base()

class NewsArticle(Base):
    __tablename__ = 'news_articles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), unique=True)
    content = Column(Text)
    published = Column(DateTime)
    source = Column(String(255))
    category = Column(String(50))

# Create the MySQL engine
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
db_session = Session()
