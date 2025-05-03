from collections import deque
from utils import print_matrix, annotate_matrix, bold

def bfs(residual, source, sink, parent):
    """
        Breadth-First Search to find an augmenting path from source to sink in the residual graph.

        Args:
            residual (list[list[int]]): The residual capacity graph.
            source (int): The source node.
            sink (int): The sink node.
            parent (list[int]): Array to store the path.

        Returns:
            bool: True if a path from source to sink is found, False otherwise.
    """
    n = len(residual)
    visited = [False] * n  # List to follow the visited vertices
    queue = deque([source])  # Waiting queue initialized with the source vertex
    visited[source] = True

    while queue:
        u = queue.popleft()
        for v in range(n):  # Go through all adjacent vertices
            if not visited[v] and residual[u][v] > 0:
                parent[v] = u
                visited[v] = True
                queue.append(v)  # Add the vertex v to the waiting queue
                if v == sink:
                    return True
    return False


def ford_fulkerson(graph):
    """
        Implements the Ford-Fulkerson method using BFS to compute the maximum flow.

        Args:
            graph: A graph object with residual and flow matrices.

        Returns:
            int: The value of the maximum flow from source to sink.
    """
    source = 0
    sink = graph.n - 1
    parent = [-1] * graph.n
    max_flow = 0
    iteration = 1

    # Looping while there is a path from source to sink in the residual graph
    while bfs(graph.residual, source, sink, parent):
        print(bold(f"\nITERATION {iteration}"))
        display_bfs_trace(parent, source, sink, graph.n)  # Showing BFS tree
        path_flow = get_path_flow(graph.residual, parent, source, sink)  # Finding the bottleneck
        display_augmenting_path(parent, source, sink, graph.n, path_flow)  # Showing the augmenting path and its flow
        update_residual_and_flow(graph, parent, source, sink, path_flow)  # Updating residual and flow graphs with new flows
        display_residual_graph(graph.residual)  # Displaying updated residual graph
        max_flow += path_flow
        iteration += 1

    return max_flow


def display_bfs_trace(parent, source, sink, n):
    """
        Displays the BFS tree from the last successful augmenting path search.
    """
    print(bold(f"\nBFS trace:"))
    visited_nodes = []
    for i in range(n):
        if parent[i] != -1 and i != source:
            # Convert indices to labels
            node = 't' if i == sink else chr(i + 96)
            pred = 's' if parent[i] == source else ('t' if parent[i] == sink else chr(parent[i] + 96))
            visited_nodes.append(f"Π({node}) = {pred}")
    print(" → ".join(visited_nodes))

def get_path_flow(residual, parent, source, sink):
    """
        Calculates the minimum capacity along the found augmenting path.

        Returns:
            int: The bottleneck (minimum residual capacity) on the path.
    """
    flow = float('inf')
    v = sink
    while v != source:
        u = parent[v]
        flow = min(flow, residual[u][v])  # Find minimum capacity in the path
        v = u
    return flow

def display_augmenting_path(parent, source, sink, n, path_flow):
    """
        Displays the path found during BFS and the corresponding flow.
    """
    path = []
    v = sink
    while v != source:
        path.append(v)
        v = parent[v]
    path.append(source)
    path = path[::-1]  # Reverse to get path from source to sink
    # Convert node indices to readable labels
    labels = ['s' if i == 0 else 't' if i == n - 1 else chr(i + 96) for i in path]
    print(f"Improving chain : {bold('[' + ' → '.join(labels) + ']')} with a flow {bold(path_flow)}.")


def update_residual_and_flow(graph, parent, source, sink, path_flow):
    """
        Updates the residual and flow matrices along the augmenting path.
    """
    v = sink
    while v != source:
        u = parent[v]
        graph.residual[u][v] -= path_flow  # Reducing capacity in forward edge
        graph.residual[v][u] += path_flow  # Increasing capacity in reverse edge
        graph.flow[u][v] += path_flow  # Adding flow in forward direction
        graph.flow[v][u] -= path_flow  # Substracting flow in reverse direction
        v = u

def display_residual_graph(residual):
    """
        Displays the current residual graph.
    """
    print(bold(f"\nRESIDUAL GRAPH"))
    annotated = annotate_matrix(residual)
    print_matrix(annotated)



