FROM python:3.10-slim
LABEL authors="Michciak"

RUN pip install fastapi pydantic pandas sqlalchemy scikit-learn pymysql cryptography
RUN pip install "uvicorn[standard]"

WORKDIR /model

COPY api.py /model
COPY finalized_model.sav /model
COPY model.py /model

EXPOSE 5000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "5000"]
