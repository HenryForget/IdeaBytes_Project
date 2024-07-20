'''This module contains methods for differnet time series forecasting'''
# from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA, ARIMAResults
from pandas.plotting import autocorrelation_plot
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
         - p=, d=, q='''
        # train-test sets: 85/15
        size = int(len(self.data)*0.85)
        train_set, test_set = self.data[0:size], self.data[size:len(self.data)]
        start = time.time()
        # don't interpolate missing values in data preparation, take dataset as it is and use missing 
        # parameter to drop from the training
        model = ARIMA(endog=train_set[train_set.columns[0]], order=(1,0,2), exog=train_set[train_set.columns[1]])
        model_fit = model.fit()
        end = time.time()
        forecast_set = model_fit.predict(start=len(train_set), end=len(self.data)-1, exog=test_set[test_set.columns[1]], missing='drop' )
        print(f'ARIMA training time for {len(test_set)} test instances: \
              {end-start} seconds.')
        self.plot_forecast(test_set, forecast_set, 'ARIMA')
        print(model_fit.summary())
        forecast_set.to_csv('./forecast.csv')
        print(f'Root Mean Squared Error: {self.calculate_rmse(test_set[test_set.columns[0]], forecast_set)}')

    def run_prophet(data):
        '''Uses Prophet model for predictions'''

    def run_sarimax(data):
        '''Uses SARIMAX model for predictions'''
