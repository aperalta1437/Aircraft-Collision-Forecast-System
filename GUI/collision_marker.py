from kivy_garden.mapview import MapMarkerPopup
import sys

class CollisionMarker(MapMarkerPopup):

    def __init__(self, data, **kwargs):
        super(CollisionMarker, self).__init__()
        self.data = data
        # self.lat = data[15]
        # self.lon = data[16]


    def set_source(self, source):
        self.source = source

    def on_release(self):
        # Open up the LocationsPopupMenu
        pass
