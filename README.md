# Simple-IMS-for-Spare-Parts

This project primarily uses Django to simplify the process of inventory control.

To avoid installing MySQL directly on my computer, I used Docker to streamline the setup.

You can simply navigate to the MySQL directory and run the command below to deploy it. However, make sure Docker is
installed on your system beforehand.
cd to MySQL folder, run below in terminal
docker-compose build

After build, run below in terminal

docker-compose up

Aun below in terminal get mysql-database container id

docker container ls

Aun below in terminal to run mysql bash, 26f307921199 is the container id

docker exec -it 26f307921199 /bin/bash

Pass is password, Root is username

mysql -ppass -uroot
