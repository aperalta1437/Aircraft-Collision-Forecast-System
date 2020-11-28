from kivy.app import App
import sqlite3
from kivy.properties import ObjectProperty
from GUI.modified_classes import NewFloatLayout
from GUI.popups import show_message_popup, show_question_popup
from GUI.data_manager import DataManager
from threading import Thread

class LoginView(NewFloatLayout):
    username_input = ObjectProperty(None)
    password_input = ObjectProperty(None)

    def __init__(self, window):
        self.login_window = window
        self.app = App.get_running_app()
        super(LoginView, self).__init__()

    def log_in(self):
        username = self.username_input.text
        password = self.password_input.text

        if username == '':
            show_message_popup('Username is required')
        else:
            users_connection = sqlite3.connect(r'DATA\AIRCRAFT_COLLISION_FORECAST_SYSTEM.db')
            users_cursor = users_connection.cursor()
            query = f"SELECT PASSWORD FROM USER_CREDENTIALS WHERE USERNAME = '{username}'"
            users_cursor.execute(query)
            result = users_cursor.fetchall()
            users_connection.close()

            if result == []:
                show_message_popup('Invalid username')
            else:
                if password == result[0][0]:
                    self.login_window.dismiss()
                    self.app.data_manager = DataManager(airport_id_index=2, airplane_id_index=4)
                    Thread(target=self.app.data_manager.load_airports).start()
                else:
                    show_message_popup('Invalid password')

    def close_app(self):
        def close_yes_or_no(flag):
            if flag:
                self.app.stop()
            else:
                popup_window.dismiss() # By the time this executes, popup_window will exists.

        popup_window = show_question_popup('Are you sure you want to quit?', condition_function=close_yes_or_no)


