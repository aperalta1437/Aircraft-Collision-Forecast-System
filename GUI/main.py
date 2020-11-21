from kivy.core.window import Window
from kivymd.app import MDApp
import sqlite3
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from GUI.popups import show_message_popup
from kivy.uix.modalview import ModalView
from GUI.login_view import LoginView
from GUI.settings_view import SettingsView
from GUI.data_manager import DataManager
from threading import Thread
from GUI.locations_mapview import LocationsMapView

# import kivy
# kivy.require('1.9.0')
# from kivy.config import Config


class MainLayout(Widget):
    btn_toggle_airports = ObjectProperty(None)
    btn_toggle_airplanes = ObjectProperty(None)
    locations_map = ObjectProperty(None)

    def toggle_airports(self):
        if self.locations_map.show_airports:
            self.locations_map.show_airports = False
        else:
            if self.locations_map.zoom > 5:
                self.locations_map.show_airports = True
                self.locations_map.start_getting_locations_in_fov()
            else:
                self.btn_toggle_airports.state = 'normal'
                show_message_popup("Zoom level must be greater than 5.")


    def toggle_airplanes(self):
        if self.locations_map.show_airplanes:
            self.locations_map.show_airplanes = False
        else:
            if self.locations_map.zoom > 5:
                self.locations_map.show_airplanes = True
                self.locations_map.start_getting_locations_in_fov()
            else:
                self.btn_toggle_airplanes.state = 'normal'
                show_message_popup("Zoom level must be greater than 5.")

    def open_settings_window(self):
        settings_window = ModalView(size_hint=(None, None), size=(500, 400), auto_dismiss=False)
        settings_window.add_widget(SettingsView(settings_window))
        settings_window.open()

    def close_app(self):
        MDApp.get_running_app().stop()


class MainApp(MDApp):
    airports_connection = None
    airports_cursor = None
    data_manager = None

    def build(self):
        return MainLayout()

    def on_start(self):
        # Config.set('graphics', 'width', '1050')
        # Config.set('graphics', 'height', '800')
        # Config.write()
        Window.clearcolor = (0,0,0,1)
        Window.size = (1200, 800)
        self.airports_connection = sqlite3.connect("DATA\\global_airports.db")
        self.airports_cursor = self.airports_connection.cursor()

        settings_connection = sqlite3.connect('DATA\\AIRCRAFT_COLLISION_FORECAST_SYSTEM.db')
        settings_cursor = settings_connection.cursor()
        query = f"SELECT STATE FROM SETTINGS WHERE NAME = 'SHOW LOGIN WINDOW'"
        settings_cursor.execute(query)
        result = settings_cursor.fetchall()
        settings_connection.close()

        if result[0][0] == '1':
            login_window = ModalView(size_hint=(None, None), size=(500, 400), auto_dismiss=False)
            login_window.add_widget(LoginView(login_window))
            login_window.open()
        else:
            # progress_bar = show_loading_popup(2)
            #
            # progress_bar.increment()
            # progress_bar.set_stage_name('Loading Airports...')
            self.data_manager = DataManager()
            #Clock.schedule_once(self.set_data_manager, 2)
            Thread(target=self.data_manager.load_airports).start()





if __name__ == "__main__":
    MainApp().run()