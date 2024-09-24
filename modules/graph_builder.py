from modules.models import Agent, Node, Graph, State, import_models

state = import_models(State)[0]

def build_agents():
    from langchain_core.prompts import ChatPromptTemplate
    model_agents = import_models(Agent)
    constructed_agents = {}
    for agent in model_agents:
        prompt = ChatPromptTemplate([
            ("system", agent.system_instruction),
            ("user", "{query}"),
        ])
        constructed_agents[agent.name] = prompt
    return constructed_agents

def build_nodes():
    from llm import llm
    model_nodes = import_models(Node)
    agents = build_agents()
    constructed_nodes = {}
    for node in model_nodes:
        def node_function(state):
            query = getattr(state, node.input_value)
            agent = agents[node.agent]
            response = llm.invoke(agent.invoke(query))
            print(response)
            return {"messages": response}
        constructed_nodes[node.name] = node_function
    return constructed_nodes

def build_graph():
    from langgraph.graph import StateGraph
    model_graphs = import_models(Graph)
    nodes = build_nodes()
    graph_builder = StateGraph(state.__class__)
    for node in nodes:
        graph_builder.add_node(node, nodes[node])
    for graph in model_graphs:
        graph_builder.add_edge(graph.startKey, graph.endKey)

    graph = graph_builder.compile()
    return graph