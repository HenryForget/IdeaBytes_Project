from temp_analysis import TempAnalysis
from compressor_efficiency_2 import compEff
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


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
### TODO: Clean up this code, move it to comp eff 2 and make it a callable function.

# x values for plot/linRegress
x_vals = np.array([], dtype=np.int8)

# Plot data and add i to x_vals
for i in range(len(deg_per_hour)):
    plt.scatter(i, deg_per_hour[i], color='green')
    x_vals = np.append(x_vals, i)
plt.show()

# Get line of best fit and print slope
slope, intercept, r_value, p_value, std_err = stats.linregress(x_vals, deg_per_hour)
print(slope)

### Slope of this line (slope) is what we're looking for. Can be displayed as:
### Compressor effeciency is trending (slope) degrees per compressor cycle.













