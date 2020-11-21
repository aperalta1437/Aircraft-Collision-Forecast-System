from data_structures import AVLTree
from GUI.airport_marker import AirportMarker
from GUI.airplane_marker import AirplaneMarker
from kivy.app import App
from GUI.popups import show_loading_popup
from opensky_api import OpenSkyApi
import sqlite3


class DataManager:
    def __init__(self):
        self.app = App.get_running_app()
        self.progress_bar = show_loading_popup()

    def load_airports(self):
        self.airports_tree_manager = AVLTree(2)
        self.airports_tree = None

        airports_connection = sqlite3.connect("DATA\\global_airports.db")
        airports_cursor = airports_connection.cursor()

        airports_cursor.execute("SELECT * FROM AIRPORTS")
        airports = airports_cursor.fetchall()

        self.progress_bar.set_max(len(airports))

        self.progress_bar.set_stage_name('Loading airports...')

        for index in range(0, len(airports)):
            self.progress_bar.increment()
            if airports[index][self.airports_tree_manager.index] == r'N/A':
                continue
            self.airports_tree = self.airports_tree_manager.insert_node(self.airports_tree,
                                                                        AirportMarker(data=airports[index]))

    def load_airplanes(self):
        self.api = OpenSkyApi()
        self.airplanes_tree_manager = AVLTree(4)
        self.airplanes_tree = None

        self.progress_bar.set_stage_name('Requesting airplanes...')

        airplanes = self.api.get_states().states

        self.progress_bar.set_stage_name('Loading airplanes...')

        for airplane in airplanes:
            self.progress_bar.increment()
            curr_airplane = (airplane.baro_altitude, airplane.callsign, airplane.geo_altitude, airplane.heading,
                             airplane.icao24, airplane.last_contact, airplane.latitude, airplane.longitude,
                             airplane.on_ground, airplane.origin_country, airplane.position_source, airplane.sensors,
                             airplane.spi, airplane.squawk, airplane.time_position, airplane.velocity,
                             airplane.vertical_rate)
            self.airplanes_tree = self.airplanes_tree_manager.insert_node(self.airplanes_tree,
                                                                          AirplaneMarker(data=curr_airplane))