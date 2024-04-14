CREATE DATABASE IF NOT EXISTS cars_db;

USE cars_db;

CREATE TABLE IF NOT EXISTS used_cars (
    ID INT,
    Brand VARCHAR(255) NOT NULL,
    Model VARCHAR(255) NOT NULL,
    Model_year INT NOT NULL,
    Milage INT NOT NULL,
    Fuel_type VARCHAR(255) NOT NULL,
    Engine VARCHAR(255) NOT NULL,
    Transmission VARCHAR(255) NOT NULL,
    Accident VARCHAR(16) NOT NULL,
    Clean_title VARCHAR(16) NOT NULL,
    Price INT NOT NULL
);

LOAD DATA INFILE '/var/lib/mysql-files//dataset.csv'
INTO TABLE used_cars
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- \sql
-- \connect --mysql -u root
-- SOURCE C:\Users\Michc\Dropbox\Uczelnia\IAD2\Semestr1\ProcesyObliczeniowe\Projekt\database\db.sql
-- SELECT * FROM used_cars;