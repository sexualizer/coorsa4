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
#from kafka import KafkaProducer

from app.utils.db import Client
from app.utils.queries import QUERIES

load_dotenv()
token = os.getenv("API_TOKEN")

class Stealer:
    def __init__(self, api_key: str, ch_client: Client):
        """Stealer Initial"""
        self.api_url = "https://api.football-data.org/v4"
        self.headers = {"X-Auth-Token": api_key}
        self.ch_client = ch_client
        # self.producer = KafkaProducer(
        #     bootstrap_servers='localhost:29092',
        #     value_serializer=lambda v: str(v).encode('utf-8')
        # )
        # print('Producer init')
        # self.open_conn()

    def open_conn(self):
        """Connection test"""
        try:
            msg = f'Kafka: Open connection {datetime.now()}'
            self.producer.send('logs', value=msg)
            print(f"Kafka: Producer sent - {msg}")
            self.producer.flush()
        except Exception as e:
            print(f"Producer - Caught exception while trying to connect to Kafka at localhost:29092: {e}")

    def send_msg(self, topic: str, msg: dict):
        """Send message into topic"""
        try:
            self.producer.send(topic, msg)
        except Exception as e:
            print(f"Catch error while trying to send message into {topic} - {e}")

    def flush(self):
        """Flush pending messages"""
        self.producer.flush()

    def get_existing_match_ids(self) -> set:
        """Get matches ID already in db"""
        query = QUERIES['get_matches_id']
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
            'utc_date': utc_date,
            'status': match['status'],
            'home_score': match.get('score', {}).get('fullTime', {}).get('home'),
            'away_score': match.get('score', {}).get('fullTime', {}).get('away'),
            'winner': match.get('score', {}).get('winner'),
            'last_updated': datetime.now()
        }

    def update_matches(self):
        """Initial method"""
        existing_ids = self.get_existing_match_ids()
        matches = self.fetch_matches(days=10) #Put a number of days here

        new_matches = [
            self.transform_match(m)
            for m in matches
            if m['id'] not in existing_ids
        ]

        #print(new_matches)
        if new_matches:
            self.ch_client.execute(QUERIES['insert_matches'] ,new_matches)
            print(f"Добавлено {len(new_matches)} новых матчей")
        else:
            print("Новых матчей не найдено")

        # if new_matches:
        #     success_count = 0
        #     for match in new_matches:
        #         if self.producer.send('matches', value=match):
        #             success_count += 1
        #     print(f"Sent {success_count}/{len(new_matches)} to Kafka")
        # else:
        #     print("No new matches found")
