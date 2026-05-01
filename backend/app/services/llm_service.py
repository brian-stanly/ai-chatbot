import os
from typing import List

from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from app.models.schemas import Message

# Use a small, fast model
MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

SYSTEM_PROMPT = (
    "You are a helpful, friendly, and knowledgeable AI assistant. "
    "Answer questions clearly and concisely. "
    "If you don't know something, say so honestly."
)


def _build_llm() -> ChatHuggingFace:
    """Initialize the Hugging Face pipeline to run locally."""
    print(f"Loading local model {MODEL_ID}... (This might take a moment)")
    
    from transformers import AutoConfig
    try:
        config = AutoConfig.from_pretrained(MODEL_ID)
        # Fix for 'PreTrainedConfig' object has no attribute 'max_position_embeddings'
        if not hasattr(config, "max_position_embeddings"):
            config.max_position_embeddings = 2048
    except Exception as e:
        print(f"Error loading config: {e}")
        config = None

    hf_pipeline = pipeline(
        "text-generation",
        model=MODEL_ID,
        config=config,
        max_new_tokens=50,
        device="cpu",  # Use CPU for better compatibility in this environment
        return_full_text=False,
    )
    
    llm = HuggingFacePipeline(pipeline=hf_pipeline)
    return ChatHuggingFace(llm=llm, model_id=MODEL_ID)


# Lazily initialized model (avoids loading on import)
_llm: ChatHuggingFace | None = None


def get_llm() -> ChatHuggingFace:
    global _llm
    if _llm is None:
        _llm = _build_llm()
    return _llm


def build_langchain_messages(history: List[Message], new_message: str) -> list:
    """Convert conversation history + new message into LangChain message objects."""
    messages = [SystemMessage(content=SYSTEM_PROMPT)]

    for msg in history:
        if msg.role == "user":
            messages.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            messages.append(AIMessage(content=msg.content))

    messages.append(HumanMessage(content=new_message))
    return messages


async def get_chat_response(history: List[Message], user_message: str) -> str:
    """
    Send user message (with conversation history) to the LLM
    and return the assistant's reply as a string.
    """
    from transformers import AutoTokenizer
    from fastapi.concurrency import run_in_threadpool

    # Initialize model if not already done
    llm_wrapper = get_llm()
    pipeline_obj = llm_wrapper.llm.pipeline
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

    # Build chat list for template
    chat = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in history:
        chat.append({"role": msg.role, "content": msg.content})
    chat.append({"role": "user", "content": user_message})

    # Apply template
    prompt = tokenizer.apply_chat_template(
        chat, 
        tokenize=False, 
        add_generation_prompt=True
    )

    # Run heavy synchronous inference in a thread pool
    def _invoke():
        outputs = pipeline_obj(
            prompt,
            max_new_tokens=150, # Give it more room
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.95,
        )
        return outputs[0]["generated_text"]

    full_output = await run_in_threadpool(_invoke)
    
    # Extract only the assistant's response (pipeline_obj is set to return_full_text=False usually, 
    # but let's be safe if it returns full text)
    if prompt in full_output:
        reply = full_output.replace(prompt, "").strip()
    else:
        reply = full_output.strip()

    print(f"LLM Response: '{reply}'")
    return reply
