import pandas as pd
import os

def clean_data(input_path, output_path):
    print("Loading raw data...")
    # Note: This specific Kaggle dataset requires ISO-8859-1 encoding
    df = pd.read_csv(input_path, encoding='ISO-8859-1') 
    
    print(f"Original shape: {df.shape}")

    # 1. Drop rows with missing CustomerID (we can't segment unknown users)
    df = df.dropna(subset=['CustomerID'])

    # 2. Remove cancelled orders (InvoiceNo starts with 'C')
    df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]

    # 3. Remove negative or zero quantities and unit prices (data entry errors)
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

    # 4. Fix data types
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['CustomerID'] = df['CustomerID'].astype(int) # Convert from float

    # 5. Calculate Total Spend per item (Quantity * UnitPrice)
    # We will need this later for the 'Monetary' part of our RFM model
    df['TotalSpend'] = df['Quantity'] * df['UnitPrice']

    print(f"Cleaned shape: {df.shape}")
    
    # Save the cleaned dataset
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")

if __name__ == "__main__":
    # Paths assuming you run this from inside the 'analysis' folder
    RAW_DATA_PATH = "../data/data.csv" 
    CLEAN_DATA_PATH = "../data/cleaned_customers.csv"
    
    clean_data(RAW_DATA_PATH, CLEAN_DATA_PATH)