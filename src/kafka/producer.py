"""
Kafka producer class.
Author: sexualizer
Date: 09.05.2025
Project: Stealer
"""

from kafka import KafkaProducer
from datetime import datetime

class Producer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers='localhost:29092',
             value_serializer=lambda v: str(v).encode('utf-8')
        )
        #self.test_conn()

    def test_conn(self):
        """Connection test"""
        try:
            msg = f'Test connection {datetime.now()}'
            self.producer.send('test_topic', value=msg)
            print(f'Sent:{msg}')
            self.producer.flush()
        except Exception as e:
            print(f"Producer - Caught exception while trying to connect to Kafka at localhost:29092: {e}")

    def send_msg(self, topic: str, msg: dict):
        """Send message into topic"""
        try:
            self.producer.send(topic, msg)
        except Exception as e:
            print(f"Catch error while trying to send message into {topic} - {e}")

    def flush(self):
        """Flush pending messages"""
        self.producer.flush()

#producer = Producer()