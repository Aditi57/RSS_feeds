import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

# Define stopwords for English
stop_words = set(stopwords.words('english'))

# Function to clean, tokenize, remove stopwords, and lemmatize the text
def preprocess(text):
    # Tokenization and lowercase the text
    tokens = word_tokenize(text.lower())
    
    # Remove stopwords and non-alphabetic tokens
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    
    # Lemmatization using spaCy
    doc = nlp(' '.join(filtered_tokens))
    lemmatized_tokens = [token.lemma_ for token in doc]
    
    return ' '.join(lemmatized_tokens)


df = pd.read_csv("training_dataset.csv")
print(df.head(5))

# Preprocess the news articles
df['cleaned_content'] = df['content'].apply(preprocess)


# TF-IDF vectorizer to convert text into numerical features
tfidf = TfidfVectorizer(max_features=5000)
X = tfidf.fit_transform(df['cleaned_content'])

# Labels (categories)
y = df['category']


#Training

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model 1: Naive Bayes Classifier
nb_model = MultinomialNB()
nb_model.fit(X_train, y_train)
joblib.dump(nb_model, 'naive_bayes_news_classifier.pkl')

# Model 2: Logistic Regression Classifier
lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_train, y_train)
joblib.dump(lr_model, 'logistic_regression_news_classifier.pkl')

# Predict on the test set
nb_predictions = nb_model.predict(X_test)
lr_predictions = lr_model.predict(X_test)

# Evaluate the models
print("Naive Bayes Accuracy:", accuracy_score(y_test, nb_predictions))
print("Naive Bayes Classification Report:\n", classification_report(y_test, nb_predictions))

print("Logistic Regression Accuracy:", accuracy_score(y_test, lr_predictions))
print("Logistic Regression Classification Report:\n", classification_report(y_test, lr_predictions))



# Also, save the TF-IDF vectorizer, since you'll need it for preprocessing future articles
joblib.dump(tfidf, 'tfidf_vectorizer.pkl')
