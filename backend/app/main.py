from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.chat import router as chat_router

app = FastAPI(
    title="AI Chatbot API",
    description="A FastAPI-powered chatbot using LangChain and Hugging Face Mistral-7B.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Allow Angular dev server (and production) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(chat_router)


@app.get("/")
async def root():
    return {
        "message": "AI Chatbot API is running",
        "docs": "/docs",
        "health": "/api/health",
    }
