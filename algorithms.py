from collections import deque
from utils import print_matrix, annotate_matrix

def bfs(residual, source, sink, parent):
    n = len(residual)  # Nombre de sommets dans le graphe résiduel
    visited = [False] * n  # Liste pour suivre les sommets visités
    queue = deque([source])  # File d'attente pour la recherche en largeur, initialisée avec le sommet source
    visited[source] = True  # Marquer le sommet source comme visité

    while queue:  # Tant que la file d'attente n'est pas vide
        u = queue.popleft()  # Extraire un sommet de la file d'attente
        for v in range(n):  # Parcourir tous les sommets adjacents
            if not visited[v] and residual[u][v] > 0:  # Si le sommet n'a pas été visité et qu'il y a une capacité résiduelle
                parent[v] = u  # Enregistrer le parent de v
                visited[v] = True  # Marquer le sommet v comme visité
                queue.append(v)  # Ajouter le sommet v à la file d'attente
                if v == sink:  # Si le sommet v est le puits
                    return True  # Chemin trouvé, retourner True
    return False  # Aucun chemin trouvé, retourner False


def ford_fulkerson(graph):
    source = 0
    sink = graph.n - 1
    parent = [-1] * graph.n
    max_flow = 0
    iteration = 1

    while bfs(graph.residual, source, sink, parent):
        print(f"\n\033[1mITERATION {iteration} \033[0m")
        display_bfs_trace(parent, source, sink, graph.n)
        path_flow = get_path_flow(graph.residual, parent, source, sink)
        display_augmenting_path(parent, source, sink, graph.n, path_flow)
        update_residual_and_flow(graph, parent, source, sink, path_flow)
        display_residual_graph(graph.residual)
        max_flow += path_flow
        iteration += 1

    return max_flow


def display_bfs_trace(parent, source, sink, n):
    print("\n\033[1mBFS trace:\033[0m")
    visited_nodes = []
    for i in range(n):
        if parent[i] != -1 and i != source:
            node = 't' if i == sink else chr(i + 96)
            pred = 's' if parent[i] == source else ('t' if parent[i] == sink else chr(parent[i] + 96))
            visited_nodes.append(f"Π({node}) = {pred}")
    print(" → ".join(visited_nodes))

def get_path_flow(residual, parent, source, sink):
    flow = float('inf')
    v = sink
    while v != source:
        u = parent[v]
        flow = min(flow, residual[u][v])
        v = u
    return flow

def display_augmenting_path(parent, source, sink, n, path_flow):
    path = []
    v = sink
    while v != source:
        path.append(v)
        v = parent[v]
    path.append(source)
    path = path[::-1]
    labels = ['s' if i == 0 else 't' if i == n - 1 else chr(i + 96) for i in path]
    print(f"Improving chain : [{' → '.join(labels)}] with a flow {path_flow}.")


def update_residual_and_flow(graph, parent, source, sink, path_flow):
    v = sink
    while v != source:
        u = parent[v]
        graph.residual[u][v] -= path_flow
        graph.residual[v][u] += path_flow
        graph.flow[u][v] += path_flow
        graph.flow[v][u] -= path_flow
        v = u

def display_residual_graph(residual):
    print("\n\033[1mRESIDUAL GRAPH:\033[0m\n")
    annotated = annotate_matrix(residual)
    print_matrix(annotated)



def push_relabel(graph):
    n = graph.n  # Nombre de sommets dans le graphe
    source = 0  # Définir la source comme le premier sommet
    sink = n - 1  # Définir le puits comme le dernier sommet
    
    height = [0] * n  # Hauteur des sommets
    excess = [0] * n  # Flot excédentaire aux sommets
    seen = [0] * n  # Suivi des voisins vus pour la décharge
    
    # Initialiser le pré-flot
    height[source] = n  # La hauteur de la source est définie comme le nombre de sommets
    for v in range(n):  # Parcourir tous les sommets
        if graph.capacity[source][v] > 0:  # Si la capacité de la source au sommet v est positive
            graph.flow[source][v] = graph.capacity[source][v]  # Initialiser le flot de la source à v
            graph.flow[v][source] = -graph.flow[source][v]  # Flot opposé de v à la source
            excess[v] = graph.capacity[source][v]  # Mettre à jour le flot excédentaire au sommet v
            excess[source] -= graph.capacity[source][v]  # Réduire le flot excédentaire à la source
    
    def push(u, v):  # Fonction pour pousser le flot de u à v
        delta = min(excess[u], graph.capacity[u][v] - graph.flow[u][v])  # Calculer le flot à pousser
        graph.flow[u][v] += delta  # Mettre à jour le flot de u à v
        graph.flow[v][u] -= delta  # Mettre à jour le flot opposé de v à u
        excess[u] -= delta  # Réduire le flot excédentaire à u
        excess[v] += delta  # Augmenter le flot excédentaire à v
    
    def relabel(u):  # Fonction pour relabeler un sommet u
        min_height = float('Inf')  # Initialiser la hauteur minimale à l'infini
        for v in range(n):  # Parcourir tous les sommets
            if graph.capacity[u][v] > graph.flow[u][v]:  # Si la capacité résiduelle est positive
                min_height = min(min_height, height[v])  # Trouver la hauteur minimale parmi les voisins
        height[u] = min_height + 1  # Relabeler u avec la nouvelle hauteur

    def discharge(u):  # Fonction pour décharger un sommet u
        while excess[u] > 0:  # Tant qu'il y a un flot excédentaire à u
            if seen[u] < n:  # Vérifier le prochain voisin
                v = seen[u]  # Obtenir le voisin v
                if graph.capacity[u][v] > graph.flow[u][v] and height[u] > height[v]:  # Si les conditions de poussée sont remplies
                    push(u, v)  # Pousser le flot de u à v
                else:
                    seen[u] += 1  # Passer au voisin suivant
            else:
                relabel(u)  # Relabeler u si tous les voisins ont été vus
                seen[u] = 0  # Réinitialiser le compteur de voisins vus

    # Ensemble des sommets excluant la source et le puits
    active = [i for i in range(n) if i != source and i != sink]

    # Décharger les sommets actifs
    while any(excess[i] > 0 for i in active):  # Tant qu'il y a des sommets avec un flot excédentaire
        for u in active:  # Parcourir tous les sommets actifs
            if excess[u] > 0:  # Si le sommet a un flot excédentaire
                discharge(u)  # Décharger le sommet

    # Retourner le flot maximum, qui est le flot total entrant dans le puits
    return sum(graph.flow[v][sink] for v in range(n))


