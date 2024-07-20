import Code.analysisEmerald as analysis
import Code.config as config

# import vibration data into pandas dataframe
vibedata_sorted = analysis.analysisEmerald.importer(config.InputFile, config.DateCol)
# capture all non-zero instances and non-null and remove duplicates
vibedata_cleaned = analysis.analysisEmerald.cleanData(vibedata_sorted)
# convert all datetime values from String to datetime format and convert data values to float64 datatype
analysis.analysisEmerald.colToDateTime(vibedata_cleaned, config.DateCol, config.DateTimeFormat)
analysis.analysisEmerald.colToFlt64(vibedata_cleaned, config.ValueCol)

# plot the daily data with matplotlib:
vibedata_dividedDays = analysis.analysisEmerald.divideDays(vibedata_cleaned, config.DateCol)
# Derive stats from the daily data
analysis.analysisEmerald.vibrationStats(vibedata_dividedDays, config.ValueColName, config.StatsFilePath)
# Print daily data as pdf
analysis.analysisEmerald.plotDaysDataframesPDF(vibedata_dividedDays, 7, config.GraphFilePath)

# check data for predictions
analysis.analysisEmerald.predictData(vibedata_cleaned, config.ValueColName)