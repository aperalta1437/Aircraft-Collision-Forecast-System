from kivy.app import App
import sqlite3
from kivy.properties import ObjectProperty
from GUI.modified_classes import NewFloatLayout
from GUI.popups import show_question_popup


class SettingsView(NewFloatLayout):
    btn_toggle_login_window = ObjectProperty(None)
    show_login_window = None

    def __init__(self, window):
        self.settings_window = window
        self.app = App.get_running_app()
        self.saved = True
        self.setting_connection = sqlite3.connect('DATA\\AIRCRAFT_COLLISION_FORECAST_SYSTEM.db')
        self.setting_cursor = self.setting_connection.cursor()

        super(SettingsView, self).__init__()

        query = f"SELECT STATE FROM SETTINGS WHERE NAME = 'SHOW LOGIN WINDOW';"
        self.setting_cursor.execute(query)
        self.show_login_window = (self.setting_cursor.fetchall())[0][0]

        self.btn_toggle_login_window.text = 'ON' if self.show_login_window == '1' else 'OFF'
        self.btn_toggle_login_window.state = 'down' if self.show_login_window == '1' else 'normal'

    def turn_login_window(self):

        self.saved = False

        if self.show_login_window == '1':
            query = f"UPDATE SETTINGS SET STATE = '0' WHERE NAME = 'SHOW LOGIN WINDOW';"
            self.btn_toggle_login_window.text = 'OFF'
        else:
            query = f"UPDATE SETTINGS SET STATE = '1' WHERE NAME = 'SHOW LOGIN WINDOW';"
            self.btn_toggle_login_window.text = 'ON'

        self.setting_cursor.execute(query)
        query = f"SELECT STATE FROM SETTINGS WHERE NAME = 'SHOW LOGIN WINDOW';"
        self.setting_cursor.execute(query)
        self.show_login_window = (self.setting_cursor.fetchall())[0][0]

    def save_settings(self):
        if not self.saved:
            query = f"COMMIT;"
            self.setting_cursor.execute(query)
            self.saved = True

    def close_window(self):
        if self.saved:
            self.setting_connection.close()
            self.settings_window.dismiss()
        else:
            def close_yes_or_no(flag):
                if flag:
                    self.setting_connection.close()
                    self.settings_window.dismiss()
                    popup_window.dismiss()          # By the time this executes, popup_window will exists.
                else:
                    popup_window.dismiss()  # By the time this executes, popup_window will exists.

            popup_window = show_question_popup('Settings have not been saved.\n' \
                                               'Are you sure you want to quit settings?', condition_function=close_yes_or_no)