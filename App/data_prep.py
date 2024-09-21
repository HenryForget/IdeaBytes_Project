'''This module handles temperature data. Methods are used to prepare and validate data for later training'''
import configparser
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

class TempAnalysis():
    ''' Temperature analysis '''
    def __init__(self, datapath, configpath) -> None:
        ''' Initialize object '''
        config = configparser.ConfigParser()
        config.read(configpath)
        self.date_format = config.get('MAIN','DATE_FORMAT')
        self.index = config.get('MAIN','INDEX')
        # TODO: we are going to use 3 columns: 1 for datetime (index), 2 for temp, 3 for compressor status (ON/OFF) 
        # TODO: this will indicate number or name of the column that has compressor status. We'll need to query only data we use.
        self.status_col = int(config.get('MAIN','STATUS_COL'))
        # TODO: read data from JSON, not from csv
        # TODO: add compressor data preparation method and class variable to store it
        # TODO: add outlier detection and cleaning - based on temp thresholds sent from alerting?
        self.data = pd.read_csv(datapath, index_col=[self.index],
                                parse_dates=[self.index], date_format=self.date_format)
        self.data.index = pd.to_datetime(self.data.index, format='%d-%m-%Y %H:%M')
        print(f"Total instances before data preparation: {len(self.data)}")
        print(f"Features: {self.data.columns}")

    def prepare_data(self):
        '''Validates data (removes duplicates, formats, sorts, deals with missing data)'''
        # remove duplicates
        if not self.data.index.is_unique:
            self.data = self.data.reset_index().drop_duplicates(subset=self.data.index.name)
            self.data = self.data.set_index(self.index)
        # get the number of the column in the file
        col = self.data.shape[1]
        le = LabelEncoder()
        # TODO: we are going to use 3 columns: 1 for datetime (index), 2 for temp, 3 for compressor status (ON/OFF) 
        # REDO this logic to only applicable to one column. Don't loop.
        for x in range(col):
            if self.data[self.data.columns[x]].dtypes == 'object':
                # convert categorical to numerical for non numeric data
                label = le.fit_transform(self.data[self.data.columns[x]])
                self.data.drop(self.data.columns[x], axis=1)
                self.data[self.data.columns[x]] = label
        #  sort dataset by the first column
        self.data = self.data.sort_index()
        print(f"Total instances after data preparation: {len(self.data)}")

