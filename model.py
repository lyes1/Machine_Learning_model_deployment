import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as snb
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
from module import utils

# Data loading
TRAINFILEPATH = os.path.join('train.csv')
data = pd.read_csv(TRAINFILEPATH, index_col=0)

# Data preprocessing:

# We keep only the trips with a duration less than = 6 hours (21600 s) in in our dataset
data = data[data["trip_duration"]<21600]

# changing the date format of pickup_datetime and dropoff_datetime from objectto datetime64
data['pickup_datetime'] = pd.to_datetime(data['pickup_datetime'])
data['dropoff_datetime'] = pd.to_datetime(data['dropoff_datetime'])

    # create a copy of our dataset in order to have a backup
train = data
    # Month, day, hour, minute and second extraction from the pickup date time
        # adding the new columns to the train dataframe

train['month_pickup']=data['pickup_datetime'].dt.month
train['day_pickup']=data['pickup_datetime'].dt.dayofweek
train['hour_pickup']=data['pickup_datetime'].dt.hour
train['minute_pickup']=data['pickup_datetime'].dt.minute
train['second_pickup']=data['pickup_datetime'].dt.second
        # deleting the column pickup_datetime from the train dataframe
train = train.drop(columns=['pickup_datetime'])
    # Crow flies distance of the trips
        #We will add a new colunm to the dataset that gives the crow flies distance between the pickup and dropoff trips.


# adding the trip distance column to the train dataframe
train['trip_distance']=data.apply(utils.distance, axis=1)

# Log transform of the trip duration
train['trip_duration_log']=data['trip_duration'].apply(np.log)

X = train[utils.features]
y = train[utils.target]


# Scoring method
from sklearn.metrics import make_scorer
from sklearn.model_selection import cross_val_score

# Find in the comment of Enrique Pérez Herrero in: https://www.kaggle.com/marknagelberg/rmsle-function
def rmsle_func(ypred, ytest) :
    assert len(ytest) == len(ypred)
    return np.sqrt(np.mean((np.log1p(ypred) - np.log1p(ytest))**2))


# Model
from sklearn.ensemble import RandomForestRegressor
rmsle = make_scorer(rmsle_func) # Make RMSLE as a scorer

rfr = RandomForestRegressor(n_estimators=15)
# Model training
#scores_rfr = cross_val_score(rfr, X, y, cv=5, scoring=rmsle)
# Model fiting
rfr.fit(X, y)

# Saving model to disk
pickle.dump(rfr, open('model.pkl','wb'))