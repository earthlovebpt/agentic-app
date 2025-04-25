from langchain_core.messages import HumanMessage
from .graph.nodes import agent_node, create_available_variables

class DS_Agent:
    def __init__(self):
        # Conversation and state initialization
        self.chat_history = []                # list of messages (HumanMessage, AIMessage, ToolMessage)
        self.intermediate_outputs = []        # list of strings for debugging/context
        self.output_image_paths = {}         # maps message index to image paths
        self.current_variables = []          # tracks which variables are still available

    def user_sent_message(self, user_query: str, schema_context: str, datasets: dict):
        """
        Send a user query to the ReAct agent, injecting the schema header only on the first turn.
        """
        # 1️⃣ Prepare messages: header + user query on first turn, else just history + query
        if not self.chat_history:
            header_text = (
                "The following data is available:\n"
                + schema_context
                + create_available_variables({
                    "current_variables": self.current_variables,
                    "datasets": datasets
                })
            )
            header = HumanMessage(content=header_text)
            messages = [header, HumanMessage(content=user_query)]
            # record header for debugging
            self.intermediate_outputs.append(header_text)
        else:
            messages = self.chat_history + [HumanMessage(content=user_query)]

        # 2️⃣ Build the agent state dict
        state = {
            "messages": messages,
            "schema_context": schema_context,
            "datasets": datasets,
            "current_variables": self.current_variables,
            "output_image_paths": []
        }

        # 3️⃣ Invoke the ReAct agent (LLM + tools internally)
        result = agent_node.invoke(state)

        # 4️⃣ Update chat history
        self.chat_history = result.get("messages", [])

        # 5️⃣ Handle new image paths
        new_images = set(result.get("output_image_paths", [])) - set(sum(self.output_image_paths.values(), []))
        if new_images:
            self.output_image_paths[len(self.chat_history) - 1] = list(new_images)

        # 6️⃣ Append any intermediate outputs from the agent
        if "intermediate_outputs" in result:
            self.intermediate_outputs.extend(result["intermediate_outputs"])

        # 7️⃣ Update available variables if agent updated them
        if "current_variables" in result:
            self.current_variables = result["current_variables"]

    def reset_chat(self):
        """Clear all conversation history and reset state."""
        self.chat_history = []
        self.intermediate_outputs = []
        self.output_image_paths = {}
        self.current_variables = []
