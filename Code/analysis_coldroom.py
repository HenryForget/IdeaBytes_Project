'''Running temp analysis for cold room data'''
import temp_analysis as temp

dataset = temp.TempAnalysis(datapath='/mnt/c/IdeaBytes/Git/IdeaBytes_Project/Data/Temperature_NewDataSet/ColdRoom_DataLogger.csv',
                            configpath='/mnt/c/IdeaBytes/Git/IdeaBytes_Project/Code/temp.conf')
dataset.prepare_data()
dataset.plot_general(name = 'coldroom_general')
dataset.plot_daily(name = 'coldroom_daily')
adf = dataset.calculate_adf()
print(f'Dataset stationary(ADF): {adf}')
kpss = dataset.calculate_kpss()
print(f'Dataset stationary(KPSS): {kpss}')
