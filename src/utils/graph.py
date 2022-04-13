from typing import List, Set, Tuple, Type
from unicodedata import bidirectional


class Street:
    """
    Represents a Street as an edge to a graph

    Attributes
    ----------
    initial : Junction
        the junction at the start of the street
    final : Junction
        the junction at the start of the street
    length : int
        the length of the street in meters
    time : int
        the time, in virtual seconds, a car needs to traverse the street
    bidirectional : bool
        true if street is bidirectional
    """

    def __init__(self, initial: 'Junction', final: 'Junction', length: int, time: int, bidirectional: bool):
        self.initial = initial
        self.final = final
        self.length = length
        self.time = time
        self.bidirectional = bidirectional
        self.visited = False

    def __str__(self):
        return "Street from junction " + str(self.initial) + " to " + str(self.final) + " is bi? " + str(self.bidirectional)


class Junction:
    """
    Represents a Street Junction as a node to a graph

    Attributes
    ----------
    coords : (float, float)
        the coordinates in latitude (first, -90 <= lat <= 90) and longitude (second, -180 <= long <= 180) in decimal degrees
    streets : List of Street
        the neighbouring streets
    """

    def __init__(self, coords: Tuple[float, float], id : int):
        self.coords = coords  # type: Tuple[float, float]
        self.streets = []   # type: List[Street]
        self.neighbours = set()  # type: Set[int]
        self.id = id
        self.visited = False

    def add_street(self, street: Street):
        self.streets.append(street)

        if not (street.initial is self):
            self.neighbours.add(street.initial.id)

        if not (street.final is self):
            self.neighbours.add(street.final.id)

    def __str__(self):
        return "Junction at " + ','.join(map(str, self.coords))


class Graph:
    def __init__(self):
        self.junctions = []  # type: List[Junction]
        self.streets = []  # type: List[Street]

    def add_junction(self, coords: Tuple[float, float]):
        self.junctions.append(Junction(coords, len(self.junctions)))

    def reset_streets(self):
        for street in self.streets:
            street.visited = False

    def add_street(self, init: int, end: int, length: int, time: int, bidirectional: bool):
        init_junction = self.junctions[init]
        end_junction = self.junctions[end]

        street = Street(
            init_junction,
            end_junction,
            length,
            time,
            bidirectional
        )
        self.streets.append(street)

        init_junction.add_street(street)
        if (bidirectional):
            end_junction.add_street(street)
