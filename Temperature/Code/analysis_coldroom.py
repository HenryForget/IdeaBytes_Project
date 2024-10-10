'''Running temp analysis for cold room data'''
from temp_analysis import TempAnalysis
from time_series_forecasting import TsForecasting

coldroom = TempAnalysis(datapath='/mnt/c/IdeaBytes/Git/IdeaBytes_Project/Temperature/Data/Temperature_NewDataSet/Freezer_DataLogger1.csv',
                            configpath='/mnt/c/IdeaBytes/Git/IdeaBytes_Project/Temperature/Code/temp.conf')
coldroom.prepare_data()
print(coldroom.get_stats())
coldroom.plot_general(name = 'coldroom_general')
coldroom.plot_daily(name = 'coldroom_daily')
adf = coldroom.calculate_adf()
# print(f'Dataset stationary(ADF): {adf}')
# kpss = coldroom.calculate_kpss()
# print(f'Dataset stationary(KPSS): {kpss}')
# if adf==kpss==True:
# coldroom_models = TsForecasting(dataset = coldroom.data, graph_dir=coldroom.graphs_dir)
# coldroom_models.run_arima()
# coldroom_models.run_sarimax()
# coldroom_models.run_prophet()
