# naming conventions are: 

# "Group B - Team 4 - Problem 5 - Ford-Fulkerson"
# "“B4-trace5-FF.txt”"
import os



PATH_TO_PROPOSITIONS = r"Propositions"

propositions = os.listdir(PATH_TO_PROPOSITIONS)
algorithms = ["FF", "PR", "MCF"]

try:
    os.chdir("traces")
except:
    os.mkdir("traces")
    os.chdir("traces")


from algorithms import ford_fulkerson, push_relabel, min_cost_flow

from graph import Graphic

os.chdir("../Propositions")

for i in range(1,11):
    # open the graph
    graph = Graphic(0)
    graph = Graphic.read_graph(f"Proposition {i}.txt")

    for algo in ["FF", "PR", "MIN"]:
        with open(os.path.join("../traces/", f"INT1_5-trace{i}-{algo}.txt"), "w", encoding="utf8") as trace:
            graph.display(trace)
            match algo:
                case "FF":
                    max_flow = ford_fulkerson(graph, output=trace)
                    graph.display_flow(output=trace)
                    trace.write(f"Value of max flow = {max_flow}")
                case "PR":
                    max_flow = push_relabel(graph, output=trace)
                    trace.write(f"value of max flow = {max_flow}")
                case "MIN":
                    if i > 5:
                        min_cost_flow(graph, max_flow, output=trace)
                    else:
                        trace.write("MIN does not apply here")
            
        
            

        

