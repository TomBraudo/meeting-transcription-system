"""Pytest configuration and fixtures"""
import pytest
import os
import tempfile
from unittest.mock import Mock, AsyncMock, patch
from fastapi.testclient import TestClient

# Set dummy environment variables before importing app to avoid initialization errors
# These will be mocked/overridden in actual tests
os.environ.setdefault("OPENAI_API_KEY", "test-key-dummy")
os.environ.setdefault("GROQ_API_KEY", "test-key-dummy")

from app.main import app
from app.services.whisper_service import WhisperService
from app.services.groq_service import GroqService
from app.services.word_export_service import WordExportService


@pytest.fixture
def client():
    """FastAPI test client"""
    return TestClient(app)


@pytest.fixture
def mock_whisper_service():
    """Mock WhisperService"""
    service = Mock(spec=WhisperService)
    service.transcribe_audio = AsyncMock(return_value="This is a test transcription.")
    return service


@pytest.fixture
def mock_groq_service():
    """Mock GroqService"""
    service = Mock(spec=GroqService)
    service.analyze_transcription = AsyncMock(return_value={
        "summary": "Test meeting summary",
        "participants": ["Speaker 1", "Speaker 2"],
        "decisions": ["Decision 1", "Decision 2"],
        "action_items": [
            {
                "task": "Complete task 1",
                "assignee": "John Doe",
                "deadline": "2024-01-15"
            }
        ]
    })
    return service


@pytest.fixture
def sample_audio_file():
    """Create a temporary audio file for testing"""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    temp_file.write(b'fake audio content')
    temp_file.close()
    yield temp_file.name
    if os.path.exists(temp_file.name):
        os.unlink(temp_file.name)


@pytest.fixture
def sample_transcription_data():
    """Sample transcription response data"""
    return {
        "transcription": "This is a test transcription of a meeting.",
        "summary": "Test meeting summary discussing various topics.",
        "participants": ["Alice", "Bob", "Charlie"],
        "decisions": [
            "We will proceed with the new feature",
            "Budget approved for Q1"
        ],
        "action_items": [
            {
                "task": "Implement new feature",
                "assignee": "Alice",
                "deadline": "2024-02-01"
            },
            {
                "task": "Prepare budget report",
                "assignee": "Bob",
                "deadline": None
            }
        ]
    }


@pytest.fixture
def mock_upload_file():
    """Mock FastAPI UploadFile"""
    mock_file = Mock()
    mock_file.filename = "test_audio.mp3"
    mock_file.read = AsyncMock(return_value=b'fake audio content')
    mock_file.content_type = "audio/mpeg"
    return mock_file

