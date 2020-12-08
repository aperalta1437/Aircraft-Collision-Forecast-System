class Config:
    __singletonConfig = None

    """
    Singleton Implementation taken from:
    https://www.tutorialspoint.com/python_design_patterns/python_design_patterns_singleton.htm
    """

    @staticmethod
    def get_instance():
        if Config.__singletonConfig is None:
            Config()
        return Config.__singletonConfig

    def __init__(self):
        if Config.__singletonConfig is not None:
            raise Exception("This is a singleton class, cannot instantiate")
        else:
            self._predict_time = 10    # in seconds, it is how far in the future the program will predict collisions
            self._airport_bbox_settings = (3200000, 3200000, 3200000, 3200000)  # in meters, offset from airport, (min_latitude, max_latitude, min_longitude, max_longitude)
            self._airplane_bbox_settings = (1000000, 1000000, 1000000, 1000000)  # in meters, same as above but for a specific target plane
            self._collision_bbox_settings = (1000000, 1000000, 1000000, 1000000)    # in meters, offset from target plane predicted coordinates used for finding collisions
            self._altitude_range = 1000000  # in meters, range in which we consider other planes for collisions
            Config.__singletonConfig = self

    def get_predict_time(self):
        return self._predict_time

    def get_airport_bbox_settings(self):
        return self._airport_bbox_settings

    def get_airplane_bbox_settings(self):
        return self._airplane_bbox_settings

    def get_collision_bbox_settings(self):
        return self._collision_bbox_settings

    def get_altitude_range(self):
        return self._altitude_range

    def set_predict_time(self, time):
        self._predict_time = time

    def set_airport_bbox_settings(self, bbox):
        self._airport_bbox_settings = bbox

    def set_airplane_bbox_settings(self, bbox):
        self._airplane_bbox_settings = bbox

    def set_collision_bbox_settings(self, bbox):
        self._collision_bbox_settings = bbox

    def set_altitude_range(self, range):
        self._altitude_range = range
