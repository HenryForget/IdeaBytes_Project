import analysisEmerald as analysis
import config as config
import math

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
from sklearn.cluster import KMeans

# Import Data
vibedata = analysis.analysisEmerald.importer('../Data/Motor1Vibrator.csv', config.DateCol)

## To be removed ##
vibedata['index'] = range(0, len(vibedata))
##               ##

# convert all datetime values from String to datetime format and convert data values to float64 datatype
analysis.analysisEmerald.colToDateTime(vibedata, config.DateCol, config.DateTimeFormat)
analysis.analysisEmerald.colToFlt64(vibedata, config.ValueCol)

# Creating elbow graph
analysis.analysisEmerald.optimise_k_means(vibedata[[config.ValueColName]], config.maxKMeans,config.ElbowFilePath)

kmeans = KMeans(n_clusters=config.kMeansNumClusters)
kmeans.fit(vibedata[['vibration (mm/s)']])
vibedata['kmeans_3'] = kmeans.labels_

anomaly = vibedata.loc[analysis.analysisEmerald.closest(vibedata['vibration (mm/s)'], 0)]['kmeans_3']

pltColors = np.full(config.kMeansNumClusters, "#00FF00")
pltColors[anomaly] = "#FF0000"
cmap = colors.LinearSegmentedColormap.from_list("", pltColors)

plt.clf()
plt.scatter(y=vibedata['vibration (mm/s)'], x=vibedata['index'], c=vibedata['kmeans_3'], cmap=cmap)
plt.savefig('./KMeans/KMeans' + 'OneBigFig' + '.png')

# Divide the daily data
vibedata_dividedDays = analysis.analysisEmerald.divideDays(vibedata, config.DateCol)

# Derive stats from the daily data
analysis.analysisEmerald.vibrationStats(vibedata_dividedDays, config.ValueColName, config.StatsFilePath)

# Create figure and subplots
figX = 0
figY = 0
if config.kMeansNumCols > 1:
     fig, ax = plt.subplots(math.ceil(vibedata_dividedDays.__len__() / config.kMeansNumCols), config.kMeansNumCols,
                            sharey=True)
else :
     fig, ax = plt.subplots(math.ceil(vibedata_dividedDays.__len__()), sharey=True)

for n in range(vibedata_dividedDays.__len__()):

     if config.kMeansNumCols > 1:
          # Add scatter plot to figure
          ax[figY][figX].scatter(y=vibedata_dividedDays[n]['vibration (mm/s)'], x=vibedata_dividedDays[n]['index'],
                               c=vibedata_dividedDays[n]['kmeans_3'], cmap=cmap)
          # Set title and axis labels
          ax[figY][figX].set_title("Day " + str(n + 1))
          ax[figY][figX].set_xlabel("Data Point")
          ax[figY][figX].set_ylabel("Vibration (mm/s)")

          # Get row/col position
          if (n + 1) % config.kMeansNumCols == 0:
               figY += 1
               figX = 0
          else:
               figX += 1
     else:
          # Add scatter plot to figure
          ax[n].scatter(y=vibedata_dividedDays[n]['vibration (mm/s)'], x=vibedata_dividedDays[n]['index'],
                               c=vibedata_dividedDays[n]['kmeans_3'], cmap=cmap)
          # Set title and axis labels
          ax[n].set_title("Day " + str(n + 1))
          ax[n].set_xlabel("Data Point")
          ax[n].set_ylabel("Vibration (mm/s)")

# Set figure size and save
fig.set_size_inches(config.kMeansPlotFigWidth * config.kMeansNumCols,
                    config.kMeansPlotFigHeight * (vibedata_dividedDays.__len__()/config.kMeansNumCols))
fig.tight_layout()
fig.savefig('./KMeans/KMeans' + 'OneFig' + '.png')

### TODO: Move to analysisEmerals as function
# Print the number of anomalies per day and change below to export to a CSV
#for n in range(vibedata.__len__()):
#     if vibedata.loc[n]['kmeans_3'] == anomaly:
#          print('Anomaly: ' + str(vibedata.loc[n]['Date/Time']) + '  ' + str(vibedata.loc[n]['vibration (mm/s)']))
