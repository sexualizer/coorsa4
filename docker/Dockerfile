FROM apache/airflow:2.9.2

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY ../src /opt/airflow/src
COPY ../requirements.txt /opt/airflow/

RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

ENV PYTHONPATH=/opt/airflow/src:$PYTHONPATH
ENV AIRFLOW__CORE__DAGS_FOLDER=/opt/airflow/dags

USER airflow