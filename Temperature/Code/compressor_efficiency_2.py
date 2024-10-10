import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

class compEff():

    def getPeaksValleysStatus(values, comp_stat):
        '''
            Uses compressor status to construct peak/valley pairs.
            :param values:  list of temperature values
            :param comp_stat:  list of compressor status values (1 or 0)
            :return peaks: array of peak indices
            :return valleys: array of valley indices
        '''

        # Create empty arrays
        peaks = np.array([], dtype=np.int8)
        valleys = np.array([], dtype=np.int8)

        # Loop through each compt_stat (cs) value
        i = 0
        while i < len(comp_stat) - 2:
            # If the first index has cs = 1 then it's a peak
            if i == 0:
                if comp_stat[i] == 1:
                    peaks = np.append(peaks, i)
            # If the last value has cs = 1 then it's a valley
            # [Note] End of array needs fixing, off by one error, won't pick up last peak/valley pair
            elif i == len(comp_stat) - 1:
                if comp_stat[i + 1] == 1:
                    valleys = np.append(valleys, i + 1)
                elif comp_stat[i] == 1:
                    valleys = np.append(valleys, i)
            # Check cs @ i+1 vs cs @ i; if they differ, we're at the beginning or end of a string of ones/zeros
            elif comp_stat[i + 1] != comp_stat[i]:
                # Some cs values are missing... fill them in if there's a one space break in a string
                if comp_stat[i + 2] == comp_stat[i]:
                    comp_stat[i + 1] = comp_stat[i]
                # if cs @ i+1 is a 1, then i+1 is a peak; add i to peaks
                elif comp_stat[i + 1] == 1:
                    peaks = np.append(peaks, i + 1)
                # if not, cs @ i must be a valley, so add i to valleys
                else:
                    valleys = np.append(valleys, i)
            i = i + 1

        # We now have 2 lists of peak/valley indices.

        # First index must be a peak, last a valley, lengths of each array must match.
        # Delete first valley index until the first valley is after the first peak
        while valleys[0] < peaks[0]:
            valleys = np.delete(valleys, 0)
        # Delete the last peak index until the last peak index is right before the last valley
        while peaks[peaks.size - 1] > valleys[valleys.size - 1]:
            peaks = np.delete(peaks, peaks.size - 1)
        # return the two arrays.
        return peaks, valleys

    ### Depreciated, using compressor status to detect peaks valleys ###
    def getPeaksValleys(values):
        peaks, _ = find_peaks(values, distance=5)
        valleys, _ = find_peaks(values * -1, distance=5)

        while valleys[0] < peaks[0]:
            valleys = np.delete(valleys, 0)
        while peaks[peaks.size - 1] > valleys[valleys.size - 1]:
            peaks = np.delete(peaks, peaks.size - 1)

        i = 0
        while i < len(peaks) - 2:
            while peaks[i + 1] < valleys[i]:
                if values[peaks[i + 1]] > values[peaks[i]]:
                    peaks = np.delete(peaks, i)
                else:
                    peaks = np.delete(peaks, i + 1)
            while valleys[i + 1] < peaks[i + 1]:
                if values[valleys[i + 1]] < values[valleys[i]]:
                    valleys = np.delete(valleys, i)
                else:
                    valleys = np.delete(valleys, i + 1)
            i += 1

        return peaks, valleys

    def getTimeDiffs(dateTime, peaks, valleys):
        time_diffs = []
        for i in range(peaks.size):
            time_diffs.append((dateTime[valleys[i]] - dateTime[peaks[i]]) / np.timedelta64(1, 'h'))
        return time_diffs

    def getTempDiffs(values, peaks, valleys):
        temp_diffs = []
        for i in range(peaks.size):
            temp_diffs.append(values[peaks[i]] - values[valleys[i]])
        return temp_diffs

    def getDegreesPerHour(peaks, temp_diffs, time_diffs):
        deg_per_hour = []
        for i in range(peaks.size):
            deg_per_hour.append((temp_diffs[i] / time_diffs[i]))
        return deg_per_hour

    def plotPeaksValleys(dateTime, values, peaks, valleys, comp_stat, deg_per_hour):
        # Clear plot
        plt.clf()
        # Set figure size
        plt.figure(figsize=(150, 26))
        # Plot data and scatter
        plt.plot(dateTime, values)
        plt.scatter(dateTime, values)
        # Recolour points where compressor is running
        for i in range(comp_stat.size):
            if comp_stat[i] == 1:
                plt.scatter(dateTime[i], values[i], color='yellow')
        # Plot peaks
        for p in peaks:
            plt.scatter(dateTime[p], values[p], color='red', s=200)
        # Plot Valleys
        for v in valleys:
            plt.scatter(dateTime[v], values[v], color='green', s=200)
        # Plot peak to valley line segments
        for i in range(peaks.size):
            plt.plot([dateTime[peaks[i]], dateTime[valleys[i]]], [values[peaks[i]], values[valleys[i]]], 'r-',
                     label=str(round(deg_per_hour[i], 2)) + " Degrees/Hour")
        # Show legend and plot
        plt.legend(fontsize=10, loc='right')
        plt.show()