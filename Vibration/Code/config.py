# KMeansClustering.py
# Importing -----------------------------
InputFile = '../Data/Motor1Vibrator.csv'
StartingIndex = 0
NumEntries = 1440
dataIncrement = 720
importWaitSec = 0

# Conversion ----------------------------
DateCol = 0
DateTimeFormat = '%d-%m-%Y %H:%M'
ValueCol = 1

# KMeans Calculation --------------------
kMeansNumClusters = 4 # Determined with elbow
maxKMeans = 10 # 10 is more then enough for any set

# KMeans Plotting and coloring ----------
bigFigTitle = "Motor1Vibrator.csv Anomalies"
goodColor = "#00FF00"
badColor = "#FF0000"

# File Directories ----------------------
ElbowFilePath = '../Data/Motor1Weekly_KMeansElbow.png'
BigFigFilePath = '../Data/Figs/Motor1_KMeansBigFig'