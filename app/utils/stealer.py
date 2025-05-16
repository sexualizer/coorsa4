"""
Stealer class with common methods.
Author: sexualizer
Date: 02.05.2025
Project: Stealer
"""

import requests
import os

from datetime import datetime, timedelta, timezone
from typing import List, Dict
from dotenv import load_dotenv

from app.db import Client, get_ch_client
from app.queries import QUERIES

load_dotenv()
token = os.getenv("API_TOKEN")

class Stealer:
    def __init__(self, api_key: str, ch_client: Client):
        """Stealer Initial"""
        self.api_url = "https://api.football-data.org/v4"
        self.headers = {"X-Auth-Token": api_key}
        self.ch_client = ch_client

    def get_existing_match_ids(self) -> set:
        """Get matches ID already in db"""
        query = "SELECT id FROM project.matches"
        res = self.ch_client.execute(query)
        return {row[0] for row in res}

    def fetch_matches(self, days: int = 1) -> List[Dict]:
        """Get matches of last N days"""
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
        matches = self.fetch_matches(days=3)  # Берем матчи за 3 дня

        new_matches = [
            self.transform_match(m)
            for m in matches
            if m['id'] not in existing_ids
        ]

        if new_matches:
            self.insert_matches(new_matches)
            print(f"Added {len(new_matches)} new matches")
        else:
            print("No new matches found")

    def insert_matches(self, matches: List[Dict]):
        """Insert into Clickhouse"""
        data = [
            (
                match['id'],
                match['area_name'],
                match['competition_name'],
                match['home_team'],
                match['away_team'],
                match['utc_date'],
                match['status'],
                match['home_score'],
                match['away_score'],
                match['winner'],
                match['last_updated']
            )
            for match in matches
        ]
        query = QUERIES['insert_matches']
        self.ch_client.execute(query, data)


client = get_ch_client()
stealer = Stealer(token, client)
stealer.update_matches()
