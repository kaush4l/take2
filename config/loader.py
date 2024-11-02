import json
import os
from pydantic import parse_obj_as
from modules.models import LangGraphConfig, PromptTemplate, Edge, Models, Node, AgentState

FILE = "config/configuration.json"

def create_empty_skeleton():
    prompts = PromptTemplate(name="Basic",
                             system_instruction="You are an assistant")
    node = Node(name="n1",
                input_key="query",
                model="llama",
                output_key="response",
                prompt="Basic")
    edge_1 = Edge(name="e1",
                  startKey="__start__",
                  endKey="n1")
    edge_2 = Edge(name="e2",
                  startKey="n1",
                  endKey="__end__")
    model_1 = Models(name="llama",
                     key="llama3.2:3b-instruct-fp16",
                     provider="ollama")
    state = AgentState(query="",
                       response="")
    skeleton = LangGraphConfig(
        edges=[edge_1, edge_2],
        models=[model_1],
        nodes=[node],
        prompts=[prompts],
        state=state)
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