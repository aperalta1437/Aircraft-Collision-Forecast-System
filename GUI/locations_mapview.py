from kivy_garden.mapview import MapView
from kivy.clock import Clock
from kivy.app import App
from GUI.airport_marker import AirportMarker


class LocationsMapView(MapView):
    getting_locations_timer = None
    show_airports = False
    show_airplanes = False
    visible_airports_ids = []
    markers_on_map = []

    def start_getting_locations_in_fov(self):
        # After one second, get markers in field of view.
        try:
            self.getting_locations_timer.cancel()
        except:
            pass
        self.getting_locations_timer = Clock.schedule_once(self.get_locations_in_fov, 1)

    def get_locations_in_fov(self, *args):
        if self.zoom <= 5:
            return

        min_lat, min_lon, max_lat, max_lon = self.get_bbox()

        print(self.show_airports)
        print(self.show_airplanes)
        print(self.zoom)

        app = App.get_running_app()
        query = "SELECT * FROM airports WHERE  LAT_DECIMAL > {min_lat:f} AND LAT_DECIMAL < {max_lat:f} " \
                        "AND LON_DECIMAL > {min_lon:f} AND LON_DECIMAL < {max_lon:f}".format(
            min_lat=min_lat, max_lat=max_lat, min_lon=min_lon, max_lon=max_lon)
        # sql_statement = "SELECT * FROM SQLITE_MASTER"
        app.airports_cursor.execute(query)
        airports = app.airports_cursor.fetchall()
        print(len(airports))
        print(self.get_bbox())
        print(airports)

        if self.show_airports:
            for airport in airports:
                if airport[0] in self.visible_airports_ids:
                    continue
                else:
                    self.add_airport(airport)

    def add_airport(self, airport):
        lat, lon = airport[15], airport[16]                                     # Get the marker position.

        marker = AirportMarker(airport, lat=lat, lon=lon)       # Creates the marker.

        self.add_widget(marker)                                 # Add the marker to the map.

        self.visible_airports_ids.append(airport[0])                            # Keep track of the visible airplanes.