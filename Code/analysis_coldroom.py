'''Running temp analysis for cold room data'''
from temp_analysis import TempAnalysis
from time_series_forecasting import TsForecasting

coldroom = TempAnalysis(datapath='/mnt/c/IdeaBytes/Git/IdeaBytes_Project/Data/Temperature_NewDataSet/ColdRoom_DataLogger.csv',
                            configpath='/mnt/c/IdeaBytes/Git/IdeaBytes_Project/Code/temp.conf')
coldroom.prepare_data()
print(coldroom.get_stats())
dataset.plot_general(name = 'coldroom_general')
dataset.plot_daily(name = 'coldroom_daily')
adf = coldroom.calculate_adf()
print(f'Dataset stationary(ADF): {adf}')
kpss = coldroom.calculate_kpss()
print(f'Dataset stationary(KPSS): {kpss}')
if adf==kpss==True:
    coldroom_models = TsForecasting(dataset = coldroom.data, graph_dir=coldroom.graphs_dir)
    coldroom_models.run_arima()
