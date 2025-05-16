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


load_dotenv()

app = FastAPI()

@app.get("/test")
def test_api():
    """Ручка для проверки выгрузки."""
    token = os.getenv("API_TOKEN")
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
    """Ручка для проверки работы."""
    return {"status": "OK"}