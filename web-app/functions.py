import streamlit as st
import sqlalchemy
import pandas as pd
import requests
import json

def pirce_car(brand, model, year, milage, fuel, engine, trans, accident, title, use_new_data):
    with st.spinner("Getting results..."):
        # check if all values are selected
        if (brand or model or year or fuel or engine or trans) == '-':
            return 'Please specify all parameters'
        else:
            # create dictionary based on selected values
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
                # run prediction with model microservice
                response = requests.post("http://model:5000/predict?og_mode=" + str(not use_new_data), json=car)
                response = response.json()
            except:
                # return error message
                return "Connection Error"
            response = json.loads(response)
            # get boundaries of predicted interval
            lower = round(response['lower'], 2)
            upper = round(response['upper'], 2)
            # return message with predicted inteval
            return f'Estimated value: \${lower}-{upper}'

def get_df_from_db():
    with st.spinner("Connecting to database..."):
        try:
            # database credentials nad connection engine
            database_name = "cars_db"
            user_name = "my_user"
            password = "my_password"
            engine = sqlalchemy.create_engine(f"mysql+pymysql://{user_name}:{password}@db/{database_name}")
            table_name = "used_cars"
            # database query
            query = f'SELECT * FROM {table_name}'
            # read database to dataframe
            df = pd.read_sql(query, engine)
            # return dataframe
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

# push new values to new table
def setup_new_db(df: pd.DataFrame):
    with st.spinner("Loading data to databse..."):
        try:
            # database credentials nad connection engine
            database_name = "cars_db"
            user_name = "my_user"
            password = "my_password"
            engine = sqlalchemy.create_engine(f"mysql+pymysql://{user_name}:{password}@db/{database_name}")
            # push dataframe to database
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

# run request for model to fit on new data
def fit_new():
    requests.get("http://model:5000/train")