# take2

Overview

take2 is a Python-based tool that simplifies the creation of LangChain applications by allowing users to define agent nodes, graphs, and edges using JSON configuration files. This project aims to streamline the process of building and maintaining LangGraph workflows by eliminating the need for extensive manual coding.

### TODO
 - Gradio Integration: A simple, intuitive Gradio UI to show all elements in the UI
 - Vallidate graph: Checking the edges, nodes and agents that form the graph.
 - Tool calling Nodes: Node with act as toolcalling Nodes. Use either in-build or write the base tool calling code.
 - Structured Output: The system should capable of handling structured outputs for agents, making it easier to process and do conditional routing.
 - A combined JSON for a more compact graph rather than a split one.

### Yet to understand
 - Node outputs: Graphs being created in a loop, all the responses are returned as below. But need to figure out how to send custom format of response.
```python
return {"messages": response}
```
 - Conditional Edges: Supports conditional edges, enabling dynamic control over graph flow based on user-defined conditions.
 - Tool calling: tool calling can be ToolNode. But if too many tools or parallel tool calls how do I want to handle?

Upload JSON configuration files.
Update and modify LangGraph elements in real time.
Validate and preview the structure of your graph visually before deploying.
Scalability: Build and manage multiple agents and nodes, seamlessly scaling workflows from simple graphs to complex, multi-agent systems.
