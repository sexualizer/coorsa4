"""
Kafka producer class.
Author: sexualizer
Date: 09.05.2025
Project: Stealer
"""

import json

from kafka import KafkaProducer
from datetime import datetime
from json import JSONEncoder


class DateTimeEncoder(JSONEncoder):
    """Class encodes JSON files"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class Producer:
    """KafkaProducer Initial"""
    def __init__(self, bootstrap_servers: str = 'kafka:9092'):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v, cls=DateTimeEncoder).encode('utf-8'),
            acks='all',
            retries=3,
            api_version=(2, 5, 0)
        )

    def send_match(self, topic: str, data: dict) -> bool:
        """Send message to topic"""
        try:
            future = self.producer.send(topic, value=data)
            future.get(timeout=10)
            return True
        except Exception as e:
            print(f"[Kafka] Send error: {e}")
            return False

#producer = Producer()