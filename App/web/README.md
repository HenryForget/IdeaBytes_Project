TODO for this part:
<br/>
0. Set up the list of devices. We will show them in a dropdown menu. For each of the devices graph page will be showing 3 graphs: one with real data (see p. 1), one with predicted data (see p.3), one with compressor efficiency (see p. 3).
 - we probably can  get names of devices from the PostgREST, we will double check that. If not, we will read the list from the JSON file that we will add to the webapp folder.
1. Set up method that calls database to render graphs from the "real" data
 - method will be called internally with the set up frequency -> we don't need a button for it 
 - this method will call the REST API of the PostgREST container for each  device and return the Json with data. 
 - we will set up calls frequency later
 - method will convert recieved JSON format data to pandas dataframe 
 - graph will be drawn from the pandas dataframe
 -graph should also check if thresholds are set up and if yes, it should show them as horizontal lines
2. Set up method that calls app-backend for temp predictions
 - method will be called on demand -> we need a button for it. This will work as such: the default prediction time is 1 hour, but we should gove a choice of 4 hours and 8 hours prediction intervals.
 - method will need to pass device and prediction interval (if 4 and 8 hours chosen) for which it calls the prediction method. 
 - method will call the REST API of the app-backend container (model folder scripts in repo) 
 - method will receive a tuple of JSON data from the app-backend: first one is real data, second - prediction.
 - method will convert the received data to pandas dataframes 
 - graph will be drawn so it shows real data in one color with its own label, and predicted data in another color with another label
 - graph should also check if thresholds are set up and if yes, it should show them as horizontal lines
3. Set up method that calls app-backend for compressor efficiency:
 - method will be called on demand -> we need a button for it
 - method will call the REST API of the app-backend container (model folder scripts in repo) 
 - method will receive data (probably not JSON, just a regular python datatype) to graph the compressor efficiency
 - method will render a graph from the received data
4. Set up method that checks added thresholds and creates alert message if threshold is breached
 - method should check this for all devices  
 - if the threshold is set up, the method will check the predicted data; if threshold is not set up, no actions 
 - method will call the REST API of the app-backend container (model folder scripts in repo) with set frequency 
 - we will set up calls frequency later
 - method will compare values returned from the app-backend with thresholds and set up a message for the alert
 - we don't need to convert JSON in this case to dataframe -> can convert it to dictionary and parse dictionary instead
 - message will contain: device, threshold, temp that breaks it, time when it's predicted, time when it's calculated
 - message will appear on the threshold page 