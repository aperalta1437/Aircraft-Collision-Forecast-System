import time

from kivy.clock import Clock
from data_structures import AVLTree
from GUI.airport_marker import AirportMarker
from GUI.airplane_marker import AirplaneMarker
from kivy.app import App
from GUI.popups import show_loading_popup
from opensky_api import OpenSkyApi
import sqlite3
from threading import Thread
from aircraftdata import AircraftData
import DATA.database_manager as db_manager
import os.path

class DataManager:
    def __init__(self, airport_id_index, airplane_id_index, username=None, password=None):
        self.app = App.get_running_app()

        self.airport_id_index = airport_id_index
        self.airplane_id_index = airplane_id_index

        self.progress_bar = show_loading_popup()

        self.airports_tree_manager = AVLTree(self.airport_id_index)
        self.airports_tree = None

        # Set the airport id's index on the mapview object to increment performance.
        self.app.main_layout.locations_map.airport_id_index = airport_id_index
        # Set the airplane id's index on the mapview object to increment performance.
        self.app.main_layout.locations_map.airplane_id_index = airplane_id_index

        self.api = AircraftData().get_instance(username=username, password=password)
        self.airplanes_tree_manager = AVLTree(self.airplane_id_index)
        self.airplanes_tree = None

    def load_airports(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "..", "DATA", "global_airports.db")
        airports_connection = sqlite3.connect(db_path)
        airports_cursor = airports_connection.cursor()

        airports_cursor.execute("SELECT * FROM AIRPORTS")
        airports = airports_cursor.fetchall()

        self.progress_bar.set_max(len(airports))

        self.progress_bar.set_stage_name('Loading airports...')

        for index in range(0, len(airports)):
            self.progress_bar.increment()

            if airports[index][self.airport_id_index] == r'N/A' or \
                    airports[index][15] == 0.0 or airports[index][16] == 0.0:
                continue
            self.airports_tree = self.airports_tree_manager.insert_node(self.airports_tree,
                                                                        AirportMarker(data=airports[index]))

        airports_connection.close()

        Thread(target=self.load_airplanes).start()

    def load_airplanes(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "..", "DATA", "AIRCRAFT_COLLISION_FORECAST_SYSTEM.db")

        db_manager.clean_table(db_path, 'AIRPLANES')

        airplanes = self.api.get_states().states

        print('Requested Airplanes')

        db_manager.open_db_connection(db_path)

        for airplane in airplanes:
            curr_airplane = (airplane.icao24, airplane.baro_altitude, airplane.callsign, airplane.geo_altitude,
                             airplane.heading, airplane.last_contact, airplane.latitude, airplane.longitude,
                             airplane.on_ground, airplane.origin_country, airplane.position_source, airplane.sensors,
                             airplane.spi, airplane.squawk, airplane.time_position, airplane.velocity,
                             airplane.vertical_rate)
            if curr_airplane[0] is None or curr_airplane[6] is None or curr_airplane[7] is None:
                continue

            db_manager.insert_row('AIRPLANES', is_open=True,
                                  ICAO24=f'"{curr_airplane[0]}"',
                                  BARO_ALTITUDE=(curr_airplane[1] if curr_airplane[1] is not None else 'NULL'),
                                  CALLSIGN=(f'"{curr_airplane[2]}"' if curr_airplane[2] is not None else 'NULL'),
                                  GEO_ALTITUDE=(curr_airplane[3] if curr_airplane[3] is not None else 'NULL'),
                                  HEADING=(curr_airplane[4] if curr_airplane[4] is not None else 'NULL'),
                                  LAST_CONTACT=(curr_airplane[5] if curr_airplane[5] is not None else 'NULL'),
                                  LATITUDE=(curr_airplane[6] if curr_airplane[6] is not None else 'NULL'),
                                  LONGITUDE=(curr_airplane[7] if curr_airplane[7] is not None else 'NULL'),
                                  ON_GROUND=(0 if not curr_airplane[8] else 1),
                                  ORIGIN_COUNTRY=(f'"{curr_airplane[9]}"' if curr_airplane[9] is not None else 'NULL'),
                                  POSITION_SOURCE=(curr_airplane[10] if curr_airplane[10] is not None else 'NULL'),
                                  SENSORS=(f'"{curr_airplane[11]}"' if curr_airplane[11] is not None else 'NULL'),
                                  SPI=(0 if not curr_airplane[12] else 1),
                                  SQUAWK=(f'"{curr_airplane[13]}"' if curr_airplane[13] is not None else 'NULL'),
                                  TIME_POSITION=(curr_airplane[14] if curr_airplane[14] is not None else 'NULL'),
                                  VELOCITY=(curr_airplane[15] if curr_airplane[15] is not None else 'NULL'),
                                  VERTICAL_RATE=(curr_airplane[16] if curr_airplane[16] is not None else 'NULL'))

            self.airplanes_tree = self.airplanes_tree_manager.insert_node(self.airplanes_tree,
                                                                          AirplaneMarker(data=curr_airplane))

        db_manager.close_db_connection()

        print('Airplanes Done')

        time.sleep(15)
        self.update_airplanes()

    def update_airplanes(self):

        stored_airplanes = db_manager.select_data('AIRPLANES', r'DATA\AIRCRAFT_COLLISION_FORECAST_SYSTEM.db', False,
                                                  'ICAO24')
        stored_airplanes = [row[0] for row in stored_airplanes]

        print(stored_airplanes)

        airplanes = self.api.get_states().states

        print('Received Airplanes to Update')

        db_manager.open_db_connection(r'DATA\AIRCRAFT_COLLISION_FORECAST_SYSTEM.db')

        for airplane in airplanes:
            curr_airplane = (airplane.icao24, airplane.baro_altitude, airplane.callsign, airplane.geo_altitude,
                             airplane.heading, airplane.last_contact, airplane.latitude, airplane.longitude,
                             airplane.on_ground, airplane.origin_country, airplane.position_source, airplane.sensors,
                             airplane.spi, airplane.squawk, airplane.time_position, airplane.velocity,
                             airplane.vertical_rate)

            if curr_airplane[0] in stored_airplanes:
                db_manager.update_data('AIRPLANES', is_open=True, SET={
                    'BARO_ALTITUDE': (curr_airplane[1] if curr_airplane[1] is not None else 'NULL'),
                    'CALLSIGN': (f'"{curr_airplane[2]}"' if curr_airplane[2] is not None else 'NULL'),
                    'GEO_ALTITUDE': (curr_airplane[3] if curr_airplane[3] is not None else 'NULL'),
                    'HEADING': (curr_airplane[4] if curr_airplane[4] is not None else 'NULL'),
                    'LAST_CONTACT': (curr_airplane[5] if curr_airplane[5] is not None else 'NULL'),
                    'LATITUDE': (curr_airplane[6] if curr_airplane[6] is not None else 'NULL'),
                    'LONGITUDE': (curr_airplane[7] if curr_airplane[7] is not None else 'NULL'),
                    'ON_GROUND': (0 if not curr_airplane[8] else 1),
                    'ORIGIN_COUNTRY': (f'"{curr_airplane[9]}"' if curr_airplane[9] is not None else 'NULL'),
                    'POSITION_SOURCE': (curr_airplane[10] if curr_airplane[10] is not None else 'NULL'),
                    'SENSORS': (f'"{curr_airplane[11]}"' if curr_airplane[11] is not None else 'NULL'),
                    'SPI': (0 if not curr_airplane[12] else 1),
                    'SQUAWK': (f'"{curr_airplane[13]}"' if curr_airplane[13] is not None else 'NULL'),
                    'TIME_POSITION': (curr_airplane[14] if curr_airplane[14] is not None else 'NULL'),
                    'VELOCITY': (curr_airplane[15] if curr_airplane[15] is not None else 'NULL'),
                    'VERTICAL_RATE': (curr_airplane[16] if curr_airplane[16] is not None else 'NULL')},
                                       WHERE={'ICAO24': f'"{curr_airplane[0]}"'})

                self.airplanes_tree_manager.update_node(self.airplanes_tree, data=curr_airplane)

                stored_airplanes.remove(curr_airplane[0])
            else:
                if curr_airplane[0] is None or curr_airplane[6] is None or curr_airplane[7] is None:
                    continue

                print(curr_airplane[0])
                db_manager.insert_row('AIRPLANES', is_open=True,
                                      ICAO24=f'"{curr_airplane[0]}"',
                                      BARO_ALTITUDE=(curr_airplane[1] if curr_airplane[1] is not None else 'NULL'),
                                      CALLSIGN=(f'"{curr_airplane[2]}"' if curr_airplane[2] is not None else 'NULL'),
                                      GEO_ALTITUDE=(curr_airplane[3] if curr_airplane[3] is not None else 'NULL'),
                                      HEADING=(curr_airplane[4] if curr_airplane[4] is not None else 'NULL'),
                                      LAST_CONTACT=(curr_airplane[5] if curr_airplane[5] is not None else 'NULL'),
                                      LATITUDE=(curr_airplane[6] if curr_airplane[6] is not None else 'NULL'),
                                      LONGITUDE=(curr_airplane[7] if curr_airplane[7] is not None else 'NULL'),
                                      ON_GROUND=(0 if not curr_airplane[8] else 1),
                                      ORIGIN_COUNTRY=(
                                          f'"{curr_airplane[9]}"' if curr_airplane[9] is not None else 'NULL'),
                                      POSITION_SOURCE=(curr_airplane[10] if curr_airplane[10] is not None else 'NULL'),
                                      SENSORS=(f'"{curr_airplane[11]}"' if curr_airplane[11] is not None else 'NULL'),
                                      SPI=(0 if not curr_airplane[12] else 1),
                                      SQUAWK=(f'"{curr_airplane[13]}"' if curr_airplane[13] is not None else 'NULL'),
                                      TIME_POSITION=(curr_airplane[14] if curr_airplane[14] is not None else 'NULL'),
                                      VELOCITY=(curr_airplane[15] if curr_airplane[15] is not None else 'NULL'),
                                      VERTICAL_RATE=(curr_airplane[16] if curr_airplane[16] is not None else 'NULL'))

                self.airplanes_tree = self.airplanes_tree_manager.insert_node(self.airplanes_tree,
                                                                              AirplaneMarker(data=curr_airplane))

        for airplane_icao_24 in stored_airplanes:
            db_manager.delete_data('AIRPLANES', is_open=True, ICAO24=f'"{airplane_icao_24}"')
            self.airports_tree_manager.delete_node(self.airplanes_tree, airplane_icao_24)


        db_manager.close_db_connection()

        #Clock.schedule_once(self.update_airplanes, 30)

        print('Airplanes Done')

        self.app.main_layout.locations_map.refresh_airplanes_in_fov(updated=True)
        time.sleep(15)
        Thread(target=self.update_airplanes, daemon=True).start()
