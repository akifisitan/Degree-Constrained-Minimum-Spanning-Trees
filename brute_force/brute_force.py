import itertools
import time
from sample_generation import generate_weighted_undirected_connected_graph as generate_sample
from helpers import kruskal_mst, is_acyclic, create_graph_from_edges, get_edges
from helpers import get_node_degree, print_graph, is_connected


def check_degree_constraint(graph, degree):
    for node in range(len(graph)):
        if get_node_degree(graph, node) > degree:
            return False
    return True


def brute_force(graph, degree):
    edges = get_edges(graph)  # get list of edges in the graph in [u, v, weight] format
    num_vertices, num_edges = len(graph), len(edges)
    num_tree_edges = num_vertices - 1
    path, weight_mst = kruskal_mst(graph)
    print("Calculating combinations...")
    potential_m_s_trees = itertools.combinations(edges, num_tree_edges)
    print("Calculated combinations. Starting loop...")
    for i, potential_mst in enumerate(potential_m_s_trees):
        print(f"Processing combination: {i}")
        potential_mst_weight = 0
        for u, v, weight in potential_mst:
            potential_mst_weight += weight
        if potential_mst_weight != weight_mst:
            continue
        temp_graph = create_graph_from_edges(num_vertices, potential_mst)
        # The graph is a tree if it is connected and has no cycles.
        if is_connected(temp_graph) and is_acyclic(temp_graph):
            if check_degree_constraint(temp_graph, degree):
                return temp_graph
    return None


def main():
    graph = generate_sample(num_nodes=8, min_weight=1, max_weight=4, edge_probability=0.5)
    degree_constraint = 3
    print(f"Checking for the Degree ({degree_constraint}) Constrained Spanning Tree for graph:")
    print_graph(graph)
    start = time.perf_counter()
    d_c_m_s_tree = brute_force(graph=graph, degree=degree_constraint)
    end = time.perf_counter()
    if d_c_m_s_tree:
        print(f"Found a Degree ({degree_constraint}) Constrained Minimum Spanning Tree:")
        print_graph(d_c_m_s_tree)
    else:
        print(f"Degree ({degree_constraint}) Constrained Minimum Spanning Tree not found.")
    print(f"Time taken: {end - start:0.7f} seconds")


if __name__ == '__main__':
    main()
