import random
import math
import os
import re
import time
import copy
from graph import Graphic
from algorithms import *
import matplotlib.pyplot as plt

def generate_proposition(n: int) -> tuple[list[list[int]], list[list[int]]]:
    """
        Returns a capacity and a cost matrix which c_ij and d_ij values are random between 1 and 100
        Args: integer n, the size of the matrix
    """
    # initialize the two matrices c and d.
    capacity_matrix = [[0 for j in range(n)] for i in range(n)] 
    cost_matrix = [[0 for j in range(n)] for i in range(n)]

    nb_editions_left = math.floor((n**2)/2)
    couples_edited = set()
    
    while nb_editions_left > 0:
        i, j = 0, 0
        # assign random integers to i and j as long as the couple does not meet the requirements
        while (i == j or ((i,j) in couples_edited) or i == n - 1) :
            i, j = random.randint(0, n - 1),  random.randint(0, n - 1)
        
        capacity_matrix[i][j] = random.randint(1, 100)
        # cost_matrix[i][j] = capacity_matrix[i][j] // 2
        cost_matrix[i][j] = random.randint(1, 100)
        
        couples_edited.add((i,j))   # add the new vertex so that we cannot edit it again by error
        nb_editions_left -= 1

    return capacity_matrix, cost_matrix


def proposition_to_file(capacity_matrix, cost_matrix):
    """
        Creates a proposal text file with the capacity and cost matrix following the required format
        Args: the capacity matrix and cost matrix that have to be written in the file
    """
    n = len(capacity_matrix)
    folder = "Propositions"

    # Ensure the folder exists
    os.makedirs(folder, exist_ok=True)

    # Look for existing files inside the folder
    existing_files = os.listdir(folder)
    pattern = re.compile(r"Proposition(\d+)\.txt")
    
    numbers = []
    for f in existing_files:
        match = pattern.fullmatch(f)
        if match:
            numbers.append(int(match.group(1)))

    next_index = max(numbers, default=0) + 1

    # Build the full path
    filename = os.path.join(folder, f"Random proposition{next_index}.txt")

    # Write to file
    with open(filename, "w") as f:
        f.write(f"{n}\n")
        for row in capacity_matrix:
            f.write(' '.join(map(str, row)) + '\n')
        for row in cost_matrix:
            f.write(' '.join(map(str, row)) + '\n')
    return filename

def generate_random_graph(file):
    graph = Graphic.read_graph(file)
    return graph

### Time measurement ###

def measure_ff(graph):
    start_ff = time.perf_counter()
    result_ff = ford_fulkerson(graph)
    end_ff = time.perf_counter()
    return result_ff, (end_ff - start_ff) 

def measure_pr(graph):
    start_pr = time.perf_counter()
    push_relabel(graph)
    end_pr = time.perf_counter()
    return (end_pr - start_pr)

def measure_mcf(graph, target_flow):
    start_mcf = time.perf_counter()
    min_cost_flow(graph, target_flow)
    end_mcf = time.perf_counter()
    return (end_mcf - start_mcf)

### Point Cloud ###

def point_cloud(values_to_test, nb_runs = 100):
    results = {}

    for n_val in values_to_test :
        results[n_val] = {"thetas_ff":[], "thetas_pr" :[], "thetas_mcf":[]}
        print(f"Running the test for n = {n_val}")

        for _ in range(nb_runs):
            capacity_matrix, cost_matrix = generate_proposition(n_val)
            n_vertices = len(capacity_matrix)
            graph = Graphic(n_vertices)

            graph.capacity = capacity_matrix
            graph.cost = cost_matrix

            # Measure Ford-Fulkerson
            max_ff_flow, theta_ff = measure_ff(copy.deepcopy(graph))
            results[n_val]["thetas_ff"].append(theta_ff)
            
            # Measure Push-Relabel
            theta_pr = measure_pr(copy.deepcopy(graph))
            results[n_val]["thetas_pr"].append(theta_pr)

            # Measure min-cost flow
            if graph.has_costs() :
                theta_mcf = measure_mcf(copy.deepcopy(graph), max_ff_flow//2)
                results[n_val]["thetas_mcf"].append(theta_mcf)
            print(f"\nVALUE {n_val}: θFF={theta_ff} | θPR={theta_pr} | θMIN={theta_mcf} |\n")
    return results

def plot_point_cloud(results):
    plt.figure(figsize=(10, 6))
    for n_val, thetas in results.items():
        # Plot Ford-Felkerson results
        plt.scatter([n_val] * len(thetas["thetas_ff"]), thetas["thetas_ff"], 
                    color='blue', label='θFF(n)' if n_val == list(results.keys())[0] else "", alpha=0.6)
        # Plot Push-Relabel results
        plt.scatter([n_val] * len(thetas["thetas_pr"]), thetas["thetas_pr"], 
                    color='green', label='θPR(n)' if n_val == list(results.keys())[0] else "", alpha=0.6)
        # Plot Min-Cost-Flow results
        if thetas["thetas_mcf"] :
            plt.scatter([n_val] * len(thetas["thetas_mcf"]), thetas["thetas_mcf"], 
                        color='red', label='θMIN(n)' if n_val == list(results.keys())[0] else "", alpha=0.6)

    plt.xlabel('n -> Size of the problem')
    plt.ylabel('Time (seconds)')
    plt.title('Point Cloud: Execution times in function of n')
    plt.legend(title="Algorithms", loc='upper right', fontsize=10)

    plt.grid(True)
    plt.show()

# Juste pour les tests
time_results = point_cloud([10, 20], 10)
plot_point_cloud(time_results)

# LES VRAIS TRUCS A LANCER
# time_results = point_cloud([10, 20, 40, 100, 400, 4000])
# plot_point_cloud(time_results)

