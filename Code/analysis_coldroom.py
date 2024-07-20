'''Running temp analysis for cold room data'''
from temp_analysis import TempAnalysis
from time_series_forecasting import TsForecasting
import os

dataPath ="../Data/Temperature_NewDataSet/"
dir_list = os.listdir(dataPath)
for count in range(len(dir_list)):
    print(f'{count+1}: {dir_list[count]}')

dataName = input("Enter the number of the data source: ")
dataSource = dataPath+dir_list[int(dataName)-1]

print(dataSource)


coldroom = TempAnalysis(datapath=dataSource,
                            configpath='../Code/temp.conf')
coldroom.prepare_data()
print(coldroom.get_stats())
TempAnalysis.plot_general(coldroom, name = 'coldroom_general')
#TempAnalysis.plot_daily(coldroom, name = 'coldroom_daily')
adf = coldroom.calculate_adf()
print(f'Dataset stationary(ADF): {adf}')
kpss = coldroom.calculate_kpss()
print(f'Dataset stationary(KPSS): {kpss}')
if adf==kpss==True:
    coldroom_models = TsForecasting(dataset = coldroom.data, graph_dir=coldroom.graphs_dir)
    coldroom_models.run_arima()
