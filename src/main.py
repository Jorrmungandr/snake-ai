import pygame
import threading
import numpy as np
import math

from game.gui.renderer import BoardRenderer
from game.utils.load_config import load_config_dict
from game.managers.matrix import MatrixManager, codeArray
from game.managers.game import GameManager
from nn_generation.base_neural_network import BaseNeuralNetwork
from nn_generation.calculate_nn_move import calculate_nn_move
from utils.get_angle import get_angle
from utils.load_yaml import load_yaml

pygame.init()
pygame.font.init()

config = load_yaml('src/game/config.yaml')
absolute_direction_converter = load_yaml('src/var/direction_map.yaml')

node_width = config['window_dimensions'][0] / (config['game_dimensions'][0] + 2)
node_height = config['window_dimensions'][1] / (config['game_dimensions'][1] + 2)

matrix_manager = MatrixManager(*config['game_dimensions'])
game_manager = GameManager(matrix_manager, logs = True)

screen = pygame.display.set_mode(config['window_dimensions'])

renderer = BoardRenderer(screen, node_width, node_height)

nn = BaseNeuralNetwork([1, 4, 3])

def loop_output():
  def neural_net_move():
    new_direction, new_matrix, colision = calculate_nn_move(game_manager, nn)

    game_manager.matrix_manager.replace(new_matrix)

    if (colision == 'wall' or colision == 'body'):
      game_manager.over = True
      renderer.game_over(game_manager.snake_size - 1, config['window_dimensions'])

    if (colision == 'food'):
      game_manager.snake_size += 1

    game_manager.direction = new_direction

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
