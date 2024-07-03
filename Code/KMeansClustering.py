import analysisEmerald as analysis
import config as config

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Import Data
vibedata = analysis.analysisEmerald.importer('../Data/Motor3Vibrator.csv', config.DateCol)

## To be removed ##
vibedata['index'] = range(0, len(vibedata))
##               ##

# convert all datetime values from String to datetime format and convert data values to float64 datatype
analysis.analysisEmerald.colToDateTime(vibedata, config.DateCol, config.DateTimeFormat)
analysis.analysisEmerald.colToFlt64(vibedata, config.ValueCol)
# Divide the daily data
vibedata_dividedDays = analysis.analysisEmerald.divideDays(vibedata, config.DateCol)
# Creating elbow graph
analysis.analysisEmerald.optimise_k_means(vibedata[[config.ValueColName]], config.maxKMeans,config.ElbowFilePath)

### TODO: Make a multigraph ###
for n in range(vibedata_dividedDays.__len__()):
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(vibedata_dividedDays[n][['vibration (mm/s)']])
    vibedata_dividedDays[n]['kmeans_3'] = kmeans.labels_

    plt.clf()
    plt.ylim(0, None) # Never going to be negatice vibration
    plt.scatter(y=vibedata_dividedDays[n]['vibration (mm/s)'], x=vibedata_dividedDays[n]['index'], c=vibedata_dividedDays[n]['kmeans_3'])
    plt.savefig('./KMeans/KMeans' + str(n) + '.png')