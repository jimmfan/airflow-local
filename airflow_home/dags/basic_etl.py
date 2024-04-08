from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import sqlite3

import io

def extract():
    # Assuming your CSV is simple and does not require extensive cleaning
    
    csv_data = """id,date,amount
        1,2024-04-01,30.00
        2,2024-04-02,60.00
        3,2024-04-03,180.00"""
    
    csv_io = io.StringIO(csv_data)

    df = pd.read_csv(csv_io)
    return df

def transform(**kwargs):
    ti = kwargs['ti']
    df = ti.xcom_pull(task_ids='extract')
    # Example transformation: filter rows where 'amount' > 100
    df_filtered = df[df['amount'] > 100]
    ti.xcom_push(key='processed_data', value=df_filtered)

def load(**kwargs):
    ti = kwargs['ti']
    df_to_load = ti.xcom_pull(task_ids='transform', key='processed_data')
    conn = sqlite3.connect('airflow_home/database.db')
    df_to_load.to_sql('processed_data', conn, if_exists='replace', index=False)

with DAG('etl_dag', start_date=datetime(2022, 1, 1), schedule_interval='@daily', catchup=False) as dag:
    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract
    )

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform,
        provide_context=True
    )

    load_task = PythonOperator(
        task_id='load',
        python_callable=load,
        provide_context=True
    )

    extract_task >> transform_task >> load_task
