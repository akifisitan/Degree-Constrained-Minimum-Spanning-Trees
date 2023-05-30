import time
import matplotlib.pyplot as plt
from sample_generation import generate_weighted_undirected_connected_graph as generate_sample
from heuristic.heuristic import heuristic


# import other required modules and functions


def main():
    num_runs = 3  # Number of times to run the algorithm
    graph_sizes = [10, 20]  # Different graph sizes to test
    degree_constraint = 3
    execution_times = []  # List to store execution times

    for size in graph_sizes:
        avg_execution_time = 0

        for _ in range(num_runs):
            graph = generate_sample(num_nodes=size, min_weight=1, max_weight=4, edge_probability=0.5)

            start_time = time.time()
            # Perform the algorithm and measure the execution time
            tree, tree_graph = heuristic(graph, degree_constraint)
            end_time = time.time()

            execution_time = end_time - start_time
            avg_execution_time += execution_time

        avg_execution_time /= num_runs
        execution_times.append(avg_execution_time)

    # Plot the execution times
    plt.plot(graph_sizes, execution_times, marker='o')
    plt.xlabel('Graph Size')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Performance Analysis of Heuristic Algorithm')
    plt.show()


if __name__ == '__main__':
    main()
