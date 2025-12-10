import json
import os


def load_config(config_path="config.json"):
    """
    Loads configuration from json file
    :param config_path: path to configuration file
    :return: json containing source_dir, destination_dir and number of threads
    """
    if not os.path.isfile(config_path):
        raise FileNotFoundError(f"Config file not found: ",config_path)

    with open(config_path) as config_file:
        return json.load(config_file)