# Simple-IMS-for-Spare-Parts

This project primarily uses Django to simplify the process of inventory control.

To avoid installing MySQL directly on my computer, I used Docker to streamline the setup.

You can simply navigate to the MySQL directory and run the command below to deploy it. However, make sure Docker is
installed on your system beforehand.
cd to MySQL folder, run below in terminal
docker-compose build

after build, run below in terminal
docker-compose up

run below in terminal get mysql-database container id
docker container ls

run below in terminal to run mysql bash, 26f307921199 is the container id
docker exec -it 26f307921199 /bin/bash
pass is password, root is username
mysql -ppass -uroot
