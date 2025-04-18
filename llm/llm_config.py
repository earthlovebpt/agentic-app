import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# Load .env file once
load_dotenv()

# Now access securely
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = init_chat_model(
    model="gpt-4.1-2025-04-14",
    temperature=0.3,
    api_key=OPENAI_API_KEY,
    streaming=False,
)