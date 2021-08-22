codes = {
  'empty': 0,
  'wall': 1,
  'head': 2,
  'body': 3,
  'food': 4
}

codeArray = ['empty', 'wall', 'head', 'body', 'food']

class MatrixManager:
  matrix = []
  width = 0
  height = 0

  def __init__(self, width, height, base_matrix = None):
    self.width = width
    self.height = height

    if (base_matrix):
      self.matrix = [*base_matrix]
    else:
      self.mount_matrix(width, height)

  def mount_matrix(self, width, height):
    self.matrix.append([codes['wall']] * (width + 2))

    for i in range(height):
      line = []

      for j in range(width):
        line.append(codes['empty'])

      self.matrix.append([
        codes['wall'],
        *line,
        codes['wall'],
      ])

    self.matrix.append([codes['wall']] * (width + 2))


  def set_pixel(self, coords, type):
    x, y = coords
    self.matrix[self.height - y][x + 1] = codes[type]

  def get_pixel(self, coords):
    x, y = coords
    value = self.matrix[self.height - y][x + 1]

    return codeArray[value]

  def replace(self, matrix):
    self.matrix = matrix.copy()
