#!/bin/bash

#Install dependencies
echo "--------------------------------"
echo "INSTALL DEPENDENCIES"
pip install --upgrade pip

echo "--------------------------------"
echo "INSTALL REQUIREMENTS.TXT"
pip install --no-cache-dir -r ./dags/requirements.txt

# Initialize Airflow database
echo "--------------------------------"
echo "DB INIT START"

# Check if the database exists
if python -c "from airflow import models; models.Connection"; then
    echo "Airflow database already exists. Performing migrations..."
    airflow db migrate
else
    echo "Airflow database does not exist. Initializing..."
    airflow db init
fi

echo "--------------------------------"
echo "CREATE USER"

airflow users create -r Admin -u admin -e admin@example.com -f admin -l User -p 123 &

wait

# Start Airflow webserver and scheduler
echo "--------------------------------"
echo "WEBSERVER START"

airflow webserver &

echo "--------------------------------"
echo "WEBSCHEDULER START"

airflow scheduler &

wait

# start worker
echo "--------------------------------"
echo "START WORKER"

airflow worker


echo "BASH SCRIPT END"
echo "--------------------------------"