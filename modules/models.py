from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class State(BaseModel):
    messages: List[str]


class Agent(BaseModel):
    name: str
    system_instruction: str
    llm: Optional[str] = None
    custom_response: Optional[str] = None
    setting: Optional[List[str]] = None


class Node(BaseModel):
    id: str
    input_value: str
    agent: str
    output_data_type: Optional[str] = None


class Graph(BaseModel):
    startKey: str
    endKey: str


def get_primary(model: BaseModel):
    if model.__class__ == Agent:
        return model.name
    elif model.__class__ == Node:
        return model.id
    elif model.__class__ == Graph:
        return model.startKey
    if model.__class__ == State:
        return model.messages


Modules = [Agent, Node, Graph, State]