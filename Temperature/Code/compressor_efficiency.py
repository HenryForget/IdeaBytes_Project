from temp_analysis import TempAnalysis
from compressor_efficiency_2 import compEff

coldroom = TempAnalysis(datapath='../Data/eff_data_test.csv',
                            configpath='temp.conf')
coldroom.prepare_data()

# Extract date/time, values, and compressor status data from dataframe.
dateTime = coldroom.data.index.to_numpy()
values = coldroom.data['roomTemp (deg C)'].to_numpy()
comp_stat = coldroom.data['compStat'].to_numpy()

### Using Peak/Valley Detection ###
### No longer in use, but left for posterity ###

# Get Peaks/Valleys
# peaks, valleys = compEff.getPeaksValleys(values)
# Get time differentials
# time_diffs = compEff.getTimeDiffs(dateTime,peaks,valleys)
# Get temperature differentials
# temp_diffs = compEff.getTempDiffs(values, peaks, valleys)
# Get Degrees of Cooling/Hour
# deg_per_hour = compEff.getDegreesPerHour(peaks, temp_diffs, time_diffs)
# Plot data
# compEff.plotPeaksValleys(dateTime, values, peaks, valleys, comp_stat, deg_per_hour)

### Using Compressor Status ###

# Get Peaks/Valleys
peaks, valleys = compEff.getPeaksValleysStatus(values, comp_stat)
# Get time differentials
time_diffs = compEff.getTimeDiffs(dateTime,peaks,valleys)
# Get temperature differentials
temp_diffs = compEff.getTempDiffs(values, peaks, valleys)
# Get Degrees of Cooling/Hour
deg_per_hour = compEff.getDegreesPerHour(peaks, temp_diffs, time_diffs)
# Print Data
print('Degrees of Cooling/Hour:')
print(deg_per_hour)
# Plot data
# compEff.plotPeaksValleys(dateTime, values, peaks, valleys, comp_stat, deg_per_hour)

### deg_per_hour now holds list of 'Degrees of cooling per hour' ###
### TODO: Run trend analysis on list of values, determine how fast compressor effeciency is degrading.
















