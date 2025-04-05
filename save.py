import psycopg2

def save_to_postgres(data):
    conn = psycopg2.connect(
        host="postgres",  # dùng tên service Docker
        database="gold_db",
        user="postgres",
        password="postgres"
    )
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gold_prices (
            id SERIAL PRIMARY KEY,
            location TEXT,
            brand TEXT,
            buy NUMERIC,
            sell NUMERIC,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    for item in data:
        cursor.execute("""
            INSERT INTO gold_prices (location, brand, buy, sell)
            VALUES (%s, %s, %s, %s)
        """, (item['location'], item['brand'], item['buy'], item['sell']))
    
    conn.commit()
    cursor.close()
    conn.close()
