import Code.analysisEmerald as analysis

# Stages of ML
# Busines understanding
# Data collection - csv read/fetch from DB
# Data exploration - plot raw data, detect bad data
# Data preparation - select only data required, deal with missing values, outiers,
#                    bad format. Plot selected clean data.
# Prepare ML models - not in this file
# Compare and train chosen model - not in this file
# Test model - not in this file

### Preparing data for time series ###
# import temperature data into pandas dataframe
colddata_sorted = analysis.analysisEmerald.importer('../Data/Temperature_Data_Set_Coldroom.csv', 0)
# plot raw data
analysis.analysisEmerald.plotLine(colddata_sorted,'./Temperature_Data_Set_Coldroom_raw.png')
# capture all non-zero instances and non-null and remove duplicates
colddata_cleaned = analysis.analysisEmerald.cleanData(colddata_sorted)
# convert all datetime values from String to datetime format and convert data values to float64 datatype
analysis.analysisEmerald.colToDateTime(colddata_cleaned, 0, 'mixed')
analysis.analysisEmerald.colToFlt64(colddata_cleaned, 1)
# plot cleaned data
analysis.analysisEmerald.plotLine(colddata_cleaned,'./Temperature_Data_Set_Coldroom.png')
# plot the daily data with matplotlib:
colddata_dividedDays = analysis.analysisEmerald.divideDays(colddata_cleaned, 0)
analysis.analysisEmerald.plotDaysDataframesPDF(colddata_dividedDays, 6, './Temperature_Data_Set_Coldroom_Grouped.png')