def push_relabel(graph):
    """
        Computes the maximum flow using the Push-Relabel algorithm.

        Args:
            graph: Graph object with capacity and flow matrices.

        Returns:
            int: Maximum flow value from source to sink.
    """
    n = graph.n
    source = 0
    sink = n - 1
    
    height = [0] * n
    excess = [0] * n
    seen = [0] * n
    
    # Initializing the free float
    height[source] = n
    for v in range(n):
        if graph.capacity[source][v] > 0:  # If the capacity of the source at vertex v is positive
            graph.flow[source][v] = graph.capacity[source][v]
            graph.flow[v][source] = -graph.flow[source][v]
            excess[v] = graph.capacity[source][v]
            excess[source] -= graph.capacity[source][v]

    # Function to push the flow from u to v
    def push(u, v):
        delta = min(excess[u], graph.capacity[u][v] - graph.flow[u][v])
        graph.flow[u][v] += delta  # Updating the flow from u to v
        graph.flow[v][u] -= delta  # Updating the flow from v to u
        excess[u] -= delta  # Reducing the excess flow at u
        excess[v] += delta  # Increasing the excess flow at v
        print(f"\nPush from {u} to {v} (excess diff = {delta}):")


    # Function to relabel a vertex u
    def relabel(u):
        min_height = float('Inf')
        for v in range(n):
            if graph.capacity[u][v] > graph.flow[u][v]:  # If the residual capacity is positive
                min_height = min(min_height, height[v])  # Find the minimal height trough neighbours
        old_height = height[u]
        height[u] = min_height + 1  # Relabel u with new height
        print(f"\nRelabel node {u} (height {old_height} → {height[u]}):")

    # Function to discharge a vertex u
    def discharge(u):
        while excess[u] > 0:
            if seen[u] < n:
                v = seen[u]
                if graph.capacity[u][v] > graph.flow[u][v] and height[u] > height[v]:
                    push(u, v)
                else:
                    seen[u] += 1
            else:
                relabel(u)  # Relabelling u if all neighbours have been iterated through
                seen[u] = 0

    active = [i for i in range(n) if i != source and i != sink]

    while any(excess[i] > 0 for i in active):  # Until there are vertices with exceeding flows
        for u in active:
            if excess[u] > 0:
                discharge(u)

    # Returning the maximum flow
    return sum(graph.flow[v][sink] for v in range(n))


def bellman_ford(residual, cost, source, n):
    """
        Runs the Bellman-Ford algorithm to find shortest paths from source.

        Args:
            residual (list[list[int]]): Residual capacities.
            cost (list[list[int]]): Cost matrix.
            source (int): Source node.
            n (int): Number of nodes.

        Returns:
            tuple: (distances, predecessors)
    """
    dist = [float('Inf')] * n
    pred = [-1] * n
    dist[source] = 0

    for _ in range(n - 1):
        for u in range(n):
            for v in range(n):
                if residual[u][v] > 0 and dist[u] + cost[u][v] < dist[v]:  # If there's a residual capacity and a shorter path
                    dist[v] = dist[u] + cost[u][v]
                    pred[v] = u

    return dist, pred

def min_cost_flow(graph, target_flow):
    """
        Computes the minimum-cost maximum flow for a given flow target using successive shortest augmenting paths.

        Args:
            graph: Graph object with residual, cost, and flow matrices.
            target_flow (int): Desired flow to reach.

        Returns:
            int or None: Total cost of achieving target_flow, or None if impossible.
    """
    n = graph.n
    source = 0
    sink = n - 1
    total_cost = 0
    flow = 0

    while flow < target_flow:
        dist, pred = bellman_ford(graph.residual, graph.cost, source, n)

        # Checking for the presence of a negative cycle
        for u in range(n):
            for v in range(n):
                if graph.residual[u][v] > 0 and dist[u] + graph.cost[u][v] < dist[v]:
                    raise ValueError("Negative cycle detected in the graph.")

        # Checking for a new path
        if dist[sink] == float('Inf'):
            print("No path is available to reach the target flow. ")
            break

        # Finding the maximum flow to push in this path
        path_flow = float('Inf')
        v = sink
        while v != source:
            u = pred[v]
            if u == -1:
                raise ValueError("Invalid path. ")
            path_flow = min(path_flow, graph.residual[u][v])
            v = u

        # Limiting the flow for it not to exceed the target flow left
        path_flow = min(path_flow, target_flow - flow)

        v = sink
        while v != source:
            u = pred[v]
            # Updating residual graph
            graph.residual[u][v] -= path_flow
            graph.residual[v][u] += path_flow

            # Updating flow matrix
            graph.flow[u][v] += path_flow
            graph.flow[v][u] -= path_flow

            # Updating total cost
            total_cost += path_flow * graph.cost[u][v]
            v = u

        flow += path_flow
        print(f"Added flow: {path_flow}, Total flow : {flow}, Total cost : {total_cost}")

    # Checking if target flow has been reached
    if flow < target_flow:
        print("Reaching the target flow is impossible with the current capacities. ")
        return None

    return total_cost
