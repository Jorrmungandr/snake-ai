import numpy as np

from ..utils.sigmoid import sigmoid

class MainModel:
  biases = []
  weights = []

  def __init__(self, layer_sizes, biases, weights):
    self.layer_sizes = layer_sizes
    self.biases = biases
    self.weights = weights

  def feedforward(self, input):
    auxiliar_result = input


    for layer_biases, layer_weights in zip(self.biases, self.weights):
      auxiliar_result = sigmoid(np.dot(layer_weights, auxiliar_result) + layer_biases)

    return auxiliar_result.reshape(self.layer_sizes[-1], 1)

  def random_seed(self):
    self.biases = [np.random.randn(y, 1) for y in self.layer_sizes[1:]]
    self.weights = [np.random.randn(y, x) for x, y in zip(self.layer_sizes[:-1], self.layer_sizes[1:])]
