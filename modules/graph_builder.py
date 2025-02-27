from config.loader import load_configs
from modules.base import PromptTemplate, Edge, Model, Node, ConditionalNode, AgentState

def load_data():
    configs = load_configs()
    models = build_model(configs.Models)
    prompts = build_prompts(configs.Prompts)
    nodes = build_nodes(configs.Nodes, prompts, models, configs.State)
    graph = build_graph(configs.Edges, nodes, configs.State)
    return configs, graph

def build_model(models: list[Model]):
    constructed_models = {}

    # TODO add loading based on providers
    for model in models:
        from langchain_ollama.chat_models import ChatOllama
        llm = ChatOllama(
            model=model.key,
        )
        constructed_models[model.name] = llm
    return constructed_models

def build_prompts(prompts: list[PromptTemplate]):
    constructed_agents = {}

    from langchain_core.prompts import ChatPromptTemplate
    for prompt in prompts:
        template = ChatPromptTemplate.from_messages([
            ("system", prompt.system_instruction),
            ("user", "{query}"),
        ])
        constructed_agents[prompt.name] = template
    return constructed_agents

def build_nodes(nodes: list[Node], prompts, models, state):
    constructed_nodes = {}

    def node_function(node: Node, state: AgentState):
        input_key = node.input_key
        template = prompts[node.prompt]
        llm = models[node.model]
        response_key = node.output_key
        def function(state: AgentState):
            query = getattr(state, input_key)
            prompt = template.invoke(query)
            response = llm.invoke(prompt)
            return {
                **state.dict(),
                response_key : response

            }
        return function

    for node in nodes:
        constructed_nodes[node.name] = node_function(node, state)

    return constructed_nodes

def build_graph(edges: list[Edge], nodes, state: AgentState):
    from langgraph.graph import StateGraph
    graph_builder = StateGraph(state.__class__)
    for node_name, node_function in nodes.items():
        graph_builder.add_node(node_name, node_function)
    for edge in edges:
        graph_builder.add_edge(edge.startKey, edge.endKey)
    return graph_builder.compile()