import sys
import json
from datetime import datetime, timedelta
from fastapi import FastAPI
sys.path.append('/app')
import requests as req
from data_prep import DataPreparation
from models import TsForecasting
# THIS IS A PLACEHOLDER FOR THE MAIN APP THAT WILL USE data_prep and models classes

# At its first initiation will fetch a list of devices we care about (either from config or json file) and 
# query db for data that will be used in models training.

# We assume that app will be running on Ideabytes server and they'll be able to store the model in db or anywhere in fs in case of server
# shutdown. The app should be checking if the model exists at that place and not try to fetch data for training if model can be
# restored.

# Data fetched from db will be prepared (data_prep.py) to be ready for models. This step is only required on the first app's
# launch.

# Once trained, models for each of the devices will be used to predict data based on real-time feed from db. 

# TODO: we need to run this for more than one device (current implementation). There should be
# probably a factory of devices that is created upon the app launch. The list of devices 
# could be in a config file, python fileor json file.

app = FastAPI()
# read devices list and get their ids to query SQL table - each device id is a table name in Postgres database

def prepare_data(device):
    '''Prepares initial data for each device'''
    # prepare data
    temp_data = DataPreparation(configpath='/app/temp.conf')
    temp_data.read_csv_data(datapath=f'/app/{device}.csv')
    temp_data.prepare_data()
    # prepare data for compressor efficiency plot
    # prepare peaks and valleys from temperature data
    peaks, valleys = temp_data.get_peaks_valleys_status()
    # get time differentials
    time_diffs = temp_data.get_time_diffs(peaks,valleys)
    # get temperature differentials
    temp_diffs = temp_data.get_temp_diffs(peaks, valleys)
    # Get Degrees of Cooling/Hour
    deg_per_hour = temp_data.get_degrees_per_hour(peaks, temp_diffs, time_diffs)
    return (temp_data, deg_per_hour)

def prepare_model(temp_data, deg_per_hour):
    '''Train model'''
    # prepare model for temperature forecasting
    model = TsForecasting(dataset = temp_data.data)
    model_trained = model.run_sarimax()
    # prepare initial compressor efficiency
    model.compr_model = model.predict_slope(deg_per_hour)
    return (model, model_trained)

# TODO We need to post the initial compressor efficiency to GUI endpoint to create a graph. 
# this will be done just once upon app launch.
# later on the call from GUI will get results from "real" data,
# add it to the initial one and will update the compressor efficiency graph

with open("/app/devices.json", 'r', encoding = 'utf-8') as file:
    devices_json = json.load(file)
devices = {}
for item in devices_json:
    data, degrees = prepare_data(item["id"])
    dev_obj, device_model = prepare_model(data, degrees)
    devices.update({item["id"]:[dev_obj, device_model, degrees]})


@app.get("/comp_eff")
async def get_comp_eff(device):
    '''Prepares current data and returns the slope for the predicted compressor efficiency'''
    real_data = DataPreparation(configpath='/app/temp.conf')
    json_data = get_data(device)
    real_data.read_json_data(json_data)
    real_data.prepare_data()
    rpeaks, rvalleys = real_data.get_peaks_valleys_status()
    rtime_diffs = real_data.get_time_diffs(rpeaks,rvalleys)
    rtemp_diffs = real_data.get_temp_diffs(rpeaks, rvalleys)
    rdeg_per_hour = real_data.get_degrees_per_hour(rpeaks, rtemp_diffs, rtime_diffs)
    model = devices.get(device)[0]
    deg_per_hour = devices.get(device)[2]
    updated_degrees = model.add_data(deg_per_hour, rdeg_per_hour)
    compr_updated = model.predict_slope(updated_degrees)
    return compr_updated

@app.get("/predict")
async def get_predict(device, period: int=1):
    '''Runs the trained model with the real-time data.
       Returns a tuple with real-time data and predicted data
    '''
    real_data = DataPreparation(configpath='/app/temp.conf')
    json_data = get_data(device)
    real_data.read_json_data(json_data)
    real_data.prepare_data()
    model = devices.get(device)[0]
    model_trained = devices.get(device)[1]
    predict = model.predict(real_data.data, model_trained, period)
    return (real_data.data, predict)

def get_data(device_table):
    '''Queries database and returns data in json string'''
    # TODO: check if the below logic works ok with db.
    # Dates are tested - they are returned in the proper format
    # REST call was not tested yet -> need to upload csv files with "future" data first
    today = datetime.today().date()
    query_date = (today - timedelta(days=1)).strftime("%d-%m-%Y")
    today = today.strftime("%d-%m-%Y")
    uri = f"http://app-server-1:3000/{device_table}?and=(time_data.like.{query_date}%,time_data.like.{today}%)"
    data_req = req.get(url=uri, timeout=30, verify=False)
    if data_req.status_code != 200:
        # TODO deal with None in response in respective methods
        return None
    json_string = json.dumps(data_req.json(), indent=2)
    return json_string
