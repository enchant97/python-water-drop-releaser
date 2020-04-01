"""
file that allows for loading and saving config data.

global constant variables:
    -   CONFIG_FILENAME = the filename/path of the config file
    -   DEFAULT_CONFIGS = the default configs that will be written if file does not exist

get_config() = returns dict of configs, creates file if does not exist

write_config() = writes the dict given
"""
import json

__author__ = "enchant97"

CONFIG_FILENAME = "config.json"
DEFAULT_CONFIGS = {
    "dropdelay":0,
    "dropcount":1,
    "dropduration":200,
    "dropdistance":1,
    "flashoffset":0
    }

def get_config():
    """
    returns dict of configs
    """
    try:
        with open(CONFIG_FILENAME, "r") as fo:
            return json.load(fo)
    except FileNotFoundError:
        write_config(DEFAULT_CONFIGS)
        return DEFAULT_CONFIGS

def write_config(config_data):
    """
    writes the config to file

    args:
        config_data : the dict that will be written
    """
    with open(CONFIG_FILENAME, "w") as fo:
        json.dump(config_data, fo)
