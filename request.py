# https://pbpython.com/pandas-list-dict.html
# https://hackernoon.com/deploy-a-machine-learning-model-using-flask-da580f84e60c


import requests

url = 'http://localhost:5000/api'

data={'id':'id3004672',
'vendor_id':1,
'pickup_datetime':'2016-06-30 23:59:58',
'passenger_count':1,
'pickup_longitude':-73.988128662109375,
'pickup_latitude':40.732028961181641,
'dropoff_longitude':-73.99017333984375,
'dropoff_latitude':40.756679534912109,
'store_and_fwd_flag':'N',}

r = requests.post(url,json=data)
print(r.status_code)
print(r.json())