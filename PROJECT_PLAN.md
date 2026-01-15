# Meeting Transcription & Summarization System - Project Plan

## Project Overview
Full-stack application that transcribes audio meetings, generates summaries, identifies participants, and extracts decisions/action items using AI APIs.

**Estimated Time:** 5 hours

---

## 1. Architecture

```
Frontend (React) 
    ↓ HTTP Requests
Backend API (FastAPI)
    ↓ API Calls
    ├─→ Whisper API (Transcription)
    └─→ Groq API (Summarization, Analysis)
    ↓ Processing
Temporary File Storage
    ↓ Export
Word Document Generator (python-docx)
```

**Clear Separation:**
- **Frontend**: React app in `/frontend` directory, runs independently
- **Backend**: FastAPI app in `/backend` directory, runs independently
- Communication via REST API only

---

## 2. Technology Stack

### Frontend (`/frontend`)
- React (with hooks)
- Axios (HTTP client)
- React Dropzone (file upload)
- Tailwind CSS (styling)

### Backend (`/backend`)
- **FastAPI** (async Python web framework)
- python-multipart (file upload handling)
- openai (Whisper API client)
- groq (Groq API client)
- python-docx (Word document generation)
- python-dotenv (environment variables)

### AI APIs
- **OpenAI Whisper API** (transcription)
- **Groq API** (summarization & analysis - using Llama/Mixtral models)

---

## 3. Project Structure

```
meeting-transcription-system/
├── frontend/                    # React application
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.jsx
│   │   │   ├── ProgressBar.jsx
│   │   │   ├── TranscriptionView.jsx
│   │   │   ├── SummaryView.jsx
│   │   │   ├── ParticipantsView.jsx
│   │   │   ├── ActionItemsView.jsx
│   │   │   └── ExportButton.jsx
│   │   ├── services/
│   │   │   └── api.js          # API calls to backend
│   │   ├── App.jsx
│   │   └── index.js
│   ├── package.json
│   └── README.md
│
├── backend/                     # FastAPI application
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI app entry point
│   │   ├── routes/
│   │   │   └── transcription.py
│   │   ├── services/
│   │   │   ├── whisper_service.py
│   │   │   ├── groq_service.py
│   │   │   └── word_export.py
│   │   └── utils/
│   │       └── file_handler.py
│   ├── requirements.txt
│   └── README.md
│
├── .env.example
├── .gitignore
├── README.md
└── .PROCESS.md
```

---

## 4. API Endpoints

### Backend (FastAPI)

```
POST /api/transcribe
  - Accepts: multipart/form-data with audio file (mp3/wav)
  - Returns: {
      transcription: string,
      summary: string,
      participants: string[],
      decisions: string[],
      action_items: [{task, assignee, deadline}]
    }

GET /api/export
  - Query params: transcription, summary, participants, decisions, action_items
  - Returns: Word document file download (.docx)
```

---

## 5. Implementation Phases

### Phase 1: Backend Setup (1 hour)
- Initialize FastAPI project with virtual environment
- Create basic server with CORS, health check endpoint
- Set up file upload endpoint (validate mp3/wav, size limits)
- Configure environment variables (.env.example)

### Phase 2: Whisper Integration (1 hour)
- Integrate OpenAI Whisper API for transcription
- Handle temporary file storage (cleanup after processing)
- Error handling for API failures

### Phase 3: Groq Integration (1.5 hours)
- Integrate Groq API (Llama 3.1 or Mixtral model)
- Design and implement system prompt (see Section 6)
- Parse JSON responses (summary, participants, decisions, action items)
- Error handling and retry logic

### Phase 4: Frontend Development (1 hour)
- Create React app
- Build UI components (upload, progress, results display)
- Connect to backend API
- Handle loading states and errors

### Phase 5: Word Export (0.5 hours)
- Backend: Use python-docx to generate Word document
- Frontend: Add export button, trigger download

### Phase 6: Polish & Testing (0.5 hours)
- Error handling improvements
- UI/UX polish (loading states, notifications)
- End-to-end testing with sample audio files

---

## 6. System Prompt Design

### Prompt Structure

