import gradio as gr
from modules.graph_builder import load_data

configs, graph = load_data()

def chat_response(user_input):
    response = graph.invoke({"query": user_input})
    return response

def create_editable_field(attribute_value, attribute_label):
    if isinstance(attribute_value, str):
        return gr.Textbox(value=attribute_value, label=attribute_label, interactive=True)
    elif isinstance(attribute_value, (int, float)):
        return gr.Number(value=attribute_value, label=attribute_label, interactive=True)
    elif isinstance(attribute_value, bool):
        return gr.Checkbox(value=attribute_value, label=attribute_label, interactive=True)
    else:
        return gr.Textbox(value=str(attribute_value), label=attribute_label, interactive=True)

def create_interface():
    with gr.Blocks() as interface:
        gr.Markdown("LangGraph Interface")
        with gr.Tabs():
            for model in configs.__fields__.keys():
                with gr.Tab(model):
                    gr.Markdown(f"## {model} Information")
                    items = getattr(configs, model)
                    if isinstance(items, list) and items is not None:
                        add_button = gr.Button(value=f"Add {model}")
                        for item in items:
                            with gr.Accordion(f"{getattr(item, 'name', 'Item')}", open=False):
                                for attribute in item.__fields__.keys():
                                    attribute_value = getattr(item, attribute)
                                    setattr(item, attribute, create_editable_field(attribute_value, f"{attribute}"))
                                update_button = gr.Button(value="Update Item")
                    elif items is not None:
                        with gr.Accordion(f"{getattr(items, 'name', 'Items')}", open=False):
                            for attribute in items.model_extra.keys():
                                attribute_value = getattr(items, attribute)
                                setattr(items, attribute, create_editable_field(attribute_value, f"{attribute}"))
                            update_button = gr.Button(value="Update Item")
            with gr.Tab("Chat"):
                gr.Markdown(f"Chat arena")
                user_input = gr.Textbox(lines=5, label="User Input")
                submit = gr.Button(value="Submit")
                chat_output = gr.Textbox(lines=5, label="Chat Output")
                submit.click(chat_response, inputs=user_input, outputs=chat_output)

    return interface

def main():
    demo = create_interface()
    demo.launch(server_name="0.0.0.0", server_port=5000)

if __name__ == "__main__":
    main()