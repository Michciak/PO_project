# select image
FROM mysql:8.3.0

# copy files
COPY dataset.csv /var/lib/mysql-files/
COPY init.sql /docker-entrypoint-initdb.d/

