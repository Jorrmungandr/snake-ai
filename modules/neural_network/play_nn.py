from ..game import Game, Matrix
from .models.main_model import MainModel
from .helpers.calculate_move import calculate_move

def play_nn(config, nn: MainModel):
  matrix_manager = Matrix(*config['game_dimensions'])
  game_manager = Game(matrix_manager)

  score = 0

  while game_manager.over == False:
    new_direction = calculate_move(game_manager, nn)

    game_manager.direction = new_direction

    colision = game_manager.run_step()

    if (colision == 'wall' or colision == 'body' or colision == 'energy'):
      game_manager.over = True

    if (colision == 'food'):
      score += 1

    game_manager.direction = new_direction

  return score, nn.biases, nn.weights
