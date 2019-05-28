
# This piece of code is inspired from: http://blog.tkbe.org/archive/python-calculating-the-distance-between-two-locations/
# It calculate the "crow flies" distance between two locations 
import math

features = ['trip_distance', 'day_pickup', 'hour_pickup', 'minute_pickup', "pickup_longitude", "dropoff_longitude", "pickup_latitude", "dropoff_latitude"]
target = 'trip_duration_log'


 
def cosrad(n):
    "Return the cosine of ``n`` degrees in radians."
    return math.cos(math.radians(n))

def distance(row):
    """Calculate the distance between two points on earth.
    """
    lat1 = row['pickup_latitude']
    long1 = row['pickup_longitude']
    lat2 = row['dropoff_latitude']
    long2 = row['dropoff_longitude']
    earth_radius = 6371  # km
    dLat = math.radians(lat2 - lat1)
    dLong = math.radians(long2 - long1)
    a = (math.sin(dLat / 2) ** 2 +
         cosrad(lat1) * cosrad(lat2) * math.sin(dLong / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = earth_radius * c
    return d
