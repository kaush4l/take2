import json
import os
from pydantic import parse_obj_as
from modules.models import LangGraphConfig, Agent, Node, Edge, AgentState

FILE = "config/configuration.json"

def create_empty_skeleton():
    agent = Agent(name="Tester", system_instruction="You are an assistant")
    node = Node(name="starter", input_value="messages", agent="Tester")
    edge_1 = Edge(name="e1", startKey="__start__", endKey="starter")
    edge_2 = Edge(name="e2", startKey="starter", endKey="__end__")
    state = AgentState(messages=[])
    skeleton = LangGraphConfig(agents=[agent], nodes=[node], edges=[edge_1, edge_2], state=state)
    save_configs(skeleton)
    return skeleton

def update_configs(configs: LangGraphConfig):
    current_configs = load_configs()
    save_configs(current_configs.copy(update=configs.dict()))
    return load_configs()

def save_configs(configs: LangGraphConfig):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(configs.dict(), f, indent=4)

def load_configs() -> LangGraphConfig:
    try:
        if os.path.exists(FILE):
            with open(FILE, "r", encoding="utf-8") as f:
                return parse_obj_as(LangGraphConfig, json.load(f))
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading configuration: {e}")
    return create_empty_skeleton()