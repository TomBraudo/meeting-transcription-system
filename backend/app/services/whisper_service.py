"""Whisper API service for audio transcription"""
import os
from openai import OpenAI
from typing import Optional
import tempfile


class WhisperService:
    """Service for handling Whisper API transcription"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = OpenAI(api_key=api_key)
        self.model = "whisper-1"
    
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
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model=self.model,
                    file=audio_file,
                    language=language
                )
                return transcript.text
        except Exception as e:
            raise Exception(f"Whisper API error: {str(e)}")

