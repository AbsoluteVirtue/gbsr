import yaml


def get_config(path):
    with open(path) as f:
        c = yaml.load(f)
    return c
