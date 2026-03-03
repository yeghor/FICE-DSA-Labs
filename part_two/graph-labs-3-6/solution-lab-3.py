from graph_engine.ge_triangular import GraphEngine
from string import Template

# GraphEngine itself search in "part_two/graph-labs-3-6/graph_engine/ge_triangular.py"
if __name__ == "__main__":
    ge = GraphEngine(koef_template=Template("1.0 - $first * 0.02 - $second * 0.005 - 0.25"),  node_radius=100)
    print("Plotting not directed graph...")
    ge.plot_graph(100, 100, False)
    print("Plotting directed graph")
    ge.plot_graph(100, 100, True)
