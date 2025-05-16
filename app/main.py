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
    """Handler to check download."""
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
    """Healthcheck."""
    return {"status": "OK"}