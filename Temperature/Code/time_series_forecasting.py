'''This module contains methods for differnet time series forecasting'''
# from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from prophet import Prophet
from prophet.plot import (plot_plotly,
plot_components_plotly)
from neuralprophet import NeuralProphet
from pandas.plotting import autocorrelation_plot
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from math import sqrt
import time

class TsForecasting():
    '''Utility class for prediction models'''
    def __init__(self, dataset, graph_dir):
        '''Create the object'''
        self.data = dataset
        self.graph_dir = graph_dir
        # train-test sets:70/30
        self.size = int(len(self.data)*0.70)
        self.train_set, self.test_set = self.data[0:self.size], self.data[self.size:len(self.data)]

    def calculate_rmse(self, test, predict):
        '''Returns root squared mean error value'''
        return sqrt(mean_squared_error(test, predict))

    def prepare_prophet(self, data):
        '''Renames columns to use Prophet model'''
        data = data.reset_index()
        renamed = data.rename(columns={data.columns[0]: 'ds',
                                       data.columns[1]: 'y', data.columns[2]: 'dev_stat'})
        return renamed

    def run_prophet(self):
        '''Uses Prophet model for predictions'''
        dataset = self.prepare_prophet(self.data)
        train_set = self.prepare_prophet(self.train_set)
        test_set = self.prepare_prophet(self.test_set)
        start= time.time()
        model = Prophet(interval_width=0.90, seasonality_mode='multiplicative',
                         yearly_seasonality = 4)
        model.add_regressor(train_set.columns[2])
        model.fit(train_set)
        end = time.time()
        print(f'PROPHET training time for {len(test_set)} test instances: \
              {end-start} seconds.')
        future_set = model.make_future_dataframe(periods=len(test_set), freq='1min')
        future_set[test_set.columns[2]] = dataset[dataset.columns[1]]
        forecast_set = model.predict(future_set)
        forecast_prophet = forecast_set.iloc[self.size:]
        fig = plot_plotly(model, forecast_set)
        fig_comp = plot_components_plotly(model, forecast_set,figsize=(1200, 200))
        fig.write_image(f'{"/".join([self.graph_dir,"Prophet"])}.png')
        fig_comp.write_image(f'{"/".join([self.graph_dir,"Prophet_components"])}.png')
        plt.figure(figsize = (50, 35))
        plt.plot(test_set['ds'], forecast_prophet['yhat'], color='blue', label='Forecast Set')
        plt.plot(test_set['ds'], test_set['y'], color='black', label = 'Test Set')
        plt.savefig(f'{"/".join([self.graph_dir,"Prophet_plot"])}.png')

    def run_neural_prophet(self):
        '''Uses Neural Prophet model for predictions'''
        # Need to add the model to class variables to call rom another method
        data = self.prepare_prophet(self.data)
        # train_set = self.prepare_prophet(self.train_set)
        test_set = self.prepare_prophet(self.test_set)
        start= time.time()
        model = NeuralProphet(yearly_seasonality=False, drop_missing=True,
                              weekly_seasonality=True, daily_seasonality=True)
        model.add_future_regressor('dev_stat')
        # model.fit(train_set)
        model.fit(data)
        end = time.time()
        print(f'PROPHET training time for {len(test_set)} test instances: \
              {end-start} seconds.')
        future_set = {'ds':test_set['ds'], 'y': None, 'dev_stat':test_set['dev_stat']}
        future_set = pd.DataFrame(future_set)
        # forecast_set = model.predict(future_set)
        forecast_set = model.predict(data)
        forecast_test = model.predict(future_set)
        fig = model.plot(forecast_set)
        fig.write_image(f'{"/".join([self.graph_dir,"NeuralProphet"])}.png')
        plt.figure(figsize = (50, 35))
        plt.plot(test_set['ds'], forecast_test['yhat1'], color='blue', label='Forecast Set')
        plt.plot(test_set['ds'], test_set['y'], color='black', label = 'Test Set')
        plt.savefig(f'{"/".join([self.graph_dir,"NeuralProphet_plot"])}.png')

def predict_temp(self, period):
    '''Creates a prediction for the period specified'''
    # takes the model (will use neural prophet)
    # creates the future dataframe for the period specified in a call
    # How to save the model so we can use it here? see pickle?
    # returns the predicted values? how fast the temp goes down? how fast should we expect it to go down?
 