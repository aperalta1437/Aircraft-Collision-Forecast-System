from config import Config
from aircraftdata import AircraftData

class CollisionForecast:

    def __init__(self):
        self.config = Config.get_instance()
        self.aircraft_data = AircraftData.get_instance()

    def get_potential_collisions_from_plane(self, ICAO24):
        """find all potential collisions for the given plane

        :param ICAO24: string
        :return: potential_collisions: graph
        """
        states = self.aircraft_data.get_states_from_plane(ICAO24)
        planes = states.states
        # need to get target plane state vector object
        for plane in planes:
            if plane.icao24 == ICAO24:
                target_plane = plane
                break
        # list of planes within altitude range of target plane are considered for a collision
        planes_in_range = self._get_planes_in_altitude_range(target_plane, planes)
        potential_collisions = []   # TODO use graph here instead
        self._get_collisions(target_plane, planes_in_range, potential_collisions)
        return potential_collisions

    def get_potential_collisions_from_airport(self, airport):
        """gets collisions for every plane at the airport

        :param airport: tuple holding coordinates such as (lat, long)
        :return potential_collisions: graph
        """

        states = self.aircraft_data.get_states_from_coordinates(airport)
        planes = states.states
        potential_collisions = []  # TODO use graph here instead
        for plane in planes:
            planes_in_range = self._get_planes_in_altitude_range(plane, planes)
            if not planes_in_range:
                continue
            potential_collisions = self._get_collisions(plane, planes_in_range)
        return potential_collisions

    def _get_planes_in_altitude_range(self, target_plane, planes):
        """takes in a list of planes and returns a list of planes who are likely to collide based on altitude range"""
        predict_time = self.config.get_predict_time()
        altitude_range = self.config.get_altitude_range()
        if target_plane.baro_altitude and target_plane.vertical_rate:
            predicted_target_altitude = target_plane.baro_altitude + (target_plane.vertical_rate * predict_time)
        else:
            return
        planes_in_range = []
        # each planes estimated height is calculated and check whether if it fits in the target planes estimated altitude range
        for plane in planes:
            if plane.icao24 == target_plane.icao24: #TODO: change this so we do not need to check everytime
                continue
            if plane.baro_altitude == None or plane.vertical_rate == None:  # plane doesn't have data available
                continue
            predicted_altitude = plane.baro_altitude + (plane.vertical_rate * predict_time)

            if predicted_target_altitude-altitude_range <= predicted_altitude <= predicted_target_altitude+altitude_range:
                planes_in_range.append(plane)
                print("Planes in barometric altitude range: ICAO24: {}, current altitude: {}, new altitude: {}".format(plane.icao24, plane.baro_altitude, predicted_altitude))

        return planes_in_range

    def _get_collisions(self, target_plane, planes, collisions):
        """checks whether the planes will intersect, according to a defined collisions bbox"""
        if not planes:
            return collisions

        predicted_target_coordinates = self.aircraft_data.predict_coordinates((target_plane.latitude, target_plane.longitude),
                                                                              target_plane.velocity, target_plane.heading,
                                                                              self.config.get_predict_time())
        collision_bbox = self.aircraft_data.get_bbox(predicted_target_coordinates,
                                                     self.config.get_collision_bbox_settings())
        # check every plane and add it to the graph
        for plane in planes:
            predicted_plane_coordinates = self.aircraft_data.predict_coordinates((plane.latitude, plane.longitude),
                                                                              plane.velocity, plane.heading,
                                                                              self.config.get_predict_time())
            if self._check_bbox_collision(predicted_plane_coordinates, collision_bbox):  #TODO: figure out how to use graphs here
                collisions.append((plane.icao24, predicted_plane_coordinates))

    def _check_bbox_collision(self, predicted_plane_coordinates, collision_bbox):
        """If plane coordinates within bbox then its a collision"""
        min_lat = collision_bbox[0]
        max_lat = collision_bbox[1]
        min_long = collision_bbox[2]
        max_long = collision_bbox[3]

        plane_lat = predicted_plane_coordinates[0]
        plane_long = predicted_plane_coordinates[1]

        if not min_lat <= plane_lat <= max_lat:
            return False
        if not min_long <= plane_long <= max_long:
            return False
        return True

# # test code:
# test = CollisionForecast()
# icao24 = "a7b8a1"
# collisions = test.get_potential_collisions_from_plane(icao24)
# if not collisions:
#     print("No Collisions")
# else:
#     print("Potential Collisions")
#     for collision in collisions:
#         print(collision)





