import mysql.connector
import pandas as pd

# Load your cleaned review data
df = pd.read_csv('C:\Users\Administrator\Desktop\fintech-review-analysis\data\clean_reviews.csv')  # Make sure this file exists and is clean

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",     # Replace with your actual MySQL username
    password="root",   # Replace with your actual MySQL password
    database="bank_reviews"     # Make sure this DB already exists
)
cursor = conn.cursor()

# Insert banks into banks table and store their IDs
banks = df['bank_name'].unique()
bank_ids = {}
for bank in banks:
    cursor.execute("INSERT INTO banks (name, country) VALUES (%s, %s)", (bank, "Ethiopia"))
    bank_ids[bank] = cursor.lastrowid

# Insert review rows into reviews table
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO reviews (bank_id, user_name, review_text, sentiment, rating, review_date)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        bank_ids[row['bank_name']],
        row.get('user_name', 'Anonymous'),
        row['review_text'],
        row['sentiment'],
        float(row['rating']) if pd.notna(row['rating']) else None,
        row['review_date']
    ))

# Finalize insertions
conn.commit()
cursor.close()
conn.close()

