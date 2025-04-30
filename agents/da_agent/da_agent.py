from langchain_core.messages import HumanMessage
from .graph.state import DAAgentState
from .graph.nodes import agent_node
from utils.sanitize import sanitize
import json

class DA_Agent:
    def __init__(self):
        # initialize conversation and state fields
        self.chat_history = []            # List of messages: HumanMessage, AIMessage, ToolMessage
        self.intermediate_outputs = []    # List of strings from header or tools
        self.output_image_paths = {}      # Dict[int, List[str]]: images per message index
        self.current_variables = []       # Variables still unused
        self.final_result = None          # Saved by save_final_result

    def reset_chat(self):
        """Clear all history and reset state."""
        self.chat_history.clear()
        self.intermediate_outputs.clear()
        self.output_image_paths.clear()
        self.current_variables.clear()
        self.final_result = None

    def user_sent_message(self, user_query: str, schema_context: str, input_datasets: dict):
        """
        Send a query through the ReAct agent node and update local fields.
        """
        # Build initial state object
        # On first turn, header is injected inside call_model
        datasets = {sanitize(k): v["data"] for k, v in input_datasets.items()}

        header = (
            "\n\nThe following data is available:\n"
            + schema_context
        )

        state = DAAgentState(
            messages=[HumanMessage(content=header),HumanMessage(content=user_query)],
            schema_context=schema_context,
            datasets=datasets,
            current_variables=self.current_variables.copy(),
            output_image_paths=self.output_image_paths.copy(),
            intermediate_outputs=self.intermediate_outputs.copy()
        )

        result: DAAgentState = agent_node.invoke(state)

        # 1) Update chat history
        self.chat_history = result["messages"]
        # 2) Merge intermediate_outputs
        self.intermediate_outputs.extend(result["intermediate_outputs"])
        # 3) Update variables
        self.current_variables = result["current_variables"]
        # 4) Collect new images
        # result.output_image_paths is List[str]
        if result["output_image_paths"]:
            idx = len(self.chat_history) - 1
            self.output_image_paths[idx] = result["output_image_paths"]
        # 5) Update final_result if set
        if "final_result" in result:
            self.final_result = result["final_result"]
            print("final result:", self.final_result)

        return result