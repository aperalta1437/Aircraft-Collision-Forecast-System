from kivy_garden.mapview import MapView
from kivy.clock import Clock
from kivy.app import App
import DATA.database_manager as db_manager
from PIL import Image
from GUI.airplane_marker import AirplaneMarker
from GUI.collision_marker import CollisionMarker
import sqlite3


class LocationsMapView(MapView):
    getting_locations_timer = None
    show_airports = False
    show_airplanes = False
    focus_on_airport = False
    focus_on_airplane = False
    on_map_airports_ids = {}
    on_map_airplanes_ids = {}
    on_map_collisions_ids = {}
    visible_airports_ids = []
    visible_airplanes_ids = []
    visible_collisions_ids = []
    airport_id_index = None  # This will be set by the data manager.
    airplane_id_index = None  # This will be set by the data manager.
    potential_collisions = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

    def start_getting_locations_in_fov(self):
        # This is needed to avoid further execution of code when the login window is enable.
        if not self.app.data_manager:               # If data manger object has not been created,
            return                                      # return without getting locations in field of view.

        # After one second, get markers in field of view.
        try:
            self.getting_locations_timer.cancel()
        except:
            pass
        self.getting_locations_timer = Clock.schedule_once(self.get_locations_in_fov, 1)

    def get_locations_in_fov(self, *args, airport_focus=False, airplane_focus=False):
        if self.zoom <= 5:
            self.focus_on_airport = False
            self.focus_on_airplane = False

        min_lat, min_lon, max_lat, max_lon = self.get_bbox()

        # print(self.show_airports)
        # print(self.show_airplanes)
        # print(self.zoom)

        self.visible_airports_ids = []
        query = "SELECT * FROM airports WHERE  LAT_DECIMAL > {min_lat:f} AND LAT_DECIMAL < {max_lat:f} " \
                "AND LON_DECIMAL > {min_lon:f} AND LON_DECIMAL < {max_lon:f}".format(
                    min_lat=min_lat, max_lat=max_lat, min_lon=min_lon, max_lon=max_lon)
        # sql_statement = "SELECT * FROM SQLITE_MASTER"
        # self.app.airports_cursor.execute(query)
        airports = db_manager.execute_query(query, db_file_name=r'DATA\global_airports.db')

        self.visible_airports_ids = [airport_in_fov[0] for airport_in_fov in airports]

        if (self.show_airports or airport_focus) and (self.zoom > 5):
            # print(len(airports))
            # print(self.get_bbox())
            # print(airports)

            for airport in airports:
                if airport[0] in self.on_map_airports_ids or airport[self.airport_id_index] == 'N/A':
                    continue
                else:
                    self.add_airport(airport)
                    print(airport)

            self.refresh_airports_in_fov()

        else:
            if self.focus_on_airport:
                self.refresh_airports_in_fov()
            else:
                self.remove_airports()

        self.visible_airplanes_ids = []
        query = "SELECT * FROM AIRPLANES WHERE LATITUDE > {min_lat:f} AND LATITUDE < {max_lat:f} " \
                "AND LONGITUDE > {min_lon:f} AND LONGITUDE < {max_lon:f}".format(
                    min_lat=min_lat, max_lat=max_lat, min_lon=min_lon, max_lon=max_lon)
        airplanes = db_manager.execute_query(query, db_file_name=r'DATA\AIRCRAFT_COLLISION_FORECAST_SYSTEM.db')

        self.visible_airplanes_ids = [airplane_in_fov[self.airplane_id_index] for airplane_in_fov in airplanes]

        if (self.show_airplanes or airplane_focus) and self.zoom > 5:
            for airplane in airplanes:
                if airplane[self.airplane_id_index] in self.on_map_airplanes_ids:
                    continue
                else:
                    self.add_airplane(airplane)
                    #print(airplane)

            self.refresh_airplanes_in_fov()

        else:
            if self.focus_on_airplane:
                self.refresh_airplanes_in_fov()
            else:
                self.remove_airplanes()

        if self.potential_collisions and self.zoom > 5:
            for collision in self.potential_collisions:
                self.add_collision(collision)
        else:
            self.remove_collisions()

        self.potential_collisions = None

    def refresh_airports_in_fov(self):
        for airport_key in self.on_map_airports_ids.copy():
            if airport_key not in self.visible_airports_ids:
                self.remove_widget(self.on_map_airports_ids[airport_key])
                del self.on_map_airports_ids[airport_key]
        else:
            if len(self.on_map_airports_ids) == 0:
                self.focus_on_airport = False

    def refresh_airplanes_in_fov(self, updated=False):
        if updated:
           db_manager.open_db_connection(db_file_name=r'DATA\AIRCRAFT_COLLISION_FORECAST_SYSTEM.db')

        for airplane_key in self.on_map_airplanes_ids.copy():
            if airplane_key not in self.visible_airplanes_ids:
                self.remove_widget(self.on_map_airplanes_ids[airplane_key])
                del self.on_map_airplanes_ids[airplane_key]
            else:
                if updated:
                    updated_airplane = db_manager.select_data('AIRPLANES', is_open=True, ICAO24=f'"{airplane_key}"')
                    #print(updated_airplane)
                    self.remove_widget(self.on_map_airplanes_ids[airplane_key])
                    try:
                        self.add_airplane(updated_airplane[0])
                    except IndexError:                 # If the airplane is no longer in the field of view, just ignore.
                        pass
        else:
            if len(self.on_map_airplanes_ids) == 0:
                self.focus_on_airplane = False
            if updated:
                db_manager.close_db_connection()

    def remove_airports(self):
        for airport_key in self.on_map_airports_ids:
            self.remove_widget(self.on_map_airports_ids[airport_key])
        else:
            self.on_map_airports_ids = {}

    def remove_collisions(self):
        for collision_key in self.on_map_collisions_ids:
            self.remove_widget(self.on_map_collisions_ids[collision_key])
        else:
            self.on_map_collisions_ids = {}

    def remove_airplanes(self):
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

    def add_airplane(self, airplane):

        #marker = self.app.data_manager.airplanes_tree_manager.get_node(self.app.data_manager.airplanes_tree, airplane[
        #    self.airplane_id_index]).key  # Creates the marker.
        marker = AirplaneMarker(airplane)

        img = Image.open(r'GUI\IMAGE\airplane_marker.png')

        rotated_img = img.rotate(-1 * airplane[4], resample=Image.BICUBIC, expand=True)

        rotated_img.save(r'GUI\IMAGE\{icao24:s}_airplane_marker.png'.format(icao24=airplane[0]))

        marker.set_source(r'IMAGE\{icao24:s}_airplane_marker.png'.format(icao24=airplane[0]))
        self.add_widget(marker)  # Add the marker to the map.

        self.on_map_airplanes_ids[airplane[self.airplane_id_index]] = marker    # Keep track of all airplanes on the map.

    def add_collision(self, collision):
        marker = CollisionMarker(collision)

        img = Image.open(r'GUI\IMAGE\collision_marker.png')
        img.save(r'GUI\IMAGE\{icao24:s}_collision_marker.png'.format(icao24=collision[0]))
        marker.set_source(r'IMAGE\{icao24:s}_collision_marker.png'.format(icao24=collision[0]))
        self.add_widget(marker)

        self.on_map_collisions_ids[collision[0]] = marker


    def increment_zoom(self):
        self.zoom += 1

    def decrement_zoom(self):
        self.zoom -= 1
