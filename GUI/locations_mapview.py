from kivy_garden.mapview import MapView
from kivy.clock import Clock
from kivy.app import App
import DATA.database_manager as db_manager


class LocationsMapView(MapView):
    getting_locations_timer = None
    show_airports = False
    show_airplanes = False
    on_map_airports_ids = {}
    on_map_airplanes_ids = {}
    visible_airports_ids = []
    visible_airplanes_ids = []
    markers_on_map = []
    airport_id_index = None  # This will be set by the data manager.
    airplane_id_index = None  # This will be set by the data manager.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

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

        if self.show_airports:
            self.visible_airports_ids = []
            query = "SELECT * FROM airports WHERE  LAT_DECIMAL > {min_lat:f} AND LAT_DECIMAL < {max_lat:f} " \
                    "AND LON_DECIMAL > {min_lon:f} AND LON_DECIMAL < {max_lon:f}".format(
                        min_lat=min_lat, max_lat=max_lat, min_lon=min_lon, max_lon=max_lon)
            # sql_statement = "SELECT * FROM SQLITE_MASTER"
            self.app.airports_cursor.execute(query)
            airports = self.app.airports_cursor.fetchall()
            print(len(airports))
            print(self.get_bbox())
            print(airports)

            for airport in airports:
                if airport[0] in self.on_map_airports_ids or airport[self.airport_id_index] == 'N/A':
                    self.visible_airports_ids.append(airport[0])
                    continue
                else:
                    self.add_airport(airport)
                    print(airport)

            for airport_key in self.on_map_airports_ids.copy():
                if airport_key not in self.visible_airports_ids:
                    self.remove_widget(self.on_map_airports_ids[airport_key])
                    del self.on_map_airports_ids[airport_key]

        else:
            for airport_key in self.on_map_airports_ids:
                self.remove_widget(self.on_map_airports_ids[airport_key])
            else:
                self.on_map_airports_ids = {}

        if self.show_airplanes:
            self.visible_airplanes_ids = []
            query = "SELECT * FROM AIRPLANES WHERE LATITUDE > {min_lat:f} AND LATITUDE < {max_lat:f} " \
                    "AND LONGITUDE > {min_lon:f} AND LONGITUDE < {max_lon:f}".format(
                        min_lat=min_lat, max_lat=max_lat, min_lon=min_lon, max_lon=max_lon)
            airplanes = db_manager.execute_query(query, db_file_name=r'DATA\AIRCRAFT_COLLISION_FORECAST_SYSTEM.db')

            for airplane in airplanes:
                if airplane[self.airplane_id_index] in self.on_map_airplanes_ids:
                    self.visible_airplanes_ids.append(airplane[self.airplane_id_index])
                    continue
                else:
                    self.add_airplane(airplane)
                    print(airplane)

            for airplane_key in self.on_map_airplanes_ids.copy():
                if airplane_key not in self.visible_airplanes_ids:
                    self.remove_widget(self.on_map_airplanes_ids[airplane_key])
                    del self.on_map_airplanes_ids[airplane_key]

        else:
            for airplane_key in self.on_map_airplanes_ids:
                self.remove_widget(self.on_map_airplanes_ids[airplane_key])
            else:
                self.on_map_airplanes_ids = {}

    def add_airport(self, airport):
        marker = self.app.data_manager.airports_tree_manager.get_node(self.app.data_manager.airports_tree, airport[
            self.airport_id_index]).key  # Creates the marker.

        marker.set_source(r'IMAGE\map_marker.png')
        self.add_widget(marker)  # Add the marker to the map.

        self.on_map_airports_ids[airport[0]] = marker  # Keep track of all airports on the map.
        self.visible_airports_ids.append(airport[0])  # Keep track of the visible airports.

    def add_airplane(self, airplane):
        marker = self.app.data_manager.airplanes_tree_manager.get_node(self.app.data_manager.airplanes_tree, airplane[
            self.airplane_id_index]).key  # Creates the marker.

        marker.set_source(r'IMAGE\airplane_marker.png')
        self.add_widget(marker)  # Add the marker to the map.

        self.on_map_airplanes_ids[airplane[self.airplane_id_index]] = marker    # Keep track of all airplanes on the map.
        self.visible_airplanes_ids.append(airplane[self.airplane_id_index])     # Keep track of the visible airplanes on the map.

    def increment_zoom(self):
        self.zoom += 1

    def decrement_zoom(self):
        self.zoom -= 1
