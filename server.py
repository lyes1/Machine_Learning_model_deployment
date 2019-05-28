import pandas as pd
# Create API of ML model using flask

'''
This code takes the JSON data while POST request an performs the prediction using loaded model and returns
the results in JSON format.
'''

# Import libraries
import numpy as np
from flask import Flask, request, jsonify
import pickle
from module import utils

app = Flask(__name__)

# Load the model
model = pickle.load(open('model.pkl','rb'))

@app.route('/api',methods=['POST'])
def predict():
    # Get the data from the POST request.
    data = request.get_json(force=True)
    print("#########Data :#########")

   # data = [data]

    #test = pd.DataFrame.from_dict(data)
    test = pd.DataFrame([data])
##################################################################
    # Date type transformation
    test['pickup_datetime'] = pd.to_datetime(test['pickup_datetime'])
    # It calculate the "crow flies" distance between two locations 
    test['month_pickup']=test['pickup_datetime'].dt.month
    test['day_pickup']=test['pickup_datetime'].dt.dayofweek
    test['hour_pickup']=test['pickup_datetime'].dt.hour
    test['minute_pickup']=test['pickup_datetime'].dt.minute
    test['second_pickup']=test['pickup_datetime'].dt.second
    test = test.drop(columns=['pickup_datetime'])
    # adding the trip distance column
    test['trip_distance']=test.apply(utils.distance, axis=1)
    test_X = test[utils.features]
##################################################

    # Make prediction using model loaded from disk as per the data.
    predicted_duration_log = model.predict(test_X)
    predicted_duration = np.exp(predicted_duration_log) # reverse the log predictions

    # Take the first value of prediction
    output = predicted_duration[0]
    print (type(output))
    return jsonify(output)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
