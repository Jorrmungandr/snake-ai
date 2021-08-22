import pygame
import threading

from gui.renderer import BoardRenderer
from utils.load_config import load_config_dict
from managers.matrix import MatrixManager, codeArray
from managers.game import GameManager

pygame.init()
pygame.font.init()

config = load_config_dict()

node_width = config['window_dimensions'][0] / (config['game_dimensions'][0] + 2)
node_height = config['window_dimensions'][1] / (config['game_dimensions'][1] + 2)

matrix_manager = MatrixManager(*config['game_dimensions'])
game_manager = GameManager(matrix_manager, logs = True)

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
        'w': 'up',
        'a': 'left',
        's': 'down',
        'd': 'right',
      }

      if (event.unicode in direction_key_map):
        next_direction = direction_key_map[event.unicode]

        if (next_direction == 'up' and game_manager.direction != 'down'):
          game_manager.direction = next_direction

        if (next_direction == 'left' and game_manager.direction != 'right'):
          game_manager.direction = next_direction

        if (next_direction == 'right' and game_manager.direction != 'left'):
          game_manager.direction = next_direction

        if (next_direction == 'down' and game_manager.direction != 'up'):
          game_manager.direction = next_direction

  if (game_manager.over == False):
    renderer.matrix(game_manager.matrix_manager.matrix, config['colors'], codeArray)

  pygame.display.flip()

game_manager.over = True
pygame.quit()
