codes = {
  'empty': 0,
  'wall': 1,
  'head': 2,
  'body': 3,
  'food': 4
}

class MatrixService:
  matrix = []
  height = 0
  width = 0

  def __init__(self, width, height):
    self.width = width
    self.height = height

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


  def set_pixel(self, x, y, type):
    self.matrix[self.width - y][x + 1] = codes[type]

  def get_pixel(self, x, y):
    return self.matrix[self.width - y][x + 1]
