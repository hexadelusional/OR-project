from graph import Graphic
from algorithms import *
from utils import print_matrix, bold
import copy

def main():
    print_matrix([['Ingé1 INT-1 • Group 5'], ['Adèle Chamoux'], ['Mattéo Launay'], ['Paul Leflon'], ['Iriantsoa Rasoloarivalona']], header_column=False)
    print(bold("Welcome to our Operations Research project !"))

    running = True
    while running:
        # Asking the user to choose a proposal file
        file_choice_loop = True
        while file_choice_loop:
            try:
                file_choice = int(input("\nChoose a proposal between 1 and 10 (0 to exit): "))
                if 0 <= file_choice <= 10:
                    break
                else:
                    print("Choose a proposal between 1 and 10 (0 to exit): ")
            except ValueError:
                print("Invalid proposal. Please indicate a proposal number between 1 and 10: ")
        
        if file_choice == 0:
            print(bold("Bye !"))
            break

        # Setting the file path
        file = f"Propositions/Proposition {file_choice}.txt"
        print(f"You chose the following proposal : {file}")
        
        # Loading the graph
        try:
            graph = Graphic.read_graph(file)
            graph.display()
        except FileNotFoundError:
            print("The specified file can't been found. Please make sure the file exists. ")
            return
        
        # Asking the user to choose an algorithm
        print("\nChoose an algorithm to treat the problem:")
        print("1. Ford-Fulkerson")
        print("2. Push-Relabel")
        if graph.has_costs():
            print("3. Minimal cost flow (Bellman-Ford)")
        
        algo_choice_loop = True
        while algo_choice_loop:
            try:
                algo_choice = int(input("\nEnter the number of the algorithm (0 to go back): "))

                if algo_choice == 0:
                    print("You choose to go back.")
                    algo_choice_loop = False
                elif not graph.has_costs() and algo_choice in [1, 2]:
                    break
                elif graph.has_costs() and algo_choice in [1, 2, 3]:
                    break
                else:
                    print("Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please indicate a algorithm number between 1 and 2. ")

        # Executing the chosen algorithm
        if algo_choice == 1:
            max_flow = ford_fulkerson(graph)
            graph.display_flow()
            print(f"\nMaximal flow with Ford-Fulkerson : {bold(max_flow)}")
        elif algo_choice == 2:
            max_flow = push_relabel(graph)
            graph.display_flow()
            print(f"\nMaximal flow with Push-Relabel : {bold(max_flow)}")
        elif algo_choice == 3:
            copy_graph = copy.deepcopy(graph)
            max_flow = ford_fulkerson(copy_graph)
            while True:
                try:
                    print(f"\nThe maximum flow is of {bold(max_flow)}. \n")
                    target_flow = int(input("Enter the value of target flow : "))
                    if target_flow > 0 and target_flow <= max_flow:
                        break
                    else:
                        print("Please enter a valid target flow.")
                except ValueError:
                    print("Invalid target number. Please enter a valid target number.")
            
            total_cost = min_cost_flow(graph, target_flow)
            graph.display_flow()
            print(f"\nTotal cost of the flow :", bold(f"{total_cost}"))

if __name__ == "__main__":
    main()
