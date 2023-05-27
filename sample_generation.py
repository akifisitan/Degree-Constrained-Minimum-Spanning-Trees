import random
from helpers import is_connected as is_connected


def generate_weighted_graph(num_nodes, min_weight, max_weight, probability):
    # Initialize an empty adjacency matrix
    graph = [[0] * num_nodes for _ in range(num_nodes)]

    # Generate random weights for the edges
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() <= probability:
                weight = random.randint(min_weight, max_weight)
                graph[i][j] = weight
                graph[j][i] = weight
    return graph


def generate_weighted_undirected_connected_graph(num_nodes, min_weight, max_weight, edge_probability):
    graph = generate_weighted_graph(num_nodes, min_weight, max_weight, edge_probability)
    while not is_connected(graph):
        graph = generate_weighted_graph(num_nodes, min_weight, max_weight, edge_probability)
    return graph

