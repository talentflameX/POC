# lstm_trainer.py

import pandas as pd
import numpy as np
from anomaly_detection.lstm_detection import LSTMAnomalyModel
from config.db_config import get_mysql_connection

print("🔄 Connecting to MySQL database...")
connection = get_mysql_connection()
query = """
    SELECT * FROM nx1_automate.VIEW_Bhaskar_Trend_Hour 
    WHERE System_Type_Name='Chiller';
"""
df = pd.read_sql(query, connection)

print(f"✅ Fetched {len(df)} rows from MySQL for Chiller")
print(f"📝 Available Columns: {list(df.columns)}")

# ---- Preprocess Data ----
# ---- Preprocess Data ----
df['StartTime'] = pd.to_datetime(df['StartTime'])
df.set_index('StartTime', inplace=True)

values = df['Total_Val'].values.reshape(-1, 1)

# ---- Create Sequences ----
def create_sequences(data, seq_length):
    sequences = []
    labels = []
    for i in range(len(data) - seq_length):
        sequences.append(data[i:i + seq_length])
        labels.append(data[i + seq_length])
    return np.array(sequences), np.array(labels)

X, y = create_sequences(values, 10)

# ---- Reshape for LSTM ----
X = X.reshape(X.shape[0], X.shape[1], 1)

# ---- Train the Model ----
model = LSTMAnomalyModel()
model.create_model(input_shape=(X.shape[1], X.shape[2]))
model.train(X, y, epochs=10, batch_size=16)
