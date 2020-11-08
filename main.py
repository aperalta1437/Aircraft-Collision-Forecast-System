from kivy.core.window import Window
from kivymd.app import MDApp
from locations_mapview import LocationsMapView
import sqlite3
from kivy.uix.widget import Widget
from kivy.uix.layout import Layout
from kivy.uix.boxlayout import BoxLayout
from modified_classes import NewGridLayout
from modified_classes import NewFloatLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from popups import show_message_popup
from kivy.uix.modalview import ModalView
from login_view import LoginView


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


class MainApp(MDApp):
    airports_connection = None
    airports_cursor = None

    def build(self):
        return MainLayout()

    def on_start(self):
        # Config.set('graphics', 'width', '1050')
        # Config.set('graphics', 'height', '800')
        # Config.write()
        Window.clearcolor = (0, 0, 0, 1)
        Window.size = (1200, 800)
        self.airports_connection = sqlite3.connect("global_airports.db")
        self.airports_cursor = self.airports_connection.cursor()

        login_window = ModalView(size_hint=(None, None), size=(500, 400), auto_dismiss=False)
        login_window.add_widget(LoginView(login_window))
        login_window.open()


if __name__ == "__main__":
    MainApp().run()