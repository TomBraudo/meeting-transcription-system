"""Tests for business logic layer"""
import pytest
import os
from unittest.mock import Mock, patch, AsyncMock

from app.business.transcription_service import TranscriptionBusinessService
from app.models.schemas import ActionItem


class TestTranscriptionBusinessService:
    """Tests for TranscriptionBusinessService"""
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key", "GROQ_API_KEY": "test-key"})
    def test_init(self):
        """Test service initialization"""
        service = TranscriptionBusinessService()
        assert service.whisper_service is not None
        assert service.groq_service is not None
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key", "GROQ_API_KEY": "test-key"})
    @pytest.mark.asyncio
    async def test_process_audio_file_success(self, mock_upload_file):
        """Test successful audio file processing"""
        service = TranscriptionBusinessService()
        
        # Mock the services
        service.whisper_service.transcribe_audio = AsyncMock(
            return_value="Test transcription"
        )
        service.groq_service.analyze_transcription = AsyncMock(return_value={
            "summary": "Test summary",
            "participants": ["Alice", "Bob"],
            "decisions": ["Decision 1"],
            "action_items": [
                {"task": "Task 1", "assignee": "Alice", "deadline": "2024-01-15"}
            ]
        })
        
        result = await service.process_audio_file(mock_upload_file)
        
        assert result.transcription == "Test transcription"
        assert result.summary == "Test summary"
        assert len(result.participants) == 2
        assert len(result.decisions) == 1
        assert len(result.action_items) == 1
        assert isinstance(result.action_items[0], ActionItem)
        
        # Verify services were called
        service.whisper_service.transcribe_audio.assert_called_once()
        service.groq_service.analyze_transcription.assert_called_once()
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key", "GROQ_API_KEY": "test-key"})
    @pytest.mark.asyncio
    async def test_process_audio_file_invalid_format(self):
        """Test processing with invalid file format"""
        service = TranscriptionBusinessService()
        
        mock_file = Mock()
        mock_file.filename = "test.txt"
        
        with pytest.raises(ValueError, match="Unsupported file type"):
            await service.process_audio_file(mock_file)
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key", "GROQ_API_KEY": "test-key"})
    @pytest.mark.asyncio
    async def test_process_audio_file_no_filename(self):
        """Test processing file without filename"""
        service = TranscriptionBusinessService()
        
        mock_file = Mock()
        mock_file.filename = None
        
        with pytest.raises(ValueError, match="Filename is required"):
            await service.process_audio_file(mock_file)
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key", "GROQ_API_KEY": "test-key"})
    @pytest.mark.asyncio
    async def test_process_audio_file_mp3(self, mock_upload_file):
        """Test processing MP3 file"""
        service = TranscriptionBusinessService()
        
        mock_file = Mock()
        mock_file.filename = "test.mp3"
        mock_file.read = AsyncMock(return_value=b'fake audio')
        
        service.whisper_service.transcribe_audio = AsyncMock(return_value="Transcription")
        service.groq_service.analyze_transcription = AsyncMock(return_value={
            "summary": "Summary",
            "participants": [],
            "decisions": [],
            "action_items": []
        })
        
        result = await service.process_audio_file(mock_file)
        assert result.transcription == "Transcription"
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key", "GROQ_API_KEY": "test-key"})
    @pytest.mark.asyncio
    async def test_process_audio_file_wav(self):
        """Test processing WAV file"""
        service = TranscriptionBusinessService()
        
        mock_file = Mock()
        mock_file.filename = "test.wav"
        mock_file.read = AsyncMock(return_value=b'fake audio')
        
        service.whisper_service.transcribe_audio = AsyncMock(return_value="Transcription")
        service.groq_service.analyze_transcription = AsyncMock(return_value={
            "summary": "Summary",
            "participants": [],
            "decisions": [],
            "action_items": []
        })
        
        result = await service.process_audio_file(mock_file)
        assert result.transcription == "Transcription"
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key", "GROQ_API_KEY": "test-key"})
    @pytest.mark.asyncio
    async def test_process_audio_file_whisper_error(self, mock_upload_file):
        """Test handling Whisper API error"""
        service = TranscriptionBusinessService()
        
        service.whisper_service.transcribe_audio = AsyncMock(
            side_effect=Exception("Whisper API error")
        )
        
        with pytest.raises(Exception):
            await service.process_audio_file(mock_upload_file)
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key", "GROQ_API_KEY": "test-key"})
    @pytest.mark.asyncio
    async def test_process_audio_file_groq_error(self, mock_upload_file):
        """Test handling Groq API error"""
        service = TranscriptionBusinessService()
        
        service.whisper_service.transcribe_audio = AsyncMock(return_value="Transcription")
        service.groq_service.analyze_transcription = AsyncMock(
            side_effect=Exception("Groq API error")
        )
        
        with pytest.raises(Exception):
            await service.process_audio_file(mock_upload_file)
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key", "GROQ_API_KEY": "test-key"})
    @pytest.mark.asyncio
    async def test_process_audio_file_temp_file_cleanup(self, mock_upload_file):
        """Test that temporary files are cleaned up"""
        import tempfile
        
        service = TranscriptionBusinessService()
        
        temp_file_path = None
        
        async def mock_transcribe(file_path):
            nonlocal temp_file_path
            temp_file_path = file_path
            return "Transcription"
        
        service.whisper_service.transcribe_audio = mock_transcribe
        service.groq_service.analyze_transcription = AsyncMock(return_value={
            "summary": "Summary",
            "participants": [],
            "decisions": [],
            "action_items": []
        })
        
        await service.process_audio_file(mock_upload_file)
        
        # Verify temp file was cleaned up
        import os
        assert not os.path.exists(temp_file_path)

