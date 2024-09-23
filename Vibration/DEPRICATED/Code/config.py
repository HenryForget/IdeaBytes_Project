# KMeansClustering.py
# Importing -----------------------------
InputFile = '.../Data/Motor1Vibrator.csv'

# Conversion ----------------------------
DateCol = 0
DateTimeFormat = '%d-%m-%Y %H:%M'
ValueCol = 1

# KMeans Calculation --------------------
kMeansNumClusters = 4 # Determined with elbow
maxKMeans = 10 # 10 is more then enough for any set

# KMeans Plotting -----------------------
bigFigTitle = "Motor1Vibrator.csv Anomalies"
divisionFrequency = 'W' # D for Daily, W for Weekly, M for Monthly, Q for Quarterly, Y for yearly
kMeansNumCols = 4
kMeansPlotFigWidth = 10 # Dummy values; fig.tight_layout() accounts for size
kMeansPlotFigHeight = 5 # Dummy values; fig.tight_layout() accounts for size

# KMeans Coloring -----------------------
goodColor = "#00FF00"
badColor = "#FF0000"

# File Directories ----------------------
ElbowFilePath = '../KMeans/Motor1Weekly_KMeansElbow.png'
StatsFilePath = '.../Data/Motor1_VibratorStatsWeekly.csv'
Decimal = 3
anomalyFilePath = '.../Data/Motor1_VibratorAnomaly.csv'
BigFigFilePath = '../KMeans/Motor1_KMeansOneFig.png'
SectionFigFilePath = '../KMeans/Motor1_KMeansSectionFig_Weekly.png'

### OLD VARIABLES FOR TrendingVibration.py ###
plotDaysFigWidth = 200
plotDaysFigHeight = 250
std = 8.905
avg = 21.5
stdTreshold = 2