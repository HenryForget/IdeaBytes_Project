import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import statistics as stats
from sklearn.ensemble import IsolationForest
import Code.config as config
class analysisEmerald:
    '''
    Reusable methods for data preperation and cleaning
    '''

    def importer(path, sortCol):
        '''
        Imports a file and prints relative information
        :param path: file path to be imported
        :param sortCol: which column to sort by
        :return: Imported dataframe
        '''
        data = pd.read_csv(path)
        print(f"Total instances: {len(data)}")
        print(f"Features: {data.columns}\n")
        data.sort_values(by=f'{data.columns[sortCol]}')
        return data

    def plotLine(df, path):
        '''
        Plots the given dataframe in a line graph and saves it to the provided file path
        :param df: dataframe to graph
        :param path: file location to save to
        '''
        x_axis = df[f'{df.columns[0]}']
        y_axis = df[f'{df.columns[1]}']
        plt.figure(figsize=(config.plotWidth, config.plotHeight))
        plt.plot(x_axis, y_axis)
        plt.xticks(rotation=config.plotRotation)
        plt.savefig(path)
        print('file created at: ' + str(path) + '\n')

    def plotScatter(df, path):
        '''
        Plots the given dataframe in a scatter plot graph and saves it to the provided file path
        :param df: dataframe to graph
        :param path: file location to save to
        '''
        plt.scatter(df.iloc[:, 0], df.iloc[:, 1])
        plt.savefig(path)
        print('file created at: ' + str(path) + '\n')

    def cleanData(df):
        '''
        Clean all non-zero and non-null instances and remove dupicates
        :param df:  dataframe to clean
        :return: Cleaned dataframe
        '''
        # capture all non-zero instances and non-null
        cleaned = df.dropna(axis=0, how='any')
        cleaned = cleaned[cleaned[f'{cleaned.columns[0]}'] != 0]
        print(f"Total instances after cleaning: {len(cleaned)}\n")
        # remove duplicates
        cleaned = cleaned.drop_duplicates(keep='first')
        return cleaned

    def colToDateTime(df, col, format):
        '''
        Converts a column to DateTime format
        :param df: dataframe
        :param col: Column number to convert
        :return: Converted dataframe
        '''
        df[f'{df.columns[col]}'] = pd.to_datetime(df[f'{df.columns[col]}'], format=format)
        print(f'DF datatypes: \n{df.dtypes}\n')
        return df

    def colToFlt64(df, col):
        '''
        Converts a column to Float64 format
        :param df: dataframe
        :param col: Column number to convert
        :return: Converted dataframe
        '''
        df[f'{df.columns[col]}'] = df[f'{df.columns[col]}'].astype(float)
        print(f'DF datatypes: \n{df.dtypes}\n')
        return df

    def divideDays(df, col):
        '''
        Divide the dataframe into a list of smaller dataframes by the DateTime column
        :param df: dataframe to divide
        :param col: DateTime column
        :return: Dataframe list
        '''
        days_data = [group for n, group in
                     df.set_index(f'{df.columns[col]}').groupby(pd.Grouper(freq='D'))]
        return days_data

    def plot_data(x_axis,y_axis, ax):
        '''

        :param x_axis: x_axis value
        :param y_axis: y_axis value
        :param ax: 
        '''
        ax.set_title(x_axis[0].strftime('%Y-%m-%d'))
        ax.set_xlim(x_axis[0], x_axis[-1])
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.plot(x_axis, y_axis)

    def plotDaysDataframesPDF(df, numCol, path):
        '''
        Plot a list of dataframes
        :param df: dataframes
        :param numCol: number of columns
        :param path: file location to save to
        '''
        numRow = (int)(len(df) / numCol)
        fig, ax = plt.subplots(numRow + 1, numCol, sharey=True)

        for n in range(numRow + 1):
            for k in range (numCol):
                if n != numRow:
                    x_axis = df[n*numCol + k].index
                    y_axis = df[n*numCol + k][df[n*numCol + k].columns[0]]
                    analysisEmerald.plot_data(x_axis, y_axis, ax[n][k])
                else:
                    index = n * numCol + k
                    if index < len(df):
                        x_axis = df[n * numCol + k].index
                        y_axis = df[n * numCol + k][df[n * numCol + k].columns[0]]
                        analysisEmerald.plot_data(x_axis, y_axis, ax[n][k])
                    else:
                        break
        print("Data seperated")

        print("Plotting...")
        fig.set_size_inches(config.plotDaysFigWidth, config.plotDaysFigHeight)
        fig.savefig(path)
        print('file created at: ' + str(path) + '\n')

    def plotIsolationForest(df, colorGood, colorBad, contamination, path):
        '''
        Plot given dataframe in an isolation forest model and save the results
        :param df: dataframe
        :param colorGood: color code for the OK values
        :param colorBad: color code for the anomolies
        :param contamination: the contamination percent in decimal form (0.5 = 50%)
        :param path: file location to save to
        '''
        IF = IsolationForest(contamination=contamination)
        IF.fit(df)

        predictions = IF.predict(df)
        index = np.where(predictions < 0)
        x = df.values
        anomolyIndex = np.where(predictions < 0)

        plt.scatter(df.iloc[:, 0], df.iloc[:, 1], c=colorGood)
        plt.scatter(x[anomolyIndex, 0], x[anomolyIndex, 1], c=colorBad, edgecolors=colorBad)
        plt.savefig(path)
        print('file created at: ' + str(path) + '\n')

    def predictData(df, valueColName):
        '''
        Scan existing data and come up with predictions on the next item
        :param df: dataframe
        :param valueColName: name of the column that holds the values
        '''
        std = config.std
        avg = config.avg
        # add index
        df['index'] = range(0, len(df))

        for n in range(df.__len__()):
            # Each new instance after 0
            if n >= 1:
                # std = stats.stdev(df[valueColName][0:n+1], avg)
                # n's value is checked, if they are 3 standard deviations away from the current average
                if (df[valueColName][n] > avg+abs(std*config.stdTreshold)) | (df[valueColName][n] < avg-abs(std*config.stdTreshold)):
                    #  Print unexpected vibration
                    print('Anomolous vibration: instance ' + str(n))
                # avg = df[valueColName].mean()
            else:
                avg = df[valueColName][n]

        print("Final avg: " + str(avg) + "  Final std: " + str(std))

    def vibrationStats(df, valueCol, path):
        '''
        Derive stats from a column of values; saved to csv
        :param df: dataframe
        :param valueCol: name of the column that holds the values
        :param path: file location to save to
        '''
        data = []
        for n in range(df.__len__()):
            data.append([round(df[n][valueCol].mean(), config.Decimal),
                         round(df[n][valueCol].median(), config.Decimal),
                         round(df[n][valueCol].min(), config.Decimal),
                         round(df[n][valueCol].max(), config.Decimal)])
        statsDF = pd.DataFrame(data, columns=['Mean', 'Median', 'Min', 'Max'])
        statsDF.to_csv(path, index=False)
        print('file created at: ' + str(path) + '\n')

        trendList = [b - a for a, b in zip(statsDF['Mean'][::1], statsDF['Mean'][1::1])]
        trendVal = "%.3f" % float(sum(trendList) / len(trendList))
        print("Your vibration is trending by an average of " + trendVal + " each day.")
