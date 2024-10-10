
# News Article Categorization System

## Objective
The objective of this project is to build an application that fetches news articles from predefined RSS feeds, stores them in a relational database, and classifies them into predefined categories based on the content. This application allows users to easily monitor news updates and categorize articles into four categories:

- Terrorism / Protest / Political Unrest / Riot
- Positive / Uplifting
- Natural Disasters
- Others

## System Architecture Overview
The application is designed as a modular system consisting of the following components:

1. **RSS Feed Parser and Data Extraction**: Collects and parses data from multiple RSS feeds.
2. **Database Storage**: Stores the fetched news articles in a relational database while avoiding duplicates.
3. **Asynchronous Task Queue**: Manages the processing of news articles for categorization via a task queue (using Celery).
4. **Categorization Engine**: Utilizes machine learning models and Natural Language Processing (NLP) to classify the articles into one of the four categories.

## Tech Stack
- **Programming Language**: Python
- **Libraries**:
  - `Feedparser` for reading and parsing RSS feeds.
  - `SQLAlchemy` for database interaction with MySQL.
  - `Celery` for managing asynchronous tasks.
  - `NLTK` or `spaCy` for natural language processing and classification.
  - `Scikit-learn` for training the machine learning model.
  - `Pandas` for data manipulation.
  - `Joblib` for dumping the model.
  - `Re` (regular expression) for extracting the relevant text.
- **Database**: MySQL
- **Task Queue**: Celery with Redis as the broker.

## Detailed Components

### 1. RSS Feed Parser and Data Extraction
The RSS Feed parser collects articles from multiple RSS feeds, processes them, and extracts relevant details such as the title, content, publication date, and source URL. The `Feedparser` library is used for parsing the RSS feed data.

#### Data Extraction Logic:
- The RSS feed URLs are provided in a list.
- For each feed, the system parses the feed and extracts fields like title, summary, publication date, and link.
- Content from the summary is extracted using regular expressions to remove image URLs and text.
- Proper logging is added to track actions.
- The system ensures no duplicate articles are fetched by checking for duplicate titles or URLs before saving them to the database.

Example RSS feed URLs used:
- `http://qz.com/feed`
- `http://feeds.foxnews.com/foxnews/politics`

### 2. Database Storage
Extracted news articles are stored in a relational database (MySQL). SQLAlchemy is used as the ORM (Object Relational Mapper) to handle database operations.

#### Database Schema:
- **Table**: `news_articles`
  - `id`: Auto-incremented primary key
  - `title`: The title of the news article (unique constraint to avoid duplicates)
  - `content`: The content or summary of the article
  - `published`: The publication date of the article
  - `source`: The URL source of the article
  - `category`: The category assigned to the article based on its content (NULL until processed)

### 3. Asynchronous Task Queue and Processing
A Celery task queue handles article categorization asynchronously. Once articles are fetched and stored, they are sent to the task queue for processing.

#### Task Queue Logic:
- Unprocessed articles are pushed into a queue.
- Celery workers fetch articles from the queue, process them, and assign a category using NLP.

### 4. Categorization Engine Using NLP
Articles are classified using Natural Language Processing (NLP) techniques with `NLTK` or `spaCy`. Machine learning models are used for more complex classification.

#### Machine Learning Approach:
- A machine learning model (e.g., TF-IDF with Naive Bayes or Logistic Regression) can be used for supervised learning.

## Logging and Error Handling
The application implements logging for tracking events such as:
- Successful RSS feed parsing.
- Database insertions and categorizations.
- Errors during feed parsing, database connections, and NLP classification.

Celery’s error handling mechanisms ensure retries in case of network or database issues.

## How to Run the Application

### Prerequisites:
- Python 3.8+
- MySQL database setup
- Redis for Celery task queue
- Required Python libraries: `feedparser`, `SQLAlchemy`, `Celery`, `nltk`, `spaCy`, `re`, `pandas`, `scikit-learn`, `joblib`

### Installation Steps:
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourrepo/newsaggregator.git
   cd newsaggregator
   ```

2. **Install the required Python packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the MySQL database**:
   - Create a MySQL database.
   - Update the database connection string in the configuration file (`models.py`).

4. **Start Redis**:
   ```bash
   redis-server
   ```

5. **Run the Celery worker**:
   ```bash
   celery -A tasks worker --loglevel=info -P solo
   ```

6. **Run the feed parser**:
   ```bash
   python feed_parser.py
   ```

## Future Enhancements
- **Machine Learning Classifier**: Fine-tune the machine learning classifier for higher accuracy.
- **Web Interface**: Create a dashboard to view categorized articles.
- **Automatic Scheduling**: Implement automatic scheduling to periodically fetch new articles using `Celery beat` or a cron job.

## Conclusion
This application provides a comprehensive solution for automatically collecting, storing, and categorizing news articles from RSS feeds. The modular design ensures the system can be easily extended with advanced machine learning models or a web-based user interface.
```

