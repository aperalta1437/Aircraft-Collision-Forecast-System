from opensky_api import OpenSkyApi
api = OpenSkyApi()
print('--->')
s = api.get_states()
print(s.states[0].time_position)

# from kivy.app import App
# from kivy.uix.button import Button
#
# class TestApp(App):
#     def build(self):
#         return Button(text='Hello World')
#
# TestApp().run()