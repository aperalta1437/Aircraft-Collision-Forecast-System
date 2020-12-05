from kivymd.uix.dialog import ListMDDialog

class AirplanePopupMenu(ListMDDialog):

    def __init__(self, airplane_data):
        super(AirplanePopupMenu, self).__init__()
        # Set all of the fields of airplane data.
