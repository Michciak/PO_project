import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
import pandas as pd

class Model():
    def __init__(self):
        self.model = pickle.load(open('finalized_model.sav', 'rb'))
        self.model = self.model.best_estimator_
        self.new_model = None

    def fit_model(self, new_data: pd.DataFrame):
        if new_data is not None:
            try:
                self.new_model = pickle.load(open('finalized_model.sav', 'rb'))
                self.new_model = self.new_model.best_estimator_
                new_data.columns = new_data.columns.str.lower()
                Target = 'price'
                Predictors = ['brand', 'model', 'model_year', 'milage', 'fuel_type', 'engine', 'transmission', 'accident', 'clean_title']
                self.new_model.fit(new_data[Predictors], new_data[Target])
            except Exception as e:
                raise Exception(e)

    def predict(self, observation: dict, og_mode: bool):
        lower_quantile0, upper_quantile0, lower_quantile1, upper_quantile1, lower_quantile2, upper_quantile2 = [-3309.072, -2002.685, -4450.242, -654.887, -8357.948, 5179.976]
        if observation is None:
            return 0, 0
        pred_df = pd.DataFrame(observation, index=[0])
        if og_mode:
            p = self.model.predict(pred_df.reset_index(drop=True))
        else:
            if self.new_model is not None:
                p = self.new_model.predict(pred_df.reset_index(drop=True))
            else:
                return 0, 0
        if p < 25_000:
            if p < 10_000:
                lower = min(p, p + lower_quantile0)
                upper = max(p, p + upper_quantile0)
            else:
                lower = min(p, p + lower_quantile1)
                upper = max(p, p + upper_quantile1)
        else:
            lower = min(p, p + lower_quantile2)
            upper = max(p, p + 2 * upper_quantile2)
        return lower[0], upper[0]



