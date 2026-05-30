from typing import List

from langchain_groq import ChatGroq
from langchain.messages import HumanMessage, AIMessage, SystemMessage

from schemas.chat_schema import ChatMessageResponse
from core.config import settings

def get_llm_response(chat_history: List[ChatMessageResponse]) -> str:

    # system message for general purpose chatbot
    system_message = SystemMessage(
        content=(
            "You are a helpful, knowledgeable, and friendly AI assistant. "
            "Respond to the user’s questions and engage in natural, multi-turn conversation "
            "across a wide range of topics."
        )
    )

    prompt_template = [system_message]
    
    for chat in chat_history:
        if isinstance(chat, dict):
            role = chat.get('role')
            content = chat.get('content')
        else:
            role = chat.role
            content = chat.content
        if role == "user":
            prompt_template.append(HumanMessage(content=content))
        elif role == "assistant":
            prompt_template.append(AIMessage(content=content))

    llm = ChatGroq(
        temperature = 0.0,
        model_name = "llama-3.3-70b-versatile",
        groq_api_key = settings.GROK_API_KEY,
    )

    response = llm.invoke(prompt_template)
    return response.content
    
    
        


  