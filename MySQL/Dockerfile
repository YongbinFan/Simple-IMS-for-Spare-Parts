FROM mysql:8

ENV MYSQL_ROOT_PASSWORD pass
COPY ./data.sql /docker-entrypoint-initdb.d/data.sql


#WORKDIR /MySQL
#ADD . /MySQL
#
#
#
## Set environment variables for the new user
#ENV MYSQL_USER=external_user
#ENV MYSQL_PASSWORD=password
#ENV MYSQL_DATABASE=SparePartsDB
#
#
## Run the following commands to create the new user and grant them the necessary permissions
#RUN mysql -u root -p -e "CREATE USER '$MYSQL_USER'@'%' IDENTIFIED BY '$MYSQL_PASSWORD';"
#RUN mysql -u root -p -e "GRANT ALL PRIVILEGES ON $MYSQL_DATABASE.* TO '$MYSQL_USER'@'%';"
#RUN mysql -u root -p -e "FLUSH PRIVILEGES;"
#
#
## Expose port 3306 to allow connections to the database
#EXPOSE 3306
#
## Start the MySQL server when the container is run
#CMD ["mysqld"]


