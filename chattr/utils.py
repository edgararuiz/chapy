from yaml import load, SafeLoader
from os import path

def _ch_open_config(name):
    module_dir = path.dirname(__file__)
    config_path = path.join(module_dir, "configs", name + ".yml")
    with open(config_path, 'r') as f:
        data = load(f, Loader = SafeLoader)
    return(data)