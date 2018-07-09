from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt
import sys


def init_circular_weights(data, length=10):
  length += 1

  weights = np.zeros((length, data.shape[1]))
  angles = np.linspace(0, 2*np.pi, length)

  meanX = np.mean(data[:, 0])
  meanY = np.mean(data[:, 1])
  meanZ = np.mean(data[:, 2])

  minX = np.amin(data[:, 0])
  maxX = np.amax(data[:, 0])

  minY = np.amin(data[:, 1])
  maxY = np.amax(data[:, 1])

  radiusX = (maxX - minX) / 2.0
  radiusY = (maxY - minY) / 2.0

  weights[:, 0] = meanX + radiusX * np.sin(angles)
  weights[:, 1] = meanY + radiusY * np.cos(angles)
  weights[:, 2] = np.full(length, meanZ)

  return weights


def SOM(data, weights, shuffled_indices, learning_rate=1):
  graphs = []
  graph = np.copy(weights)
  tmax = len(shuffled_indices)
  length = len(weights)

  ##Populate Distance Matrix
  distances = np.zeros((length, length), dtype=int)
  for i in np.arange(length):
    for j in np.arange(length):
      distances[i, j] = np.amin([length - 1 + i - j, np.abs(i - j), np.abs(i - j - length + 1)])

  for t in np.arange(tmax):
    index = shuffled_indices[t]

    #Determine the winning neuron
    c = np.argmin(np.linalg.norm(graph - data[index, :], axis=1))

    eta = learning_rate * (1 - 1.0 * t / tmax)

    sigma = np.exp(- 1.0 * t / tmax)

    updateRule = eta * np.exp(-1.0 * distances[c, :] / (2.0 * sigma))

    graph = graph + np.multiply(updateRule, (data[index, :] - graph).T).T

    graphs.append(np.copy(graph))

  return graph, graphs  


if __name__ == "__main__":
  dataFile = sys.argv[1] if len(sys.argv) >= 2 else 'q3dm1-path1.csv'
  graphLength = int(sys.argv[2]) if len(sys.argv) >= 3 else 10
  learning_rate = float(sys.argv[3]) if len(sys.argv) >= 4 else 1

  data = np.genfromtxt(dataFile, delimiter=',')

  weights = init_circular_weights(data, graphLength)

  fig = plt.figure()
  ax = fig.add_subplot(111, projection="3d")

  ax.scatter(data[:, 0], data[:, 1], data[:, 2], c='w', edgecolors='k')

  ax.set_xlim([150, 1150])
  ax.set_ylim([1800, 2400])
  ax.set_zlim([0,55])

  ax.set_xlabel('X')
  ax.set_ylabel('Y')
  ax.set_zlabel('Z')

  SOMLine, = ax.plot(weights[:, 0], weights[:, 1], weights[:, 2], marker = 'o',
    markerfacecolor='r', markeredgecolor='k', color='b')

  selectedPoint, = ax.plot([], [], [], marker = 'o', markerfacecolor='k', markeredgecolor='k')

  def updateSelectedPoint(index):
    selectedPoint.set_data(data[index, 0], data[index, 1])
    selectedPoint.set_3d_properties(data[index, 2])
    return selectedPoint,

  def updateSOM(index):
    weights = updateGraphs[index]
    SOMLine.set_data(weights[:, 0], weights[:, 1])
    SOMLine.set_3d_properties(weights[:, 2])
    return SOMLine,


  indices = np.arange(data.shape[0])
  np.random.shuffle(indices)

  graph, updateGraphs = SOM(data, weights, indices, learning_rate)

  ani_1 = FuncAnimation(fig, updateSOM, frames=len(updateGraphs))

  ani_2 = FuncAnimation(fig, updateSelectedPoint, frames=indices)

  plt.show()
