
This is a tentative structure for the app:
1. alerting.py:
 - GUI: graphs with real-data, predictions, and alerts level.
 - will allow to set thresholds for temperature (and store it as an instance variable for each device/client?)
 - will have endpoint allowing to post predictions datapoints
 - will display predictions along with alert (if applicable) in UI
 - will query db to use data for graphs 

2. app.py:
- main point of the app. 
- will use classes written for data preparation and model training
- will use models to make predictions based on real-time data pushed from database

3. data_prep.py:
- will initially fetch the data from the db for models training
- will clean and prepare data for models

4. models.py:
- in its final state will have two models for prediction: one for temp, another for compressor efficiency
- will have methods that will use existing models to predict data based on real-time info from the db

5. temp.conf: 
- will have basic config for data processing

THINGS TO ADD apart from methods inside exising files:
~~- script that will create mock data every 5 minutes and push it to db~~
- script that will push initial data to db that we will use for model training  - this is not a part of app when in prod.

