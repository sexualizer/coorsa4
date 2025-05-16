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

from app.db import Client, get_ch_client
from app.main import test_api

load_dotenv()
token = os.getenv("API_TOKEN")

class Stealer:
    def __init__(self, api_key: str, ch_client: Client):
        self.api_url = "https://api.football-data.org/v4"
        self.headers = {"X-Auth-Token": api_key}
        self.ch_client = ch_client

    def get_existing_match_ids(self) -> set:
        """Получаем ID матчей, которые уже есть в БД"""
        query = "SELECT id FROM project.matches"
        res = self.ch_client.execute(query)
        return {row[0] for row in res}

    def fetch_matches(self, days: int = 1) -> List[Dict]:
        """Получаем матчи за последние N дней"""
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
        """Преобразуем структуру API под нашу таблицу"""
        return {
            'id': match['id'],
            'area_name': match['area']['name'],
            'competition_name': match['competition']['name'],
            'home_team': match['homeTeam']['name'],
            'away_team': match['awayTeam']['name'],
            'utc_date': match['utcDate'],
            'status': match['status'],
            'home_score': match.get('score', {}).get('fullTime', {}).get('home'),
            'away_score': match.get('score', {}).get('fullTime', {}).get('away'),
            'winner': match.get('score', {}).get('winner'),
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    def update_matches(self):
        """Основной метод обновления данных"""
        existing_ids = self.get_existing_match_ids()
        matches = self.fetch_matches(days=3)  # Берем матчи за 3 дня

        new_matches = [
            self.transform_match(m)
            for m in matches
            if m['id'] not in existing_ids
        ]

        if new_matches:
            self.insert_matches(new_matches)
            print(f"Добавлено {len(new_matches)} новых матчей")
        else:
            print("Новых матчей не найдено")

    def insert_matches(self, matches: List[Dict]):
        """Пакетная вставка в ClickHouse"""
        query = """
        INSERT INTO project.matches (
            id
            , area_name
            , competition_name
            , home_team
            , away_team
            , utc_date
            , status
            , home_score
            , away_score
            , winner
            , last_updated
        ) VALUES """
        self.ch_client.execute(query, matches)


client = get_ch_client()
stealer = Stealer(token, client)
print(stealer.fetch_matches(3))