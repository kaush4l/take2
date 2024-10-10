import gradio as gr
from modules.graph_builder import load_data

configs, graph = load_data()

def chat_response(user_input):
    response = graph.invoke({"messages" : ("user", user_input)})
    return response

def create_interface():
    with gr.Blocks() as interface:
        gr.Markdown("LangGraph Interface")
        with gr.Tabs():
            for model in configs.model_fields:
                with gr.Tab(model):
                    gr.Markdown(f"## {model} Information")
                    items = getattr(configs, model)
                    if isinstance(items, list):
                        for item in items:
                            with gr.Accordion(f"{getattr(item, 'name')}", open=False):
                                # gr.Markdown(f"{model}")
                                for attribute in item.model_fields:
                                    gr.Markdown(f"{attribute} : {getattr(item, attribute)}")
                    else:
                        with gr.Accordion(f"{items}", open=False):
                            # gr.Markdown(f"{model}")
                            for attribute in items.model_fields:
                                gr.Markdown(f"{attribute}")
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