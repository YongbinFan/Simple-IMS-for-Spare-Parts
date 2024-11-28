First time install mysql in docker

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
