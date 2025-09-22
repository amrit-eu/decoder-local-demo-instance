FROM apache/airflow:3.0.6

WORKDIR /opt/airflow

COPY requirements.txt .

# instance customized dependencies
RUN pip install -r requirements.txt
