from fastapi import FastAPI
from pydantic import BaseModel
import json
from model import *
import pandas as pd
import sqlalchemy

# init fastapi
app = FastAPI()

# create structure of data for prediction
class Car(BaseModel):
    brand: str
    model: str
    model_year: int
    milage: int
    fuel_type: str
    engine: str
    transmission: str
    accident: str
    clean_title: str

# init model class
model = Model()

# api post for prediction
@app.post("/predict")
async def run_prediction(car: Car, og_mode: bool):
    lower, upper = model.predict(car.dict(), og_mode)
    return json.dumps({'lower': lower, 'upper': upper})

# api get for model fitted on new data
@app.get("/train")
async def train_model():
    try:
        # connect to database to get new data
        database_name = "cars_db"
        user_name = "my_user"
        password = "my_password"
        engine = sqlalchemy.create_engine(f"mysql+pymysql://{user_name}:{password}@db/{database_name}")
        table_name = "new_table"
        query = f'SELECT * FROM {table_name}'
        df = pd.read_sql(query, engine)
    except:
        try:  # developer purpose only
            database_name = "cars_db"
            user_name = "root"
            password = "zxcvbnm"
            engine = sqlalchemy.create_engine(f"mysql+pymysql://{user_name}:{password}@db/{database_name}")
            table_name = "new_table"
            query = f'SELECT * FROM {table_name}'
            df = pd.read_sql(query, engine)
        except:
            raise Exception('Can\'t connect to database')
    # fit model with new data
    model.fit_model(df)