# KMeansClustering
InputFile = '../Data/Motor1Vibrator.csv'
DateCol = 0
DateTimeFormat = '%d-%m-%Y %H:%M'
ValueCol = 1
DateColName = 'Date/Time'
ValueColName = 'vibration (mm/s)'
StatsFilePath = '../Data/Motor1VibratorStats.csv'
anomalyFilePath = '../Data/Motor1VibratorAnomaly.csv'
ElbowFilePath = './KMeans/KMeansElbow.png'
BigFigFilePath = './KMeans/KMeansOneBigFig.png'
SectionFigFilePath = './KMeans/KMeansOneFig.png'
GraphFilePath = './Vibration_Data_Set_Motor_Grouped.png'
Decimal = 3
maxKMeans = 10

# Kmeans graphing -----------------------------
kMeansNumClusters = 4
kMeansNumCols = 2
kMeansPlotFigWidth = 10 # Width for only one sub-figure
kMeansPlotFigHeight = 5 # Height for only one sub-figure
goodColor = "#00FF00"
badColor = "#FF0000"
# ---------------------------------------------


# analysisEmerald
# plotLine()
plotWidth = 40
plotHeight = 26
plotRotation = 35

# plotDaysDataframesPDF()
plotDaysFigWidth = 200
plotDaysFigHeight = 250


### Not Needed ???
std = 8.905
avg = 21.5
stdTreshold = 2