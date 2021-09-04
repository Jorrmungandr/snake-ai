import numpy as np

def sigmoid(x):
  return 1.0 / (1.0 + np.exp(-x))

class BaseModel:
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

    return auxiliar_result.reshape(len(self.layer_sizes[-1]))

  def populate_at_random(self):
    self.biases = [np.random.randn(y, 1) for y in self.layer_sizes[1:]]
    self.weights = [np.random.randn(y, x) for x, y in zip(self.layer_sizes[:-1], self.layer_sizes[1:])]
