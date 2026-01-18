# Meeting Transcription & Summarization System

AI-powered full-stack application that transcribes audio meetings and generates summaries, participant lists, decisions, and action items.

## Features

- 🎙️ Audio transcription (MP3/WAV)
- 📝 AI-powered meeting summary
- 👥 Participant identification
- ✅ Decisions & action items extraction
- 📄 Word document export with RTL support
- 🌐 Language support: Auto-detect, English, Hebrew

## Architecture

```
React Frontend (Port 3000)
    ↓ REST API
FastAPI Backend (Port 8000)
    ├─→ Whisper API (Transcription)
    └─→ Groq API (Analysis)
```

**Backend Layers:**
- API → Business → Service → Model
- Clean separation of concerns
- Dependency injection pattern

## Quick Start

### 1. Get API Keys

- **OpenAI API Key**: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Groq API Key**: [console.groq.com/keys](https://console.groq.com/keys)

### 2. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API keys
echo "OPENAI_API_KEY=your_openai_key" > .env
echo "GROQ_API_KEY=your_groq_key" >> .env

# Run server
uvicorn app.main:app --reload
```

Backend: `http://localhost:8000`  
API Docs: `http://localhost:8000/docs`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm start
```

Frontend: `http://localhost:3000`

### 4. Usage

1. Open `http://localhost:3000`
2. Select language (Auto-detect, English, or Hebrew)
3. Upload audio file (drag & drop or click)
4. Click "Start Transcription"
5. View results and export to Word

## Technology Stack

**Backend:** FastAPI, Python 3.8+, OpenAI Whisper API, Groq API (Llama 3.3), python-docx  
**Frontend:** React 18, Axios, react-dropzone, Tailwind CSS  
**Testing:** pytest, pytest-asyncio (42 unit tests)

## API Endpoints

### POST /api/transcribe
Upload audio file and get analysis.

**Parameters:**
- `file` - Audio file (MP3/WAV)
- `language` (optional) - 'en', 'he', or null for auto-detect

**Response:**
```json
{
  "transcription": "...",
  "summary": "...",
  "participants": [...],
  "decisions": [...],
  "action_items": [...]
}
```

### POST /api/export
Export to Word document.

### GET /health
Health check endpoint.

## Project Structure

```
Assignment/
├── backend/
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── business/    # Business logic
│   │   ├── services/    # External APIs
│   │   ├── models/      # Pydantic schemas
│   │   └── prompts/     # AI prompts
│   ├── tests/           # 42 unit tests
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API client
│   │   └── App.jsx
│   └── package.json
└── README.md
```

## Troubleshooting

**Backend won't start:** Check `.env` file exists with valid API keys  
**Frontend won't start:** Ensure backend is running, check Node.js 16+  
**CORS errors:** Start backend before frontend

---

**Built with FastAPI, React, Whisper API, and Groq AI**
