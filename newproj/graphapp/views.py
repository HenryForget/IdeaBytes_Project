import csv
import io
import os

import pandas as pd
import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.shortcuts import render
from .utils.IdeaBytes_Project.Temperature.Code.temp_analysis import TempAnalysis
import configparser


# Initialize TempAnalysis function
def initialize_temp_analysis(datapath, configpath):
    return TempAnalysis(datapath, configpath)


# View to plot the general temperature graph
def plot_general_view(request):
    config_path = r'C:\black-dashboard-django-master\black-dashboard-django-master\newproj\graphapp\utils\IdeaBytes_Project\Temperature\Code\temp.conf'  # Update with the correct path
    data_path = r'C:\black-dashboard-django-master\black-dashboard-django-master\newproj\graphapp\utils\IdeaBytes_Project\Temperature\Data\Temperature_NewDataSet\ColdRoom_DataLogger.csv'  # Update with the correct path

    coldroom = initialize_temp_analysis(datapath=data_path, configpath=config_path)
    coldroom.prepare_data()  # Prepare the data before plotting

    buffer = io.BytesIO()
    coldroom.plot_general(name='coldroom_general')
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    return HttpResponse(buffer, content_type='image/png')





def show_graphs(request):
    return render(request, 'graphs.html')


def read_devices_from_csv():
    devices = []

    csv_file_path = r'C:\black-dashboard-django-master\black-dashboard-django-master\newproj\graphapp\utils\IdeaBytes_Project\Temperature\Data\Temperature_NewDataSet\ColdRoom_DataLogger.csv'

    # Use the filename as the device name
    devices.append({
        'name': os.path.basename(csv_file_path)
    })

    return devices

def device_thresholds(request):
    devices = read_devices_from_csv()
    context = {
        'devices': devices
    }
    return render(request, 'threshold.html', context)