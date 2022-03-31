import pygame

class BoardRenderer:
  main_surface = None
  cell_width = None
  cell_height = None

  def __init__(self, main_surface, cell_width, cell_height):
    self.main_surface = main_surface
    self.cell_width = cell_width
    self.cell_height = cell_height

  def create_cell(self, color):
    surface = pygame.Surface((self.cell_width, self.cell_height), pygame.SRCALPHA)
    pygame.draw.rect(surface, color, [0, 0, self.cell_width - 1, self.cell_height - 1])

    return surface

  def matrix(self, matrix, colors, codeTranslator):
    self.main_surface.fill((0, 0, 0))

    for i, row in enumerate(matrix):
      for j, cell in enumerate(row):
        cell = self.create_cell(colors[codeTranslator[cell]])

        self.main_surface.blit(cell, (self.cell_width * j, self.cell_height * i))

  def game_over(self, score, window_dimentions):
    window_width, window_height = window_dimentions

    title_font = pygame.font.SysFont('Comic Sans MS', 70)
    score_font = pygame.font.SysFont('Comic Sans MS', 30)
    self.main_surface.fill((0, 0, 0))

    title_surface = title_font.render('Game Over', False, (255, 255, 255))
    title_rect = title_surface.get_rect(center=(window_width / 2, (window_height / 2) - 20))

    score_surface = score_font.render(f'Score: {score}', False, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(window_width / 2, (window_height / 2) + 30))

    self.main_surface.blit(title_surface, title_rect)
    self.main_surface.blit(score_surface, score_rect)
