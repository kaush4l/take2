import json
import os
from typing import List, Dict, Type
from pydantic import parse_obj_as, BaseModel
from modules.models import Modules  # Assuming Modules is a list of Pydantic model classes

FILE = "config/configurations.json"


def create_empty_skeleton() -> Dict[str, List[BaseModel]]:
    """
    Create an empty skeleton configuration for each model class in Modules.
    """
    skeleton = {}
    for model_class in Modules:
        skeleton[model_class.__name__] = []
    return skeleton


def save_configs(configs: Dict[str, List[BaseModel]]):
    """
    Save configurations to the file. If the file is present, it will call load_configs
    to get the current configurations and update them.
    """
    # Load current configurations from file (or create a new skeleton if the file is absent or invalid)
    current_configs = load_configs()

    # Update the current configurations with new data
    for class_name, models_list in configs.items():
        current_configs[class_name] = [model.dict() for model in models_list]

    # Save the updated configurations to the file
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(current_configs, f, indent=4)


def load_configs() -> Dict[str, List[BaseModel]]:
    """
    Load configurations from the file. If the file does not exist, create an empty skeleton
    and save it using the save_configs method.
    Returns a dictionary mapping class names to a list of model instances.
    """
    if os.path.exists(FILE):
        try:
            with open(FILE, "r", encoding="utf-8") as f:
                loaded_configs = json.load(f)
        except json.JSONDecodeError:
            # Handle invalid JSON by creating and saving an empty skeleton
            loaded_configs = create_empty_skeleton()
            save_configs(loaded_configs)
    else:
        # Create an empty skeleton and save it since the file does not exist
        loaded_configs = create_empty_skeleton()
        save_configs(create_empty_skeleton())

    # Parse the loaded configurations into their corresponding model classes
    configurations = {}
    for model_class in Modules:
        class_name = model_class.__name__
        if class_name in loaded_configs:
            configurations[class_name] = parse_obj_as(List[model_class], loaded_configs[class_name])
        else:
            # Initialize an empty list for the class if not present
            configurations[class_name] = []

    return configurations