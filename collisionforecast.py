#  This will be the main file where the program executes from
#  Idea:
#
#  Allow user to input aiport or icao address, if airport option chosen, it will return a list of planes
#
#  Then it will allow the user to select a plane to track from that list using the GUI
#
#  Now we have the plane that we want to forecast collisions for
#
#  We use a user input distance and alitude setting to determine what other aircraft we will consider as possible collision targets
#  if planes are within certain alitude range of each other, they will be added to possible collisions
#  Ex: All planes +-150m from target will be considered
#  Use geopy distance calculator to get distance in meter
#  Ex: All planes 1500m from target will be considered
#
#  We add all the planes that fit these requirements to a graph
#  we will have a center node consisting of the target plane, and every other node is a plane with a weight that-
#  corresponds to the distance from the target plane... Im stuck here idk if this makes sense for using graphs
#
#  For the forecast part, we need to represent each plane in the graph using a function, it will be simple y=mx+b function
#  We need to use the function to approximate where the plane will be in a certain amount of time, for example 30 seconds
#  Then we use this to find the new x.y coordinates of where the plane will be
#  if the coordinates are within a certain radius of another plane's predicted position we can alert the user of a potention collision
#
#  We need to make the program execute the algorithm above every few seconds because,
#  The api will give us live information only once every 5 seconds if we use an account to login, 10 seconds if anonymous user
#
#  Issues:
#  I am still unsure if graphs are necessary and how can we make them more important to our project
#  Might have trouble getting reliable test results, as its based on real time data
#  Need to make sure we actually can get possible collisions to display, most aircraft already detects that with-
#  exception of small planes
#  Api might give errors due to server overload or something like that, so we need to use try catch block to keep the program running

from aircraftdata import AircraftData

class CollisionForecast():
    """This is where collisions are found"""
    def __init__(self, targetPlane, potentialCollisions, altitudeRange=500):
        self.targetPlane = targetPlane  # ICAO24 Address

        self.altitudeRange = altitudeRange # +- 150m from target plane's altitude, planes within the range are considered for potential collision
        self.targetBboxSettings = targetBboxSettings  # create bbox with these dimensions offset from target plane location

        self.bbox = self.get_bbox()

    def get_nearbyPlanes(self):
        pass
    def get_bbox(self):  # uses bbox distance settings and target planes coordinates to get actual bbox coordinates
        pass
