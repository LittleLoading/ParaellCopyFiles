import json
import os


def load_config(config_path="config.json"):
    if not os.path.isfile(config_path):
        raise FileNotFoundError(f"Config file not found: ",config_path)

    with open(config_path) as config_file:
        return json.load(config_file)