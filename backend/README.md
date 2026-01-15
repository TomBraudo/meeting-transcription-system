# Meeting Transcription & Summarization - Backend

FastAPI backend for transcribing audio meetings and generating summaries using Whisper and Groq APIs.

## Architecture

The backend follows a layered architecture:

- **API Layer** (`app/api/`): Routes and endpoints
- **Business Layer** (`app/business/`): Business logic orchestration
- **Service Layer** (`app/services/`): External API integrations (Whisper, Groq, Word export)
- **Model Layer** (`app/models/`): Pydantic schemas for data validation

## Setup

1. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

4. **Run the server:**
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### POST `/api/transcribe`
Upload an audio file (mp3/wav) for transcription and analysis.

**Request:** multipart/form-data with `file` field

**Response:**
```json
{
  "transcription": "...",
  "summary": "...",
  "participants": ["..."],
  "decisions": ["..."],
  "action_items": [...]
}
```

### GET `/api/export`
Export transcription data to Word document (query parameters).

### POST `/api/export`
Export transcription data to Word document (JSON body).

### GET `/health`
Health check endpoint.

## Environment Variables

- `OPENAI_API_KEY`: Required for Whisper API transcription
- `GROQ_API_KEY`: Required for Groq API analysis

