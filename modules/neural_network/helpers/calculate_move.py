import numpy as np

from ...game import Game
from ..models.main_model import MainModel
from ..utils.direction_converter import direction_converter
from ..utils.get_angle import get_angle
from ..utils.get_distance import get_distance

def calculate_move(game: Game, nn: MainModel):
  head_coords = game.current_head_coords
  food_coords = game.current_food_coords

  angle_between_head_and_food = get_angle(head_coords, food_coords)
  distance_between_head_and_food = get_distance(head_coords, food_coords)

  current_direction = game.direction

  result = nn.feedforward([[angle_between_head_and_food], [distance_between_head_and_food]])

  directions = [(0, 1), (-1, 0), (1, 0)]
  direction_index = np.argmax(result)

  chosen_direction = directions[direction_index]

  # Because the neural network is trained to move in perspective of the snake,
  # we need to convert the actual absolute direction to the perspective of the snake.

  # For example, if the snake is moving to the "right" and the neural network output is "right" the snake should move "down"
  # and if the neural network output is "left" the snake should move "up"

  # To avoid complex vector transform calculations, i stored the directions in a 4x4 matrix "direction_converter"

  next_direction = direction_converter[
    current_direction[0]
  ][
    current_direction[1]
  ][
    chosen_direction[0]
  ][
    chosen_direction[1]
  ]

  return next_direction