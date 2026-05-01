# AI Chatbot

## Project Preview
A full-stack AI chatbot built with **FastAPI** (backend) and **Angular** (frontend), powered by **LangChain** and **Mistral-7B** from Hugging Face.


## Project Structure
```
chatbot/
├── backend/          # FastAPI + LangChain + Hugging Face
└── frontend/         # Angular chatbot UI
```

---

## Backend (FastAPI)

### Setup

```powershell
cd backend

# Create & activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set your Hugging Face API token (free account at https://huggingface.co)
copy .env.example .env
# Edit .env and add your HUGGINGFACEHUB_API_TOKEN
```

### Run

```powershell
uvicorn app.main:app --reload
```

- API: http://localhost:8000
- Swagger docs: http://localhost:8000/docs
- Health check: http://localhost:8000/api/health

---

## Frontend (Angular)

### Setup & Run

```powershell
cd frontend
npm install
npm start
```

- App: http://localhost:4200

---

## Tech Stack

| Layer     | Technology                          |
|-----------|-------------------------------------|
| Backend   | FastAPI, Uvicorn, Python 3.10+      |
| AI/LLM    | LangChain, Hugging Face Inference API, Mistral-7B-Instruct |
| Frontend  | Angular 19, SCSS                    |

---

## Getting a Free Hugging Face Token

1. Sign up at https://huggingface.co (free)
2. Go to **Settings → Access Tokens**
3. Create a token with **Read** permission
4. Add it to `backend/.env` as `HUGGINGFACEHUB_API_TOKEN`