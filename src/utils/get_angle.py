import math

def get_angle(coordsA, coordsB):
  x1, y1 = coordsA
  x2, y2 = coordsB
  return math.degrees(math.atan2(y2 - y1, x2 - x1))
