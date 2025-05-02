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

    # Affiche la matrice des flots
    def display_flow(self):
        flow = self.flow
        print("\n\n* Flow matrix:\n")
        
        # Affiche l'en-tête de la matrice
        print("   ", end="")
        for i in range(len(flow)):
            if i == 0:
                print("  s", end="")
            elif i == len(flow) - 1:
                print("   t", end="")
            else:
                print(f"   {chr(i + 96)}", end="")
        print()
        
        # Parcourt chaque tâche pour créer les lignes de la matrice
        for i in range(len(flow)):
            if i == 0:
                print("s ", end="")
            elif i == len(flow) - 1:
                print("t ", end="")
            else:
                print(f"{chr(i + 96)} ", end="")
            
            for j in range(len(flow)):
                if flow[i][j] != 0:
                    print(f"{flow[i][j]:4}", end="")
                else:
                    print("   *", end="")
            print()

    # Affiche la matrice des capacités et des coûts (si disponible)
    def display(self):
        
        capacity = self.capacity
        print("\n\n* Capacity matrix:\n")
        
        # Affiche l'en-tête de la matrice
        print("   ", end="")
        for i in range(len(capacity)):
            if i == 0:
                print("  s", end="")
            elif i == len(capacity) - 1:
                print("   t", end="")
            else:
                print(f"   {chr(i + 96)}", end="")
        print()
        
        # Parcourt chaque tâche pour créer les lignes de la matrice
        for i in range(len(capacity)):
            if i == 0:
                print("s ", end="")
            elif i == len(capacity) - 1:
                print("t ", end="")
            else:
                print(f"{chr(i + 96)} ", end="")
            
            for j in range(len(capacity)):
                if capacity[i][j] != 0:
                    print(f"{capacity[i][j]:4}", end="")
                else:
                    print("   *", end="")
            print()
            
        if self.cost:
            cost = self.cost
            print("\n\n* Cost matrix:\n")
            
            # Affiche l'en-tête de la matrice
            print("   ", end="")
            for i in range(len(cost)):
                if i == 0:
                    print("  s", end="")
                elif i == len(cost) - 1:
                    print("   t", end="")
                else:
                    print(f"   {chr(i + 96)}", end="")
            print()
            
            # Parcourt chaque tâche pour créer les lignes de la matrice
            for i in range(len(cost)):
                if i == 0:
                    print("s ", end="")
                elif i == len(cost) - 1:
                    print("t ", end="")
                else:
                    print(f"{chr(i + 96)} ", end="")
                
                for j in range(len(cost)):
                    if cost[i][j] != 0:
                        print(f"{cost[i][j]:4}", end="")
                    else:
                        print("   *", end="")
                print()