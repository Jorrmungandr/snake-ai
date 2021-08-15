from services.matrix_service import MatrixService
from helpers.matrix_printer import print_matrix

matrix_service = MatrixService(11, 11)

print_matrix(matrix_service.matrix)

matrix_service.set_pixel(0, 0, 'head')

print_matrix(matrix_service.matrix)