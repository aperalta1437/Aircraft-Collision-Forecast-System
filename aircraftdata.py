import kivy
from opensky_api import OpenSkyApi
api = OpenSkyApi()
states = api.get_states()
print(len(states.states))
# for state in states.states:
#     print(state)