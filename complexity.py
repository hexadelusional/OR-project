import random
import math
import os
import re

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
    return



if __name__ == "__main__":
    n = int(input("How many vertices for your 'fake' proposition?"))
    capacity_matrix, cost_matrix = generate_proposition(n)

    if 'y' == input("Should we save it ? [y/n]").lower():
        proposition_to_file(capacity_matrix, cost_matrix)
