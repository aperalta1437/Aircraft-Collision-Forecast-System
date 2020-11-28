from kivy_garden.mapview import MapMarkerPopup

class AirplaneMarker(MapMarkerPopup):
    def __init__(self, data):
        super(AirplaneMarker, self).__init__()
        self.data = data
        self.lat = data[6]
        self.lon = data[7]

    def set_source(self, source):
        self.source = source

    def on_release(self):
        # Open up the LocationsPopupMenu
        pass