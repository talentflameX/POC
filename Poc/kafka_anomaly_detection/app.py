# app.py
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from config.db_config import get_mongo_connection
from datetime import datetime

app = FastAPI()
db = get_mongo_connection()
anomaly_collection = db["anomalies"]

# ---- Models ----
class Anomaly(BaseModel):
    System_Name: str
    KPI_Name: str
    Total_Val: float
    Avg_Val: float
    Min_Val: float
    Max_Val: float
    Timestamp: str
    LSTM_Anomaly: bool
    IF_Anomaly: bool
    Deviation: float
    Detected_At: str

# ---- Endpoints ----
@app.get("/anomalies", response_model=List[Anomaly])
def get_all_anomalies():
    anomalies = list(anomaly_collection.find())
    if not anomalies:
        raise HTTPException(status_code=404, detail="No anomalies found")
    return anomalies

@app.get("/anomalies/filter", response_model=List[Anomaly])
def filter_anomalies(
    system_name: Optional[str] = None,
    kpi_name: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    query = {}
    if system_name:
        query["System_Name"] = system_name
    if kpi_name:
        query["KPI_Name"] = kpi_name
    if start_date and end_date:
        query["Detected_At"] = {
            "$gte": start_date,
            "$lte": end_date
        }
    anomalies = list(anomaly_collection.find(query))
    if not anomalies:
        raise HTTPException(status_code=404, detail="No anomalies found for the given filters")
    return anomalies
