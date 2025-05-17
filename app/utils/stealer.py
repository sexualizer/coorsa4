"""
Stealer class with common methods.
Author: sexualizer
Date: 02.05.2025
Project: Stealer
"""

import requests
import os

from datetime import datetime, timedelta
from typing import List, Dict
from dotenv import load_dotenv

from app.utils.db import Client, get_ch_client
from app.kafka.producer import Producer

load_dotenv()
token = os.getenv("API_TOKEN")

class Stealer:
    def __init__(self, api_key: str, ch_client: Client):
        """Stealer Initial"""
        self.api_url = "https://api.football-data.org/v4"
        self.headers = {"X-Auth-Token": api_key}
        self.ch_client = ch_client
        self.kafka_producer = Producer('kafka:9092')

    def get_existing_match_ids(self) -> set:
        """Get matches ID already in db"""
        query = "SELECT id FROM project.matches"
        res = self.ch_client.execute(query)
        return {row[0] for row in res}

    def fetch_matches(self, days: int = 1) -> List[Dict]:
        """Get matches of last N days and send them to topic"""
        date_to = datetime.now()
        date_from = date_to - timedelta(days=days)

        params = {
            "dateFrom": date_from.strftime("%Y-%m-%d"),
            "dateTo": date_to.strftime("%Y-%m-%d")
        }
        response = requests.get(
            f"{self.api_url}/matches",
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        return response.json().get('matches', [])

    def transform_match(self, match: Dict) -> Dict:
        """Transform API response structure into table structure"""
        date_str = match['utcDate'].replace('Z', '+00:00')
        utc_date = datetime.fromisoformat(date_str)

        return {
            'id': match['id'],
            'area_name': match['area']['name'],
            'competition_name': match['competition']['name'],
            'home_team': match['homeTeam']['name'],
            'away_team': match['awayTeam']['name'],
            'utc_date': utc_date,  # datetime объект
            'status': match['status'],
            'home_score': match.get('score', {}).get('fullTime', {}).get('home'),
            'away_score': match.get('score', {}).get('fullTime', {}).get('away'),
            'winner': match.get('score', {}).get('winner'),
            'last_updated': datetime.now()  # datetime объект, а не строка
        }

    def update_matches(self):
        """Start method"""
        existing_ids = self.get_existing_match_ids()
        matches = self.fetch_matches(days=5) #Put a number of days here

        new_matches = [
            self.transform_match(m)
            for m in matches
            if m['id'] not in existing_ids
        ]

        if new_matches:
            success_count = sum(
                1 for m in new_matches
                if self.kafka_producer.send_match('matches', m)
            )
            print(f"Sent {success_count}/{len(new_matches)} to Kafka")
        else:
            print("No new matches found")
