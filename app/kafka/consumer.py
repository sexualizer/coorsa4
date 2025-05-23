"""
Kafka consumer class.
Author: sexualizer
Date: 09.05.2025
Project: Stealer
"""


from kafka import KafkaConsumer
from datetime import datetime

#from app.utils.queries import QUERIES
#from app.utils.db import get_ch_client


class Consumer:
    def __init__(self, topic: str = 'matches'):
        """KafkaConsumer Initial"""
        self.consumer = KafkaConsumer(
            'test_topic',
            bootstrap_servers='localhost:29092',
            auto_offset_reset='earliest',
            value_deserializer=lambda x: x.decode('utf-8')
        )
        self.test_conn()
        #self.ch_client = get_ch_client()

    def test_conn(self):
        try:
            for message in self.consumer:
                print(f"Received: {message.value}")
        except Exception as e:
            print(f"Consumer - Caught exception while trying to connect to Kafka at localhost:9092: {e}")

    # def process_messages(self):
    #     """Processing message from topic"""
    #     for message in self.consumer:
    #         try:
    #             data = message.value
    #             data['utc_date'] = datetime.fromisoformat(data['utc_date'])
    #             data['last_updated'] = datetime.fromisoformat(data['last_updated'])
    #
    #             self.ch_client.execute(
    #                 QUERIES['insert_matches'],
    #                 [data]
    #             )
    #             print(f"[Kafka] Processed match ID: {data['id']}")
    #         except Exception as e:
    #             print(f"[Kafka] Processing error: {e}")

consumer = Consumer()