from kafka import KafkaProducer
from datetime import datetime

class Producer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers='localhost:29092',
             value_serializer=lambda v: str(v).encode('utf-8')
        )
        self.test_conn()

    def test_conn(self):
        msg = f'Test connection {datetime.now()}'
        self.producer.send('test_topic', value=msg)
        print(f'Sent:{msg}')
        self.producer.flush()

producer = Producer()