from kivy_garden.mapview import MapMarkerPopup
from GUI.popups import show_message_popup

class CollisionMarker(MapMarkerPopup):

    def __init__(self, data, **kwargs):
        super(CollisionMarker, self).__init__()
        self.data = data
        self.lat = data[1][0]
        self.lon = data[1][1]


    def set_source(self, source):
        self.source = source

    def on_release(self):
        # Open up the LocationsPopupMenu
        airplane_status_message = f"Collision ICAO 24:      {self.data[0]:>20}\n" \
                                  f"Collision Latitude:     {self.data[1][0] if self.data[1][0] is not None else 'None':>20}\n" \
                                  f"Collision Longitude:    {self.data[1][1] if self.data[1][1] is not None else 'None':>20}\n"
        show_message_popup(airplane_status_message, height_hint=0.5, width_hint=0.5)
