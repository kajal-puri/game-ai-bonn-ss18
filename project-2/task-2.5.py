import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

DATA_PATH = './data/simpleMap-1-20x20.txt'

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
    path_edges = zip(path, path[1:])

    # highlight the start point
    nx.draw_networkx_nodes(g, pos, nodelist=[s], node_color='steelblue', node_size=80)
    # highlight the end point
    nx.draw_networkx_nodes(g, pos, nodelist=[v], node_color='orangered', node_size=80)
    # draw the shortest-path on the graph
    nx.draw_networkx_edges(g, pos, edgelist=path_edges, edge_color='mediumaquamarine', width=5)

    # hide the axes and show the plot
    plt.axis('off')
    plt.show()
