import time
from helpers import kruskal_mst, draw_graph, get_node_degree, create_graph_from_edges
from sample_generation import generate_weighted_undirected_connected_graph as generate_sample


def infeasible_nodes(graph, edge, degree):
    i_nodes = 0
    if get_node_degree(graph, edge[0]) > degree:
        i_nodes += 1
    if get_node_degree(graph, edge[1]) > degree:
        i_nodes += 1
    return i_nodes


def get_w_min_max(tree):
    weights = []
    for u, v, weight in tree:
        weights.append(weight)
    return min(weights), max(weights)


def blacklisting_function(graph, tree, degree, edge):
    w_min, w_max = get_w_min_max(tree)
    old_weight = graph[edge[0]][edge[1]]
    if old_weight == w_min:
        return
    new_weight = old_weight + infeasible_nodes(graph, edge, degree) * (
            (old_weight - w_min) / (w_max - w_min) ) * w_max
    graph[edge[0]][edge[1]] = new_weight
    graph[edge[1]][edge[0]] = new_weight


def check_degree_constraint(graph: list, degree: int):
    for node in range(len(graph)):
        if get_node_degree(graph, node) > degree:
            return False
    return True


def heuristic(graph: list, degree: int):
    tree, tree_weight = kruskal_mst(graph)
    tree_graph = create_graph_from_edges(len(graph), tree)
    while not check_degree_constraint(tree_graph, degree):
        for edge in tree:
            blacklisting_function(graph, tree, degree, edge)
        tree, tree_weight = kruskal_mst(graph)
        tree_graph = create_graph_from_edges(len(graph), tree)
    return tree, tree_graph


def main():
    graph = generate_sample(num_nodes=12, min_weight=1, max_weight=4, edge_probability=0.5)
    degree_constraint = 3
    tree, tree_graph = heuristic(graph, degree_constraint)
    print(f"Heuristic Minimum Spanning Tree: {tree_graph}")


if __name__ == '__main__':
    main()
