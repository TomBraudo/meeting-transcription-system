# Meeting Transcription & Summarization System

AI-powered full-stack application for transcribing audio meetings and generating summaries.

## Features

- 🎙️ Audio transcription (Whisper API)
- 📝 Meeting summarization (Groq LLM)
- 👥 Participant identification
- ✅ Decisions & action items extraction
- 📄 Word document export
- 📊 Logging of AI responses

## Quick Start

### Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cd backend
cp .env.example .env
# Add your OPENAI_API_KEY and GROQ_API_KEY to .env

# Run server
uvicorn app.main:app --reload
```

Backend: `http://localhost:8000`
API Docs: `http://localhost:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm start
```

Frontend: `http://localhost:3000`

## Testing

```bash
# Unit tests
cd backend
pytest

# Test with real audio
python test_api.py path/to/audio.mp3
```

## Environment Variables

Create `backend/.env`:
```
OPENAI_API_KEY=your_key
GROQ_API_KEY=your_key
```

## Project Structure

```
├── backend/          # FastAPI backend
│   ├── app/         # Application code
│   │   ├── api/     # API routes
│   │   ├── business/ # Business logic
│   │   ├── services/ # External services
│   │   └── models/  # Data schemas
│   ├── tests/       # Unit tests
│   └── logs/        # AI service logs
├── frontend/        # React frontend (TBD)
└── requirements.txt # Python dependencies
```

## Technology Stack

- **Backend:** FastAPI, Python 3.8+
- **AI:** OpenAI Whisper, Groq (Llama 3.3)
- **Export:** python-docx
- **Testing:** pytest

## License

MIT
