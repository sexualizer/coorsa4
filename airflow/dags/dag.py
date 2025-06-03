"""
Main DAG.
Author: sexualizer
Date: 31.05.2025
Project: Stealer
"""

import os

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from dotenv import load_dotenv

load_dotenv()

default_args = {
    'owner': 'sexualizer',
    'depends_on_past': False,
    'start_date': datetime(2025, 5, 31),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'catchup': False
}

def update_data():
    try:
        from app.utils.stealer import Stealer
        from app.utils.db import get_ch_client

        token = os.getenv("API_TOKEN")

        ch_client = get_ch_client()
        stealer = Stealer(token, ch_client)

        stealer.update_matches()

    except Exception as e:
        print(f"Failed to update matches: {str(e)}")

with DAG(
    'pipe',
    default_args=default_args,
    schedule_interval="@hourly",
    max_active_runs=1
) as dag:

    update_task = PythonOperator(
        task_id='update_task',
        python_callable=update_data,
        dag=dag
    )

update_task