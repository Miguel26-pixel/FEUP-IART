class Router:
    """
    Represents a Street View Routing Problem and provides methods to solve it.

    Attributes
    ----------
    time_itinerary : int
        the virtual time in seconds allowed for the car itineraries
    num_cars : int
        the number of cars in the fleet
    initial_junction : int
        the junction at which all the cars are located initially
    graph : Graph
        the street map represented as a graph
    """

    def __init__(self, time_itinerary, num_cars, initial_junction, graph) -> None:
        self.time_itinerary = time_itinerary
        self.num_cars = num_cars
        self.initial_junction = initial_junction
        self.graph = graph
