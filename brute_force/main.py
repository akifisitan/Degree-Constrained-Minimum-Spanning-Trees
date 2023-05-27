import itertools
import time
from sample_generation import generate_weighted_undirected_connected_graph as generate_sample
from helpers import kruskal_mst, is_acyclic, print_graph, create_graph_from_edges, is_connected, draw_graph


sample_graph = [
        [0, 3, 2, 0, 0],
        [3, 0, 1, 0, 3],
        [2, 1, 0, 4, 0],
        [0, 0, 4, 0, 2],
        [0, 3, 0, 2, 0]
]


def get_edges(graph):
    edges = []
    for i in range(len(graph)):
        for j in range(i + 1, len(graph)):
            if i != j and graph[i][j] != 0:
                edges.append([i, j, graph[i][j]])
    return edges


def check_degree_constraint(graph, degree):
    for i in range(len(graph)):
        temp_degree = 0
        for j in range(len(graph)):
            if graph[i][j] > 0:
                temp_degree += 1
        if temp_degree > degree:
            return False
    return True


def brute_force(graph, degree):
    edges = get_edges(graph)
    num_vertices, num_edges = len(graph), len(edges)
    num_tree_edges = num_vertices - 1
    start = time.perf_counter()
    path, weight_mst = kruskal_mst(graph)
    end = time.perf_counter()
    print(f"Kruskal: {end - start:0.7f} seconds")
    # print(f"Path: {path}, Weight of the MST: {weight_mst}")
    potential_m_s_trees = list(itertools.combinations(edges, num_tree_edges))
    m_s_trees = []
    print(f"Vertices: {num_vertices}, Edges: {num_edges}, Potential Minimum Spanning Trees: {len(potential_m_s_trees)}")
    loop_start = time.perf_counter()
    for i, potential_mst in enumerate(potential_m_s_trees):
        print(f"Processing combination: {i}: {potential_mst}")
        potential_mst_weight = 0
        for u, v, weight in potential_mst:
            potential_mst_weight += weight
        if potential_mst_weight != weight_mst:
            continue
        temp_graph = create_graph_from_edges(num_vertices, potential_mst)
        # The graph is a tree if it is connected and has no cycles.
        if is_connected(temp_graph) and is_acyclic(temp_graph):
            m_s_trees.append(temp_graph)
            if check_degree_constraint(temp_graph, degree):
                print_graph(temp_graph)
                draw_graph(temp_graph)
                # print(f"Degree ({degree}) Constrained Minimum Spanning Tree: {potential_mst}")
                # print_graph(temp_graph)
                # loop_end = time.perf_counter()
                # print(f"Loop time taken: {loop_end - loop_start:0.7f} seconds (Early Exit)")
                return temp_graph, m_s_trees
    loop_end = time.perf_counter()
    print(f"Loop time taken: {loop_end - loop_start:0.7f} seconds")
    return None, m_s_trees


def main():
    graph = generate_sample(num_nodes=9, min_weight=1, max_weight=4, edge_probability=0.5)
    degree_constraint = 3
    print(f"Checking for the Degree ({degree_constraint}) Constrained Spanning Tree for graph:")
    print_graph(graph)
    draw_graph(graph)
    start = time.perf_counter()
    d_c_m_s_tree, m_s_trees = brute_force(graph=graph, degree=degree_constraint)
    end = time.perf_counter()
    print(f"Algorithm full time taken: {end - start:0.7f} seconds")
    if d_c_m_s_tree:
        print(f"Degree ({degree_constraint}) Constrained Minimum Spanning Tree:")
        print_graph(d_c_m_s_tree)
    else:
        print(f"Degree ({degree_constraint}) Constrained Minimum Spanning Tree not found!")

    print(f"Some MSTrees: {m_s_trees}")
    """for tree in m_s_trees:
        graph = create_graph_from_edges(len(graph), get_edges(tree))
        draw_graph(graph)"""


if __name__ == '__main__':
    main()
