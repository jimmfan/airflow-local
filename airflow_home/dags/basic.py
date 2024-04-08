from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# Define the Python function
def hello_airflow():
    print("Hello, Airflow!")

# Define default arguments for your DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 4, 6),  # Use your desired start date
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Instantiate the DAG
dag = DAG(
    'hello_world',
    default_args=default_args,
    description='A simple Hello World DAG',
    schedule_interval=timedelta(days=1),  # This DAG will run daily
)

# Define the task using PythonOperator
hello_task = PythonOperator(
    task_id='print_hello',
    python_callable=hello_airflow,
    dag=dag,
)

# You can add more tasks and set up dependencies here if needed

# For a single task, no need to set dependencies
