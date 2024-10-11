'''This module handles temperature data. Methods are used to prepare and validate data for later training'''
import configparser
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
import numpy as np
from scipy import stats

class DataPreparation():
    ''' Temperature analysis '''
    def __init__(self, datapath, configpath) -> None:
        ''' Initialize object '''
        config = configparser.ConfigParser()
        config.read(configpath)
        self.date_format = config.get('MAIN','DATE_FORMAT')
        self.index = config.get('MAIN','INDEX')
        self.data_freq = config.get('MAIN','DATA_FREQ')
        self.status_col = config.get('MAIN','STATUS_COL')
        self.data = pd.read_csv(datapath, index_col=[self.index],
                                parse_dates=[self.index], date_format=self.date_format)
        self.data.index = pd.to_datetime(self.data.index, format=self.date_format)
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
        for x in range(col):
            if self.data[self.data.columns[x]].dtypes == 'object':
                # convert categorical to numerical for non numeric data
                label = le.fit_transform(self.data[self.data.columns[x]])
                self.data.drop(self.data.columns[x], axis=1)
                self.data[self.data.columns[x]] = label
        #  sort dataset by the first column
        self.data = self.data.sort_index()
        # fill missing values:
        # resample dataset - will fill the missing values as null
        self.data = self.data.asfreq(freq = 'h')
        # pchip for interpolation
        self.data[self.data.columns[0]] = self.data[self.data.columns[0]].interpolate('pchip')
        self.data[self.data.columns[1]] = self.data[self.data.columns[1]].ffill()
        print(f"Total instances after data preparation: {len(self.data)}")
    
    def get_peaks_valleys_status(self):
        '''
            Uses compressor status to construct peak/valley pairs.
            :return peaks: array of peak indices
            :return valleys: array of valley indices
        '''
        # Create empty arrays
        peaks = np.array([], dtype=np.int8)
        valleys = np.array([], dtype=np.int8)
        comp_stat = self.data[self.data.columns[1]].to_numpy()
        # Loop through each compt_stat (cs) value
        i = 0
        while i < len(comp_stat) - 2:
            # If the first index has cs = 1 then it's a peak
            if i == 0:
                if comp_stat[i] == 1:
                    peaks = np.append(peaks, i)
            # If the last value has cs = 1 then it's a valley
            # [Note] End of array needs fixing, off by one error, won't pick up last peak/valley pair
            elif i == len(comp_stat) - 1:
                if comp_stat[i + 1] == 1:
                    valleys = np.append(valleys, i + 1)
                elif comp_stat[i] == 1:
                    valleys = np.append(valleys, i)
            # Check cs @ i+1 vs cs @ i; if they differ, we're at the beginning or end of a string of ones/zeros
            elif comp_stat[i + 1] != comp_stat[i]:
                # Some cs values are missing... fill them in if there's a one space break in a string
                if comp_stat[i + 2] == comp_stat[i]:
                    comp_stat[i + 1] = comp_stat[i]
                # if cs @ i+1 is a 1, then i+1 is a peak; add i to peaks
                elif comp_stat[i + 1] == 1:
                    peaks = np.append(peaks, i + 1)
                # if not, cs @ i must be a valley, so add i to valleys
                else:
                    valleys = np.append(valleys, i)
            i = i + 1

        # We now have 2 lists of peak/valley indices.

        # First index must be a peak, last a valley, lengths of each array must match.
        # Delete first valley index until the first valley is after the first peak
        while valleys[0] < peaks[0]:
            valleys = np.delete(valleys, 0)
        # Delete the last peak index until the last peak index is right before the last valley
        while peaks[peaks.size - 1] > valleys[valleys.size - 1]:
            peaks = np.delete(peaks, peaks.size - 1)
        # return the two arrays.
        return peaks, valleys
    
    def get_time_diffs(self, peaks, valleys):
        '''Returns time differences'''
        dateTime = self.data.index.to_numpy()
        time_diffs = []
        for i in range(peaks.size):
            time_diffs.append((dateTime[valleys[i]] - dateTime[peaks[i]]) / np.timedelta64(1, 'h'))
        return time_diffs

    def get_temp_diffs(self, peaks, valleys):
        '''returns temperature differences'''
        values =  self.data[self.data.columns[0]].to_numpy()
        temp_diffs = []
        for i in range(peaks.size):
            temp_diffs.append(values[peaks[i]] - values[valleys[i]])
        return temp_diffs

    def get_degrees_per_hour(self, peaks, temp_diffs, time_diffs):
        '''Returns degrees per hour'''
        deg_per_hour = []
        for i in range(peaks.size):
            deg_per_hour.append((temp_diffs[i] / time_diffs[i]))
        return deg_per_hour