```
You are an expert meeting analyst. Analyze the following meeting transcription and extract key information.

TRANSCRIPTION:
{transcription_text}

Provide the following in JSON format:

1. **summary**: A concise 2-3 paragraph overview of the meeting, highlighting main topics discussed.

2. **participants**: A list of all unique speakers/participants identified. If speaker identification is not possible, use ["Speaker 1", "Speaker 2", etc.].

3. **decisions**: An array of strings describing all decisions, conclusions, or agreements reached.

4. **action_items**: An array of objects with:
   - "task": description of the task
   - "assignee": person responsible (or "Unassigned")
   - "deadline": deadline mentioned (or null)

Return ONLY valid JSON in this exact format:
{
  "summary": "...",
  "participants": ["..."],
  "decisions": ["..."],
  "action_items": [
    {"task": "...", "assignee": "...", "deadline": "..."}
  ]
}
```

### Design Rationale
- **Structured JSON**: Ensures easy parsing
- **Clear format**: Reduces parsing errors
- **Flexible participants**: Handles cases without speaker diarization
- **Actionable items**: Structured format with assignee/deadline

---

## 7. AI Usage Strategy

### Whisper API
- Model: `whisper-1`
- Language: Auto-detect
- Error handling: Retry logic for rate limits

### Groq API
- Model: `llama-3.1-70b-versatile` or `mixtral-8x7b-32768`
- Temperature: 0.3 (deterministic for structured output)
- Max Tokens: 4000
- Response Format: JSON (parse text response, handle malformed JSON)

### Smart Usage Principles
- Iterative prompt refinement based on test results
- JSON parsing with fallback/retry
- Graceful error handling
- Token management for long transcriptions

---

## 8. Key Challenges & Solutions

**Speaker Diarization**: Whisper may not identify speakers → Prompt Groq to identify from context, fallback to "Speaker 1", "Speaker 2"

**Long Audio Files**: API limits, processing time → Show progress indicators, consider chunking if needed

**Structured Output Parsing**: LLM may return malformed JSON → Implement JSON parsing with fallback, retry with clearer instructions

**Temporary Storage**: Files need cleanup → Use tempfile module, cleanup after processing

---

## 9. Testing Strategy

- Happy path: Upload mp3 → Get all outputs → Export Word
- File validation: Reject invalid formats, oversized files
- API failures: Handle Whisper/Groq errors gracefully
- Edge cases: Empty/short audio, long recordings (30+ min)
- Multiple speakers: Verify participant identification

---

## 10. Deployment

### Local Development
- **Frontend**: `cd frontend && npm start` (runs on port 3000)
- **Backend**: `cd backend && uvicorn app.main:app --reload` (runs on port 8000)
- Frontend configured to call backend at `http://localhost:8000`

### Production (Optional)
- Frontend: Vercel/Netlify
- Backend: Render/Railway/Fly.io
- File storage: Temporary (in-memory or local filesystem)

---

## 11. Documentation Deliverables

### README.md
- Project overview, setup instructions, API docs, environment variables

### .PROCESS.md
- Planning process, AI usage details (prompts, iterations), obstacles encountered, solutions, actual time spent, final system prompt + explanation

### GitHub Repository
- Clean commit history, proper .gitignore, separate frontend/backend directories

---

## 12. Time Allocation

| Phase | Task | Time |
|-------|------|------|
| 1 | Backend Setup (FastAPI) | 1 hour |
| 2 | Whisper Integration | 1 hour |
| 3 | Groq Integration | 1.5 hours |
| 4 | Frontend Development | 1 hour |
| 5 | Word Export | 0.5 hours |
| 6 | Polish & Testing | 0.5 hours |
| **Total** | | **5 hours** |

---

## 13. Success Criteria

✅ Upload mp3/wav files  
✅ Generate full transcription  
✅ Generate meeting summary  
✅ Identify participants  
✅ Extract decisions & action items  
✅ Export to Word document  
✅ Clean, intuitive UI  
✅ Proper error handling  
✅ Clear frontend/backend separation  

---

## 14. Next Steps

1. Set up GitHub repository
2. Initialize backend (FastAPI) and frontend (React) separately
3. Get API keys (OpenAI Whisper, Groq)
4. Create `.env.example` files for both projects
5. Implement backend endpoints
6. Integrate Whisper API
7. Integrate Groq API with system prompt
8. Build frontend components
9. Implement Word export
10. Test end-to-end
11. Write documentation (.PROCESS.md with time tracking)

---

**Ready for implementation!**
