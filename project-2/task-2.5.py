import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

DATA_PATH = './data/simpleMap-1-20x20.txt'

if __name__ == '__main__':
    mat = np.flip(np.loadtxt(DATA_PATH, delimiter=' ').T, 1)
    g = nx.grid_2d_graph(mat.shape[0], mat.shape[1])
    pos = dict((n, n) for n in g.nodes())

    walls = []
    for ix, iy in np.ndindex(mat.shape):
        if mat[ix, iy] == 1:
            walls.append((ix, iy))
    walls = dict([(n, n) for n in walls])

    g.remove_nodes_from(walls)
    
    nx.draw_networkx(g, pos=pos, node_size=10, with_labels=False)
    plt.axis('off')
    plt.show()
