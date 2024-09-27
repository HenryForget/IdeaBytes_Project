'''This module contains model to be trained and forecasting'''
import json
from statsmodels.tsa.statespace.sarimax import SARIMAX
import pandas as pd



class TsForecasting():
    '''Utility class for prediction models'''
    def __init__(self, dataset):
        '''Create the object'''
        self.data = dataset
        self.temp_model = None
        self.compr_model = None
        # TODO: We'll need to add model for compressor efficiency prediction

    def run_sarimax(self):
        '''Uses SARIMAX model for predictions
         - seasonal component - 1,0,1,12
         - use exogenous variables
         - p=1, d=0, q=2'''
        self.temp_model = SARIMAX(endog=self.data[self.data.columns[0]],  enforce_stationarity=False,
                        order=(1,1,1), mle_regression = False,
                        seasonal_order=(1,0,0,12), missing='drop', freq='min',  time_varying_regression=True)
        model_fit = self.temp_model.fit()
        return model_fit

    def predict(self,data, model_fit, period):
        '''Takes current model and predicts future data based on real-time input
        - data is last 24 hours real-time db data'''
        forecast_set = model_fit.apply(data[data.columns[0]])
        forecasted = forecast_set.forecast(period).to_json()
        forecasted = json.dumps(forecasted)
        return forecasted

    # TODO: add method that will use real-time data to predict compressor trend
