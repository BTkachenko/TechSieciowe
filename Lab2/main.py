import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import argparse
from statistics import mean
import math
# import matplotlib.pyplot as plt


import random as rand


def system_test(graph, matrix, reps=1000):
    delays = []
    for rep in range(reps):
        g = nx.Graph(graph)

        for e in graph.edges():
            if rand.random() > g.get_edge_data(*e).get('p'):
                g.remove_edge(*e)

        if not nx.is_connected(g):
            continue

        set_a(g, matrix)

        for e in g.edges():
            if g.get_edge_data(*e).get('a') > g.get_edge_data(*e).get('c'):
                break
        else:
            delays.append(delay(g, matrix))

    if len(delays) == 0:
        print("failed")
        return 1
    else:
        print("Succeded in", len(delays) / reps * 100, "%. Average delay:", sum(delays) / len(delays))

    return delays


def reliability(graph, matrix, Tmax, p=0.95):
    g = nx.Graph(graph)
    nx.set_edge_attributes(g, p, 'p')
    delays = system_test(g, matrix) or [1]
    counter = 0

    if isinstance(delays, list):
        for d in delays:

            if d < Tmax:
                counter += 1
        return counter / len(delays) * 100


def approx(G):
    counter = 0
    for i in range(10000):
        Gprim = nx.Graph(G)
        for e in G.edges:
            if (rand.random() > G.get_edge_data(*e).get("p")):
                Gprim.remove_edge(*e)
        if (nx.is_connected(Gprim)):
            counter = counter + 1
    print(counter / 10000)


C = nx.cycle_graph(20)

C1 = nx.Graph(C)
for i in range(1, 10):
    C1.add_edge(i * 2, i % 2)
nx.set_edge_attributes(C1, 0.95, 'p')
nx.set_edge_attributes(C1, 0, 'a')
nx.set_edge_attributes(C1, 1500, 'c')
nx.draw(C1)
plt.show()


# N def
SIZE = C1.number_of_nodes()
N = np.zeros((SIZE, SIZE))
for i in range(SIZE):
    for j in range(SIZE):
        if i == j:
            N[i][j] = 0
        else:
            N[i][j] = rand.randint(0, 30)




# Funkcja opóżnienia T
def delay(Graph, Nmatrix):
    G = Nmatrix.sum()
    return (1 / G) * (
        sum([Graph.get_edge_data(*e).get('a') / (((Graph.get_edge_data(*e).get('c') / 1)- Graph.get_edge_data(*e).get('a')))
             for e in Graph.edges()]))


# a - suma natężeń na najkrótszej ścieżce
def set_a(Graph, Nmatrix):
    nx.set_edge_attributes(Graph, 0, 'a')
    for i, row in enumerate(Nmatrix):
        for j, n in enumerate(row):
            path = nx.shortest_path(Graph, i, j)
            for k in range(len(path) - 1):
                Graph[path[k]][path[k + 1]]['a'] += n


set_a(C1, N)
Nt = N

print("Przykladowe wywołanie z domyslnymi parametrami: ")
print("Realiability: ", reliability(C1, N, 0.005, 0.95), "%")
print("________________________________\n\n")

print("Przepustowosc powiekszana o 200 co krok(3 razy):")
print("Realiability: ", reliability(C1, N, 0.005, 0.95), "%")
nx.set_edge_attributes(C1, 1700, 'c')
print("Realiability: ", reliability(C1, N, 0.005, 0.95), "%")
nx.set_edge_attributes(C1, 1900, 'c')

print("Realiability: ", reliability(C1, N, 0.005, 0.95), "%")
nx.set_edge_attributes(C1, 2100, 'c')
print("Realiability: ", reliability(C1, N, 0.005, 0.95), "%")
nx.set_edge_attributes(C1, 1500, 'c')

print("________________________________\n\n")





print("MyGraph test with N*1.2 every round (5 times):")
for i in range(1, 6):
    print("Realiability: dla kroku #",i,"  = ",reliability(C1, Nt, 0.005, 0.95), "%")
    Nt = Nt * 1.1
    print("________________________________")

print("________________________________\n\n")

C2 = nx.Graph(C1)
for i in range(1, 10):
    C2.add_edge(20-(i * 2), 20-(i % 2))
nx.set_edge_attributes(C2, 0.95, 'p')
nx.set_edge_attributes(C2, 0, 'a')
nx.set_edge_attributes(C2, 1500, 'c')
nx.draw(C2)
plt.show()
set_a(C2, N)



print("MyGraph2 test with N*1.1 every round (5 times):")
for i in range(1, 6):
    print("Realiability: dla kroku # ",i,"  =  ", reliability(C2, N, 0.005, 0.95), "%")
    N = N * 1.1
    print("________________________________")

print("________________________________\n\n")