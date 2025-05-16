# isolation_forest.py

from sklearn.ensemble import IsolationForest
import pickle

class ChillerAnomalyModel:
    def __init__(self, contamination=0.05):
        self.model = IsolationForest(n_estimators=100, contamination=contamination)

    def train(self, X):
        """
        Train the Isolation Forest model.
        """
        print("🔄 Training the Isolation Forest model...")
        self.model.fit(X)
        print("✅ Training complete.")

    def save_model(self, path="models/isolation_forest_chiller.pkl"):
        """
        Save the trained model to disk.
        """
        with open(path, 'wb') as model_file:
            pickle.dump(self.model, model_file)
        print(f"✅ Model saved to {path}")

    def load_model(self, path="models/isolation_forest_chiller.pkl"):
        """
        Load the model from disk.
        """
        with open(path, 'rb') as model_file:
            self.model = pickle.load(model_file)
        print(f"✅ Model loaded from {path}")

    def predict(self, X):
        """
        Predict anomalies using the trained model.
        """
        return self.model.predict(X)
