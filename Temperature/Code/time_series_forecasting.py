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

    def get_acf(self):
        '''Calculate ACF'''
        result = acf(self.data[self.data.columns[0]])
        return result

    def plot_acf_func(self,  name):
        '''Plots autocorrelation function'''
        # statsmodels acf plot
        plot_acf(self.data[self.data.columns[0]])
        # pandas acf plot
        # autocorrelation_plot(self.data)
        plt.savefig(f'{"/".join([self.graph_dir,name])}.png')

    def get_pacf(self):
        '''Calculate PACF'''
        result = pacf(self.data[self.data.columns[0]])
        return result

    def plot_pacf_func(self, name):
        '''Plots autocorrelation function'''
        plot_pacf(self.data[self.data.columns[0]], method = 'ols')
        plt.savefig(f'{"/".join([self.graph_dir,name])}.png')

    def plot_forecast(self, test, predict, name):
        '''Plots results of temperature prediction'''
        plt.figure(figsize = (50, 35))
        plt.plot(test.index,test[test.columns[0]], color='grey', label= 'Test Set')
        plt.plot(test.index,predict, color='blue', label = 'Prediction')
        plt.savefig(f'{"/".join([self.graph_dir,name])}.png')

    def calculate_rmse(self, test, predict):
        '''Returns root squared mean error value'''
        return sqrt(mean_squared_error(test, predict))

    def run_arima(self):
        '''Uses ARIMA model for predictions
         - no seasonal component
         - no exogenous variables
         - p=1, d=0, q=0'''
        start = time.time()
        # if not interpolate missing values in data preparation, take dataset as it is
        # and use missing parameter to drop from the training
        model = ARIMA(endog=self.train_set[self.train_set.columns[0]], order=(1,0,6))
        model_fit = model.fit()
        end = time.time()
        # if missing values use missing='drop'
        forecast_set = model_fit.predict(start=len(self.train_set), end=len(self.data)-1 )
        print(f'ARIMA training time for {len(self.test_set)} test instances: \
              {end-start} seconds.')
        self.plot_forecast(self.test_set, forecast_set, 'ARIMA')
        print(model_fit.summary())
        print(f'Root Mean Squared Error: \
              {self.calculate_rmse(self.test_set[self.test_set.columns[0]], forecast_set)}')

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

    def run_sarimax(self):
        '''Uses SARIMAX model for predictions
         - seasonal component - 1,0,1,12
         - use exogenous variables
         - p=1, d=0, q=2'''
        start = time.time()
        self.train_set.index = pd.DatetimeIndex(self.train_set.index).to_period('min')
        model = SARIMAX(endog=self.train_set[self.train_set.columns[0]],
                        exog=self.train_set[self.train_set.columns[1]], order=(1,0,4),
                        seasonal_order=(1,0,5,6), missing='drop', freq='min')
        model_fit = model.fit()
        end = time.time()

        forecast_set = model_fit.predict(start=len(self.train_set),
                                         end=len(self.data)-1,
                                         exog=self.test_set[self.test_set.columns[1]])
        print(f'SARIMAX training time for {len(self.test_set)} test instances: \
              {end-start} seconds.')
        self.plot_forecast(self.test_set, forecast_set, 'SARIMAX')
        print(model_fit.summary())
        forecast_set.to_csv('./forecast.csv')
        print(f'Root Mean Squared Error: {self.calculate_rmse(self.test_set[self.test_set.columns[0]], forecast_set)}')

    def run_neural_prophet(self):
        '''Uses Neural Prophet model for predictions'''
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


