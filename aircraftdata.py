from opensky_api import OpenSkyApi
from math import pi, cos
import time
import requests
import geopy
import geopy.units
import geopy.distance
import sys

class AircraftData():
    """Handles all data from api, and provides appropriate calculations for the aircraft forecast"""

    def __init__(self, username=None, password=None):  # bbox -  [min_latitude, max_latitude, min_longitude, max_longitude]  each meters
        self.api = OpenSkyApi(username, password)
        if username and password:  #if not logging in, you will get 10 sec delay compared to 5 for logged in users
            self.delay = 5
        else:
            self.delay = 10

        self.username = username
        self.password = password
                                                                    # 20 miles is about 32000m
    def get_statesFromCoordinates(self, coordinates, Bboxsettings = (32000, 32000, 32000, 32000)):  # coordinates represented in (lat, long) tuple
        bbox = self.get_bbox(coordinates, Bboxsettings)
        states = self._get_statesFromApi(bbox)
        return states

    def get_statesFromPlane(self, ICAO24, Bboxsettings = (10000, 10000, 10000, 10000)):  # plane represented in with ICAO24 address, should be a 6-character hex representation
        start_time = time.time()  # https://stackoverflow.com/questions/3620943/measuring-elapsed-time-with-the-time-module/46544199
        states = self._get_statesFromApi(icao24=ICAO24)
        elapsed_time = time.time() - start_time  #represents the time it took to get the chosen plane state
        #  this value will be used to calculate the predicted coordinates because we can only data 5-10 secs and the api sometimes has issues fetching data
        #  we use the prediction to get a more accurate bounding box around the plane
        try:
            plane = states.states[0]
        except IndexError:
            print("Cannnot find plane with specified ICAO24 address")
            sys.exit()
        predictedCoordinates = self.predict_coordinates((plane.latitude, plane.longitude), plane.velocity, plane.heading, elapsed_time)
        bbox = self.get_bbox(predictedCoordinates, Bboxsettings)

        states = self._get_statesFromApi(bbox=bbox)
        return states

    def _get_statesFromApi(self, icao24=None, bbox=None):
        noStates = True
        while noStates:
            #try:
            if bbox:  #only a bbox or icao24, not both
                states = self.api.get_states(bbox=bbox)
            else:
                states = self.api.get_states(icao24=icao24)
            if not states:
            #except requests.exceptions.ReadTimeout:
                print("Waiting for OpenSky Network API")
                time.sleep(self.delay)  # wait for timer before trying to get states again
            else:
                noStates = False
        return states

    def predict_coordinates(self, currentPos, velocity, heading, time):  # https://stackoverflow.com/questions/24427828/calculate-point-based-on-distance-and-direction
        distance = velocity*time

        distanceKm = geopy.units.kilometers(meters=distance)

        # Define starting point.
        start = geopy.Point(currentPos[0], currentPos[1])

        # Define a general distance object.
        d = geopy.distance.distance(kilometers=distanceKm)

        final = d.destination(point=start, bearing=heading)



        print("from predict coordinates func, currentpos: {}. newpos: {} ".format(currentPos, (final.latitude, final.longitude)))
        return final.latitude, final.longitude

    def get_bbox(self, source, Bboxsettings): # source can airplane or airport (lat,long)
        # logic here to coefficients to existing lat,long and return bbox
        # solution given here: https://stackoverflow.com/questions/7477003/calculating-new-longitude-latitude-from-old-n-meters
        r_earth = 6378137.0 #  radius of earth in meters according to WGS84 datum, source: http://www.unoosa.org/pdf/icg/2012/template/WGS_84.pdf

        latitude = source[0]
        longitude = source[1]

        lowerXDistance = Bboxsettings[0]
        higherXDistance = Bboxsettings[1]

        lowerYDistance = Bboxsettings[2]
        higherYDistance = Bboxsettings[3]

        min_latitude = latitude - (lowerYDistance  / r_earth) * (180 / pi)
        max_latitude = latitude + (higherYDistance / r_earth) * (180 / pi)

        min_longitude = longitude - (lowerXDistance / r_earth) * (180 / pi) / cos(latitude * pi / 180)
        max_longitude = longitude + (higherXDistance / r_earth) * (180 / pi) / cos(latitude * pi / 180)
        print("from get bbox func, source: {}, bbox: {}".format(source, (min_latitude, max_latitude, min_longitude, max_longitude)))
        return min_latitude, max_latitude, min_longitude, max_longitude


# issue it returns none when error is caught for getting states instead of actual error

test = AircraftData()
icao24 = "4951d4"
states = test.get_statesFromPlane(ICAO24=icao24)
print(len(states.states))
for state in states.states:
    if state.icao24 == icao24:
        print("it works!")
for state in states.states:
    print(state)


# x=0
# while x!=5:
#     try:
#         api = OpenSkyApi()
#         print(api)
#         states = api.get_states()
#         for state in states.states:
#             print(state)
#         print("Waiting for OpenskyNetworkAPI")
#         time.sleep(5)
#         x = x+1
#     except requests.exceptions.ReadTimeout:
#         print("Server Issue, trying again")
#         continue

# api = OpenSkyApi(username="dizzi", password="bentley")
# bbox = (46.2934807470979, 52.04269856546284, -2.1722615264697356, 6.62071430705047)
# states = api.get_states(bbox=bbox)
# print(len(states.states))
# for state in states.states:
#     if state.icao24 == "a39f0d":
#         print("it works!")
