import pandas as pd
import sqlite3
import os

def setup_database():
    csv_path = "../data/final_segments.csv"
    db_path = "../data/customers.db"
    
    print("Loading segmented data...")
    df = pd.read_csv(csv_path)
    
    print("Connecting to SQLite database...")
    conn = sqlite3.connect(db_path)
    
    print("Saving data to database...")
    # Save the dataframe to a SQL table named 'customers'
    df.to_sql("customers", conn, if_exists="replace", index=False)
    
    conn.close()
    print(f"✅ Database setup complete! SQLite DB saved to {db_path}")

if __name__ == "__main__":
    setup_database()