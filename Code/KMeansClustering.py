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

# Create figure and subplots
fig,ax = plt.subplots(8,1,sharey=True)

for n in range(vibedata_dividedDays.__len__()):
    kmeans = KMeans(n_clusters=config.kMeansNumClusters)
    kmeans.fit(vibedata_dividedDays[n][['vibration (mm/s)']])
    vibedata_dividedDays[n]['kmeans_3'] = kmeans.labels_

    # Add scatter plot to figure
    ax[n].scatter(y=vibedata_dividedDays[n]['vibration (mm/s)'], x=vibedata_dividedDays[n]['index'], c=vibedata_dividedDays[n]['kmeans_3'])
    ax[n].set_title("Day" + str(n+1))

# Set figure size and save
fig.set_size_inches(config.kMeansPlotFigWidth,config.kMeansPlotFigHeight)
fig.tight_layout()
fig.savefig('./KMeans/KMeans' + 'OneFig' + '.png')