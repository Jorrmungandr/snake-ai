import math
import random
from managers.matrix import MatrixManager

class GameManager():
  matrix_manager = None
  snake_ghost = []
  snake_size = 1
  direction = 'up'
  logs = False
  over = False

  def __init__(self, matrix_manager, logs = False):
    self.matrix_manager = matrix_manager
    self.logs = logs

    self.spawn_snake()
    self.spawn_random_food()

  def spawn_snake(self):
    middle_height = math.ceil(self.matrix_manager.height / 2)
    middle_width = math.ceil(self.matrix_manager.width / 2)

    self.matrix_manager.set_pixel((middle_width - 1, middle_height - 1), 'head')
    self.snake_ghost = [
      { 'coords': (middle_width - 1, middle_height - 1), 'age': 1 },
    ]

  def spawn_random_food(self):
    def get_random_coords():
      random_x = random.randint(1, self.matrix_manager.width)
      random_y = random.randint(1, self.matrix_manager.height)

      return (random_x, random_y)

    def place_food():
      coords = get_random_coords()

      if self.matrix_manager.get_pixel(coords) == 'empty':
        self.matrix_manager.set_pixel(coords, 'food')
      else:
        place_food()

    place_food()

  def compile_output(self, direction):
    colision = None

    new_matrix_manager = MatrixManager(
      self.matrix_manager.width,
      self.matrix_manager.height,
      self.matrix_manager.matrix,
    )

    change_list = []

    for x in range(new_matrix_manager.width):
      for y in range(new_matrix_manager.height):
        cell_value = self.matrix_manager.get_pixel((x, y))

        output_dict = {
          'up': (x, y + 1),
          'down': (x, y - 1),
          'right': (x + 1, y),
          'left': (x - 1, y)
        }

        if (cell_value == 'head'):
          next_x, next_y = output_dict[direction]

          next_pixel = self.matrix_manager.get_pixel((next_x, next_y))

          if (next_pixel == 'wall'): colision = 'wall'
          elif (next_pixel == 'body'): colision = 'body'
          else:
            if next_pixel == 'food':
              colision = 'food'
              self.spawn_random_food()

            change_list.append({ 'coords': (next_x, next_y), 'type': 'head' })
            change_list.append({ 'coords': (x, y), 'type': 'body' })

            prev_snake_ghost = self.snake_ghost
            next_snake_ghost = []

            next_snake_ghost.append({ 'coords': (next_x, next_y), 'age': 1 })

            for snake_bodypart in prev_snake_ghost:
              if (snake_bodypart['age'] <= self.snake_size):
                next_snake_ghost.append({
                  'coords': snake_bodypart['coords'],
                  'age': snake_bodypart['age'] + 1,
                })
              else:
                change_list.append({ 'coords': snake_bodypart['coords'], 'type': 'empty' })

            self.snake_ghost = next_snake_ghost

    for dict in change_list:
      new_matrix_manager.set_pixel(dict['coords'], dict['type'])

    return new_matrix_manager.matrix, colision
