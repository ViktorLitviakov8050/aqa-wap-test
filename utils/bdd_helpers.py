"""Helper utilities for BDD testing."""

import json
import os
from utils.logging_utils import get_logger

logger = get_logger()


def load_test_data_from_examples(examples):
    """
    Convert BDD scenario outline examples to a list of dictionaries.
    
    Args:
        examples: Examples table from BDD scenario
        
    Returns:
        list: List of dictionaries with test data
    """
    headers = examples[0]
    rows = examples[1:]
    result = []
    
    for row in rows:
        data = {}
        for i, header in enumerate(headers):
            data[header] = row[i]
        result.append(data)
    
    return result


def load_feature_file(feature_name):
    """
    Load a feature file as a string.
    
    Args:
        feature_name: Name of the feature file without extension
        
    Returns:
        str: Content of the feature file
    """
    feature_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "tests",
        "features",
        f"{feature_name}.feature"
    )
    
    with open(feature_path, 'r') as f:
        return f.read()


def extract_scenarios(feature_content):
    """
    Extract scenario names from feature content.
    
    Args:
        feature_content: Content of the feature file
        
    Returns:
        list: List of scenario names
    """
    scenarios = []
    lines = feature_content.split('\n')
    
    for line in lines:
        line = line.strip()
        if line.startswith('Scenario:') or line.startswith('Scenario Outline:'):
            scenario_name = line.split(':', 1)[1].strip()
            scenarios.append(scenario_name)
    
    return scenarios


def print_available_scenarios(feature_name="twitch"):
    """
    Print all available scenarios in a feature file.
    
    Args:
        feature_name: Name of the feature file without extension
    """
    try:
        feature_content = load_feature_file(feature_name)
        scenarios = extract_scenarios(feature_content)
        
        logger.info(f"Available scenarios in '{feature_name}.feature':")
        for i, scenario in enumerate(scenarios, 1):
            logger.info(f"{i}. {scenario}")
            
    except Exception as e:
        logger.error(f"Error loading scenarios: {str(e)}")
        return [] 