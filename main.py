from modules.graph_builder import build_graph

def main():
    graph = build_graph()
    while True:
        user_input = input("User: ")
        result = graph.invoke({
            "messages": ["user", user_input]
        })
        print(result)

# def setup():
#     agent = Agent(name="sample", system_instruction="Answer consistently")
#     node = Node(name="starter", input_value="messages[-1]")
#     graph1 = Graph(startKey="__start__", endKey="starter")
#     graph2 = Graph(startKey="starter", endKey="__end__")
#     state = State(messages=[])
#     save_config(agent)
#     save_config(node)
#     save_config(graph1)
#     save_config(graph2)
#     save_config(state)

if __name__ == "__main__":
    # clear_config_folder()
    # setup()
    main()