from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

from python.src.pipeline import pipeline

with DAG("dag_partidos_futbol",
		start_date=datetime(2024,2,28),
		description="DAG para obtener datos de la web de los partidos de futbol",
		schedule_interval=timedelta(days=1),
		catchup=False) as dag:

	tarea_pipeline=PythonOperator(task_id="pipeline", python_callable=pipeline)

tarea_pipeline