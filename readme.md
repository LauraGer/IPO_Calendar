#run docker-compose and create admin user

```bash
docker-compose up

docker exec -it airflow /bin/bash
flask fab create-admin
```