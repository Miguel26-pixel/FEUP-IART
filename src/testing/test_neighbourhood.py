import random
import pytest
from utils import neighbourhood
from utils import graph

network = graph.Graph()

network.add_junction((0, 0))
network.add_junction((1, 1))
network.add_junction((2, 2))
network.add_junction((3, 3))
network.add_junction((4, 4))
network.add_junction((5, 4))
network.add_junction((6, 4))
network.add_junction((7, 4))

network.add_street(0, 1, 1, 1, True)
network.add_street(0, 2, 1, 1, False)
network.add_street(2, 4, 1, 1, False)
network.add_street(3, 4, 1, 1, False)
network.add_street(4, 5, 1, 1, False)
network.add_street(5, 6, 1, 1, False)
network.add_street(5, 7, 1, 1, False)
network.add_street(7, 6, 1, 1, True)


def test_add_node_empty():
    sol = neighbourhood.add_node([], network)
    print("SOLUTION", sol)
    assert len(sol) == 1
    assert len(sol[0]) == 1
    assert sol[0][0] >= 0 and sol[0][0] < len(network.junctions)


def test_add_node_no_solution():
    empty_graph = graph.Graph()
    sol = neighbourhood.add_node([], empty_graph)
    assert len(sol) == 0


def test_add_connectivity():
    sol = neighbourhood.add_node([7], network)
    assert len(sol) == 1
    assert sol[0] == [7, 6]

    sol = neighbourhood.add_node([5], network)
    assert len(sol) == 2
    assert sol[0] == [5, 6]
    assert sol[1] == [5, 7]


def test_remove_node_empty():
    sol = neighbourhood.remove_node([], network)
    assert len(sol) == 0


def test_remove_last_node():
    sol = neighbourhood.remove_node([2], network)
    assert sol == [[]]
    sol = neighbourhood.remove_node([2, 3], network)
    assert sol == [[2]]


def test_single_car():
    random.seed(0)

    sol = neighbourhood.neighbour_single_car([[0, 5], [0]], network)
    assert sol == [[0, 5], []]

    random.seed(1)

    sol = neighbourhood.neighbour_single_car([[0, 5], [0]], network)
    assert sol == [[0, 5, 7], [0]]

    random.seed(3)

    sol = neighbourhood.neighbour_single_car([[0, 5], [0]], network)
    assert sol == [[0, 5, 7], [0]]


def test_multiple_car():
    random.seed(0)
    sol = neighbourhood.neighbour_multiple_cars([[0, 5], [0]], network)
    assert sol == [[0, 5], []]

    random.seed(1)
    sol = neighbourhood.neighbour_multiple_cars([[0, 5], [0]], network)
    assert sol == [[0, 5, 7], []]

    random.seed(4)
    sol = neighbourhood.neighbour_multiple_cars([[0, 5], [0]], network)
    assert sol == [[0, 5, 7], [0, 1]]
