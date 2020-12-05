from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from config import Config
from kivy.app import App
from GUI.modified_classes import NewGridLayout
from GUI.modified_classes import NewBoxLayout

class SettingsPanelView(NewBoxLayout):
    config = Config.get_instance()

    predict_time = ObjectProperty(None)
    altitude_range = ObjectProperty(None)

    ap_bbox_min_lat = ObjectProperty(None)
    ap_bbox_max_lat = ObjectProperty(None)
    ap_bbox_min_long = ObjectProperty(None)
    ap_bbox_max_long = ObjectProperty(None)

    ac_bbox_min_lat = ObjectProperty(None)
    ac_bbox_max_lat = ObjectProperty(None)
    ac_bbox_min_long = ObjectProperty(None)
    ac_bbox_max_long = ObjectProperty(None)

    c_bbox_min_lat = ObjectProperty(None)
    c_bbox_max_lat = ObjectProperty(None)
    c_bbox_min_long = ObjectProperty(None)
    c_bbox_max_long = ObjectProperty(None)

    airport_bbox = config.get_airport_bbox_settings()
    aircraft_bbox = config.get_airplane_bbox_settings()
    collision_bbox = config.get_collision_bbox_settings()

    def __init__(self, **kwargs):
        super(SettingsPanelView, self).__init__(**kwargs)

    def load_settings(self):

        self.predict_time.text = str(self.config.get_predict_time())
        self.altitude_range.text = str(self.config.get_altitude_range())

        self.ap_bbox_min_lat.text = str(self.airport_bbox[0])
        self.ap_bbox_max_lat.text = str(self.airport_bbox[1])
        self.ap_bbox_min_long.text = str(self.airport_bbox[2])
        self.ap_bbox_max_long.text = str(self.airport_bbox[3])

        self.ac_bbox_min_lat.text = str(self.aircraft_bbox[0])
        self.ac_bbox_max_lat.text = str(self.aircraft_bbox[1])
        self.ac_bbox_min_long.text = str(self.aircraft_bbox[2])
        self.ac_bbox_max_long.text = str(self.aircraft_bbox[3])

        self.c_bbox_min_lat.text = str(self.collision_bbox[0])
        self.c_bbox_max_lat.text = str(self.collision_bbox[1])
        self.c_bbox_min_long.text = str(self.collision_bbox[2])
        self.c_bbox_max_long.text = str(self.collision_bbox[3])

    def apply_btn(self):
        self.config.set_predict_time(float(self.predict_time.text))
        self.config.set_airport_bbox_settings((float(self.ap_bbox_min_lat.text), float(self.ap_bbox_max_lat.text), float(self.ap_bbox_min_long.text), float(self.ap_bbox_max_long.text)))
        self.config.set_airplane_bbox_settings((float(self.ac_bbox_min_lat.text), float(self.ac_bbox_max_lat.text), float(self.ac_bbox_min_long.text), float(self.ac_bbox_max_long.text)))
        self.config.set_collision_bbox_settings((float(self.c_bbox_min_lat.text), float(self.c_bbox_max_lat.text), float(self.c_bbox_min_long.text), float(self.c_bbox_max_long.text)))
        self.config.set_altitude_range(float(self.altitude_range.text))
        print("{}, {}, {}, {}, {}".format(self.config.get_predict_time(), self.config.get_airport_bbox_settings(), self.config.get_airplane_bbox_settings(), self.config.get_collision_bbox_settings(), self.config.get_altitude_range()))


class Settings_Panel_View(App):
    def build(self):
        test = SettingsPanelView()
        test.load_settings()
        return test

if __name__ == "__main__":
    Settings_Panel_View().run()