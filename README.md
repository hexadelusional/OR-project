# Operations Research Project

---
Small python app able to :
  - read and understand txt files describing flow problems
  - display in tabular form their capacity matrix, and costs matrix
  - for max flow problem descriptions, use FF or PR method to find the max flow possible
  - for min cost flow problem descriptions, do the same as before, and also apply bellman-ford to
compute the cost provided a particular flow

---
## USAGE
Before anything : 
- `git clone https://github.com/hexadelusional/OR-project` into the folder of your choice

### Interactive mode:
- `py main.py` to run the app. Then, follow the instructions given in the CLI.

### Complexity analysis:
- `py complexity.py` to launch complexity computations. We recommend using pypy instead of py to speed up process
- `py plot_complexity.py` to plot the data previously collected

### Trace generation:
- `py generate_traces.py` to create all traces under .txt format