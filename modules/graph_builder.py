from typing import List

from config.loader import load_configs
from modules.models import Agent, Node, Graph, State, Modules


def load_data():
    # for front end use
    configs = load_configs()
    state = configs[State.__name__][0]
    # for backend use
    agents = build_agents(configs[Agent.__name__])
    nodes = build_nodes(configs[Node.__name__], agents)
    graph = build_graph(configs[Graph.__name__], nodes, state)
    return configs, graph


def build_agents(agents: list[Agent]):
    from langchain_core.prompts import ChatPromptTemplate
    constructed_agents = {}
    for agent in agents:
        prompt = ChatPromptTemplate([
            ("system", agent.system_instruction),
            ("user", "{query}"),
        ])
        constructed_agents[agent.name] = prompt
    return constructed_agents

def build_nodes(nodes: list[Node], agents):
    from llm import llm
    constructed_nodes = {}
    for node in nodes:
        def node_function(state):
            query = getattr(state, node.input_value)
            agent = agents[node.agent]
            response = llm.invoke(agent.invoke(query))
            return { "messages" : response }
        constructed_nodes[node.id] = node_function
    return constructed_nodes

def build_graph(graph: list[Graph], nodes, state):
    from langgraph.graph import StateGraph
    graph_builder = StateGraph(state.__class__)
    for node in nodes:
        graph_builder.add_node(node, nodes[node])
    for element in graph:
        graph_builder.add_edge(element.startKey, element.endKey)
    graph = graph_builder.compile()
    return graph