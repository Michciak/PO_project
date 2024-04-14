FROM python:3.10-slim
LABEL authors="Michciak"

RUN pip install requests streamlit pandas sqlalchemy pymysql cryptography

WORKDIR /app

COPY app.py /app
COPY functions.py /app

EXPOSE 5000

CMD ["streamlit", "run", "app.py", "--server.port", "5000", "--server.enableXsrfProtection", "false"]