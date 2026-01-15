# Meeting Transcription & Summarization - Backend

FastAPI backend for transcribing audio meetings and generating summaries using Whisper and Groq APIs.

## Architecture

**Layered architecture:**
- **API Layer** (`app/api/`): Routes and endpoints
- **Business Layer** (`app/business/`): Business logic orchestration
- **Service Layer** (`app/services/`): External API integrations (Whisper, Groq, Word export)
- **Model Layer** (`app/models/`): Pydantic schemas for data validation

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create `.env` file in the `backend/` directory:
```bash
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
```

### 3. Run the Server
```bash
uvicorn app.main:app --reload
```

API available at: `http://localhost:8000`

## API Documentation

Interactive docs: `http://localhost:8000/docs`

### Main Endpoints

**POST /api/transcribe**
- Upload audio file (mp3/wav)
- Returns: transcription, summary, participants, decisions, action_items

**POST /api/export**
- Export results to Word document
- Accepts: JSON body with transcription data
- Returns: .docx file

**GET /health**
- Health check endpoint

## Testing

### Run Unit Tests
```bash
pytest
```

### Test with Real Audio File
```bash
python test_api.py path/to/audio.mp3
```

Or use Swagger UI at `http://localhost:8000/docs`

## Features

- 🎙️ Audio transcription (Whisper API)
- 📝 Meeting summarization (Groq API)
- 👥 Participant identification
- ✅ Decisions & action items extraction
- 📄 Word document export
- 📊 Logging of AI responses

## Logs

AI service logs are saved in `logs/`:
- `ai_whisper_YYYYMMDD.log` - Whisper transcription logs
- `ai_groq_YYYYMMDD.log` - Groq analysis logs

## Requirements

- Python 3.8+
- OpenAI API key (for Whisper)
- Groq API key (for LLM analysis)

## Project Structure

```
backend/
├── app/
│   ├── api/          # API routes
│   ├── business/     # Business logic
│   ├── services/     # External services
│   ├── models/       # Pydantic schemas
│   └── utils/        # Utilities (logging)
├── tests/            # Unit tests
├── logs/             # AI service logs
└── test_api.py       # Integration test script
```
