import json
import os
from pydantic import parse_obj_as, BaseModel
from modules.models import LangGraphConfig, Agent, Node, Edge, State

FILE = "config/configuration.json"

def create_empty_skeleton():
    """
    Create an empty skeleton configuration for each model class in Modules.
    """
    agent = Agent(name="Tester",
                  system_instruction="You are an assistant")
    node = Node(name="starter",
                input_value="messages",
                agent="Tester")
    edge_1 = Edge(startKey="__start__", endKey="starter")
    edge_2 = Edge(startKey="starter", endKey="__end__")
    state = State(messages=[])
    skeleton = LangGraphConfig(agents=[agent], nodes=[node], edges=[edge_1, edge_2], state=state)
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(skeleton.dict(), f, indent=4)
    save_configs(skeleton)
    return skeleton

def update_configs(configs: LangGraphConfig):
    """
    Update configurations of the file. If the file is present, it will call load_configs
    to get the current configurations and update them.
    """
    current_configs = load_configs()
    # TODO: Probably needs to check and update only the needed elements
    save_configs(current_configs.copy(update=configs.dict()))
    return load_configs()

def save_configs(configs: LangGraphConfig):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(configs.dict(), f, indent=4)

def load_configs() -> LangGraphConfig:
    """
    Load configurations from the file. If the file does not exist, create an empty skeleton
    and save it using the save_configs method.
    Returns a dictionary mapping class names to a list of model instances.
    """
    if os.path.exists(FILE):
        try:
            with open(FILE, "r", encoding="utf-8") as f:
                loaded_configs = parse_obj_as(LangGraphConfig, json.load(f))
        except json.JSONDecodeError:
            # Handle invalid JSON by creating and saving an empty skeleton
            loaded_configs = create_empty_skeleton()
    else:
        # Create an empty skeleton and save it since the file does not exist
        loaded_configs = create_empty_skeleton()

    return loaded_configs