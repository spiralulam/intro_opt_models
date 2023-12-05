import random
from itertools import chain, combinations

import matplotlib.pyplot as plt
import mip
import networkx as nx
import numpy as np
from mip import BINARY, Model, minimize, xsum


# Computes the powerset of a set without the empty set and the set itself
def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(
        combinations(s, r) for r in range(3, len(s))
    )


# Generate N nodes with random distances
num_nodes = 100

nodes = range(num_nodes)
edges = set(combinations(nodes, 2))
random.seed(73)
coord = {
    n: (random.randint(0, 100), random.randint(0, 100)) for n in nodes
}
dist = {
    (n, m): np.sqrt(
        (coord[n][0] - coord[m][0]) ** 2
        + (coord[n][1] - coord[m][1]) ** 2
    )
    for (n, m) in edges
}

n_se_constrs = 0

# Optimization model
m = Model("TSP")

# Decision variable
x = {e: m.add_var(var_type=BINARY) for e in edges}

# constraint : leave and enter each node only once
for n in nodes:
    m += (
        xsum(x[n, v] for v in nodes if (n, v) in edges)
        + xsum(x[v, n] for v in nodes if (v, n) in edges)
        == 2
    )

# Objective
m.objective = minimize(xsum(dist[e] * x[e] for e in edges))

# optimizing
m.optimize()


def compute_cycles(x: mip.Var, nodes) -> list[list]:
    G = nx.Graph()
    G.add_nodes_from(nodes)
    edges_used = [e for e in x if x[e].x > 0.99]
    G.add_edges_from(edges_used)
    cycles = nx.minimum_cycle_basis(G)
    return cycles


cycles = compute_cycles(x, nodes)

while len(cycles[0]) < len(nodes):
    for cycle in cycles:
        cycle = sorted(cycle)
        m += (
            xsum(x[u, v] for (u, v) in combinations(cycle, 2))
            <= len(cycle) - 1
        )
        n_se_constrs += 1
    m.optimize()
    cycles = compute_cycles(x, nodes)


def draw_final_graph(x: mip.Var, nodes):
    G = nx.Graph()
    G.add_nodes_from(nodes)
    edges_used = [e for e in x if x[e].x > 0.99]
    G.add_edges_from(edges_used)
    nx.draw(G)
    plt.show()


print(f"{n_se_constrs} subtour elimination constraints were added.")

draw_final_graph(x, nodes)
