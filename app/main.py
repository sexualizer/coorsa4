from fastapi import FastAPI
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

@app.get("/test")
def test_api():
    token = os.getenv("API_TOKEN")
    response = requests.get(
        "https://api.football-data.org/v4/matches",
        headers={"X-Auth-Token": token}
    )
    return response.json()

@app.get("/health")
def health():
    return {"status": "OK"}