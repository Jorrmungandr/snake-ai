import pygame
import os
import threading

from gui.renderer import BoardRenderer
from managers.matrix import MatrixManager, codeArray
from managers.game import GameManager
from utils.load_yaml import load_yaml

pygame.init()
pygame.font.init()

config = load_yaml('src/game/config.yaml')

node_width = config['window_dimensions'][0] / (config['game_dimensions'][0] + 2)
node_height = config['window_dimensions'][1] / (config['game_dimensions'][1] + 2)

matrix_manager = MatrixManager(*config['game_dimensions'])
game_manager = GameManager(matrix_manager)

screen = pygame.display.set_mode(config['window_dimensions'])

renderer = BoardRenderer(screen, node_width, node_height)

def loop_output():
  def func_wrapper():
    new_matrix, colision = game_manager.compile_output(game_manager.direction)

    game_manager.matrix_manager.replace(new_matrix)

    if (colision == 'wall' or colision == 'body'):
      game_manager.over = True
      renderer.game_over(game_manager.snake_size - 1, config['window_dimensions'])

    if (colision == 'food'):
      game_manager.snake_size += 1

    if (not game_manager.over): loop_output()

  t = threading.Timer(config['snake_speed'], func_wrapper)
  t.start()
  return t

loop_output()

running = True

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN:
      direction_key_map = {
        'w': (0, 1),
        'a': (-1, 0),
        's': (0, -1),
        'd': (1, 0),
      }

      if (event.unicode in direction_key_map):
        next_direction = direction_key_map[event.unicode]

        if (
          abs(next_direction[0] - game_manager.direction[0]) != 2
          and abs(next_direction[1] - game_manager.direction[1]) != 2
        ): game_manager.direction = next_direction

  if (game_manager.over == False):
    renderer.matrix(game_manager.matrix_manager.matrix, config['colors'], codeArray)

  pygame.display.flip()

game_manager.over = True
pygame.quit()
