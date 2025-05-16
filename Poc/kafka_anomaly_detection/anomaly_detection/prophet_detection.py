# prophet_detection.py
from fbprophet import Prophet
import pandas as pd
import pickle

class ProphetAnomalyModel:
    def __init__(self):
        self.model = Prophet()

    def train(self, df):
        """
        Trains the Prophet model. Expects a DataFrame with columns: ['ds', 'y']
        """
        print("🔄 Training Prophet model...")
        self.model.fit(df)
        print("✅ Prophet Training Complete.")

    def save_model(self, path="models/prophet_anomaly_model.pkl"):
        with open(path, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"✅ Prophet Model saved to {path}")

    def load_model(self, path="models/prophet_anomaly_model.pkl"):
        with open(path, 'rb') as f:
            self.model = pickle.load(f)
        print(f"✅ Prophet Model loaded from {path}")

    def predict(self, future_df):
        return self.model.predict(future_df)
