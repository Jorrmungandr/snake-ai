import numpy as np

from game.managers.game import GameManager
from neural_network.base_model import BaseModel
from utils.get_angle import get_angle
from utils.get_distance import get_distance

absolute_direction_converter = (
  (
    (),
    (
      (
        None,
        (0, 1)
      ),
      (
        (1, 0),
      ),
      (
        (-1, 0),
      ),
    ),
    (
      (
        None,
        (-1, 0),
      ),
      (
        (1, 0),
      ),
      (
        (1, 0),
      ),
    ),
  ),
  (
    (
      (
        None,
        (1, 0),
      ),
      (
        (0, -1),
      ),
      (
        (0, 1),
      ),
    ),
  ),
  (
    (
      (
        None,
        (-1, 0),
      ),
      (
        (0, 1),
      ),
      (
        (0, -1),
      ),
    ),
  ),
)

def calculate_move(game_manager: GameManager, nn: BaseModel):
  head_coords = game_manager.current_head_coords
  food_coords = game_manager.current_food_coords

  angle_between_head_and_food = get_angle(head_coords, food_coords)
  distance_between_head_and_food = get_distance(head_coords, food_coords)

  result = nn.feedforward([[angle_between_head_and_food], [distance_between_head_and_food]])
  direction_index = np.argmax(result)
  directions = [(0, 1), (-1, 0), (1, 0)]
  chosen_direction = directions[direction_index]

  next_direction = absolute_direction_converter[
    game_manager.direction[0]
  ][
    game_manager.direction[1]
  ][
    chosen_direction[0]
  ][
    chosen_direction[1]
  ]

  new_matrix, colision = game_manager.compile_output(next_direction)

  return next_direction, new_matrix, colision