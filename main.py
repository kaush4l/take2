from modules.graph_builder import load_data
from modules.models import get_primary
import gradio as gr

def create_interface():

    configs, graph = load_data()

    with gr.Blocks() as interface:
        gr.Markdown("LangGraph Interface")
        with gr.Tabs():
            for model in configs:
                with gr.Tab(model):
                    gr.Markdown(f"## {model} Information")
                    for item in configs[model]:
                        with gr.Accordion(f"{get_primary(item)}", open=False):
                            # gr.Markdown(f"{model}")
                            for attribute in item.__fields__:
                                gr.Markdown(f"{attribute} : {getattr(item, attribute)}")

    return interface



def main():
    graph = load_data()

    demo = create_interface()
    demo.launch(server_name="0.0.0.0", server_port=5000)
    # graph = build_graph()
    # while True:
    #     user_input = input("User: ")
    #     result = graph.invoke({
    #         "messages": ["user", user_input]
    #     })
    #     print(result)

if __name__ == "__main__":
    main()