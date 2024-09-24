from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from config.loader import load_config

class State(BaseModel):
    messages: List[str]

class Agent(BaseModel):
    name: str
    system_instruction: str
    llm: Optional[str] = None
    custom_response: Optional[str] = None

class Node(BaseModel):
    name: str
    input_value: str
    agent: str
    output_data_type: Optional[str] = None

class Graph(BaseModel):
    startKey: str
    endKey: str

def import_models(base_model: BaseModel):
    name = base_model.__name__
    model_data = load_config(name)
    models = [base_model(**data) for data in model_data]
    return models