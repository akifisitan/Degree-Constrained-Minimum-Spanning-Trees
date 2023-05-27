import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd


class DisjointSet:
    def __init__(self, vertices):
        self.parent = [-1] * vertices

    def find(self, vertex):
        if self.parent[vertex] < 0:
            return vertex
        self.parent[vertex] = self.find(self.parent[vertex])
        return self.parent[vertex]

    def union(self, root1, root2):
        if root1 == root2:
            return
        if self.parent[root1] > self.parent[root2]:
            self.parent[root2] += self.parent[root1]
            self.parent[root1] = root2
        else:
            self.parent[root1] += self.parent[root2]
            self.parent[root2] = root1


def kruskal_mst(graph):
    edges = []
    vertices = len(graph)

    # Create a list of all edges with their weights
    for i in range(vertices):
        for j in range(i + 1, vertices):
            if graph[i][j] != 0:
                edges.append((graph[i][j], i, j))

    # Sort the edges based on their weights
    edges.sort()

    mst = []
    disjoint_set = DisjointSet(vertices)

    for edge in edges:
        weight, u, v = edge
        root1 = disjoint_set.find(u)
        root2 = disjoint_set.find(v)

        if root1 != root2:
            mst.append((u, v, weight))
            disjoint_set.union(root1, root2)
    tree_weight = 0
    for u, v, weight in mst:
        tree_weight += weight
    return mst, tree_weight


def dfs(graph, visited, start):
    """
  Performs a depth-first search on a graph.

  Args:
    graph: The adjacency matrix of the graph.
    visited: A list of boolean values indicating which nodes have been visited.
    start: The index of the starting node.
  """

    # Mark the starting node as visited.
    visited[start] = True

    # For each neighbor of the starting node, do a depth-first search.
    for neighbor in range(len(graph)):
        if graph[start][neighbor] != 0 and not visited[neighbor]:
            dfs(graph, visited, neighbor)


def is_acyclic(graph):
    # Number of vertices in the graph
    num_vertices = len(graph)

    # Create a visited array to keep track of visited vertices
    visited = [False] * num_vertices

    # Perform depth-first search (DFS) on each unvisited vertex
    for vertex in range(num_vertices):
        if not visited[vertex]:
            if dfs_util(graph, vertex, visited, -1):
                return False

    return True


def dfs_util(graph, vertex, visited, parent):
    # Mark the current vertex as visited
    visited[vertex] = True

    # Iterate through all the neighbors of the current vertex
    for neighbor in range(len(graph[vertex])):
        # If the neighbor is not visited, recursively call DFS on it
        if graph[vertex][neighbor] != 0 and not visited[neighbor]:
            if dfs_util(graph, neighbor, visited, vertex):
                return True
        # If the neighbor is visited and not the parent of the current vertex, a cycle is found
        elif graph[vertex][neighbor] != 0 and visited[neighbor] and neighbor != parent:
            return True

    return False


def print_graph(graph):
    for row in graph:
        print(row)


def is_connected(graph):
    """
    Checks if a graph is connected.

    Args:
        graph: The adjacency matrix of the graph.

    Returns:
        True if the graph is connected, False otherwise.
    """

    # Initialize a visited array.
    visited = [False] * len(graph)

    # Start at any node and do a depth-first search.
    dfs(graph, visited, 0)

    # If all nodes have been visited, then the graph is connected.
    return all(visited)


def create_graph_from_edges(vertices, edges):
    graph = [[0] * vertices for _ in range(vertices)]
    for u, v, weight in edges:
        graph[u][v] = weight
        graph[v][u] = weight
    return graph


def draw_graph(graph):
    df = pd.DataFrame(graph)
    graph = nx.from_pandas_adjacency(df)
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=12, font_weight='bold')
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.show()

