from graph import Graphic
from algorithms import *
import copy

def main():
    print("Welcome to our Operations Research project !")
    
    running = True
    while running:
        # Ask the user to choose a file
        file_choice_loop = True
        while file_choice_loop:
            try:
                file_choice = int(input("\nChoose a number between 1 and 10 (0 to exit): "))
                if 0 <= file_choice <= 10:
                    break
                else:
                    print("Choose a number between 1 and 10 (0 to exit): ")
            except ValueError:
                print("Invalid number. Choose a number between 1 and 10: ")
        
        if file_choice == 0:
            print("ok Bye !")
            break 


        # File path
        file = f"Propositions/Proposition {file_choice}.txt"
        print(f"File selected : {file}")
        
        # Display the corresponding graph
        try:
            graph = Graphic.read_graph(file)
            graph.display()
        except FileNotFoundError:
            print("The specified file can't been found. Please make sure the file exists. ")
            return
        
        # Ask the user to choose an algorithm
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
                print("Invalid input. Please indicate a algorithm number. ")

        # Execute the chosen algorithm
        if algo_choice == 1:
            max_flow = ford_fulkerson(graph)
            graph.display_flow()
            print(f"\nMaximal flow with Ford-Fulkerson : {max_flow}")
        elif algo_choice == 2:
            max_flow = push_relabel(graph)
            graph.display_flow()
            print(f"\nMaximal flow with Push-Relabel : {max_flow}")
        elif algo_choice == 3:
            copy_graph = copy.deepcopy(graph)
            max_flow = ford_fulkerson(copy_graph)
            while True:
                try:
                    print(f"\nThe maximum flow is of {max_flow}.", end=" ")
                    target_flow = int(input("Enter the value of target flow : "))
                    if target_flow > 0 and target_flow <= max_flow:
                        break
                    else:
                        print("Please enter a valid target flow.")
                except ValueError:
                    print("Invalid target number. Please enter a valid target number.")
            
            total_cost = min_cost_flow(graph, target_flow)
            graph.display_flow()
            print(f"\nTotal cost of the flow : {total_cost}")

if __name__ == "__main__":
    main()
