import random
import numpy as np

from ..neural_network.play_nn import play_nn
from ..neural_network.models.main_model import MainModel

class Conductor():
  config = {}

  def __init__(self, config):
    self.config = config
    self.seed_length = 10

  def run_individual(self, biases, weights):
    nn = MainModel([2, 10, 10, 3], biases, weights)

    if (len(biases) == 0 or len(weights) == 0):
      nn.random_seed()

    return play_nn(self.config, nn)

  def run_generation(self, generation_size, seeds = [], seed_variance = 0.1):
    individuals = []

    def run_individual_from_seed(i):
      individual_biases = seeds[i % len(seeds)][0] if len(seeds) > 0 else []
      individual_weights = seeds[i % len(seeds)][1] if len(seeds) > 0 else []

      variated_biases = []
      variated_weights = []

      for column in individual_biases:
        variated_biases.append(np.array([[value * random.uniform(1 - seed_variance, 1 + seed_variance) for value in line] for line in column]))

      for column in individual_weights:
        variated_weights.append(np.array([[value * random.uniform(1 - seed_variance, 1 + seed_variance) for value in line] for line in column]))

      score, biases, weights = self.run_individual(variated_biases, variated_weights)

      return (score, biases, weights)

    for i in range(generation_size):
      individuals.append(run_individual_from_seed(i))

    return sorted(individuals, key = lambda tuple: tuple[0], reverse=True)

  def orchestrate(self, generation_number, generation_size, seed_variance, logs = False):
    seeds = []

    for i in range(generation_number):
      if (logs == True): print(f'Starting generation nº {i}')
      individuals = self.run_generation(generation_size, seeds, seed_variance)
      seeds = [(individual[1], individual[2]) for individual in individuals[:self.seed_length]]

      print(f'Generation: {i};\nBest {self.seed_length} individuals: {[individual[0] for individual in individuals[:self.seed_length]]};\nAverage score: {np.average([individual[0] for individual in individuals])};\n')

    return seeds
