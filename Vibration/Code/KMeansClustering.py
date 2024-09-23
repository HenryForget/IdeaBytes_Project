import analysisEmerald as analysis
import config as config
import time as time

# Creating elbow graph
analysis.analysisEmerald.createElbow(config.InputFile, config.maxKMeans,config.ElbowFilePath)
i = 0;

while True:
    try:
        #   Import rows & set them to the proper types
        df = analysis.analysisEmerald.importAndCleanSections(config.InputFile, config.DateCol, config.ValueCol,config.DateTimeFormat, i)
    except:
        print("Not enough data points")
    else:
        #   Assign group of T/F for anomaly
        analysis.analysisEmerald.KMeansLabels(df)
        #   Create bigfig & json
        analysis.analysisEmerald.KMeansBigFig(df, config.BigFigFilePath, config.bigFigTitle, i)
        #   Wait for more data
        time.sleep(config.importWaitSec)
        i = i+1

    if 1 == 0:
        break