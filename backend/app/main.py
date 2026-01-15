"""FastAPI application entry point"""
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print(f"Loaded environment variables from: {env_path}")
else:
    print(f"Warning: .env file not found at {env_path}")
    print("Make sure to create a .env file with OPENAI_API_KEY and GROQ_API_KEY")

from app.api.routes import transcription, health

# Create FastAPI app
app = FastAPI(
    title="Meeting Transcription & Summarization API",
    description="API for transcribing audio meetings and generating summaries",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(transcription.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Meeting Transcription & Summarization API",
        "version": "1.0.0",
        "docs": "/docs"
    }

