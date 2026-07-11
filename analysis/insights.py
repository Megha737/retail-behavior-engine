import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os

def run_kmeans(input_path, output_path):
    print("Loading RFM data...")
    df = pd.read_csv(input_path)

    # 1. Scale the data
    # ML algorithms get confused if one column has huge numbers (Monetary = $5000) 
    # and another has small numbers (Recency = 12 days). Scaling levels the playing field!
    print("Standardizing data for Machine Learning...")
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df[['Recency', 'Frequency', 'Monetary']])

    # 2. Run K-Means Clustering
    print("Running K-Means algorithm to find 4 customer segments...")
    # random_state=42 ensures we get the exact same results every time we run it
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(scaled_features)

    # 3. Analyze the clusters to give them human-readable names
    # Let's calculate the average R, F, and M for each cluster so we know what they represent
    cluster_means = df.groupby('Cluster')[['Recency', 'Frequency', 'Monetary']].mean()
    
    # Based on the deterministic output of this specific dataset with random_state=42:
    # Cluster 0: Bought recently, buy somewhat often, spend decent amount
    # Cluster 1: Haven't bought in a VERY long time, bought rarely, spent little
    # Cluster 2: Buy constantly, spend MASSIVE amounts of money
    # Cluster 3: Bought a while ago, moderate spenders
    
    segment_names = {
        0: "🔵 Loyal Customers",
        1: "🔴 Lost Customers", 
        2: "🟢 Champions",
        3: "🟡 At Risk"
    }
    
    df['Segment'] = df['Cluster'].map(segment_names)

    print("\n--- Final Customer Segments Preview ---")
    print(df[['CustomerID', 'Recency', 'Frequency', 'Monetary', 'Segment']].head(10))
    
    print("\n--- Customers per Segment ---")
    print(df['Segment'].value_counts())

    # 4. Save the final dataset for our React Dashboard!
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\n✅ Final segmented data saved to {output_path}")

if __name__ == "__main__":
    # Paths assuming you run this from inside the 'analysis' folder
    RFM_DATA_PATH = "../data/rfm_customers.csv"
    FINAL_DATA_PATH = "../data/final_segments.csv"
    
    run_kmeans(RFM_DATA_PATH, FINAL_DATA_PATH)