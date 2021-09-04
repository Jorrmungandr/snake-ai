import time
import numpy as np

from generation_conduction.conductor import Conductor
from utils.load_yaml import load_yaml

config = load_yaml('src/game/config.yaml')

conductor = Conductor(config)

start = time.process_time()

best_individuals = conductor.orchestrate(50, 400, 0.005)

with open('saves/save.npy', 'wb') as f:
  np.save(f, np.array([*best_individuals[0]], dtype = object), allow_pickle = True)

print(time.process_time() - start)
