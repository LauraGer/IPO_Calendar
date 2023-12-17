#!/bin/bash

# Initialize Airflow database
echo "--------------------------------"
echo "DB INIT START"


# Check if the database exists
if python -c "from airflow import models; models.Connection"; then
    echo "Airflow database already exists. Performing migrations..."
    airflow db upgrade
else
    echo "Airflow database does not exist. Initializing..."
    airflow db init
    # Additional initialization steps if needed
fi

# Create Admin user
echo "--------------------------------"
echo "CREATE USER"

airflow users create -r Admin -u admin -e admin@example.com -f admin -l User -p 123

echo "DB INIT END"
echo "--------------------------------"

# Start Airflow webserver and scheduler
echo "--------------------------------"
echo "WEBSERVER START"

airflow webserver &

echo "--------------------------------"
echo "WEBSCHEDULER START"

airflow scheduler &

echo "SCHEDULER AND WEBSERVER END"
echo "--------------------------------"

# Wait for processes to complete their setup tasks
wait

# Start Airflow or whatever command you want to execute
# start scheduler
echo "--------------------------------"
echo "START SCHEDULER"
airflow scheduler 

wait 

echo "--------------------------------"
echo "START WORKER"
# start worker
airflow worker


echo "BASH SCRIPT END"
echo "--------------------------------"