"""
Main DAG.
Author: sexualizer
Date: 31.05.2025
Project: Stealer
"""
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
  'owner': 'sexualizer',
  'depends_on_past': False,
  'start_date': datetime.now(),
  'schedule_interval': "@hourly",
  'catchup': False
}

dag = DAG(
    dag_id='test',
    default_args=default_args
)

def test():
    print("Helo")

testing = PythonOperator(
    task_id='testing',
    python_callable=test,
    dag=dag
)

(testing)