# Use the official Apache Airflow image as the base image
FROM apache/airflow:latest

COPY ./requirements.txt /opt/airflow/requirements.txt
COPY ./airflow_setup.sh /opt/airflow/airflow_setup.sh