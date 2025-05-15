"""
Manages configurations.
"""

# Import standard modules.
import os
import sys
import yaml


def read(filename):
    """
    Reads JSON content from the specified file and returns it as a dictionary.
    
    Args:
        filename (str): The name of the configuration file to read.
        
    Returns:
        dict: The JSON content parsed into a dictionary.
    """
    conf = {}
    conf_dir = os.environ['CONFIG_DIR']
    filepath = os.path.join(conf_dir, filename)
    with open(filepath,'r',encoding="utf-8") as file:
        conf = yaml.safe_load(file)
    return conf


config = {}

# Load MySQL database configurations.
config['mysql'] = read('mysql.yml')
try:
    config['mysql']['password'] = os.environ['MYSQL_PASSWORD']
except KeyError:
    print('Please provide MySQL password.')
    sys.exit(1)

# Load application configurations.
config['app'] = read('app.yml')
try:
    config['app']['app_secret'] = os.environ['APP_SECRET']
    config['app']['cookie_secret'] = os.environ['COOKIE_SECRET']
except KeyError as k:
    print(f'Config {k} is missing.')
    sys.exit(1)
