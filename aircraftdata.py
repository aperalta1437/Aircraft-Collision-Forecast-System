from opensky_api import OpenSkyApi
from math import pi, cos
import time
import geopy
import geopy.units
import geopy.distance
from config import Config


# Docs: https://opensky-network.org/apidoc/python.html

class AircraftData:
    """
    Handles all data from api, and provides appropriate calculations for the aircraft forecast
    Singleton Implementation taken from:
    https://www.tutorialspoint.com/python_design_patterns/python_design_patterns_singleton.htm"""
    # Note: it returns none when error is caught for getting states instead of actual error

    __singletonAircraftData = None

    @staticmethod
    def get_instance(username=None, password=None):
        if AircraftData.__singletonAircraftData is None:
            AircraftData(username, password)
        return AircraftData.__singletonAircraftData

    def __init__(self, username=None, password=None):
        if AircraftData.__singletonAircraftData is not None:
            raise Exception("This is a singleton class, cannot instantiate")
        else:
            self.api = OpenSkyApi(username, password)
            if username and password:  # if not logging in, you will get 10 sec delay compared to 5 for logged in users
                self.delay = 5
            else:
                self.delay = 10
            self.config = Config.get_instance()  # contains all the settings
            self.username = username
            self.password = password
            AircraftData.__singletonAircraftData = self

    def get_states_from_coordinates(self, coordinates):
        """Used for getting states from an airport or other static location
        :param coordinates: represented in (lat, long) tuple
        :return states object: contains each aircraft represent as a state, see api docs for more info
        """
        bbox = self.get_bbox(coordinates, self.config.get_airport_bbox_settings())
        states = self._get_states_from_api(bbox)
        return states

    def get_states_from_plane(self, ICAO24):  # plane represented in with ICAO24 address, should be a 6-character hex representation
        """Gets states from a moving object such as a plane
        :param ICAO24: string
        :return states object:
        """
        start_time = time.time()  # https://stackoverflow.com/questions/3620943/measuring-elapsed-time-with-the-time-module/46544199
        states = self._get_states_from_api(icao24=ICAO24)
        elapsed_time = time.time() - start_time  # represents the time it took to get the chosen plane state
        #  this value will be used to calculate the predicted coordinates because we can only data 5-10 secs and the api sometimes has issues fetching data
        #  we use the prediction to get a more accurate bounding box around the plane
        try:
            plane = states.states[0]
        except IndexError:
            print("Cannot find plane with specified ICAO24 address")
            return None
        predictedCoordinates = self.predict_coordinates((plane.latitude, plane.longitude), plane.velocity,
                                                        plane.heading, elapsed_time)
        bbox = self.get_bbox(predictedCoordinates, self.config.get_airplane_bbox_settings())

        states = self._get_states_from_api(bbox=bbox)
        return states

    def _get_states_from_api(self, icao24=None, bbox=None):
        noStates = True
        while noStates:
            # try:
            if bbox:  # only a bbox or icao24, not both
                states = self.api.get_states(bbox=bbox)
            else:
                states = self.api.get_states(icao24=icao24)
            if not states:
                # except requests.exceptions.ReadTimeout:
                print("Waiting for OpenSky Network API")
                time.sleep(self.delay)  # wait for timer before trying to get states again #TODO: potential issue with sleep
            else:
                noStates = False
        return states

    def predict_coordinates(self, currentPos, velocity, heading,
                            time):  # https://stackoverflow.com/questions/24427828/calculate-point-based-on-distance-and-direction
        """Determines where the plane will be in a certain amount of time
        :param currentPos: (lat, long) coordinates
        :param velocity: in m/s
        :param heading: in decimal degree, 0 degrees is true north
        :param time: how far in the future you want to see, multiplied with velocity
        :return predicted position: a tuple containing the expected position of a single plane, (lat, long)
        """
        distance = velocity * time
        distanceKm = geopy.units.kilometers(meters=distance)
        # Define starting point.
        start = geopy.Point(currentPos[0], currentPos[1])
        # Define a general distance object.
        d = geopy.distance.distance(kilometers=distanceKm)
        final = d.destination(point=start, bearing=heading)
        print("predict coordinates, currentpos: {}, newpos: {} ".format(currentPos,
                                                                                  (final.latitude, final.longitude)))
        return final.latitude, final.longitude

    def get_bbox(self, source, bbox_settings):  # source can airplane or airport (lat,long)
        """returns a bbox based on current position added to the bbox settings
        :param source: tuple consisting of (lat, long) coordinates
        :param bbox_settings: a tuple in the form, (min_latitude, max_latitude, min_longitude, max_longitude)
        :return: bbox: a tuple in the form, (min_latitude, max_latitude, min_longitude, max_longitude)
        """
        # logic here is to add constant values to existing lat,long and return bbox
        # solution given here: https://stackoverflow.com/questions/7477003/calculating-new-longitude-latitude-from-old-n-meters
        r_earth = 6378137.0  # radius of earth in meters according to WGS84 datum, source: http://www.unoosa.org/pdf/icg/2012/template/WGS_84.pdf

        latitude = source[0]
        longitude = source[1]

        lowerXDistance = bbox_settings[0]
        higherXDistance = bbox_settings[1]

        lowerYDistance = bbox_settings[2]
        higherYDistance = bbox_settings[3]

        min_latitude = latitude - (lowerYDistance / r_earth) * (180 / pi)
        max_latitude = latitude + (higherYDistance / r_earth) * (180 / pi)

        min_longitude = longitude - (lowerXDistance / r_earth) * (180 / pi) / cos(latitude * pi / 180)
        max_longitude = longitude + (higherXDistance / r_earth) * (180 / pi) / cos(latitude * pi / 180)
        # print("from get bbox func, source: {}, bbox: {}".format(source, (min_latitude, max_latitude, min_longitude, max_longitude)))
        return min_latitude, max_latitude, min_longitude, max_longitude
