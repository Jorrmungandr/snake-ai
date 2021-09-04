import numpy as np

def get_distance(coordsA, coordsB):
  pointA = np.array(coordsA)
  pointB = np.array(coordsB)

  return np.linalg.norm(pointA - pointB)
