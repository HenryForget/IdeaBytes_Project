import Code.analysisEmerald as analysis
import Code.config as config
import plotly.express as px

# import vibration data into pandas dataframe
vibedata_sorted = analysis.analysisEmerald.importer(config.InputFile, config.DateCol)
# capture all non-zero instances and non-null and remove duplicates
vibedata_cleaned = analysis.analysisEmerald.cleanData(vibedata_sorted)
# convert all datetime values from String to datetime format and convert data values to float64 datatype
analysis.analysisEmerald.colToDateTime(vibedata_cleaned, config.DateCol, config.DateTimeFormat)
analysis.analysisEmerald.colToFlt64(vibedata_cleaned, config.ValueCol)

# plot the daily data with matplotlib:
vibedata_dividedDays = analysis.analysisEmerald.divideDays(vibedata_cleaned, vibedata_cleaned.columns[config.DateCol])
# Derive stats from the daily data
analysis.analysisEmerald.vibrationStats(vibedata_dividedDays, vibedata_cleaned.columns[config.ValueCol], config.StatsFilePath)
# Print daily data as pdf
analysis.analysisEmerald.plotDaysDataframesPDF(vibedata_dividedDays, 7, config.GraphFilePath)
# check data for predictions
vibedata_predictions = analysis.analysisEmerald.predictData(vibedata_cleaned, vibedata_cleaned.columns[config.ValueCol])

vibedata_predictions.to_csv('out.csv', index=False)
fig = px.scatter(x=vibedata_predictions['Date/Time'], y=vibedata_predictions['vibration (mm/s)'], color=vibedata_predictions['anomaly'])
fig.write_image('./pltcolor.png')