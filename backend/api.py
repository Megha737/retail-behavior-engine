from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import pandas as pd
import shutil
import os

# --- NEW: Import our Machine Learning Engine ---
from ml_engine import process_uploaded_data

app = FastAPI(title="Customer Segmentation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "../data/customers.db"

def get_db_connection():
    return sqlite3.connect(DB_PATH)

@app.get("/api/summary")
def get_segment_summary():
    conn = get_db_connection()
    query = "SELECT Segment as name, COUNT(*) as value FROM customers GROUP BY Segment"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_dict(orient="records")

@app.get("/api/customers")
def get_top_customers(segment: str = '🟢 Champions'):
    conn = get_db_connection()
    query = """
        SELECT CustomerID, Recency, Frequency, ROUND(Monetary, 2) as Monetary 
        FROM customers 
        WHERE Segment = ? 
        ORDER BY Monetary DESC 
        LIMIT 100
    """
    df = pd.read_sql_query(query, conn, params=(segment,))
    conn.close()
    return df.to_dict(orient="records")



@app.post("/api/upload")
async def upload_dataset(file: UploadFile = File(...)):
    """Receives a CSV file, saves it, and runs the ML pipeline"""
    os.makedirs("../data", exist_ok=True)
    file_location = f"../data/{file.filename}"
    
    # 1. Save the file
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
        
    # 2. Trigger the Machine Learning Pipeline!
    process_uploaded_data(file_location, DB_PATH)
        
    return {
        "message": "File processed successfully! The dashboard has been updated.", 
        "filename": file.filename
    }