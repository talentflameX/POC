# trainer.py
import sys
import os
import pandas as pd
from sklearn.ensemble import IsolationForest
import pickle
from config.db_config import get_mysql_connection

# ---- Fix Import Path ----
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# ---- Configuration ----
MODEL_PATH = "models/isolation_forest_chiller.pkl"  # Path to save the model

# ---- Fetch Data from MySQL ----
def fetch_historical_data():
    """
    Fetch historical data for 'Chiller' from MySQL.
    """
    print("🔄 Connecting to MySQL database...")
    connection = get_mysql_connection()
    
    query = """
    SELECT * FROM nx1_automate.VIEW_Bhaskar_Trend_Hour 
    WHERE System_Type_Name='Chiller';
    """
    
    # Using Pandas to fetch the data
    print("🔄 Running SQL Query...")
    df = pd.read_sql(query, connection)
    connection.close()
    
    print(f"✅ Fetched {len(df)} rows from MySQL for Chiller")
    print(f"📝 Available Columns: {df.columns.tolist()}")
    
    # Ensure Total_Val column exists
    if 'Total_Val' not in df.columns:
        print("❌ Column 'Total_Val' not found in the data. Please check your database.")
        return pd.DataFrame()  # Return an empty DataFrame if not found
    
    return df

# ---- Train the Model ----
def train_model(df):
    """
    Trains the Isolation Forest model and saves it to disk.
    """
    print("🔄 Training the Isolation Forest model...")
    
    # Select the Total_Val column as the feature
    X = df[['Total_Val']].values
    
    # Initialize and train Isolation Forest
    model = IsolationForest(n_estimators=100, contamination=0.05)
    model.fit(X)
    
    # Save the model
    with open(MODEL_PATH, 'wb') as model_file:
        pickle.dump(model, model_file)
    
    print(f"✅ Model trained and saved to {MODEL_PATH}")

# ---- Main Execution ----
if __name__ == "__main__":
    # Step 1: Fetch data from MySQL
    data_frame = fetch_historical_data()
    
    # Step 2: Train the model
    if not data_frame.empty:
        train_model(data_frame)
    else:
        print("❌ No data found for training.")
