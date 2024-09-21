# THIS IS A PLACEHOLDER FOR THE MAIN APP THAT WILL USE data_prep and models classes 
# Most likely will have couple of REST endpoints so that data can be sent there for predictions

# At its first initiation will fetch a list of devices we care about (either from config or json file) and 
# query db for data that wil be used in models training.

# We assume that app will be running on Ideabytes server and they'll be able to store the model in db or anywhere in fs in case of server
# shutdown. The app should be checking if the model exists at that place and not try to fetch data for training if model can be
# restored.

# Data fetched from db will be prepared (data_prep.py) to be ready for models. This step is only required on the first app's
# launch.

# Once trained, models for each of the devices will be used to predict data based on real-time feed from db. 
