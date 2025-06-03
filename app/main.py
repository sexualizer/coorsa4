"""
Main file with DAG.
Author: sexualizer
Date: 02.05.2025
Project: Stealer
"""

import os
import requests

from fastapi import FastAPI
from dotenv import load_dotenv

from app.utils.stealer import Stealer
#from app.kafka.consumer import Consumer
from app.utils.db import get_ch_client

load_dotenv()
token = os.getenv("API_TOKEN")

app = FastAPI()

@app.get("/test")
def test_api():
    """Handler to check download."""
    response = requests.get(
        "https://api.football-data.org/v4/matches",
        headers={"X-Auth-Token": token},
        params={
            'sort': 'date',
            'order': 'asc'
        }
    )
    return response.json()

@app.get("/health")
def health():
    """Healthcheck."""
    return {"status": "OK"}

client = get_ch_client()
# consumer = Consumer()
stealer = Stealer(token, client)
stealer.update_matches()

# try:
#     consumer.read_msg()
# except KeyboardInterrupt:
#     print("Shutting down gracefully...")
#     consumer.close_connections()


