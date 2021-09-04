from game.managers.matrix import MatrixManager
from game.managers.game import GameManager
from neural_network.base_model import BaseModel
from neural_network.calculate_move import calculate_move

def play_nn(config, nn: BaseModel):
  matrix_manager = MatrixManager(*config['game_dimensions'])
  game_manager = GameManager(matrix_manager)

  score = 0

  while game_manager.over == False:
    new_direction, new_matrix, colision = calculate_move(game_manager, nn)

    game_manager.matrix_manager.replace(new_matrix)

    if (colision == 'wall' or colision == 'body' or colision == 'energy'):
      game_manager.over = True
      # score = game_manager.snake_size - 1

    if (colision == 'food'):
      score += 1

    game_manager.direction = new_direction

  return score, nn.biases, nn.weights
