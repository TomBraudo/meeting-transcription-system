"""Business logic layer for transcription processing"""
import os
import tempfile
from typing import Optional

from fastapi import UploadFile

from app.services.whisper_service import WhisperService
from app.services.groq_service import GroqService
from app.models.schemas import TranscriptionResponse, ActionItem


class TranscriptionBusinessService:
    """Business logic for orchestrating transcription and analysis"""
    
    def __init__(self):
        self.whisper_service = WhisperService()
        self.groq_service = GroqService()
    
    async def process_audio_file(self, file: UploadFile, language: Optional[str] = None) -> TranscriptionResponse:
        """
        Process audio file: transcribe and analyze
        
        Args:
            file: Uploaded audio file
            language: Optional language code (e.g., 'he' for Hebrew, 'en' for English)
        
        Returns:
            TranscriptionResponse with all extracted information
        """
        # Validate file type
        if not file.filename:
            raise ValueError("Filename is required")
        
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ['.mp3', '.wav']:
            raise ValueError(f"Unsupported file type: {file_ext}. Only .mp3 and .wav are supported.")
        
        # Save uploaded file temporarily
        temp_file = None
        try:
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=file_ext)
            
            # Write uploaded content to temp file
            content = await file.read()
            temp_file.write(content)
            temp_file.flush()
            temp_file.close()
            
            # Transcribe audio with language parameter
            transcription = await self.whisper_service.transcribe_audio(temp_file.name, language=language)
            
            # Analyze transcription with language awareness
            analysis = await self.groq_service.analyze_transcription(transcription, language=language)
            
            # Convert action items to ActionItem objects
            action_items = [
                ActionItem(
                    task=item.get("task", ""),
                    assignee=item.get("assignee", "Unassigned"),
                    deadline=item.get("deadline")
                )
                for item in analysis.get("action_items", [])
            ]
            
            # Build response
            return TranscriptionResponse(
                transcription=transcription,
                summary=analysis.get("summary", ""),
                participants=analysis.get("participants", []),
                decisions=analysis.get("decisions", []),
                action_items=action_items
            )
            
        finally:
            # Clean up temporary file
            if temp_file and os.path.exists(temp_file.name):
                os.unlink(temp_file.name)

