"""Tests for service layer"""
import pytest
import os
import json
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from io import BytesIO

from app.services.whisper_service import WhisperService
from app.services.groq_service import GroqService
from app.services.word_export_service import WordExportService
from app.models.schemas import ActionItem


class TestWhisperService:
    """Tests for WhisperService"""
    
    def test_init_missing_api_key(self):
        """Test that missing API key raises ValueError"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="OPENAI_API_KEY"):
                WhisperService()
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    def test_init_success(self):
        """Test successful initialization"""
        service = WhisperService()
        assert service.client is not None
        assert service.model == "whisper-1"
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @pytest.mark.asyncio
    async def test_transcribe_audio_success(self, sample_audio_file):
        """Test successful transcription"""
        service = WhisperService()
        
        with patch.object(service.client.audio.transcriptions, 'create') as mock_create:
            mock_response = Mock()
            mock_response.text = "Transcribed text"
            mock_create.return_value = mock_response
            
            result = await service.transcribe_audio(sample_audio_file)
            assert result == "Transcribed text"
            mock_create.assert_called_once()
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @pytest.mark.asyncio
    async def test_transcribe_audio_error(self, sample_audio_file):
        """Test transcription error handling"""
        service = WhisperService()
        
        with patch.object(service.client.audio.transcriptions, 'create') as mock_create:
            mock_create.side_effect = Exception("API Error")
            
            with pytest.raises(Exception, match="Whisper API error"):
                await service.transcribe_audio(sample_audio_file)


class TestGroqService:
    """Tests for GroqService"""
    
    def test_init_missing_api_key(self):
        """Test that missing API key raises ValueError"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="GROQ_API_KEY"):
                GroqService()
    
    @patch.dict(os.environ, {"GROQ_API_KEY": "test-key"})
    def test_init_success(self):
        """Test successful initialization"""
        service = GroqService()
        assert service.client is not None
        assert service.model == "llama-3.1-70b-versatile"
        assert service.temperature == 0.3
    
    @patch.dict(os.environ, {"GROQ_API_KEY": "test-key"})
    def test_get_system_prompt(self):
        """Test system prompt generation"""
        service = GroqService()
        prompt = service._get_system_prompt()
        assert "expert meeting analyst" in prompt.lower()
        assert "json" in prompt.lower()
        assert "summary" in prompt.lower()
        assert "participants" in prompt.lower()
    
    @patch.dict(os.environ, {"GROQ_API_KEY": "test-key"})
    @pytest.mark.asyncio
    async def test_analyze_transcription_success(self):
        """Test successful transcription analysis"""
        service = GroqService()
        
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps({
            "summary": "Test summary",
            "participants": ["Alice", "Bob"],
            "decisions": ["Decision 1"],
            "action_items": [{"task": "Task 1", "assignee": "Alice", "deadline": None}]
        })
        
        with patch.object(service.client.chat.completions, 'create', return_value=mock_response):
            result = await service.analyze_transcription("Test transcription")
            
            assert result["summary"] == "Test summary"
            assert len(result["participants"]) == 2
            assert len(result["decisions"]) == 1
            assert len(result["action_items"]) == 1
    
    @patch.dict(os.environ, {"GROQ_API_KEY": "test-key"})
    @pytest.mark.asyncio
    async def test_analyze_transcription_invalid_json(self):
        """Test handling of invalid JSON response"""
        service = GroqService()
        
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Not valid JSON {invalid"
        
        with patch.object(service.client.chat.completions, 'create', return_value=mock_response):
            result = await service.analyze_transcription("Test transcription")
            
            # Should fallback to extracted or default structure
            assert "summary" in result
            assert "participants" in result
            assert "decisions" in result
            assert "action_items" in result
    
    @patch.dict(os.environ, {"GROQ_API_KEY": "test-key"})
    @pytest.mark.asyncio
    async def test_analyze_transcription_api_error(self):
        """Test API error handling"""
        service = GroqService()
        
        with patch.object(service.client.chat.completions, 'create') as mock_create:
            mock_create.side_effect = Exception("API Error")
            
            with pytest.raises(Exception, match="Groq API error"):
                await service.analyze_transcription("Test transcription")
    
    @patch.dict(os.environ, {"GROQ_API_KEY": "test-key"})
    def test_normalize_response(self):
        """Test response normalization"""
        service = GroqService()
        
        # Test with all fields
        response = {
            "summary": "Summary",
            "participants": ["Alice"],
            "decisions": ["Decision"],
            "action_items": []
        }
        normalized = service._normalize_response(response)
        assert normalized == response
        
        # Test with missing fields
        incomplete = {"summary": "Summary"}
        normalized = service._normalize_response(incomplete)
        assert normalized["summary"] == "Summary"
        assert normalized["participants"] == []
        assert normalized["decisions"] == []
        assert normalized["action_items"] == []
    
    @patch.dict(os.environ, {"GROQ_API_KEY": "test-key"})
    def test_extract_json_from_text(self):
        """Test JSON extraction from text"""
        service = GroqService()
        
        # Valid JSON in text
        text = "Some text before {\"summary\": \"Test\"} some text after"
        result = service._extract_json_from_text(text)
        assert result["summary"] == "Test"
        
        # No JSON found
        text = "Just plain text without JSON"
        result = service._extract_json_from_text(text)
        assert "summary" in result
        assert len(result["summary"]) > 0


class TestWordExportService:
    """Tests for WordExportService"""
    
    def test_create_document_success(self):
        """Test successful Word document creation"""
        service = WordExportService()
        
        doc_stream = service.create_document(
            transcription="Test transcription",
            summary="Test summary",
            participants=["Alice", "Bob"],
            decisions=["Decision 1"],
            action_items=[
                ActionItem(task="Task 1", assignee="Alice", deadline="2024-01-15")
            ],
            filename="test_meeting"
        )
        
        assert doc_stream is not None
        assert isinstance(doc_stream, BytesIO)
        assert doc_stream.tell() == 0  # Should be at start
        
        # Verify it's a valid docx file (starts with PK header)
        content = doc_stream.read(4)
        assert content.startswith(b'PK')  # ZIP file header (docx is a ZIP)
    
    def test_create_document_empty_data(self):
        """Test document creation with empty data"""
        service = WordExportService()
        
        doc_stream = service.create_document(
            transcription="",
            summary="",
            participants=[],
            decisions=[],
            action_items=[],
            filename="empty_meeting"
        )
        
        assert doc_stream is not None
        content = doc_stream.read(4)
        assert content.startswith(b'PK')
    
    def test_create_document_default_filename(self):
        """Test document creation with default filename"""
        service = WordExportService()
        
        doc_stream = service.create_document(
            transcription="Test",
            summary="Summary",
            participants=[],
            decisions=[],
            action_items=[]
        )
        
        assert doc_stream is not None

