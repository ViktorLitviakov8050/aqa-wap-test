"""Configuration for the Twitch test automation framework"""

import os
import yaml

def load_config():
    """
    Load configuration from config.yaml file
    
    Returns:
        dict: The loaded configuration
    """
    config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f) 