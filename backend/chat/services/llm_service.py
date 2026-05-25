from typing import List

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from chat.serializers import Message

# Load environment variables from .env file
load_dotenv()

MODEL_ID = "llama-3.3-70b-versatile"


def get_chat_response(messages: List[Message]) -> str:
    """
    Send user message (with conversation history) to the LLM and return the assistant's reply as a string.
    This function now supports general-purpose conversation rather than brand name specific advice.
    """

    llm = ChatGroq(temperature=0.0, model_name=MODEL_ID)

    system_message = SystemMessage(content=("You are a helpful, knowledgeable, and friendly AI assistant. Respond to the user’s questions and engage in natural, multi‑turn conversation across a wide range of topics."))

    prompt_template = [system_message]

    for msg in messages:
        # ``messages`` comes from the serializer and is a list of plain dicts
        # rather than ``Message`` objects. Access the fields via key lookup.
        if isinstance(msg, dict):
            role = msg.get("role")
            content = msg.get("content")
        else:
            # Fallback for any future Message objects
            role = getattr(msg, "role", None)
            content = getattr(msg, "content", None)
        if role == "user":
            prompt_template.append(HumanMessage(content=content))
        elif role == "assistant":
            prompt_template.append(AIMessage(content=content))

    response = llm.invoke(prompt_template)
    return response.content
