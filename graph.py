from utils import print_matrix, annotate_matrix, bold


class Graphic:
    def __init__(self, n):
        self.n = n # Number of vertices
        self.capacity = [[0] * n for _ in range(n)]
        self.cost = [[0] * n for _ in range(n)]
        self.residual = [[0] * n for _ in range(n)]
        self.flow = [[0] * n for _ in range(n)]

    # Checking if the graph has costs
    def has_costs(self):
        """
            Checks whether the graph has an associated cost matrix.

            Returns:
                bool: True if a cost matrix exists, False otherwise.
        """
        if self.cost is None:
            return False
        else:
            return True
    
    # Adding an edge with a given capacity between vertices u and v
    def add_edge(self, u, v, capacity):
        """
            Adds a directed edge from vertex u to vertex v with the given capacity.
            Also initializes the corresponding value in the residual graph.

            Args:
                u (int): The source vertex.
                v (int): The destination vertex.
                capacity (int): The capacity of the edge from u to v.
        """
        self.capacity[u][v] = capacity
        self.residual[u][v] = capacity


    # Creates a graph from a txt file
    @classmethod
    def read_graph(cls, filename):
        """
            Reads a graph from a file. The file should contain:
            - The number of vertices in the first line.
            - The capacity matrix in the next 'n' lines.
            - Optionally, the cost matrix in the next 'n' lines (if present).

            Args:
                filename (str): Path to the file from which the graph is to be read.

            Returns:
                cls: An instance of the graph initialized with capacities and optional costs.
        """
        with open(filename, 'r') as file:
            # Reading the number of vertices
            n = int(file.readline().strip())
            
            # Instantiating Graphic
            graph = cls(n)
            
            # Reading the capacity matrix
            for i in range(n):
                row = list(map(int, file.readline().strip().split()))
                graph.capacity[i] = row
            
            # Reads the n remaining lines, for the costs matrix if they exist
            remaining_lines = file.readlines()
            if len(remaining_lines) == n:
                for i in range(n):
                    row = list(map(int, remaining_lines[i].strip().split()))
                    graph.cost[i] = row
            else:
                graph.cost = None  # There is no cost matrix

        # Initializing the residual matrix so that it corresponds exactly to the capacity
        graph.residual = [row[:] for row in graph.capacity]
        return graph

    # Display of the flow matrix
    def display_flow(self):
        """
            Displays the flow matrix in a formatted and annotated way.
            Assumes that a helper function `annotate_matrix` exists to enhance readability.
        """
        print(bold(f"\nFLOW MATRIX:"))
        annotated_flow = annotate_matrix(self.flow)
        print_matrix(annotated_flow)

    # Display of the capacity and cost matrices
    def display(self):
        """
            Displays the capacity matrix and, if available, the cost matrix in a human-readable format.
            Uses helper functions `annotate_matrix` and `print_matrix`.
        """
        print(bold(f"\nCAPACITY MATRIX:"))
        annotated_capacity = annotate_matrix(self.capacity)
        print_matrix(annotated_capacity)

        if self.cost:
            print(bold(f"\nCOST MATRIX:"))
            annotated_cost = annotate_matrix(self.cost)
            print_matrix(annotated_cost)

    # Display of the residual matrix
    def display_residual(self):
        """
            Displays the residual matrix of the graph, which is used in flow algorithms.
            Uses `annotate_matrix` to format and `print_matrix` to print the matrix.
        """
        print(bold(f"\nRESIDUAL GRAPH:"))
        annotated_residual = annotate_matrix(self.residual)
        print_matrix(annotated_residual)

