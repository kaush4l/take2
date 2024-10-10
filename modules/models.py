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
    name: str
    input_value: str
    agent: str
    output_data_type: Optional[str] = None

class Edge(BaseModel):
    name: str
    startKey: str
    endKey: str

class LangGraphConfig(BaseModel):
    agents: List[Agent] = [None]
    nodes: List[Node] = [None]
    edges: List[Edge] = [None]
    state: State = None