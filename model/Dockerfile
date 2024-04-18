# select image
FROM python:3.10-slim
LABEL authors="Michciak"

# install required packages
RUN pip install fastapi pydantic pandas sqlalchemy scikit-learn pymysql cryptography
RUN pip install "uvicorn[standard]"

# change working directory
WORKDIR /model

# copy files
COPY api.py /model
COPY finalized_model.sav /model
COPY model.py /model

# expose port 5000
EXPOSE 5000

# run api
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "5000"]
