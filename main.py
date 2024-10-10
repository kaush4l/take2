import gradio as gr
from modules.graph_builder import load_data
from modules.models import LangGraphConfig

def create_interface(configs: LangGraphConfig):
    with gr.Blocks() as interface:
        gr.Markdown("LangGraph Interface")
        with gr.Tabs():
            for model in configs.model_fields:
                with gr.Tab(model):
                    gr.Markdown(f"## {model} Information")
                    items = getattr(configs, model)
                    if isinstance(items, list):
                        for item in items:
                            with gr.Accordion(f"{item}", open=False):
                                # gr.Markdown(f"{model}")
                                for attribute in item.model_fields:
                                    gr.Markdown(f"{attribute} : {getattr(item, attribute)}")
                    else:
                        with gr.Accordion(f"{items}", open=False):
                            # gr.Markdown(f"{model}")
                            for attribute in items.model_fields:
                                gr.Markdown(f"{attribute}")

    return interface



def main():
    config, graph = load_data()
    demo = create_interface(config)
    demo.launch(server_name="0.0.0.0", server_port=5000)

if __name__ == "__main__":
    main()