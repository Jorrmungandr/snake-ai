import time
import numpy as np
import os

from modules.genetic_evolution.conductor import Conductor
from .utils.load_yaml import load_yaml

config = load_yaml(os.path.join(os.path.dirname(os.path.realpath('__file__')), 'modules/genetic_evolution/default_config.yaml'))

conductor = Conductor(config)

start = time.process_time()

best_individuals = conductor.orchestrate(20, 1000, 0.005)

with open('saves/save.npy', 'wb') as f:
  np.save(f, np.array([*best_individuals[0]], dtype = object), allow_pickle = True)

print(time.process_time() - start)
