from langchain.globals import set_debug, set_verbose
set_verbose(True)

from langchain_ollama.chat_models import ChatOllama
llm = ChatOllama(
    model="llama3.2:3b-instruct-fp16",
    # temperature=0.1,
)