# producer.py
from kafka import KafkaProducer
import pandas as pd
import json
import time
from config.db_config import get_mysql_connection

# ---- Configuration ----
BROKER_URL = 'kafka:9092'
TOPIC = 'raw_data'

# Initialize the producer
producer = KafkaProducer(
    bootstrap_servers=[BROKER_URL],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

def fetch_data():
    """
    Fetches the latest Chiller data from MySQL.
    """
    print("🔄 Fetching data from MySQL...")
    connection = get_mysql_connection()
    
    query = """
    SELECT * FROM nx1_automate.VIEW_Bhaskar_Trend_Hour 
    WHERE System_Type_Name='Chiller'
    ORDER BY EndTime DESC 
    LIMIT 100;
    """
    
    df = pd.read_sql(query, connection)
    connection.close()
    
    print(f"✅ Fetched {len(df)} rows from MySQL for Chiller")
    return df

def produce_messages():
    """
    Reads MySQL data and sends it to Kafka topic.
    """
    df = fetch_data()
    
    if df.empty:
        print("❌ No data found. Exiting...")
        return
    
    for _, row in df.iterrows():
        message = {
            "System_Name": row['System_Name'],
            "KPI_Name": row['KPI_Name'],
            "Total_Val": row['Total_Val'],
            "Avg_Val": row['Avg_Val'],
            "Min_Val": row['Min_Val'],
            "Max_Val": row['Max_Val'],
            "Timestamp": str(row['EndTime'])
        }
        print(f"📡 Sending message to Kafka: {message}")
        producer.send(TOPIC, value=message)
        time.sleep(1)  # Throttle the messages to avoid overload
    
    print("✅ All messages sent to Kafka.")

if __name__ == "__main__":
    produce_messages()
