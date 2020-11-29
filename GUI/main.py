from kivy.core.window import Window
from kivymd.app import MDApp
import sqlite3
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from GUI.popups import show_message_popup
from kivy.uix.modalview import ModalView
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from GUI.modified_classes import DataButton
from GUI.login_view import LoginView
from GUI.settings_view import SettingsView
from GUI.data_manager import DataManager
from threading import Thread
import os.path

# Program needs this to import LocationsMapView class (IGNORE INTERPRETER WARNING).
from GUI.locations_mapview import LocationsMapView


class MainLayout(Widget):
    btn_toggle_airports = ObjectProperty(None)          # Hold a reference to the "Show Airports" button after the graphics are rendered.
    btn_toggle_airplanes = ObjectProperty(None)         # Hold a reference to the "Show Airplanes" button after the graphics are rendered.
    locations_map = ObjectProperty(None)                # Hold a reference to the map after the graphics are rendered.
    airports_search_bar = ObjectProperty(None)          # Hold a reference to the airports search bar after the graphics are rendered.
    airplanes_search_bar = ObjectProperty(None)         # Hold a reference to the airplanes search bar after the graphics are rendered.

    def __init__(self):
        super(MainLayout, self).__init__()
        self.suggestions_dropdown = DropDown()          # Declare and initialize the suggestions drop-down object for both search bars.
        self.app = MDApp.get_running_app()              # Hold a reference to the main class which inherits from App to jump-start the app.

    def toggle_airports(self):
        """
        Allows to application to add the airports found within the field of view.
        :return: None
        """
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
        """
        Allows the application to add the airplanes found within the field of view.
        :return: None
        """
        if self.locations_map.show_airplanes:
            self.locations_map.show_airplanes = False
        else:
            if self.locations_map.zoom > 5:
                self.locations_map.show_airplanes = True
                self.locations_map.start_getting_locations_in_fov()
            else:
                self.btn_toggle_airplanes.state = 'normal'
                show_message_popup("Zoom level must be greater than 5.")

    def get_airport_suggestions(self):
        """
        Renders the airports suggestions as options within a drop-down menu
        based on the text given by the user within the airports search bar.
        :return: None
        """
        if not self.airports_search_bar.focus:      # If the function gets called after the user has chosen option,
            self.suggestions_dropdown.dismiss()         # hide drop-down.
            return
        else:                                       # else, if the function is called to select option,
            self.suggestions_dropdown.dismiss()         # hide previous drop-down.

        self.suggestions_dropdown = DropDown()

        airports_data = self.app.data_manager.airports_tree_manager.get_in_order_list(self.app.data_manager.airports_tree, self.airports_search_bar.text.upper())

        airport_id_index = self.app.data_manager.airports_tree_manager.index

        if airports_data is None:
            btn_suggestion = Button(text='NOT FOUND', size_hint_y=None, height=44)
            self.suggestions_dropdown.add_widget(btn_suggestion)
        else:
            for airport_data in airports_data:
                btn_suggestion = DataButton(data=airport_data, text=airport_data[airport_id_index], size_hint_y=None, height=44)
                btn_suggestion.bind(on_release=lambda btn_suggestion_ref: self.focus_on_airport(btn_suggestion_ref))
                self.suggestions_dropdown.add_widget(btn_suggestion)

        self.suggestions_dropdown.bind(on_select=lambda instance, btn_suggestion_ref: setattr(self.airports_search_bar, 'text', btn_suggestion_ref))
        self.suggestions_dropdown.open(self.airports_search_bar)
        self.airports_search_bar.bind(on_parent=self.suggestions_dropdown.dismiss)

    def focus_on_airport(self, btn_suggestion):
        """
        Focuses the map's current field of view on the chosen airport.
        :param btn_suggestion: The button carrying the airport's information.
        :return: None
        """
        self.suggestions_dropdown.select(btn_suggestion.text)
        self.locations_map.zoom = 8
        print(btn_suggestion.data)
        self.locations_map.center_on(btn_suggestion.data[15], btn_suggestion.data[16])
        self.airports_search_bar.focus = False
        self.locations_map.add_airport(btn_suggestion.data)

    def get_airplane_suggestions(self):
        """
        Renders the airplanes suggestions as options within a drop-down menu
        based on the text given by the user within the airplanes search bar.
        :return: None
        """
        if not self.airplanes_search_bar.focus:      # If the function gets called after the user has chosen option,
            self.suggestions_dropdown.dismiss()         # hide drop-down.
            return
        else:                                       # else, if the function is called to select option,
            self.suggestions_dropdown.dismiss()         # hide previous drop-down.

        self.suggestions_dropdown = DropDown()

        airplanes_data = self.app.data_manager.airplanes_tree_manager.get_in_order_list(self.app.data_manager.airplanes_tree, self.airplanes_search_bar.text.upper())

        airplane_id_index = self.app.data_manager.airplanes_tree_manager.index

        if airplanes_data is None:
            btn_suggestion = Button(text='NOT FOUND', size_hint_y=None, height=44)
            self.suggestions_dropdown.add_widget(btn_suggestion)
        else:
            for airplane_data in airplanes_data:
                btn_suggestion = DataButton(data=airplane_data, text=airplane_data[airplane_id_index], size_hint_y=None, height=44)
                btn_suggestion.bind(on_release=lambda btn_suggestion_ref: self.focus_on_airplane(btn_suggestion_ref))
                self.suggestions_dropdown.add_widget(btn_suggestion)

        self.suggestions_dropdown.bind(on_select=lambda instance, btn_suggestion_ref: setattr(self.airplanes_search_bar, 'text', btn_suggestion_ref))
        self.suggestions_dropdown.open(self.airplanes_search_bar)
        self.airplanes_search_bar.bind(on_parent=self.suggestions_dropdown.dismiss)

    def focus_on_airplane(self, btn_suggestion):
        """
        Focuses the map's current field of view on the chosen airplane.
        :param btn_suggestion: The button carrying the airplane's information.
        :return: None
        """
        self.suggestions_dropdown.select(btn_suggestion.text)
        self.locations_map.zoom = 8
        self.locations_map.center_on(btn_suggestion.data[6], btn_suggestion.data[7])
        self.airports_search_bar.focus = False
        self.locations_map.add_airplane(btn_suggestion.data)


    @staticmethod
    def open_settings_window():
        """
        Opens the settings window.
        :return: None
        """
        settings_window = ModalView(size_hint=(None, None), size=(500, 400), auto_dismiss=False)
        settings_window.add_widget(SettingsView(settings_window))
        settings_window.open()

    @staticmethod
    def close_app():
        """
        Cleans the airplanes database information and closes the application.
        :return: None
        """
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        db_path = os.path.join(BASE_DIR, "..", "DATA", "AIRCRAFT_COLLISION_FORECAST_SYSTEM.db")
        db_connection = sqlite3.connect(db_path)
        db_cursor = db_connection.cursor()
        query = f"DELETE FROM AIRPLANES"
        db_cursor.execute(query)
        db_connection.close()

        MDApp.get_running_app().stop()


class MainApp(MDApp):
    airports_connection = None
    airports_cursor = None
    data_manager = None

    def build(self):
        """
        Builds the application main layout.
        :return: The application's main layout.
        """
        self.main_layout = MainLayout()
        return self.main_layout

    def on_start(self):
        """
        Sets the main window's size, opens airports database connection, decides to render the login window
        based on the saved settings, and initializes the data manager once the application starts.
        :return: None
        """
        # Config.set('graphics', 'width', '1050')
        # Config.set('graphics', 'height', '800')
        # Config.write()
        Window.clearcolor = (0, 0, 0, 1)
        Window.size = (1200, 800)
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        db_path = os.path.join(BASE_DIR, "..", "DATA", "global_airports.db")
        self.airports_connection = sqlite3.connect(db_path)
        self.airports_cursor = self.airports_connection.cursor()

        db_path = os.path.join(BASE_DIR, "..", "DATA", "AIRCRAFT_COLLISION_FORECAST_SYSTEM.db")
        settings_connection = sqlite3.connect(db_path)

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
            self.data_manager = DataManager(airport_id_index=2, airplane_id_index=0)
            Thread(target=self.data_manager.load_airports).start()


if __name__ == "__main__":
    MainApp().run()
