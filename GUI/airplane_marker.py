from kivy.app import App
from kivy_garden.mapview import MapMarkerPopup
from GUI.popups import show_message_popup
from threading import Thread

class AirplaneMarker(MapMarkerPopup):
    def __init__(self, data):
        super(AirplaneMarker, self).__init__()
        self.data = data
        self.lat = data[6]
        self.lon = data[7]

    def set_source(self, source):
        self.source = source

    def on_release(self):
        app = App.get_running_app()
        Thread(target=app.data_manager.get_potential_collisions, args=(app.data_manager.collision_forecaster.get_potential_collisions_from_plane, self.data[0],)).start()

        #potential_collisions = App.get_running_app().data_manager.collision_forecaster.get_potential_collisions_from_plane(
        #self.data[0])

        print(self.data[0])
        airplane_status_message =   f"ICAO 24:        {self.data[0]:>20}\n" \
                                    f"Baro Altitude:  {self.data[1] if self.data[1] is not None else 'None':>20}\n" \
                                    f"Call Sign:      {self.data[2] if self.data[2] is not None else 'None':>20}\n" \
                                    f"Geo Altitude:   {self.data[3] if self.data[3] is not None else 'None':>20}\n" \
                                    f"Heading:        {self.data[4] if self.data[4] is not None else 'None':>20}\n" \
                                    f"Last Contact:   {self.data[5] if self.data[5] is not None else 'None':>20}\n" \
                                    f"Latitude:       {self.data[6] if self.data[6] is not None else 'None':>20}\n" \
                                    f"Longitude:      {self.data[7] if self.data[7] is not None else 'None':>20}\n" \
                                    f"On Ground:      {self.data[8] if self.data[8] is not None else 'None':>20}\n" \
                                    f"Origin Country: {self.data[9] if self.data[9] is not None else 'None':>20}\n" \
                                    f"Position Source:{self.data[10] if self.data[10] is not None else 'None':>20}\n" \
                                    f"Sensors:        {self.data[11] if self.data[11] is not None else 'None':>20}\n" \
                                    f"SPI:            {self.data[12] if self.data[12] is not None else 'None':>20}\n" \
                                    f"Squawk:         {self.data[13] if self.data[13] is not None else 'None':>20}\n" \
                                    f"Time Position:  {self.data[14] if self.data[14] is not None else 'None':>20}\n" \
                                    f"Velocity:       {self.data[15] if self.data[15] is not None else 'None':>20}\n" \
                                    f"Vertical Rate:  {self.data[16] if self.data[16] is not None else 'None':>20}\n"
        show_message_popup(airplane_status_message, height_hint=0.75)