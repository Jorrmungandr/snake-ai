import pygame
import threading
from helpers.printer import print_matrix
from services.matrix import Matrix, codeArray
from services.game import Game

pygame.init()
pygame.font.init()

color_dict = {
  'wall': (250, 250, 250),
  'empty': (32, 44, 55),
  'head': (46, 142, 213),
  'body': (46, 142, 213),
  'food': (218, 69, 56),
}

game_width = 23
game_height = 23

window_height = 800
window_width = 800

node_height = window_height / (game_height + 2)
node_width = window_width / (game_width + 2)

matrix_service = Matrix(game_width, game_height)
game_service = Game(matrix_service, logs = True)

screen = pygame.display.set_mode([window_width, window_height])

def render_square(x, y, color):
  surface = pygame.Surface((node_width, node_height), pygame.SRCALPHA)
  pygame.draw.rect(surface, color, [0, 0, node_width - 1, node_height - 1])

  screen.blit(surface, (x, y))

def render_matrix():
  screen.fill((0, 0, 0))

  for i, row in enumerate(game_service.matrix_service.matrix):
    for j, cell in enumerate(row):
      render_square(node_width * j, node_height * i, color_dict[codeArray[cell]])

def render_game_over(score):
  title_font = pygame.font.SysFont('Comic Sans MS', 70)
  score_font = pygame.font.SysFont('Comic Sans MS', 30)
  screen.fill((0, 0, 0))

  title_surface = title_font.render('Game Over', False, (255, 255, 255))
  title_rect = title_surface.get_rect(center=(window_width / 2, (window_height / 2) - 20))

  score_surface = score_font.render(f'Score: {score}', False, (255, 255, 255))
  score_rect = score_surface.get_rect(center=(window_width / 2, (window_height / 2) + 30))

  screen.blit(title_surface, title_rect)
  screen.blit(score_surface, score_rect)

def loop_output():
  def func_wrapper():
    new_matrix, colision = game_service.compile_output(game_service.direction)

    game_service.matrix_service.replace(new_matrix)

    if (colision == 'wall' or colision == 'body'):
      game_service.over = True
      render_game_over(game_service.snake_size - 1)

    if (colision == 'food'):
      game_service.snake_size += 1

    if (not game_service.over): loop_output()

  t = threading.Timer(0.2, func_wrapper)
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

        if (next_direction == 'up' and game_service.direction != 'down'):
          game_service.direction = next_direction

        if (next_direction == 'left' and game_service.direction != 'right'):
          game_service.direction = next_direction

        if (next_direction == 'right' and game_service.direction != 'left'):
          game_service.direction = next_direction

        if (next_direction == 'down' and game_service.direction != 'up'):
          game_service.direction = next_direction

  if (game_service.over == False):
    render_matrix()

  pygame.display.flip()

game_service.over = True
pygame.quit()
