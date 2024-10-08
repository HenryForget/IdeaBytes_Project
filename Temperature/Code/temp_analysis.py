'''This module handles temperature data. Methods are used to prepare, validate
 and analyse temperature data'''
import configparser
import pandas as pd
from statsmodels.tsa.stattools import adfuller, kpss
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.preprocessing import LabelEncoder

class TempAnalysis():
    ''' Temperature analysis '''
    def __init__(self, datapath, configpath) -> None:
        ''' Initialize object '''
        config = configparser.ConfigParser()
        config.read(configpath)
        self.sign_level = float(config.get('MAIN','SIGN_LEVEL'))
        self.graphs_dir = config.get('MAIN','PLOT_DEST')
        self.date_format = config.get('MAIN','DATE_FORMAT')
        self.data_freq = config.get('MAIN','DATA_FREQ')
        self.index = config.get('MAIN','INDEX')
        self.statuses = int(config.get('MAIN','STATUS_COL'))
        self.data = pd.read_csv(datapath, index_col=[self.index],
                                parse_dates=[self.index], date_format=self.date_format)
        self.ext_data = None
        print(f"Total instances: {len(self.data)}")
        print(f"Features: {self.data.columns}")

    def prepare_data(self):
        '''Validates data (removes duplicates, formats, sorts, deals with missing data)'''
        # drop duplicated index and reset index
        if not self.data.index.is_unique:          
            #self.data = self.data.reset_index().drop_duplicates(subset=self.data.index.name, keep='first')
            self.data = self.data.reset_index().drop_duplicates(subset='Date/Time', keep='first').set_index('Date/Time')
        # get the number of the column in the file
        col = self.data.shape[1]
        le = LabelEncoder()
        for x in range(col):
            if self.data[self.data.columns[x]].dtypes == 'object':
                # convert categorical to numerical for non numeric data
                label = le.fit_transform(self.data[self.data.columns[x]])
                self.data.drop(self.data.columns[x], axis=1)
                self.data[self.data.columns[x]] = label
            else:
            # convert data values to float64 datatype
                self.data[self.data.columns[x]] = self.data[self.data.columns[x]].astype(float)
            #  sort dataset by the first column
                self.data = self.data.sort_index()

    def calculate_kpss(self):
        ''' Test if the series is stationary using KPSS method'''
        values = self.data[self.data.columns[0]]
        print("KPSS test:")
        kpss_test = kpss(values, regression='ct')
        kpss_result = pd.Series(kpss_test[0:3], index=['Test Statistic','p-value','Lags Used'])
        for key,value in kpss_test[3].items():
            kpss_result[f'Critical Value {key}'] = value
        print (kpss_result)
            #    if test is greater than critical value, then the dataset is not stationary
        if (kpss_result['p-value'] < self.sign_level) or \
            (kpss_result['Test Statistic'] < kpss_result['Critical Value (5%)']):
            return True
        return False

    def calculate_adf(self):
        ''' Test if the series is stationary using ADF method '''
        values = self.data[self.data.columns[0]]
        print("ADF test:")
        # get the results of ADF on temperature set
        df_test = adfuller(values, autolag='AIC')
        df_result = pd.Series(df_test[0:4], index=['Test Statistic','p-value',
                                                   '#Lags Used','Number of Observations Used'])
        for key,value in df_test[4].items():
            df_result[f'Critical Value {key}'] = value
        print (df_result)
        #    if test is greater than critical value, then the dataset is not stationary
        if (df_result['p-value'] < self.sign_level) or \
            (df_result['Test Statistic'] < df_result['Critical Value (5%)']):
            return True
        return False

    def get_stats(self):
        '''Returns descriptive statistics for timeseries values'''
        return self.data.describe(include='all')

    def plot_general(self, name, data = None):
        '''Plots the data for the period'''
        plt.figure(figsize=(60, 46))
        if not data:
            data = self.data
        x = data.index
        y = data[data.columns[0]]
        plt.plot(x,y)
        plt.xticks(rotation=35)
        plt.savefig(f'{"/".join([self.graphs_dir,name])}.png')

    def plot_comp_status(self, name):
        '''Plots additional axis for compressor/evaporator/defroster status'''
        colors = ['blue','red','green','black','yellow']
        fig, ax1 = plt.subplots()
        ax1.plot(self.data.index,self.data[self.data.columns[0]], color=colors[0])
        for i in range(0,self.statuses):
            ax2 = ax1.twinx()
            ax2.set_ylabel(self.data.columns[i+1], color=colors[i+1])
            ax2.plot(self.data.index,self.data[self.data.columns[i+1]], color=colors[i+1])
        fig.tight_layout()
        fig.set_size_inches(200, 250)
        fig.savefig(f'{"/".join([self.graphs_dir,name])}.png')


    def plot_util(self,  x_axis, y_axis, ax):
        ''' Utility function for plotting everyday data'''
        colors = ['blue','red','green','black','yellow','brown','black']
        ax.set_title(x_axis[0].strftime('%Y-%m-%d'))
        ax.set_xlim(x_axis[0], x_axis[-1])
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.plot(x_axis, y_axis)
        for i in range(0,self.statuses):
            ax2 = ax.twinx()
            ax2.set_ylabel(self.data.columns[i+1], color=colors[i+1])
            ax2.plot(self.data.index,self.data[self.data.columns[i+1]], color=colors[i+1])

    def plot_daily(self, name):
        '''Plots the data with daily breakdown'''
        days_data = [group for n, group in self.data.groupby(pd.Grouper(freq='D'))]
        plot_cols = 6
        plot_rows = (int)(len(days_data)/plot_cols)
        fig, ax = plt.subplots(plot_rows+1,plot_cols, sharey=True)
        # plot all the days dataframes
        for n in range(plot_rows+1):
            for k in range (plot_cols):
                if (n != plot_rows) or ((n * plot_cols + k) < len(days_data)):
                    x_axis = days_data[n*plot_cols+ k].index
                    y_axis = days_data[n*plot_cols + k][days_data[n*plot_cols + k].columns[0]]
                    if x_axis.size > 0:
                        self.plot_util(x_axis, y_axis, ax[n][k])
                else:
                    break
        fig.set_size_inches(200, 250)
        fig.savefig(f'{"/".join([self.graphs_dir,name])}.png')

    def analyze_ext_data(self, datapath, ext_index):
        '''Plots and analyzes external dataset (i.e. city temp)'''
        #  upload data - use Australia
        # self.ext_data = pd.read_csv(datapath)

    def calculate_corr(self):
        '''Calcualtes a correlation between equipment data and external data'''

    def get_dataset(self):
        '''Returns the prepared dataset'''
        self.prepare_data()
        return self.data
