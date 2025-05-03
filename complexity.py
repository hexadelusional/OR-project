import random
import math
import os
import re
import time
import copy
from graph import Graphic
from algorithms import *


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
    """Runs FF on a graph and returns the execution time"""
    start_ff = time.perf_counter()
    max_flow = ford_fulkerson(graph)
    end_ff = time.perf_counter()
    return max_flow, (end_ff - start_ff) 

def measure_pr(graph):
    """Runs PR on a graph and returns the execution time"""
    start_pr = time.perf_counter()
    push_relabel(graph, False)
    end_pr = time.perf_counter()
    return (end_pr - start_pr)

def measure_mcf(graph, target_flow):
    """Runs MCF on a graph, provided a target flow, and returns the execution time"""
    start_mcf = time.perf_counter()
    min_cost_flow(graph, target_flow)
    end_mcf = time.perf_counter()
    return (end_mcf - start_mcf)

### Saving stuff ###

def generate_execution_time_data(graph_sizes: list[int], nb_runs = 100) -> dict:
    results = {}

    for size in graph_sizes :
        results[size] = {"thetas_ff":[], "thetas_pr" :[], "thetas_mcf":[]}
        
        print(f"Running the test for n = {size}")
        for _ in range(nb_runs):
            # initialize a random graph 
            capacity_matrix, cost_matrix = generate_proposition(size)
            n_vertices = len(capacity_matrix)
            graph = Graphic(n_vertices)

            graph.capacity = capacity_matrix
            graph.cost = cost_matrix

            #   Measure execution times for each algorithm
            # Measure Ford-Fulkerson
            max_ff_flow, theta_ff = measure_ff(graph)
            results[size]["thetas_ff"].append(theta_ff)
            
            # Measure Push-Relabel
            theta_pr = measure_pr(graph)
            results[size]["thetas_pr"].append(theta_pr)

            # Measure min-cost flow
            theta_mcf = measure_mcf(graph, max_ff_flow//2)
            results[size]["thetas_mcf"].append(theta_mcf)


            # print(f"\nVALUE {size}: θFF={theta_ff} | θPR={theta_pr} | θMIN={theta_mcf} |\n")
    return results

def save_execution_time_data(execution_time_data: dict, path_to_file) -> None:
    # Write to file
    new_file_path = path_to_file
    while os.path.exists(new_file_path):
        new_file_path = "execution_trace_" + str(int(new_file_path[-5])+1) + ".txt"
    
    with open(new_file_path, "w") as f:
        f.write(str(execution_time_data))




# Juste pour les tests
t1 = time.time()

time_results = generate_execution_time_data([10, 20, 40, 100, 200, 400, 1000], 100)
save_execution_time_data(time_results, "execution_trace_0.txt")

t2 = time.time()
print(f"whole process lasted {t2-t1}s")

