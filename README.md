# AI Chatbot

A full-stack, session-based AI chatbot application featuring a **Django & Django REST Framework (DRF)** backend and a modern **Angular 21** frontend. The chatbot integrates with **LangChain** and is powered by **Groq Cloud API** using the state-of-the-art `llama-3.3-70b-versatile` model. The application features robust SQLite conversation persistence, allowing multi-turn conversations and history tracking per session.

---

## Project Architecture

```
┌─────────────────────────┐
│       Angular UI        │  (Runs on http://localhost:4200)
│  (Standalone components)│
└────────────┬────────────┘
             │ REST API (HttpClient)
             ▼
┌─────────────────────────┐
│   Django / DRF Backend  │  (Runs on http://localhost:8000)
└──────┬─────────────┬────┘
       │             │
       │ LangChain   │ ORM / DB
       ▼             ▼
┌──────────────┐ ┌───────────────┐
│  Groq Cloud  │ │  SQLite DB    │  (Stores Chat Sessions
│   (LLaMA 3)  │ │ (chatbot.db)  │   & Messages history)
└──────────────┘ └───────────────┘
```

## Project Structure
```
chatbot/
├── backend/                  # Django REST Framework + LangChain + Groq
│   ├── app/                  # Main project configuration (settings, global URLs)
│   ├── chat/                 # Chat application (models, views, serializers, service)
│   │   ├── services/         # LangChain & LLM service integration
│   │   └── migrations/       # Database schema migrations
│   ├── manage.py             # Django management CLI
│   └── requirements.txt      # Backend Python dependencies
└── frontend/                 # Angular chatbot UI (v21)
    ├── src/
    │   ├── app/              # Main App component & services
    │   │   ├── components/   # Standalone UI components (chat-window, message-bubble, etc.)
    │   │   └── services/     # ChatService communicating with backend APIs
    └── package.json          # Frontend packages & scripts
```

---

## Backend (Django & DRF)

### Prerequisites
- Python 3.10+
- A Groq Cloud API Key (Get a free key from the [Groq Console](https://console.groq.com/))

### Setup & Run

1. **Navigate to backend and activate virtual environment:**
   ```powershell
   cd backend
   
   # If environment is not created:
   python -m venv .venv
   
   # Activate on Windows:
   .\.venv\Scripts\activate
   # OR on macOS/Linux:
   source .venv/bin/activate
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   Create a `.env` file from the example and fill in your `GROQ_API_KEY`:
   ```powershell
   copy .env.example .env
   # Open .env and add your GROQ_API_KEY
   ```

4. **Run database migrations (Optional, SQLite db is pre-created):**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

### Key API URLs
- **Backend API Root**: `http://localhost:8000/api/`
- **Swagger Documentation**: `http://localhost:8000/api/docs/` (Interactive API docs built with `drf-yasg`)
- **Django Admin Console**: `http://localhost:8000/admin/`

---

## Frontend (Angular 21)

### Setup & Run

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install node dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

- **Local Web Application URL**: `http://localhost:4200/`

---

## API Specifications

All endpoints are prefixed with `/api`. Below are the core REST endpoints for managing sessions and sending messages:

### 1. Create a Chat Session
* **Endpoint**: `POST /api/v1/session/create/`
* **Request Body**:
  ```json
  {
    "title": "Optional Custom Session Title"
  }
  ```
* **Response**:
  ```json
  {
    "session_id": "a7b3c114-d2a6...",
    "title": "Optional Custom Session Title",
    "created_at": "2026-05-28T10:22:58Z"
  }
  ```

### 2. List Chat Sessions
* **Endpoint**: `GET /api/v1/session/list/`
* **Response**:
  ```json
  [
    {
      "session_id": "a7b3c114-d2a6...",
      "title": "Optional Custom Session Title",
      "created_at": "2026-05-28T10:22:58Z"
    }
  ]
  ```

### 3. Get Conversation History
* **Endpoint**: `GET /api/v1/session/<session_id>/`
* **Response**:
  ```json
  [
    {
      "role": "user",
      "content": "Hello, how can I use Django with Angular?"
    },
    {
      "role": "assistant",
      "content": "You can connect Django and Angular by building a RESTful API..."
    }
  ]
  ```

### 4. Send Message & Generate AI Response
* **Endpoint**: `POST /api/v1/session/<session_id>/`
* **Request Body**:
  ```json
  {
    "message": "Hello, explain Django models."
  }
  ```
* **Response**:
  ```json
  {
    "reply": "Django models are the single, definitive source of truth about your data..."
  }
  ```

### 5. Delete Chat Session & History
* **Endpoint**: `DELETE /api/v1/session/<session_id>/`
* **Response**:
  ```json
  {
    "reply": "Session deleted"
  }
  ```

---

## Tech Stack Details

| Layer | Technology | Description |
|---|---|---|
| **Backend Framework** | Django 5+ & Django REST Framework (DRF) | Core API engine with custom serializers and routing |
| **API Documentation** | drf-yasg (Swagger) | Interactive OpenAPI spec generator and UI at `/api/docs/` |
| **Database** | SQLite3 | Local SQL engine storing persistent `Session` and `Message` tables |
| **Orchestration** | LangChain Core & LangChain Groq | Handles multi-turn chat memory and system prompts |
| **LLM Provider** | Groq Cloud API | Superfast inference processing of requests |
| **LLM Model** | LLaMA 3.3 70B (`llama-3.3-70b-versatile`) | High-capacity conversational model |
| **Frontend Framework** | Angular 21 | Modern SPA using standalone components & reactive Signals |
| **Styling & CSS** | SCSS & Vanilla CSS | Sleek sidebar layout and responsive chat container design |

---

## Setting up your Groq API Key

1. Sign up/log in at [Groq Cloud Console](https://console.groq.com/).
2. Navigate to **API Keys** in the sidebar.
3. Click **Create API Key**, copy the key.
4. Create a `backend/.env` file and insert:
   ```env
   GROQ_API_KEY=gsk_your_key_here
   ```