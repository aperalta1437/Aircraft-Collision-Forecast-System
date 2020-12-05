from kivy_garden.mapview import MapMarkerPopup
from GUI.popups import show_message_popup
import sys

class AirportMarker(MapMarkerPopup):

    def __init__(self, data, **kwargs):
        super(AirportMarker, self).__init__()
        self.data = data
        self.lat = data[15]
        self.lon = data[16]

    def set_source(self, source):
        self.source = source

    def on_release(self):
        print(self.data)
        airplane_status_message = f"ICAO Code:          {self.data[0]:>20}\n" \
                                  f"IATA Code:          {self.data[1] if self.data[1] is not None else 'None':>20}\n" \
                                  f"Airport Name:       {self.data[2] if self.data[2] is not None else 'None':>20}\n" \
                                  f"City/Town:          {self.data[4] if self.data[4] is not None else 'None':>20}\n" \
                                  f"Country:            {self.data[5] if self.data[5] is not None else 'None':>20}\n" \
                                  f"Latitude Degrees:   {self.data[6] if self.data[6] is not None else 'None':>20}\n" \
                                  f"Latitude Minutes:   {self.data[7] if self.data[7] is not None else 'None':>20}\n" \
                                  f"Latitude Seconds:   {self.data[8] if self.data[8] is not None else 'None':>20}\n" \
                                  f"Latitude Direction: {self.data[9] if self.data[9] is not None else 'None':>20}\n" \
                                  f"Longitude Degrees:  {self.data[10] if self.data[10] is not None else 'None':>20}\n" \
                                  f"Longitude Minutes:  {self.data[11] if self.data[11] is not None else 'None':>20}\n" \
                                  f"Longitude Seconds:  {self.data[12] if self.data[12] is not None else 'None':>20}\n" \
                                  f"Longitude Direction:{self.data[13] if self.data[13] is not None else 'None':>20}\n" \
                                  f"Altitude:           {self.data[14] if self.data[14] is not None else 'None':>20}\n" \
                                  f"Lat Decimal Degrees:{self.data[15] if self.data[15] is not None else 'None':>20}\n" \
                                  f"Lon Decimal Degrees:{self.data[16] if self.data[16] is not None else 'None':>20}\n"
        show_message_popup(airplane_status_message, height_hint=0.75)

'''
import sqlite3
from data_structures import AVLTree

connection = sqlite3.connect("global_airports.db")

cursor = connection.cursor()

#cursor.execute("SELECT * FROM AIRPORTS WHERE NAME LIKE '%N/A%'")
cursor.execute("SELECT * FROM airports")

result = cursor.fetchall()
print(result)

tree = AVLTree(2)
root = None


for index in range(0, len(result)):
    if result[index][tree.index] == r'N/A':
        continue
    lat, lon = result[index][15], result[index][16]
    root = tree.insert_node(root, AirportMarker(data=list(result[index]), lat=lat, lon=lon))
    print(result[index][tree.index])
tree.printHelper(root, "", True)
'''