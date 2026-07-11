import pandas as pd
import datetime as dt
import os

def generate_rfm(input_path, output_path):
    print("Loading cleaned data...")
    df = pd.read_csv(input_path)
    
    # Ensure InvoiceDate is a datetime object
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

    # Create a reference date (usually 1 day after the last transaction in the dataset)
    # This acts as "today" so we can calculate how many days ago they bought
    latest_date = df['InvoiceDate'].max() + dt.timedelta(days=1)

    print("Calculating Recency, Frequency, and Monetary values...")
    
    # Group by CustomerID to calculate the RFM metrics
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (latest_date - x.max()).days,  # Recency: days since last purchase
        'InvoiceNo': 'nunique',                                 # Frequency: number of unique purchases
        'TotalSpend': 'sum'                                     # Monetary: total money spent
    }).reset_index()

    # Rename columns to make them clean and readable
    rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

    # Drop any edge cases where Monetary ended up zero or negative
    rfm = rfm[rfm['Monetary'] > 0]

    print("\nPreview of RFM Data:")
    print(rfm.head())
    print(f"\nTotal unique customers: {rfm.shape[0]}")

    # Save the RFM dataset
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    rfm.to_csv(output_path, index=False)
    print(f"RFM data saved to {output_path}")

if __name__ == "__main__":
    # Paths assuming you run this from inside the 'analysis' folder
    CLEAN_DATA_PATH = "../data/cleaned_customers.csv"
    RFM_DATA_PATH = "../data/rfm_customers.csv"
    
    generate_rfm(CLEAN_DATA_PATH, RFM_DATA_PATH)