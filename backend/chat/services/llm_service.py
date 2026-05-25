from typing import List

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from chat.serializers import Message

# Load environment variables from .env file
load_dotenv()

MODEL_ID = "llama-3.3-70b-versatile"


async def get_chat_response(messages: List[Message]) -> str:
    """
    Send user message (with conversation history) to the LLM
    and return the assistant's reply as a string.
    """

    llm = ChatGroq(temperature=0.0, model_name=MODEL_ID)

    system_message = SystemMessage(content=("You are a professional brand name strategist, creative consultant, and business advisor.\
            Help the user brainstorm, refine, and evaluate unique company names, product concepts. "))

    prompt_template = [system_message]

    for msg in messages:
        if msg.role == "user":
            prompt_template.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            prompt_template.append(AIMessage(content=msg.content))

    response = llm.invoke(prompt_template)
    return response.content
