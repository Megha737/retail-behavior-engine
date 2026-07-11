import pandas as pd
import datetime as dt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import sqlite3
import os

def process_uploaded_data(file_path, db_path):
    print(f"Starting ML processing for {file_path}...")
    
    # 1. Load the Data
    df = pd.read_csv(file_path, encoding='ISO-8859-1')

    # --- NEW: SAAS DATA NORMALIZATION ---
    # This automatically maps common column variations to the exact names our engine needs
    column_mapping = {
        'Customer ID': 'CustomerID',
        'Customer_ID': 'CustomerID',
        'Invoice': 'InvoiceNo',
        'Price': 'UnitPrice'
    }
    df = df.rename(columns=column_mapping)
    # ------------------------------------
    
    # 2. Clean the Data
    df = df.dropna(subset=['CustomerID'])
    df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['CustomerID'] = df['CustomerID'].astype(int)
    df['TotalSpend'] = df['Quantity'] * df['UnitPrice']

    # 3. Build RFM Model
    latest_date = df['InvoiceDate'].max() + dt.timedelta(days=1)
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (latest_date - x.max()).days,
        'InvoiceNo': 'nunique',
        'TotalSpend': 'sum'
    }).reset_index()
    rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']
    rfm = rfm[rfm['Monetary'] > 0]

    # 4. Run K-Means Clustering
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(rfm[['Recency', 'Frequency', 'Monetary']])
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    rfm['Cluster'] = kmeans.fit_predict(scaled_features)

    segment_names = {
        0: "🔵 Loyal Customers",
        1: "🔴 Lost Customers",
        2: "🟢 Champions",
        3: "🟡 At Risk"
    }
    rfm['Segment'] = rfm['Cluster'].map(segment_names)

    # 5. Overwrite the SQLite Database
    print("Saving new clusters to database...")
    conn = sqlite3.connect(db_path)
    rfm.to_sql("customers", conn, if_exists="replace", index=False)
    conn.close()
    
    print("✅ M L Processing Complete!")
    return True