import yaml

def load_yaml(path):
  with open(path) as file:
    config = yaml.load(file.read(), Loader=yaml.FullLoader)

    return config
