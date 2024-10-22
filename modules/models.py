from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any

class AgentState(BaseModel):
    """
    Represents the dynamic state for the agentic flow.
    By default, it has messages but allows dynamic elements to be added as attributes.
    """
    class Config:
        extra = 'allow'

    def __init__(self, **data: Any):
        super().__init__()

        user_dict = {k: v for k, v in data.items()}
        for key, value in user_dict.items():
            setattr(self, key, value)

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

class ConditionalNode(Node):
    condition: str  # A logical expression to determine the next nodes

class Edge(BaseModel):
    name: str
    startKey: str
    endKey: str

class LangGraphConfig(BaseModel):
    agents: List[Agent] = []
    nodes: List[Node] = []
    edges: List[Edge] = []
    state: AgentState = Field(default_factory=AgentState)

    @validator('agents', 'nodes', 'edges', each_item=True)
    def validate_fields(cls, v):
        if not v.name:
            raise ValueError(f"Each element must have a name: {v}")
        return v