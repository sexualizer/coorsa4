"""
File for connecting to Clickhouse.
Author: sexualizer
Date: 02.05.2025
Project: Stealer
"""

from clickhouse_driver import Client
from app.utils.queries import QUERIES


def get_ch_client():
    """Get Clickhouse Client"""
    return Client(
        host='localhost',
        port=9000,
        user='admin',
        password='password',
        database='project'
    )
try:
    ch_client = get_ch_client()
    test = ch_client.execute(QUERIES['test_conn'])
    print("Connected to Clickhouse at localhost:9000 in 'project' as admin")
except Exception as e:
    print(f"Caught exception while connecting to localhost:9000 - {e}")