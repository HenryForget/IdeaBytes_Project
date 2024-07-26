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

# import vibration data into pandas dataframe
vibedata_sorted = analysis.analysisEmerald.importer('../Data/VAM_CT_Motor_1__vibration.csv', 1)
# Getting rid of divice ID
vibedata_sorted = vibedata_sorted.drop(['deviceId'], axis=1)
# Creating index column -- replacing the sensorTime column since clf.fit cant use datetime format and an index acheives the same goal for our purposes
vibedata_sorted['sensorTime'] = range(1, len(vibedata_sorted)+1)
# plot raw data
analysis.analysisEmerald.plotScatter(vibedata_sorted, './Vibration_Data_Set_raw.png')
# plot anomolys
analysis.analysisEmerald.plotIsolationForest(vibedata_sorted, "b", "r", 0.05, './Vibration_Data_Set_outliers.png' )