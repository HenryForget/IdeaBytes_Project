'''This module contains models to be trained and forecasting methods'''
from statsmodels.tsa.statespace.sarimax import SARIMAX
from prophet import Prophet
import pandas as pd


class TsForecasting():
    '''Utility class for prediction models'''
    def __init__(self, dataset, graph_dir):
        '''Create the object'''
        self.data = dataset
        self.temp_model = None
        self.compr_model = None
        # TODO: Most likely we'll not divide the data to train and test and size will be removed
        # TODO: We'll need to add model for compressor efficiency prediction
        self.size = int(len(self.data)*0.9)
        self.train_set, self.test_set = self.data[0:self.size], self.data[self.size:len(self.data)]

    def prepare_prophet(self, data):
        '''Renames columns to use Prophet model'''
        data = data.reset_index()
        renamed = data.rename(columns={data.columns[0]: 'ds',
                                       data.columns[1]: 'y',
                                       data.columns[2]: 'dev_stat'})
        return renamed

    def run_prophet(self):
        '''Trains Prophet model for later predictions'''
        dataset = self.prepare_prophet(self.data)
        train_set = self.prepare_prophet(self.train_set)
        test_set = self.prepare_prophet(self.test_set)
        self.temp_model = Prophet(interval_width=0.95, seasonality_mode='multiplicative',
                         daily_seasonality = True)
        self.temp_model.add_regressor(train_set.columns[2])
        self.temp_model = self.temp_model.fit(train_set)

    # TODO: I will try again to train it and see the predictions. If it works, we'll have it instead of Prophet.
    def run_sarimax(self):
        '''Uses SARIMAX model for predictions
         - seasonal component - 1,0,1,12
         - use exogenous variables
         - p=1, d=0, q=2'''
        self.train_set.index = pd.DatetimeIndex(self.train_set.index).to_period('min')
        self.temp_model = SARIMAX(endog=self.train_set[self.train_set.columns[0]],  enforce_stationarity=False,
                        exog=self.train_set[self.train_set.columns[2]], order=(1,0,2),
                        seasonal_order=(1,0,5,12), missing='drop', freq='min')
        self.temp_model = self.temp_model.fit()

    # TODO: add methods that will use real-time data to predict the temp and compressor trends
