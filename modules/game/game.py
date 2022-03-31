import math
import random

from .matrix import Matrix

class Game():
  def __init__(self, matrix_manager: Matrix):
    self.matrix_manager = matrix_manager
    self.snake_ghost = []
    self.snake_size = 1
    self.current_food_coords = None
    self.current_head_coords = None
    self.direction = (0, 1)
    self.over = False

    number_of_tiles_in_board = matrix_manager.height * matrix_manager.width
    self.default_energy = number_of_tiles_in_board
    self.current_energy = number_of_tiles_in_board

    self.spawn_snake()
    self.spawn_random_food()

  def spawn_snake(self):
    middle_height = math.ceil(self.matrix_manager.height / 2)
    middle_width = math.ceil(self.matrix_manager.width / 2)

    self.matrix_manager.set_pixel((middle_width - 1, middle_height - 1), 'head')
    self.current_head_coords = (middle_width - 1, middle_height - 1)
    self.snake_ghost = [
      { 'coords': (middle_width - 1, middle_height - 1), 'age': 1 },
    ]

  def spawn_random_food(self):
    empty_nodes = []

    for x in range(self.matrix_manager.width):
      for y in range(self.matrix_manager.height):
        node_value = self.matrix_manager.get_pixel((x, y))

        if (node_value == 'empty'):
          empty_nodes.append((x, y))

    if (len(empty_nodes) == 0): return

    random_index = random.randint(0, len(empty_nodes) - 1)

    coords = empty_nodes[random_index]

    self.matrix_manager.set_pixel(coords, 'food')
    self.current_food_coords = coords

  def calculate_output_matrix(self):
    colision = None

    change_list = []

    x, y = self.current_head_coords

    next_x, next_y = (x + self.direction[0], y + self.direction[1])

    next_pixel = self.matrix_manager.get_pixel((next_x, next_y))

    if (next_pixel == 'wall'): colision = 'wall'
    elif (next_pixel == 'body'): colision = 'body'
    else:
      self.current_energy -= 1

      if next_pixel == 'food':
        colision = 'food'
        self.current_energy = self.default_energy
        self.spawn_random_food()

      if (self.current_energy == 0):
        colision = 'energy'
      else:
        change_list.append({ 'coords': (next_x, next_y), 'type': 'head' })
        self.current_head_coords = (next_x, next_y)
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

    new_matrix_manager = Matrix(
      self.matrix_manager.width,
      self.matrix_manager.height,
      self.matrix_manager.matrix,
    )

    for dict in change_list:
      new_matrix_manager.set_pixel(dict['coords'], dict['type'])

    return new_matrix_manager.matrix, colision

  def run_step(self):
    new_matrix, colision = self.calculate_output_matrix()

    self.matrix_manager.replace(new_matrix)

    if (colision == 'wall' or colision == 'body'):
      self.over = True

    if (colision == 'food'):
      self.snake_size += 1

    return colision
