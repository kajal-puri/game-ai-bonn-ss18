import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from sys import maxint

DATA_PATH = './data/simpleMap-1-20x20.txt'
# DATA_PATH = './data/simpler.txt'


def minimum_node(set):
    minValue = maxint
    minIndex = 0
    for i in range(len(set)):
        if set[i] < minValue:
            minValue = set[i]
            minIndex = i
    return (minValue, minIndex)

def get_minimum(set):
    # TODO optimize this with min-heap
    minValue = maxint
    minIndex = 0
    for i in range(len(set)):
        if set[i] < minValue:
            minValue = set[i]
            minIndex = i
    return (minValue, minIndex)
visited_dict = {}
cost_dict = {}
par_dict = {}
def get_cost(node):
    if cost_dict.has_key(node) == False:
        return maxint
    return cost_dict[node]

def set_parent(node, parent, cost):
    cost_dict[node] = cost
    par_dict[node] = parent

def calculate_dijkstra(g, s, v):
    visited_dict = {}
    cost_dict = {}
    par_dict = {}
    q = []
    q.append(s)
    set_parent(s, s, 0)


    while(len(q) != 0):
        min = get_minimum(q)
        parent = q[min[1]]

        if (parent == v):
            break;
        
        visited_dict[parent] = True
        cost = get_cost(parent)
        neighbors = nx.all_neighbors(g, parent)

        for neighbor in neighbors:
            if visited_dict.has_key(neighbor) == False:
                c = get_cost(neighbor)
                if c > cost + 1:
                    set_parent(neighbor, parent, cost + 1)
                
                q.append(neighbor)
            
        q.remove(parent)
    
    
def dijkstra_path(g, s, v):
    calculate_dijkstra(g, s, v)
    path = [v]
    cur = v
    while cur != s:
        cur = par_dict.get(cur)
        path.append(cur)
    return path

if __name__ == '__main__':
    # read input text and parse the graph
    mat = np.flip(np.loadtxt(DATA_PATH, delimiter=' ').T, 1)
    g = nx.grid_2d_graph(mat.shape[0], mat.shape[1])
    pos = dict((n, n) for n in g.nodes())

    for x, y in g.edges():
        g[x][y]['weight'] = 1.0

    walls = []
    for ix, iy in np.ndindex(mat.shape):
        if mat[ix, iy] == 1:
            walls.append((ix, iy))
    walls = dict([(n, n) for n in walls])

    s = (1, 10)[::-1]
    v = (7, 3)[::-1]
    # path2 = dijkstra_path(g, s, v)

    # print path2


    # set plot settings
    fig = plt.figure('1')
    plt.axis('equal')
    fig.patch.set_facecolor('beige')

    # remove walls from the graph
    g.remove_nodes_from(walls)

    # draw nodes and their connecting edges
    nodes = nx.draw_networkx_nodes(g, pos=pos, node_size=30, with_labels=False, node_color='w')
    nodes.set_edgecolor('black')
    edges = nx.draw_networkx_edges(g, pos=pos, node_size=30, with_labels=False, edge_color='r')

    # calculate the shortest path between some arbitrary points s and v with dijkstra algorithm
    s = (10, 1)[::-1]
    v = (2, 15)[::-1]
    path = nx.dijkstra_path(g, s, v)
    path2 = dijkstra_path(g, s, v)
    path_edges = zip(path, path[1:])

    # highlight the start point
    nx.draw_networkx_nodes(g, pos, nodelist=[s], node_color='steelblue', node_size=80)
    # highlight the end point
    nx.draw_networkx_nodes(g, pos, nodelist=[v], node_color='orangered', node_size=80)
    # draw the shortest-path on the graph
    nx.draw_networkx_edges(g, pos, edgelist=path_edges, edge_color='mediumaquamarine', width=5)

    # hide the axes and show the plot
    # plt.axis('off')
    # plt.show()
