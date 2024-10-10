import analysisEmerald as analysis
import config as config

# Import Data
vibedata = analysis.analysisEmerald.importer(config.InputFile, config.DateCol)

# convert all datetime values from String to datetime format and convert data values to float64 datatype
analysis.analysisEmerald.colToDateTime(vibedata, config.DateCol, config.DateTimeFormat)
analysis.analysisEmerald.colToFlt64(vibedata, config.ValueCol)

# Creating elbow graph
analysis.analysisEmerald.optimise_k_means(vibedata[[vibedata.columns[config.ValueCol]]], config.maxKMeans,config.ElbowFilePath)

# KMeans analysis saved as one big figure and a sectioned figure
analysis.analysisEmerald.KMeansBigFig(vibedata, config.BigFigFilePath) # Quick View
print("-----------------------------------------------\n")
analysis.analysisEmerald.KMeansSectionFig(vibedata, config.SectionFigFilePath, config.divisionFrequency) # Includes section stats
