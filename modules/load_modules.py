from models import Agent, Node, Graph, State
from config.loader import load_config


def import_models(base_model: BaseModel):
    name = base_model.__name__
    model_data = load_config(name)
    models = [base_model(**data) for data in model_data]