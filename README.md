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

### 1. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
# Create .env file with your API keys:
# OPENAI_API_KEY=your_openai_key
# GROQ_API_KEY=your_groq_key

# Run server
uvicorn app.main:app --reload
```

Backend will run at `http://localhost:8000`  
API Documentation: `http://localhost:8000/docs`

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will run at `http://localhost:3000`

### Usage

1. Open `http://localhost:3000` in your browser
2. Upload an audio file (MP3 or WAV)
3. Select language (English or Hebrew)
4. Click "Start Transcription"
5. View results and export to Word if needed

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
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── business/     # Business logic
│   │   ├── services/     # External services (Whisper, Groq, Word)
│   │   ├── models/       # Pydantic schemas
│   │   ├── prompts/      # AI prompts
│   │   └── utils/        # Utilities (logging)
│   ├── tests/            # Unit tests (42 tests)
│   ├── logs/             # AI service logs
│   └── requirements.txt
├── frontend/             # React frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── services/     # API client
│   │   ├── App.jsx       # Main app
│   │   └── index.js
│   └── package.json
└── PROJECT_PLAN.md
```

## Technology Stack

### Backend
- **Framework:** FastAPI (Python 3.8+)
- **AI Services:** OpenAI Whisper API, Groq API (Llama 3.3)
- **Export:** python-docx (Word documents)
- **Testing:** pytest, pytest-asyncio
- **Logging:** Structured logging for AI interactions

### Frontend
- **Framework:** React 18
- **HTTP Client:** Axios
- **File Upload:** react-dropzone
- **Styling:** Tailwind CSS
- **UI:** Modern, responsive design with drag-and-drop

### Language Support
- English
- Hebrew (with RTL support in Word export)

## License

MIT