def bellman_ford(residual, cost, source, n):
    dist = [float('Inf')] * n  # Initialiser les distances à l'infini pour tous les sommets
    pred = [-1] * n  # Initialiser les prédécesseurs à -1 pour tous les sommets
    dist[source] = 0  # La distance de la source à elle-même est 0

    for _ in range(n - 1):  # Répéter n-1 fois
        for u in range(n):  # Pour chaque sommet u
            for v in range(n):  # Pour chaque sommet v
                if residual[u][v] > 0 and dist[u] + cost[u][v] < dist[v]:  # Si il y a une capacité résiduelle et un chemin plus court
                    dist[v] = dist[u] + cost[u][v]  # Mettre à jour la distance de v
                    pred[v] = u  # Mettre à jour le prédécesseur de v

    # Vérifier les cycles négatifs (optionnel, non requis ici)
    return dist, pred  # Retourner les distances et les prédécesseurs

def min_cost_flow(graph, target_flow):
    n = graph.n  # Nombre de sommets dans le graphe
    source = 0  # Définir la source comme le premier sommet
    sink = n - 1  # Définir le puits comme le dernier sommet
    total_cost = 0  # Initialiser le coût total à 0
    flow = 0  # Initialiser le flot à 0

    while flow < target_flow:  # Tant que le flot total est inférieur au flot cible
        # Trouver les plus courts chemins dans le graphe résiduel
        dist, pred = bellman_ford(graph.residual, graph.cost, source, n)

        # Vérifier si un cycle négatif est présent
        for u in range(n):  # Pour chaque sommet u
            for v in range(n):  # Pour chaque sommet v
                if graph.residual[u][v] > 0 and dist[u] + graph.cost[u][v] < dist[v]:  # Si il y a un cycle négatif
                    raise ValueError("Negative cycle detected in the graph.")  # Lever une exception

        # Vérifier si un chemin est trouvable
        if dist[sink] == float('Inf'):  # Si la distance au puits est infinie
            print("No path is available to reach the target flow. ")  # Afficher un message
            break  # Sortir de la boucle

        # Trouver le flot maximum possible à pousser dans ce chemin
        path_flow = float('Inf')  # Initialiser le flot du chemin à l'infini
        v = sink  # Commencer du puits
        while v != source:  # Remonter le chemin trouvé par Bellman-Ford
            u = pred[v]  # Trouver le prédécesseur de v
            if u == -1:  # Si le prédécesseur est invalide
                raise ValueError("Invalid path. ")  # Lever une exception
            path_flow = min(path_flow, graph.residual[u][v])  # Trouver la capacité résiduelle minimale le long du chemin
            v = u  # Passer au sommet précédent

        # Limiter le flot pour ne pas dépasser le flot cible restant
        path_flow = min(path_flow, target_flow - flow)  # Limiter le flot

        # Pousser le flot le long du chemin augmentant
        v = sink  # Recommencer du puits
        while v != source:  # Remonter le chemin trouvé par Bellman-Ford
            u = pred[v]  # Trouver le prédécesseur de v
            # Mise à jour du graphe résiduel
            graph.residual[u][v] -= path_flow  # Réduire la capacité résiduelle le long du chemin
            graph.residual[v][u] += path_flow  # Augmenter la capacité résiduelle dans la direction opposée

            # Mise à jour de la matrice de flot
            graph.flow[u][v] += path_flow  # Augmenter le flot le long du chemin
            graph.flow[v][u] -= path_flow  # Réduire le flot dans la direction opposée

            # Mise à jour du coût total
            total_cost += path_flow * graph.cost[u][v]  # Ajouter le coût du chemin au coût total
            v = u  # Passer au sommet précédent

        # Mettre à jour le flot total
        flow += path_flow  # Ajouter le flot du chemin au flot total
        print(f"Added flow: {path_flow}, Total flow : {flow}, Total cost : {total_cost}")  # Afficher les informations du flot

    # Vérifier si le flot cible a été atteint
    if flow < target_flow:  # Si le flot total est inférieur au flot cible
        print("Reaching the target flow is impossible with the current capacities. ")  # Afficher un message
        return None  # Retourner None

    return total_cost  # Retourner le coût total
