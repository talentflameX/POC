""# Kafka Anomaly Detection System

This system is designed to detect anomalies in chiller data using two different models:

1. **Isolation Forest** - An unsupervised machine learning algorithm.
2. **LSTM (Long Short-Term Memory)** - A neural network for time-series prediction.

## Project Structure

```
.
├── Dockerfile
├── actions
│   ├── action_handler.py
│   ├── iot_api.py
│   └── notification.py
├── agents
│   ├── preventive_agent.py
│   ├── root_cause_agent.py
│   └── suggestion_agent.py
├── anomaly_detection
│   ├── isolation_forest.py
│   ├── lstm_detection.py
│   ├── trainer.py
│   ├── lstm_trainer.py
│   └── z_score.py
├── config
│   ├── db_config.py
│   └── kafka_config.py
├── data_pipeline
│   ├── consumer.py
│   ├── producer.py
│   └── stream_processor.py
├── docker-compose.yml
├── logs
│   └── anomaly_detection.log
├── main.py
├── requirements.txt
└── tests
    ├── test_anomaly_detection.py
    ├── test_consumer.py
    └── test_producer.py
```

---

## 📦 **Setup Instructions**

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd kafka_anomaly_detection
   ```

2. **Install Docker and Docker Compose**
   Make sure Docker and Docker Compose are installed:

   ```bash
   docker --version
   docker-compose --version
   ```

3. **Build and Run Docker Containers**

   ```bash
   docker-compose up --build -d
   ```

4. **Verify Containers**
   Check if all services are running:

   ```bash
   docker ps
   ```

   You should see:

   * `kafka_anomaly_detection-kafka-1`
   * `kafka_anomaly_detection-mongo-1`
   * `kafka_anomaly_detection-anomaly_app-1`

---

## 🔄 **Model Training**

Before running the consumer, train the models:

1. **Isolation Forest**

   ```bash
   docker exec -it kafka_anomaly_detection-anomaly_app-1 python3 anomaly_detection/trainer.py
   ```

2. **LSTM Model**

   ```bash
   docker exec -it kafka_anomaly_detection-anomaly_app-1 python3 anomaly_detection/lstm_trainer.py
   ```

---

## 📡 **Data Streaming and Anomaly Detection**

1. **Start the Producer**
   This fetches data from MySQL and sends it to Kafka:

   ```bash
   docker exec -it kafka_anomaly_detection-anomaly_app-1 python3 data_pipeline/producer.py
   ```

2. **Start the Consumer**
   This listens to Kafka and runs anomaly detection:

   ```bash
   docker exec -it kafka_anomaly_detection-anomaly_app-1 python3 data_pipeline/consumer.py
   ```

---

## ⚠️ **Troubleshooting**

* If you see `NoBrokersAvailable`, make sure Kafka is running:

  ```bash
  docker logs kafka_anomaly_detection-kafka-1
  ```

* If MongoDB is not accessible, verify the port:

  ```bash
  docker logs kafka_anomaly_detection-mongo-1
  ```

* If LSTM model does not load, check the path:

  ```bash
  docker exec -it kafka_anomaly_detection-anomaly_app-1 ls /app/models
  ```

---

## 🎯 **Next Steps**

* Integrate anomaly results with the MongoDB handler.
* Visualize anomaly trends using Grafana or a dashboard.
* Add automated alerts for critical anomalies.

Happy Coding! 🚀
""
