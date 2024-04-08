lsof -ti:8090 | xargs kill -9

# export AIRFLOW_HOME=/Users/james/Desktop/projects/airflow-local/airflow_home

AIRFLOW_VERSION=2.8.4

# Extract the version of Python you have installed. If you're currently using a Python version that is not supported by Airflow, you may want to set this manually.
# See above for supported versions.
# PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
PYTHON_VERSION=3.8

CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# For example this would install 2.8.4 with python 3.8: https://raw.githubusercontent.com/apache/airflow/constraints-2.8.4/constraints-3.8.txt

python3 -m venv venv
source venv/bin/activate

python3 -m pip install --upgrade pip

python3 -m pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# DAG libraries dependencies
python3 -m pip install pandas==2.2.1
# Create an admin user (skip if it already exists)
airflow db init

airflow users create \
    --username admin \
    --firstname FIRST_NAME \
    --lastname LAST_NAME \
    --role Admin \
    --email admin@example.com \
    --password admin || true

# Start Airflow webserver
airflow webserver --port 8090

## May need to be in a separate terminal
# airflow webserver --port 8091