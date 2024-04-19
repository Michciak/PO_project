# Used cars pricing

## Table of Contents
1. Introduction
2. Technologies
3. Microserivcies description
4. Setup guide
5. Visual presentation

___

## Introduction

This project is created for Computing Processes Study. 

The result of the work on this project is a system of microservices communicating with each other, consisting of a machine learning module, database and visual interface in the form of a web-app.

Among the provided functionalities are:

- browsing used cars database,
- pricing car based on provided data,
- updating model with new data.

___

## Technologies
This project was created with:
- <img src="./images/icons/docker.png" width="30" height="30" style="vertical-align: middle;">&nbsp;**Docker**: 25.0.3
- <img src="./images/icons/mysql.png" width="30" height="30" style="vertical-align: middle;">&nbsp;**MySQL**: 8.3.0
- <img src="./images/icons/python.png" width="30" height="30" style="vertical-align: middle;">&nbsp;**Python**: 3.10
- <img src="./images/icons/streamlit.png" width="30" height="30" style="vertical-align: middle;">&nbsp;**Streamlit**: 1.33.0
- <img src="./images/icons/fastapi.png" width="30" height="30" style="vertical-align: middle;">&nbsp;**FastAPI**: 0.110.0

___

## Microserivcies description

### Database server

This service is responsible for providing database functionality. Its architecture is based on the *MySQL* server.

### Web-app UI

This service is responsible for the visual interface of the application. It allows the user to use the API and the functionalities described above. It is based on the *Streamlit* framework.

### API 

This service is responsible for handling the machine learning model and provides functionalities like making predictions fitting the model using new data provided by user, for this purpose it also has the ability to communicate with the database. Its architecture is based on *FastAPI*.
___

## Setup guide
In few steps I will describe process how run software by yourself.

### Prerequisites
To install this software and be able to run it you need to previously install Docker on your machine. If you don't have Docker you can download it from official distribution: [docker.com](<https://www.docker.com/products/docker-desktop/>).

### Installing application
After you clone repository you need to run system terminal and go to directory 'PO_project' which contains all files.

Next you need to set up application by building container, to achieve this run command 

```
docker compose up -d
```

### Running application
Finally, you should be able to use application by going to <http://localhost:5001/>

___

## Visual presentation

![tab1](images/image1.png)

![tab2](images/image2.png)

![img.png](images/image3.png)
