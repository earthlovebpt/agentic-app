from langchain_core.messages import HumanMessage
from typing import List
from dataclasses import dataclass
from langgraph.graph import StateGraph
from graph.state import AgentState
from graph.nodes import call_model, call_tools, route_to_tools

class PythonChatbot:
    def __init__(self):
        super().__init__()
        self.reset_chat()
        self.graph = self.create_graph()
        
    def create_graph(self):
        workflow = StateGraph(AgentState)
        workflow.add_node('agent', call_model)
        workflow.add_node('tools', call_tools)

        workflow.add_conditional_edges('agent', route_to_tools)

        workflow.add_edge('tools', 'agent')
        workflow.set_entry_point('agent')
        return workflow.compile()
    
    def user_sent_message(self, user_query, schema_context, datasets):
        starting_image_paths_set = set(sum(self.output_image_paths.values(), []))
        input_state = {
            "messages": self.chat_history + [HumanMessage(content=user_query)],
            "output_image_paths": list(starting_image_paths_set),
            "schema_context": schema_context,
            "datasets": datasets
        }

        result = self.graph.invoke(input_state, {"recursion_limit": 25})
        self.chat_history = result["messages"]
        new_image_paths = set(result["output_image_paths"]) - starting_image_paths_set
        self.output_image_paths[len(self.chat_history) - 1] = list(new_image_paths)
        if "intermediate_outputs" in result:
            self.intermediate_outputs.extend(result["intermediate_outputs"])

    def reset_chat(self):
        self.chat_history = []
        self.intermediate_outputs = []
        self.output_image_paths = {}