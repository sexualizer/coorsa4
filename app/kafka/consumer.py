"""
Kafka consumer class.
Author: sexualizer
Date: 09.05.2025
Project: Stealer
"""

from kafka import KafkaConsumer
from datetime import datetime

from app.utils.queries import QUERIES
from app.utils.db import get_ch_client


class Consumer:
    def __init__(self):
        """KafkaConsumer Initial"""
        self.consumer = KafkaConsumer(
            'test_topic',
            'matches',
            bootstrap_servers='localhost:29092',
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            #group_id='',
            value_deserializer=lambda x: x.decode('utf-8')
        )
        print('Consumer init')
        self.ch_client = get_ch_client()
        #self.test_conn()

    def read_msg(self):
        self.consumer.subscribe(['logs'])
        #self.consumer.group_id = 'logs_group'
        print("Reading messages...")

        for message in self.consumer:
            if message.topic == 'logs':
                log_data = {
                    'time': datetime.now(),
                    'log': str(message.value)
                }
                print(log_data)
                self.ch_client.execute(
                    QUERIES['insert_log'],
                    [log_data]
                )
                print(f"Inserted log: {message.value}")
                #self.consumer.commit()

        self.consumer.close()



    def close_connections(self):
        msg = {'message': f"Kafka: Close connection {datetime.now()}"}
        # self.ch_client.execute(QUERIES['insert_log'], msg)
        self.consumer.close()

    def process_messages(self):
        """Processing message from topic"""
        for message in self.consumer:
            try:
                data = message.value
                data['utc_date'] = datetime.fromisoformat(data['utc_date'])
                data['last_updated'] = datetime.fromisoformat(data['last_updated'])

                self.ch_client.execute(
                    QUERIES['insert_matches'],
                    [data]
                )
                print(f"[Kafka] Processed match ID: {data['id']}")
            except Exception as e:
                print(f"[Kafka] Processing error: {e}")
        self.consumer.close()
#consumer = Consumer()