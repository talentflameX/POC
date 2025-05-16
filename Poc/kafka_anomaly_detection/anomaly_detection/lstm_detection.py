# lstm_detection.py

import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense
import os

MODEL_PATH = 'models/lstm_chiller.h5'   # ✅ Correct format



class LSTMAnomalyModel:
    def __init__(self):
        self.model = None

    def create_model(self, input_shape):
        """
        Build LSTM Model
        """
        model = Sequential()
        model.add(LSTM(64, input_shape=input_shape))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')
        self.model = model

    def train(self, X, y, epochs=10, batch_size=16):
        """
        Train the LSTM Model
        """
        print("🔄 Training the LSTM Model...")
        self.model.fit(X, y, epochs=epochs, batch_size=batch_size)
        self.save()
        print(f"✅ LSTM Model trained and saved to {MODEL_PATH}")

   
    def save(self):
        print(f"✅ Saving model to {MODEL_PATH}")
        self.model.save(MODEL_PATH)



    @staticmethod
    def load(self):
        print(f"✅ Loading model from {MODEL_PATH}")
        self.model = keras.models.load_model(MODEL_PATH)

