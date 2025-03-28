"""Test data for the Twitch test automation framework"""

import json
import os

def load_test_data(filename):
    """
    Load test data from JSON file
    
    Args:
        filename: Name of the JSON file in the data directory
        
    Returns:
        dict or list: The loaded test data
    """
    data_path = os.path.join(os.path.dirname(__file__), filename)
    
    with open(data_path, 'r') as f:
        return json.load(f) 