"""
Main DAG.
Author: sexualizer
Date: 31.05.2025
Project: Stealer
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'sexualizer',
    'depends_on_past': False,
    'start_date': datetime(2025, 5, 31),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'catchup': False
}

def test():
    print("Hello from Airflow")

with DAG(
    dag_id='test_dag',
    default_args=default_args,
    schedule_interval="@hourly",
    max_active_runs=1,
    tags=['test']
) as dag:

    testing_task = PythonOperator(
        task_id='testing_task',
        python_callable=test
    )
