"""Tests for API layer (routes)"""
import pytest
import json
from unittest.mock import AsyncMock, Mock
from io import BytesIO

from app.models.schemas import ActionItem
from app.api.routes.transcription import get_transcription_service, get_word_export_service


class TestTranscriptionRoutes:
    """Tests for transcription API routes"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
        assert "version" in response.json()
    
    def test_transcribe_endpoint_success(self, client):
        """Test successful transcription endpoint"""
        from app.models.schemas import TranscriptionResponse
        from app.business.transcription_service import TranscriptionBusinessService
        from app.main import app
        
        mock_result = TranscriptionResponse(
            transcription="Test transcription",
            summary="Test summary",
            participants=["Alice", "Bob"],
            decisions=["Decision 1"],
            action_items=[
                ActionItem(task="Task 1", assignee="Alice", deadline="2024-01-15")
            ]
        )
        
        mock_service = Mock(spec=TranscriptionBusinessService)
        mock_service.process_audio_file = AsyncMock(return_value=mock_result)
        
        # Override dependency
        app.dependency_overrides[get_transcription_service] = lambda: mock_service
        
        try:
            # Create a test file
            files = {"file": ("test.mp3", b"fake audio content", "audio/mpeg")}
            response = client.post("/api/transcribe", files=files)
            
            assert response.status_code == 200
            data = response.json()
            assert data["transcription"] == "Test transcription"
            assert data["summary"] == "Test summary"
            assert len(data["participants"]) == 2
            assert len(data["decisions"]) == 1
            assert len(data["action_items"]) == 1
        finally:
            # Clean up override
            app.dependency_overrides.clear()
    
    def test_transcribe_endpoint_no_file(self, client):
        """Test transcription endpoint without file"""
        response = client.post("/api/transcribe")
        assert response.status_code == 422  # Validation error
    
    def test_transcribe_endpoint_invalid_file_type(self, client):
        """Test transcription endpoint with invalid file type"""
        from app.business.transcription_service import TranscriptionBusinessService
        from app.main import app
        
        mock_service = Mock(spec=TranscriptionBusinessService)
        mock_service.process_audio_file = AsyncMock(side_effect=ValueError("Unsupported file type"))
        
        app.dependency_overrides[get_transcription_service] = lambda: mock_service
        
        try:
            files = {"file": ("test.txt", b"content", "text/plain")}
            response = client.post("/api/transcribe", files=files)
            assert response.status_code == 400
        finally:
            app.dependency_overrides.clear()
    
    def test_transcribe_endpoint_processing_error(self, client):
        """Test transcription endpoint with processing error"""
        from app.business.transcription_service import TranscriptionBusinessService
        from app.main import app
        
        mock_service = Mock(spec=TranscriptionBusinessService)
        mock_service.process_audio_file = AsyncMock(side_effect=Exception("Processing error"))
        
        app.dependency_overrides[get_transcription_service] = lambda: mock_service
        
        try:
            files = {"file": ("test.mp3", b"content", "audio/mpeg")}
            response = client.post("/api/transcribe", files=files)
            
            assert response.status_code == 500
            assert "error" in response.json()["detail"].lower()
        finally:
            app.dependency_overrides.clear()
    
    def test_export_get_endpoint_success(self, client):
        """Test GET export endpoint"""
        from app.services.word_export_service import WordExportService
        from app.main import app
        
        mock_doc = BytesIO(b'fake docx content')
        mock_doc.seek(0)
        mock_service = Mock(spec=WordExportService)
        mock_service.create_document = Mock(return_value=mock_doc)
        
        app.dependency_overrides[get_word_export_service] = lambda: mock_service
        
        try:
            response = client.get(
                "/api/export",
                params={
                    "transcription": "Test transcription",
                    "summary": "Test summary",
                    "participants": "Alice,Bob",
                    "decisions": "Decision 1,Decision 2",
                    "action_items": json.dumps([
                        {"task": "Task 1", "assignee": "Alice", "deadline": "2024-01-15"}
                    ]),
                    "filename": "test_meeting"
                }
            )
            
            assert response.status_code == 200
            assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            assert "attachment" in response.headers["content-disposition"]
        finally:
            app.dependency_overrides.clear()
    
    def test_export_post_endpoint_success(self, client):
        """Test POST export endpoint"""
        from app.services.word_export_service import WordExportService
        from app.main import app
        
        mock_doc = BytesIO(b'fake docx content')
        mock_doc.seek(0)
        mock_service = Mock(spec=WordExportService)
        mock_service.create_document = Mock(return_value=mock_doc)
        
        app.dependency_overrides[get_word_export_service] = lambda: mock_service
        
        try:
            payload = {
                "transcription": "Test transcription",
                "summary": "Test summary",
                "participants": ["Alice", "Bob"],
                "decisions": ["Decision 1"],
                "action_items": [
                    {"task": "Task 1", "assignee": "Alice", "deadline": "2024-01-15"}
                ],
                "filename": "test_meeting"
            }
            
            response = client.post("/api/export", json=payload)
            
            assert response.status_code == 200
            assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        finally:
            app.dependency_overrides.clear()
    
    def test_export_get_endpoint_empty_data(self, client):
        """Test GET export endpoint with empty data"""
        from app.services.word_export_service import WordExportService
        from app.main import app
        
        mock_doc = BytesIO(b'fake docx content')
        mock_doc.seek(0)
        mock_service = Mock(spec=WordExportService)
        mock_service.create_document = Mock(return_value=mock_doc)
        
        app.dependency_overrides[get_word_export_service] = lambda: mock_service
        
        try:
            response = client.get(
                "/api/export",
                params={
                    "transcription": "",
                    "summary": "",
                    "participants": "",
                    "decisions": "",
                    "action_items": "[]"
                }
            )
            
            assert response.status_code == 200
        finally:
            app.dependency_overrides.clear()
    
    def test_export_endpoint_error(self, client):
        """Test export endpoint error handling"""
        from app.services.word_export_service import WordExportService
        from app.main import app
        
        mock_service = Mock(spec=WordExportService)
        mock_service.create_document = Mock(side_effect=Exception("Export error"))
        
        app.dependency_overrides[get_word_export_service] = lambda: mock_service
        
        try:
            payload = {
                "transcription": "Test",
                "summary": "Summary",
                "participants": [],
                "decisions": [],
                "action_items": []
            }
            
            response = client.post("/api/export", json=payload)
            assert response.status_code == 500
        finally:
            app.dependency_overrides.clear()

