from fastapi import FastAPI
from pydantic import BaseModel
import json
from model import *
import pandas as pd
import sqlalchemy

app = FastAPI()

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

model = Model()

@app.post("/predict")
async def run_prediction(car: Car, og_mode: bool):
    lower, upper = model.predict(car.dict(), og_mode)
    return json.dumps({'lower': lower, 'upper': upper})

@app.get("/train")
async def train_model():
    try:
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
    model.fit_model(df)