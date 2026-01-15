"""Whisper API service for audio transcription"""
import os
from datetime import datetime
from typing import Optional

from openai import OpenAI

from app.utils.logger import get_ai_logger


class WhisperService:
    """Service for handling Whisper API transcription"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = OpenAI(api_key=api_key)
        self.model = "whisper-1"
        self.logger = get_ai_logger("whisper")
    
    async def transcribe_audio(self, audio_file_path: str, language: Optional[str] = None) -> str:
        """
        Transcribe audio file using Whisper API
        
        Args:
            audio_file_path: Path to the audio file
            language: Optional language code (e.g., 'en', 'es'). If None, auto-detect.
        
        Returns:
            Transcribed text as string
        """
        try:
            self.logger.info(f"Starting transcription for file: {audio_file_path}")
            self.logger.info(f"Model: {self.model}, Language: {language or 'auto-detect'}")
            
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model=self.model,
                    file=audio_file,
                    language=language
                )
                
                transcription_text = transcript.text
                
                # Log transcription result
                self.logger.info("=" * 80)
                self.logger.info("WHISPER TRANSCRIPTION RESULT")
                self.logger.info("=" * 80)
                self.logger.info(f"Timestamp: {datetime.now().isoformat()}")
                self.logger.info(f"Audio File: {audio_file_path}")
                self.logger.info(f"Model: {self.model}")
                self.logger.info(f"Language: {language or 'auto-detect'}")
                self.logger.info("-" * 80)
                self.logger.info("TRANSCRIPTION:")
                self.logger.info("-" * 80)
                self.logger.info(transcription_text)
                self.logger.info("=" * 80)
                self.logger.info(f"Transcription length: {len(transcription_text)} characters")
                self.logger.info("=" * 80)
                
                return transcription_text
        except Exception as e:
            error_msg = f"Whisper API error: {str(e)}"
            self.logger.error(f"TRANSCRIPTION FAILED: {error_msg}")
            self.logger.error(f"File: {audio_file_path}")
            raise Exception(error_msg)

