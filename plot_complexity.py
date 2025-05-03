import matplotlib.pyplot as plt

def read_execution_time_data(path_to_file) -> dict:
    with open(path_to_file, "r") as f:
        data = eval(f.read())

    thetas_ff = {}
    thetas_pr = {}
    thetas_mcf = {}
    
    for size in data.keys():
        thetas_ff[size] = []
        thetas_pr[size] = []
        thetas_mcf[size] = []

    for size in data.keys():
        thetas_ff[size] = data[size]["thetas_ff"]
        thetas_pr[size] = data[size]["thetas_pr"]
        thetas_mcf[size] = data[size]["thetas_mcf"]

    return thetas_ff, thetas_pr, thetas_mcf
    

def plot_point_cloud(results:dict, algorithm_name:str):
    plt.figure(figsize=(10, 6))
    match algorithm_name:
        case "ff":
            color = "blue"
            label = "θFF(n)"
        case "pr":
            color = "red"
            label = "θPR(n)"
        case "mcf":
            color = "green"
            label = "θMCF(n, cost//2)"
        case _:
            color = "black"
            label = "?"


    for n_val, thetas in results.items():
        # Plot Ford-Fulkerson results
        plt.scatter([n_val] * len(thetas), thetas, 
                    color=color, label=label if n_val == next(iter(results.keys())) else "", alpha=0.6)
    plt.xlabel('n -> # vertices in the problem')
    plt.ylabel('Time (seconds)')
    plt.title('Point Cloud: Execution times in function of n')
    plt.legend(title="Algorithm", loc='upper left', fontsize=10)

    plt.grid(True)
    plt.show()




if __name__ == "__main__":
    thetas_ff, thetas_pr, thetas_mcf = read_execution_time_data("execution_trace_2.txt")
    
    for thetas, algoname in [[thetas_ff, "ff"], [thetas_pr, "pr"], [thetas_mcf, "mcf"]]:
        print(f"\nPlot for {algoname}. Close the window to proceed.\n")
        plot_point_cloud(thetas, algoname)


    thetas_ff_over_pr = {size: [ff / pr for ff, pr in zip(thetas_ff[size], thetas_pr[size])] for size in thetas_ff.keys()}

    print(f"\n Plot for FF/PR.\n")
    plot_point_cloud(thetas_ff_over_pr, "shhhhhhhh")
