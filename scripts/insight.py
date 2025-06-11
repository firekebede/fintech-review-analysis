import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os

# Load cleaned reviews
df = pd.read_csv('data/clean_reviews.csv', parse_dates=['review_date'])

# Create output folder for plots
os.makedirs('outputs/plots', exist_ok=True)

# 1. Sentiment Distribution per Bank
plt.figure(figsize=(8,6))
sns.countplot(data=df, x='bank_name', hue='sentiment', palette='pastel')
plt.title('Sentiment Distribution per Bank')
plt.xlabel('Bank')
plt.ylabel('Count')
plt.legend(title='Sentiment')
plt.tight_layout()
plt.savefig('outputs/plots/sentiment_distribution.png')
plt.close()

# 2. Rating Distribution
plt.figure(figsize=(8,6))
sns.histplot(data=df, x='rating', bins=5, kde=True, hue='bank_name', multiple='stack')
plt.title('Rating Distribution')
plt.xlabel('Rating')
plt.ylabel('Number of Reviews')
plt.tight_layout()
plt.savefig('outputs/plots/rating_distribution.png')
plt.close()

# 3. Sentiment Trend Over Time
df['month'] = df['review_date'].dt.to_period('M')
monthly_sentiment = df.groupby(['month', 'sentiment']).size().unstack().fillna(0)
monthly_sentiment.plot(kind='line', figsize=(10,6), marker='o')
plt.title('Monthly Sentiment Trend')
plt.xlabel('Month')
plt.ylabel('Review Count')
plt.tight_layout()
plt.savefig('outputs/plots/monthly_sentiment_trend.png')
plt.close()

# 4. Word Cloud - Positive Reviews
text_pos = ' '.join(df[df['sentiment'] == 'positive']['review_text'])
wordcloud_pos = WordCloud(width=800, height=400, background_color='white').generate(text_pos)
plt.figure(figsize=(10,5))
plt.imshow(wordcloud_pos, interpolation='bilinear')
plt.axis('off')
plt.title('Positive Reviews Word Cloud')
plt.savefig('outputs/plots/positive_wordcloud.png')
plt.close()

# 5. Word Cloud - Negative Reviews
text_neg = ' '.join(df[df['sentiment'] == 'negative']['review_text'])
wordcloud_neg = WordCloud(width=800, height=400, background_color='black', colormap='Reds').generate(text_neg)
plt.figure(figsize=(10,5))
plt.imshow(wordcloud_neg, interpolation='bilinear')
plt.axis('off')
plt.title('Negative Reviews Word Cloud')
plt.savefig('outputs/plots/negative_wordcloud.png')
plt.close()

print("All Task 4 visualizations saved in 'outputs/plots'")

