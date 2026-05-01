import os
from typing import List

from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from fastapi.concurrency import run_in_threadpool

from app.models.schemas import Message

# Use a small, fast model
MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

SYSTEM_PROMPT = (
    "You are a helpful and friendly AI assistant. "
    "Respond to the user's messages in a natural, conversational way. "
    "Keep your answers helpful and relevant to the conversation."
)


# Lazily initialized model
_llm = None

async def get_chat_response(history: List[Message], user_message: str) -> str:
    """
    Send user message (with conversation history) to the LLM
    and return the assistant's reply as a string.
    """
    global _llm

    if _llm is None:
        # Initialize model if not already done
        llm_wrapper = pipeline(
            "text-generation",
            model=  MODEL_ID,
            max_new_tokens=100,
            device="cpu",  # Use CPU for better compatibility in this environment
            return_full_text=False,
        )

        llm = HuggingFacePipeline(pipeline=llm_wrapper)
        _llm = ChatHuggingFace(llm=llm, model=MODEL_ID)
    

    messages = [SystemMessage(content=SYSTEM_PROMPT)]

    for msg in history:
        if msg.role == "user":
            messages.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            messages.append(AIMessage(content=msg.content))
    
    messages.append(HumanMessage(content=user_message))

    # Run heavy synchronous inference in a thread pool
    def _invoke():
        return _llm.invoke(messages)

    response = await run_in_threadpool(_invoke)
    reply = response.content.strip()

    print(f"LLM Response: '{reply}'")
    return reply
