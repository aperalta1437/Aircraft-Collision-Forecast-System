from kivy_garden.mapview import MapMarkerPopup
import sys

class AirportMarker(MapMarkerPopup):
    source = 'map_marker.png'

    def __init__(self, data, lat, lon):
        super(AirportMarker, self).__init__()
        self.data = data
        self.lat = lat
        self.lon = lon

    def on_release(self):
        # Open up the LocationsPopupMenu
        pass

'''
import sqlite3
from data_structures import AVLTree

connection = sqlite3.connect("global_airports.db")

cursor = connection.cursor()

#cursor.execute("SELECT * FROM AIRPORTS WHERE NAME LIKE '%N/A%'")
cursor.execute("SELECT * FROM airports")

result = cursor.fetchall()


tree = AVLTree(2)
root = None


for index in range(0, len(result)):
    lat, lon = result[index][15], result[index][16]
    root = tree.insert_node(root, AirportMarker(data=list(result[index]), lat=lat, lon=lon))
    print(index)
tree.printHelper(root, "", True)
'''





