import pandas as pd
from transformers import pipeline

# Load preprocessed reviews
df = pd.read_csv('data/clean_reviews.csv')

# Load sentiment model
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Apply sentiment analysis
def analyze_sentiment(text):
    result = classifier(text[:512])[0]  # Limit to 512 characters
    return pd.Series([result['label'], result['score']])

df[['sentiment_label', 'sentiment_score']] = df['review'].apply(analyze_sentiment)

# Save partial result
df.to_csv('data/sentiment_reviews.csv', index=False)
print("Sentiment analysis complete. Saved to sentiment_reviews.csv.")


from sklearn.feature_extraction.text import TfidfVectorizer

# Get keywords from all reviews
vectorizer = TfidfVectorizer(stop_words='english', max_features=100)
X = vectorizer.fit_transform(df['review'])

# Extract top keywords for the corpus
keywords = vectorizer.get_feature_names_out()
df['keywords'] = df['review'].apply(lambda x: ', '.join([word for word in keywords if word in x.lower()]))

# Manually define themes based on keywords (basic approach)
def classify_theme(text):
    text = text.lower()
    if 'login' in text or 'password' in text:
        return 'Account Access Issues'
    elif 'crash' in text or 'bug' in text or 'error' in text:
        return 'App Stability'
    elif 'slow' in text or 'loading' in text or 'performance' in text:
        return 'Performance'
    elif 'interface' in text or 'ui' in text or 'navigation' in text:
        return 'User Interface'
    elif 'feature' in text or 'update' in text:
        return 'Feature Request'
    else:
        return 'Other'

df['theme'] = df['review'].apply(classify_theme)
df.to_csv('data/analyzed_reviews.csv', index=False)
print("Saved reviews with sentiment and themes.")
