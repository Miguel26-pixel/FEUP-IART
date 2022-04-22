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
network.add_junction((5, 5))
network.add_junction((6, 6))

network.add_street(0, 5, 2, 1, True)
network.add_street(5, 6, 10, 1, True)
network.add_street(6, 4, 2, 1, True)
network.add_street(0, 1, 2, 1, True)
network.add_street(1, 2, 2, 2, False)
network.add_street(2, 3, 2, 2, False)
network.add_street(3, 4, 2, 1, False)
network.add_street(0, 4, 1, 1, False)


def test_inverse_dijkstra():
    dists = neighbourhood.inverse_dijkstra(network, 0)
    assert dists[4][1] == 6


def test_dijkstra():
    dists = neighbourhood.dijkstra(network, 0)
    assert dists[4][1] == 0


def test_multiple():
    random.seed(4)
    assert neighbourhood.add_multiple_nodes([0, 4], network) == [[0, 5, 6, 4]]


def test_remove_multiple():
    assert neighbourhood.remove_multiple_nodes(
        [0, 5, 6, 4], network) == [[0, 5]]
