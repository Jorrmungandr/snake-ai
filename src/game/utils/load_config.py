import yaml

def load_config_dict():
  with open('src/game/config.yaml') as file:
    config = yaml.load(file.read(), Loader=yaml.FullLoader)

    return config
