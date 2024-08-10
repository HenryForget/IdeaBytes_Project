'''Running temp analysis for cold room data'''
from temp_analysis import TempAnalysis
from time_series_forecasting import TsForecasting

coldroom = TempAnalysis(datapath='/mnt/c/IdeaBytes/Git/IdeaBytes_Project/Temperature/Data/Temperature_NewDataSet/ColdRoom_DataLogger.csv',
                            configpath='/mnt/c/IdeaBytes/Git/IdeaBytes_Project/Temperature/Code/temp.conf')
coldroom.prepare_data()
coldroom_models = TsForecasting(dataset = coldroom.data, graph_dir=coldroom.graphs_dir)
coldroom_models.run_prophet()
coldroom_models.run_neural_prophet()
