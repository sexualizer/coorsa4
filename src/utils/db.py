"""
File for connecting to Clickhouse.
Author: sexualizer
Date: 02.05.2025
Project: Stealer
"""

from clickhouse_driver import Client
from src.utils.queries import QUERIES


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
    msg = "[Clickhouse] Connected to Clickhouse at localhost:9000 in 'project' as admin"
    print(msg)
    ch_client.execute(QUERIES['insert_log'], msg)
    #ch_client.execute(QUERIES['init_db'])
except Exception as e:
    msg = f"[Clickhouse] Caught exception while connecting to localhost:9000 - {e}"
    print(msg)
    ch_client.execute(QUERIES['insert_log'], msg)