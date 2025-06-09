from google_play_scraper import Sort, reviews
import pandas as pd

# Bank apps and their package IDs (verify these!)
apps = {
    "CBE": "com.combanketh.mobilebanking",           # Commercial Bank of Ethiopia
    "BOA": "com.boa.boaMobileBanking",    # Bank of Abyssinia
    "Dashen": "com.dashen.dashensuperapp"   # Dashen Bank
}

all_reviews = []

for bank, app_id in apps.items():
    print(f"Scraping reviews for {bank} (app_id: {app_id})...")
    try:
        # Try different lang and country parameters if needed
        result, _ = reviews(
            app_id,
            lang='en',        # try removing this or set to 'en' to filter English reviews
            country='et',     # try 'us' or 'gb' if you get zero reviews here
            sort=Sort.NEWEST,
            count=500
        )
        
        print(f"Found {len(result)} reviews for {bank}")
        if len(result) > 0:
            print("Sample review:", result[0]["content"][:200], "...")  # print first 200 chars
            
        for r in result:
            all_reviews.append({
                "review": r["content"],
                "rating": r["score"],
                "date": r["at"].strftime("%Y-%m-%d"),
                "bank": bank,
                "source": "Google Play"
            })
    except Exception as e:
        print(f"Error scraping {bank}: {e}")

# Save to CSV if any reviews were scraped
if all_reviews:
    df = pd.DataFrame(all_reviews)
    df.to_csv("data/raw_reviews.csv", index=False)
    print(f"Saved {len(df)} reviews to data/raw_reviews.csv")
else:
    print("No reviews scraped. Please check app IDs, language, and country parameters.")


# scripts/preprocess_reviews.py
import pandas as pd

# Load raw data
df = pd.read_csv('data/raw_reviews.csv')

# Drop duplicates and missing
df.drop_duplicates(subset="review", inplace=True)
df.dropna(subset=["review", "rating", "date", "bank"], inplace=True)

# Save cleaned data
df.to_csv('data/clean_reviews.csv', index=False)
print(f"Cleaned reviews saved: {len(df)}")
