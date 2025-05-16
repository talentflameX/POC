# db_config.py
import mysql.connector
from pymongo import MongoClient

# ---- MySQL Configuration ----
MYSQL_CONFIG = {
    'user': 'Engg_intern',           
    'password': 'Omkar@DB731',       
    'host': '4.247.128.80',               
    'database': 'nx1_automate',        
    'port': 3306                             
}

def get_mysql_connection():
    """
    Establishes a connection to the MySQL database.
    """
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        print("✅ MySQL connection successful")
        return connection
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
        return None

# ---- MongoDB Configuration ----
MONGO_URI = "mongodb://root:example@mongo:27017/"
MONGO_DB_NAME = "anomaly_detection"

def get_mongo_connection():
    """
    Establishes a connection to the MongoDB database.
    """
    try:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB_NAME]
        print("✅ MongoDB connection successful")
        return db
    except Exception as e:
        print(f"❌ MongoDB Connection Error: {e}")
        return None
