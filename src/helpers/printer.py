import os

clear = lambda: os.system('clear')

def print_matrix(matrix):
  clear()
  for line in matrix:
    print(' '.join(str(cell) for cell in line))

