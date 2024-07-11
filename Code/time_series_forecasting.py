'''This module contains methods for differnet time series forecasting'''
# from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
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
        print(test)
        print(predict)
        # fig, ax = plt.subplots()
        # ax.set_label('Test Set')
        # ax.plot(test.index,test[test.columns[0]], color='grey')
        # ax1 = ax.twinx()
        # ax1.set_label("Prediction")
        # ax1.plot(predict.index,predict[predict.columns[0]], color='green')
        # fig.tight_layout()
        # fig.set_size_inches(100, 150)
        # fig.savefig(f'{"/".join([self.graph_dir,name])}.png')

    def calculate_rmse(self, test, predict):
        '''Returns root squared mean error value'''
        return sqrt(mean_squared_error(test, predict))

    def run_arima(self):
        '''Uses ARIMA model for predictions
         - no exogenous regressors used
         - no seasonal component'''
        # train-test sets: 90/10
        size = int(len(self.data)*0.9)
        train_set, test_set = self.data[0:size], self.data[size:len(self.data)]
        forecast_set = list()
        train_rolling = [x for x in train_set[train_set.columns[0]]]
        start = time.time()
        for i in range(len(test_set)):
            model = ARIMA(endog=train_rolling, order=(1,1,1))
            model_fit = model.fit()
            # rolling forecast method takes forever, use predict instead?
            forecast = model_fit.forecast()
            forecast_set.append(forecast[0])
            train_rolling.append(test_set[test_set.columns[0]].iloc[i])
            print(f'Iteration {i}: Predicted {forecast[0]}, \
                  Expected {test_set[test_set.columns[0]].iloc[i]}')
        end = time.time()
        print(f'Rolling forecast execution time for len{test_set} test instances: \
              {start-end} seconds.')
        # self.plot_forecast(test_set, forecast_set, 'ARIMA')
        print(model_fit.summary())
        print(self.calculate_rmse(test_set, forecast_set))

    def run_prophet(data):
        '''Uses Prophet model for predictions'''

    def run_sarimax(data):
        '''Uses SARIMAX model for predictions'''
