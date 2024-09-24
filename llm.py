from langchain.globals import set_debug, set_verbose
set_verbose(True)

from langchain_ollama.chat_models import ChatOllama
llm = ChatOllama(
    # model="llama3.1:8b-instruct-q8_0",
    model="llama3.1:8b-instruct-q6_K",
    # temperature=0.1,
)