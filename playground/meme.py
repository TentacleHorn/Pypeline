import time

import networkx as nx

g = nx.path_graph(100000, create_using=nx.DiGraph)
g: nx.DiGraph
# g = nx.DiGraph()
# g.add_edge(0, 1)
# g.add_edge(1, 2)
# g.add_edge(2, 3)

print(g)

# nx.draw(g)
# plt.savefig("./filename.png")

s = time.time()
r = g.predecessors(-1 * 1000)
print(time.time() - s)
