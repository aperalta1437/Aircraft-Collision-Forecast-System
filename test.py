from opensky_api import OpenSkyApi
api = OpenSkyApi()
s = api.get_states().states

print(s[0])


'''
1. Install in interpreter
2. Re-apply interpreter
'''