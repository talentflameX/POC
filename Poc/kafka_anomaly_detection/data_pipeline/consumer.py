# consumer.py
from kafka import KafkaConsumer
import json
import pickle
import numpy as np
from anomaly_detection.isolation_forest import ChillerAnomalyModel
from anomaly_detection.lstm_detection import LSTMAnomalyModel
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import MeanSquaredError as MSE

# ---- Configuration ----
BROKER_URL = 'kafka:9092'
TOPIC = 'raw_data'
MODEL_PATH_IF = 'models/isolation_forest_chiller.pkl'
MODEL_PATH_LSTM = 'models/lstm_chiller.h5'

# ---- Register Custom Metric ----
mse = MeanSquaredError()

# ---- Load Models ----
model_if = None
model_lstm = None

try:
    with open(MODEL_PATH_IF, 'rb') as f:
        model_if = pickle.load(f)
    print(f"✅ Isolation Forest model loaded successfully from {MODEL_PATH_IF}")
except FileNotFoundError:
    print(f"❌ Isolation Forest model not found at {MODEL_PATH_IF}. Please train the model first.")

try:
    # 👇 This is the important change
    model_lstm = load_model(MODEL_PATH_LSTM, custom_objects={'mse': mse, 'MeanSquaredError': MSE})
    print(f"✅ LSTM model loaded successfully from {MODEL_PATH_LSTM}")
except FileNotFoundError:
    print(f"❌ LSTM model not found at {MODEL_PATH_LSTM}. Please train the model first.")

# ---- Initialize Consumer ----
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=[BROKER_URL],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# ---- Process Messages ----
def detect_anomalies(message):
    """
    Detects anomalies using Isolation Forest and LSTM models.
    """
    values = np.array([[message['Total_Val']]])
    
    # --- Isolation Forest Prediction ---
    if model_if is not None:
        if_prediction = model_if.predict(values)
        if if_prediction[0] == -1:
            print(f"⚠️ [IF] Anomaly Detected: {message}")
        else:
            print(f"✅ [IF] Normal Reading: {message}")
    
    # --- LSTM Prediction ---
    if model_lstm is not None:
        values_reshaped = values.reshape(1, 1, 1)  # LSTM expects [samples, time_steps, features]
        lstm_prediction = model_lstm.predict(values_reshaped)
        if abs(lstm_prediction[0][0] - values[0][0]) > 5:  # You can change this threshold
            print(f"⚠️ [LSTM] Anomaly Detected: {message} | Predicted: {lstm_prediction[0][0]}")
        else:
            print(f"✅ [LSTM] Normal Reading: {message} | Predicted: {lstm_prediction[0][0]}")

if __name__ == "__main__":
    print("🔍 Listening to Kafka topic...")
    for message in consumer:
        print(f"📥 Message received: {message.value}")
        detect_anomalies(message.value)
