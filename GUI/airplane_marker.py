from kivy_garden.mapview import MapMarkerPopup

class AirplaneMarker(MapMarkerPopup):
    def __init__(self, data):
        super(AirplaneMarker, self).__init__()
        self.data = data

    def on_release(self):
        # Open up the LocationsPopupMenu
        pass