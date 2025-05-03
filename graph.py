from utils import print_matrix, annotate_matrix


class Graphic:
    def __init__(self, n):
        # Attributes of the class Graphic
        self.n = n                                   # Number of vertices
        self.capacity = [[0] * n for _ in range(n)]  # Matrix for the maximum capacity of each edge
        self.cost = [[0] * n for _ in range(n)]      # Matrix for the cost of each edge
        self.residual = [[0] * n for _ in range(n)]  # Residual matrix
        self.flow = [[0] * n for _ in range(n)]      # Matrix of flows

    # Verifies if the proposition has costs
    def has_costs(self):
        if self.cost is None:
            return False
        else:
            return True
    
    # Add an edge between vertices u and v of given capacity
    def add_edge(self, u, v, capacity):
        self.capacity[u][v] = capacity
        self.residual[u][v] = capacity

    # Creates a graph from a txt file
    @classmethod
    def read_graph(cls, filename):
        with open(filename, 'r') as file:
            # First line is the number of vertices 
            n = int(file.readline().strip())
            
            # Initialize an instance of graph of size n
            graph = cls(n)
            
            # Reads the n next lines, for the capacity matrix
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
                graph.cost = None  # There is no costs matrix if there aren't n lines remaining

        # Initialize the residual matrix - By default it has the same values as the capacity matrix
        graph.residual = [row[:] for row in graph.capacity]
        return graph

    # Displayal of the flow matrix
    def display_flow(self):
        print("\n\n\033[1mFLOW MATRIX:\033[0m\n")
        annotated_flow = annotate_matrix(self.flow)
        print_matrix(annotated_flow)

    # Display of the Capacity and Cost matrices
    def display(self):
        print("\n\n\033[1mCAPACITY MATRIX:\033[0m\n")
        annotated_capacity = annotate_matrix(self.capacity)
        print_matrix(annotated_capacity)

        if self.cost:
            print("\n\n\033[1mCOST MATRIX:\033[0m\n")
            annotated_cost = annotate_matrix(self.cost)
            print_matrix(annotated_cost)

    def display_residual(self):
        print("\n\n\033[1m⋆ Residual graph:\033[0m\n")
        annotated_residual = annotate_matrix(self.residual)
        print_matrix(annotated_residual)

