import pathlib
import yaml

BASE_DIR = pathlib.Path(__file__).parent
config_path = BASE_DIR / 'config' / 'local.yaml'


def get_config(path):
    with open(path) as f:
        c = yaml.load(f)
    return c


config = get_config(config_path)
