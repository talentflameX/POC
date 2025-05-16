# stream_processor.py
from kafka import KafkaConsumer, KafkaProducer
import json

BROKER_URL = 'kafka:9092'
INPUT_TOPIC = 'raw_data'
OUTPUT_TOPIC = 'processed_data'

# Initialize Consumer
consumer = KafkaConsumer(
    INPUT_TOPIC,
    bootstrap_servers=[BROKER_URL],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Initialize Producer
producer = KafkaProducer(
    bootstrap_servers=[BROKER_URL],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("🔎 Listening for data from Kafka...")

for message in consumer:
    data = message.value
    
    # Sample transformation: Add a 'processed' flag
    data['processed'] = True
    print(f"🔄 Processed data: {data}")
    
    # Send to the next topic
    producer.send(OUTPUT_TOPIC, data)
    producer.flush()
