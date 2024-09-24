from typing import Dict, List
from pydantic import BaseModel
import json
import os

FOLDER = "config/configurations"

def clear_config_folder():
    import shutil
    if os.path.exists(FOLDER):
        shutil.rmtree(FOLDER)
        os.makedirs(FOLDER, exist_ok=True)

def load_config(config_name: str) -> List[Dict]:
    file_path = f"{FOLDER}/{config_name}.json"
    
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    else:
        os.makedirs(FOLDER, exist_ok=True)
        with open(file_path, "w") as f:
            json.dump([], f)
        return []

def save_config(model: BaseModel):
    config_name = model.__class__.__name__.lower()
    existing_configs = load_config(config_name)

    existing_configs.append(model.dict())
    
    # Save the updated configurations back to the file
    file_path = f"{FOLDER}/{config_name}.json"
    with open(file_path, "w") as f:
        json.dump(existing_configs, f, indent=4)