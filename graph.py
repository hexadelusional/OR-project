from utils import print_matrix, annotate_matrix


class Graphic:
    def __init__(self, n):
        # Initialisation de la classe Graphic avec n sommets
        self.n = n
        self.capacity = [[0] * n for _ in range(n)]  # Matrice des capacités
        self.cost = [[0] * n for _ in range(n)]      # Matrice des coûts (optionnelle)
        self.residual = [[0] * n for _ in range(n)]  # Matrice résiduelle
        self.flow = [[0] * n for _ in range(n)]      # Matrice des flots

    # Vérifie si le graphe a des coûts
    def has_costs(self):
        if self.cost is None:
            return False
        else:
            return True
    
    # Ajoute une arête avec une capacité donnée entre les sommets u et v
    def add_edge(self, u, v, capacity):
        self.capacity[u][v] = capacity
        self.residual[u][v] = capacity

    # Lit un graphe à partir d'un fichier
    @classmethod
    def read_graph(cls, filename):
        with open(filename, 'r') as file:
            # Lit le nombre de sommets
            n = int(file.readline().strip())
            
            # Crée une instance de Graphic
            graph = cls(n)
            
            # Lit la matrice des capacités
            for i in range(n):
                row = list(map(int, file.readline().strip().split()))
                graph.capacity[i] = row
            
            # Lit la matrice des coûts optionnelle
            remaining_lines = file.readlines()
            if len(remaining_lines) == n:
                for i in range(n):
                    row = list(map(int, remaining_lines[i].strip().split()))
                    graph.cost[i] = row
            else:
                graph.cost = None  # Aucune matrice de coûts fournie

        # Initialise la matrice résiduelle pour qu'elle corresponde initialement à la capacité
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

