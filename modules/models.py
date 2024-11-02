from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any

class AgentState(BaseModel):
    """
    Model to hold the state elements and values for the graph
    """
    class Config:
        extra = 'allow'

    def __init__(self, **data: Any):
        super().__init__(**data)

        user_dict = {k: v for k, v in data.items()}
        for key, value in user_dict.items():
            setattr(self, key, value)
            # if value is None:
            #     if isinstance(value, int):
            #         setattr(self, key, 0)
            #     elif isinstance(value, float):
            #         setattr(self, key, 0.0)
            #     elif isinstance(value, str):
            #         setattr(self, key, "")
            #     elif isinstance(value, bool):
            #         setattr(self, key, False)
            #     elif isinstance(value, list):
            #         setattr(self, key, [])
            #     elif isinstance(value, dict):
            #         setattr(self, key, {})
            #     else:
            #         setattr(self, key, None)
            # else:
            #     setattr(self, key, value)

class Models(BaseModel):
    """Holds the LLM's models and settings"""
    name: str
    key: str
    provider: str

class PromptTemplate(BaseModel):
    """Defines the input and output structure for an Agent's query.
    Only a chat template because tool/function calling/system instruction is only possible this way.
    Any specific instructions, guiding and pydantic output template in JSON
    """
    name: str
    system_instruction: str
    custom_response: Optional[str] = None
    setting: Optional[List[str]] = None

class Node(BaseModel):
    """Working block that defines the prompt, model, the input and output value to be updated/used"""
    name: str
    input_key: str
    model: str
    prompt: str
    output_key: str
    output_data_type: Optional[str] = None

class ConditionalNode(Node):
    condition: str

class Edge(BaseModel):
    """This is to define the connection/links between nodes"""
    # integrate normal and conditional edges to be handled together
    name: str
    startKey: str
    endKey: str

class LangGraphConfig(BaseModel):
    prompts: List[PromptTemplate] = []
    models: List[Models] = []
    edges: List[Edge] = []
    nodes: List[Node] = []
    state: AgentState = []