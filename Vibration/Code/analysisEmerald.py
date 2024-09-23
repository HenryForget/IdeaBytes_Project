import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from sklearn.cluster import KMeans
import Code.config as config

class analysisEmerald:
    '''
    Reusable methods for data preperation and cleaning
    '''

    def createElbow(dataPath, max_k, imgPath):
        '''
        Function sourced from https://youtu.be/iNlZ3IU5Ffw?si=Xu5nMiMEwdU9vJoC
        Creates an elbow graph for the optimal KMeans K value
        :param data: Dataframe
        :param max_k: Maximum number of K
        '''
        means = []
        inertias = []

        data = pd.read_csv(dataPath, header=None, usecols=[config.DateCol, config.ValueCol])
        # capture all non-zero instances and non-null
        cleaned = data.dropna(axis=0, how='any')
        cleaned = cleaned[cleaned[cleaned.columns[0]] != 0]
        print(f"Total instances after cleaning: {len(cleaned)}\n")
        # remove duplicates
        cleaned = cleaned.drop_duplicates(keep='first')

        for k in range(1, max_k):
            kmeans = KMeans(n_clusters=k)
            kmeans.fit(data[[data.columns[config.ValueCol]]])

            means.append(k)
            inertias.append(kmeans.inertia_)

        # Generate the elbow plot
        fig = plt.subplots(figsize=(10,5))
        plt.plot(means, inertias, 'o-')
        plt.xlabel('Number of Clusters')
        plt.ylabel('Inertia')
        plt.grid(True)
        plt.savefig(imgPath)
        print('file created at: ' + str(imgPath) + '\n')

    def importAndCleanSections(path, colTime, colData, timeFormat, i):
        '''
        Imports data and cleans information
        :param path: file path to be imported
        :param colTime: which column has the time data
        :param colData: which column has the value data
        :param timeFormat: time column's format
        :return: Imported dataframe
        '''
        data = pd.read_csv(path, header=None, usecols=[colTime,colData],
                           nrows=(config.StartingIndex + config.NumEntries),
                           skiprows=(config.StartingIndex + (config.dataIncrement * i)))
        data.sort_values(by=data.columns[colTime])

        # capture all non-zero instances and non-null
        cleaned = data.dropna(axis=0, how='any')
        cleaned = cleaned[cleaned[cleaned.columns[0]] != 0]
        print(f"Total section instances after cleaning: {len(cleaned)}\n")
        # remove duplicates
        cleaned = cleaned.drop_duplicates(keep='first')

        analysisEmerald.colToTypes(cleaned, colTime, colData, timeFormat)
        print("Analizing rows " + str(config.StartingIndex + (config.dataIncrement * i)) + " to " + str(config.StartingIndex + config.NumEntries + (config.dataIncrement * i)))
        return cleaned

    def colToTypes(df, colTime, colData, timeFormat):
        '''
        Converts a column to DateTime format
        :param colTime: which column has the time data
        :param colData: which column has the value data
        :param timeFormat: time column's format
        :return: Converted dataframe
        '''
        df[df.columns[colTime]] = pd.to_datetime(df[df.columns[colTime]], format=timeFormat)
        df[df.columns[colData]] = df[df.columns[colData]].astype(float)
        return df

    def KMeansLabels(df):
        '''
        Fits the dataframe to the KMeans algorithm and adds cluster labels
        :param df: dataframe
        :return: Dataframe with labels
        '''
        # Create KMeans Labels
        kmeans = KMeans(n_clusters=config.kMeansNumClusters)
        kmeans.fit(df[[df.columns[config.ValueCol]]])
        df['Kmeans Labels'] = kmeans.labels_

        # Find the group of anomalies
        anomaly = df.loc[analysisEmerald.closest(df[df.columns[config.ValueCol]], 0)]['Kmeans Labels']
        # Applying the condition
        df['Kmeans Labels'] = np.where(df['Kmeans Labels'] == anomaly, 1, 0)
        return df

    def closest(lst, K):
        '''
        Finds the closest number to K within list lst and returns it's index
        :param lst: List
        :param K: Number to find
        :return: Returns the index location of the closest to K
        '''
        lst = np.asarray(lst)
        idx = (np.abs(lst - K)).argmin()
        return idx

    def KMeansBigFig(df, path, title, i):
        '''
        Creates one big scatter graph with color labeled anomolies
        :param df: dataframe
        :param path: Path to save graph
        :param title: Title of the figure
        '''
        # Add index for graph
        df['index'] = range(0, len(df))
        # Create big fig
        plt.clf()
        plt.scatter(y=df[df.columns[config.ValueCol]], x=df['index'], c=df['Kmeans Labels'],
                    cmap=colors.LinearSegmentedColormap.from_list("", [config.goodColor, config.badColor]))
        plt.title(title)
        plt.xlabel("Data Points")
        plt.ylabel(df.columns[config.ValueCol])
        plt.savefig(path + str(i) + '.png')
        print('file created at: ' + str(path) + str(i) + '.png\n')