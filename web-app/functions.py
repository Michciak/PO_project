import streamlit as st
import sqlalchemy
import pandas as pd
import requests
import json

def pirce_car(brand, model, year, milage, fuel, engine, trans, accident, title, use_new_data):
    with st.spinner("Getting results..."):
        if (brand or model or year or fuel or engine or trans) == '-':
            return 'Please specify all parameters'
        else:
            car = {
                "brand": str(brand),
                "model": str(model),
                "model_year": int(year),
                "milage": int(milage),
                "fuel_type": str(fuel),
                "engine": str(engine),
                "transmission": str(trans),
                "accident": 'None' if accident else 'Reported',
                "clean_title": 'Unknown' if title else 'Yes'
            }
            try:
                response = requests.post("http://model:5000/predict?og_mode=" + str(not use_new_data), json=car)
                response = response.json()
            except:
                return "Connection Error"
            response = json.loads(response)
            lower = round(response['lower'],2)
            upper = round(response['upper'],2)
            return f'Estimated value: \${lower}-{upper}'

def get_df_from_db():
    with st.spinner("Connecting to database..."):
        try:
            database_name = "cars_db"
            user_name = "my_user"
            password = "my_password"
            engine = sqlalchemy.create_engine(f"mysql+pymysql://{user_name}:{password}@db/{database_name}")
            table_name = "used_cars"
            query = f'SELECT * FROM {table_name}'
            df = pd.read_sql(query, engine)
            return df
        except:
            try: # developer purpose only
                database_name = "cars_db"
                user_name = "root"
                password = "zxcvbnm"
                engine = sqlalchemy.create_engine(f"mysql+pymysql://{user_name}:{password}@db/{database_name}")
                table_name = "used_cars"
                query = f'SELECT * FROM {table_name}'
                df = pd.read_sql(query, engine)
                return df
            except:
                raise Exception('Can\'t connect to database')

def setup_new_db(df: pd.DataFrame):
    with st.spinner("Loading data to databse..."):
        try:
            database_name = "cars_db"
            user_name = "my_user"
            password = "my_password"
            engine = sqlalchemy.create_engine(f"mysql+pymysql://{user_name}:{password}@db/{database_name}")
            df.to_sql('new_table', engine, if_exists='replace', index=False)
        except:
            try: # developer purpose only
                database_name = "cars_db"
                user_name = "root"
                password = "zxcvbnm"
                engine = sqlalchemy.create_engine(f"mysql+pymysql://{user_name}:{password}@db/{database_name}")
                df.to_sql('new_table', engine, if_exists='replace', index=False)
            except:
                raise Exception('Can\'t connect to database')


def fit_new():
    requests.get("http://model:5000/train")