import json
import os
from pydantic import parse_obj_as
from modules.base import LangGraphConfig, PromptTemplate, Edge, Model, Node, AgentState

FILE = "config/configuration.json"

def create_empty_skeleton():
    prompts = PromptTemplate(name="basic",
                             system_instruction="You are an assistant")
    node = Node(name="n1",
                input_key="query",
                model="llama",
                output_key="response",
                prompt="basic")
    edge_1 = Edge(name="e1",
                  startKey="__start__",
                  endKey="n1")
    edge_2 = Edge(name="e2",
                  startKey="n1",
                  endKey="__end__")
    model_1 = Model(name="llama",
                    key="llama3.2:3b-instruct-fp16",
                    provider="ollama")
    state = AgentState(query="What is cinematography",
                       response="")
    skeleton = LangGraphConfig(
        Edges=[edge_1, edge_2],
        Models=[model_1],
        Nodes=[node],
        Prompts=[prompts],
        State=state)
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