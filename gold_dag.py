from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.append('/opt/airflow/app')  # Đảm bảo có thể import từ app/

from app.crawl import crawl_gold_data
from app.clean import clean_gold_data
from app.save import save_to_postgres

default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='gold_price_pipeline',
    default_args=default_args,
    description='Crawl, clean, and save gold prices to PostgreSQL',
    schedule_interval='0 9 * * *',  # 9h sáng mỗi ngày
    start_date=datetime(2025, 4, 5),
    catchup=False
) as dag:

    def crawl_task(**context):
        raw_data = crawl_gold_data()
        context['ti'].xcom_push(key='raw_data', value=raw_data)

    def transform_task(**context):
        raw_data = context['ti'].xcom_pull(key='raw_data', task_ids='crawl_gold')
        cleaned_data = clean_gold_data(raw_data)
        context['ti'].xcom_push(key='cleaned_data', value=cleaned_data)

    def save_task(**context):
        cleaned_data = context['ti'].xcom_pull(key='cleaned_data', task_ids='transform_gold')
        save_to_postgres(cleaned_data)

    crawl = PythonOperator(
        task_id='crawl_gold',
        python_callable=crawl_task,
        provide_context=True
    )

    transform = PythonOperator(
        task_id='transform_gold',
        python_callable=transform_task,
        provide_context=True
    )

    save = PythonOperator(
        task_id='save_gold',
        python_callable=save_task,
        provide_context=True
    )

    crawl >> transform >> save
