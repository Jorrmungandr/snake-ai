import pygame
import threading
import numpy as np
import os

from ...gui.renderer import BoardRenderer
from ...game import Game, Matrix, codeArray
from ..models.main_model import MainModel
from ..helpers.calculate_move import calculate_move
from ...gui.utils.load_yaml import load_yaml

pygame.init()
pygame.font.init()

config = load_yaml(os.path.join(os.path.dirname(os.path.realpath('__file__')), 'modules/neural_network/default_config.yaml'))

node_width = config['window_dimensions'][0] / (config['game_dimensions'][0] + 2)
node_height = config['window_dimensions'][1] / (config['game_dimensions'][1] + 2)

matrix_manager = Matrix(*config['game_dimensions'])
game_manager = Game(matrix_manager)

screen = pygame.display.set_mode(config['window_dimensions'])

renderer = BoardRenderer(screen, node_width, node_height)

with open('saves/save.npy', 'rb') as f:
  file = np.load(f, allow_pickle = True)

  biases, weights = file

  nn = MainModel([2, 15, 15, 3], biases, weights)
  nn.random_seed()

  def loop_output():
    def neural_net_move():
      new_direction = calculate_move(game_manager, nn)

      game_manager.direction = new_direction
      colision = game_manager.run_step()

      if (colision == 'wall' or colision == 'body' or colision == 'energy'):
        game_manager.over = True
        score = game_manager.snake_size - 1
        renderer.game_over(score, config['window_dimensions'])

      if (colision == 'food'):
        game_manager.snake_size += 1

      if (not game_manager.over): loop_output()

    t = threading.Timer(config['snake_speed'], neural_net_move)
    t.start()
    return t

  loop_output()

  running = True

  while running:
    if (game_manager.over == False):
      renderer.matrix(game_manager.matrix_manager.matrix, config['colors'], codeArray)

    pygame.display.flip()

  game_manager.over = True
  pygame.quit()
