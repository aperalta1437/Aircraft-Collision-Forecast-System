from itertools import combinations


class Node:
    def __init__(self, icao24_code=None, altitude=None):
        self.icao24_code = icao24_code
        self.altitude = altitude

    # getters
    def get_icao24_code(self):
        return self.icao24_code

    def get_altitude(self):
        return self.altitude

    # setters
    def set_icao24_code(self, icao24_code):
        self.icao24_code = icao24_code

    def set_altitude(self, altitude):
        self.altitude = altitude

    def print_node(self):
        print(self.icao24_code, self.altitude)


class Graph:
    def __init__(self):
        self.vertices = []
        self.length = 0
        self.edges = {}

    # getters
    def get_vertices(self):
        return self.vertices

    def get_edges(self):
        return self.edges

    # setters
    def set_vertices(self, vertices):
        self.vertices = vertices

    def set_edges(self, edges):
        self.edges = edges

    def add_vertex(self, icao24_code, altitude):
        if icao24_code is not None:
            new_node = Node(icao24_code, altitude)
            self.vertices.insert(self.length, new_node)
            self.length += 1
        else:
            return

    def create_edges(self):
        all_possible_edges = combinations(self.vertices, 2)
        for element in all_possible_edges:
            height = abs(element[0].get_altitude() - element[1].get_altitude())
            self.edges[element] = height

    def print_vertices(self):
        for element in self.vertices:
            element.print_node()

    def print_edges(self):
        for element in self.edges:
            print(element[0].get_icao24_code(), element[1].get_icao24_code(), self.edges[element])

