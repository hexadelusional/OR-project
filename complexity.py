import random
import math
import os
import re

def generate_proposition(n: int):
    """
        Creates the capacity and cost matrices to feed into a .txt file in the proposition_to_file fun
        Args: integer n, the size of the matrix
    """
    capacity_matrix = [[0 for j in range(n)] for i in range(n)]
    cost_matrix = [[0 for j in range(n)] for i in range(n)]

    nb_values = math.floor((n**2)/2)
    couples_edited = set()
    
    while nb_values > 0 :
        i, j = 0,0
        while (i==j or ((i,j) in couples_edited) or i==n-1) :
            i, j = random.randint(0,n-1),  random.randint(0,n-1 )
        capacity_matrix[i][j] = random.randint(1,100)
        cost_matrix[i][j] = capacity_matrix[i][j]//2
        couples_edited.add((i,j))
        nb_values-=1
    
    proposition_to_file(capacity_matrix, cost_matrix)

    return


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
    return



generate_proposition(6)









