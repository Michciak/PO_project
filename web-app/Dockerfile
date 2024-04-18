# select image
FROM python:3.10-slim
LABEL authors="Michciak"

# install required packages
RUN pip install requests streamlit pandas sqlalchemy pymysql cryptography

# change working directory
WORKDIR /app

# copy files
COPY app.py /app
COPY functions.py /app

# expose port 5000
EXPOSE 5000

# run web-app
CMD ["streamlit", "run", "app.py", "--server.port", "5000", "--server.enableXsrfProtection", "false"]