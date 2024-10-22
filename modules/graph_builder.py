from config.loader import load_configs
from modules.models import LangGraphConfig, Agent, Edge, Node, ConditionalNode, AgentState

def load_data():
    configs = load_configs()
    # validate_graph(configs)
    agents = build_agents(configs.agents)
    nodes = build_nodes(configs.nodes, agents)
    graph = build_graph(configs.edges, nodes, configs.state)
    return configs, graph

def validate_graph(config: LangGraphConfig):
    agent_names = {agent.name for agent in config.agents}
    node_names = {node.name for node in config.nodes}
    for node in config.nodes:
        if node.agent not in agent_names:
            raise ValueError(f"Agent '{node.agent}' in Node '{node.name}' is not defined.")
    for edge in config.edges:
        if edge.startKey not in node_names and edge.startKey != "__start__":
            raise ValueError(f"Edge '{edge.name}' starts with undefined node '{edge.startKey}'.")
        if edge.endKey not in node_names and edge.endKey != "__end__":
            raise ValueError(f"Edge '{edge.name}' ends with undefined node '{edge.endKey}'.")

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

    def node_function(node: Node, state: AgentState):
        query = state.get_element(node.input_value)
        if query is None:
            raise AttributeError(f"State has no attribute '{node.input_value}'")
        agent = agents[node.agent]
        response = llm.invoke(agent.invoke(query))
        state.add_element('response', response)  # Assuming updating response attribute here
        return state

    for node in nodes:
        constructed_nodes[node.name] = (lambda state, node=node: node_function(node, state))

    return constructed_nodes

def build_graph(edges: list[Edge], nodes, state: AgentState):
    from langgraph.graph import StateGraph
    graph_builder = StateGraph(state.__class__)
    for node_name, node_function in nodes.items():
        graph_builder.add_node(node_name, node_function)
    for edge in edges:
        graph_builder.add_edge(edge.startKey, edge.endKey)
    return graph_builder.compile()