"""Groq API service for meeting analysis"""
import os
import json
import re
from datetime import datetime
from typing import Dict, Optional

from groq import Groq

from app.utils.logger import get_ai_logger
from app.prompts.loader import prompt_loader


class GroqService:
    """Service for handling Groq API analysis"""
    
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        self.client = Groq(api_key=api_key)
        # Updated model - llama-3.1-70b-versatile was deprecated on 01/24/25
        self.model = "llama-3.3-70b-versatile"  # Fast and capable model (replacement for llama-3.1-70b-versatile)
        self.temperature = 0.3  # Lower temperature for more deterministic structured output
        self.logger = get_ai_logger("groq")
    
    def _get_system_prompt(self, language: Optional[str] = None) -> str:
        """Get the system prompt for meeting analysis"""
        # Load base prompt from file
        base_prompt = prompt_loader.load("meeting_analysis")
        
        # Add language-specific instruction prefix if needed
        lang_instruction = prompt_loader.get_language_instruction(language)
        
        return f"{lang_instruction}{base_prompt}"
    
    async def analyze_transcription(self, transcription: str, language: Optional[str] = None) -> Dict:
        """
        Analyze transcription and extract meeting insights
        
        Args:
            transcription: The transcribed meeting text
            language: Optional language code for language-aware analysis
        
        Returns:
            Dictionary with summary, participants, decisions, and action_items
        """
        try:
            self.logger.info("Starting Groq analysis of transcription")
            self.logger.info(f"Model: {self.model}, Temperature: {self.temperature}")
            self.logger.info(f"Language: {language or 'auto-detect'}")
            self.logger.info(f"Transcription length: {len(transcription)} characters")
            
            user_prompt = f"TRANSCRIPTION:\n{transcription}\n\nAnalyze this transcription and provide the requested information in JSON format."
            
            # Try to use JSON mode if supported, otherwise rely on prompt engineering
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self._get_system_prompt(language)},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=self.temperature,
                    max_tokens=4000,
                    response_format={"type": "json_object"}
                )
            except TypeError:
                # If response_format is not supported, try without it
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self._get_system_prompt(language)},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=self.temperature,
                    max_tokens=4000
                )
            
            content = response.choices[0].message.content
            
            # Parse JSON response
            try:
                result = json.loads(content)
            except json.JSONDecodeError:
                # If response format doesn't enforce JSON, try to extract JSON from text
                self.logger.warning("Failed to parse JSON directly, attempting extraction")
                result = self._extract_json_from_text(content)
            
            # Validate and normalize response structure
            normalized_result = self._normalize_response(result)
            
            # Log analysis result
            self.logger.info("=" * 80)
            self.logger.info("GROQ ANALYSIS RESULT")
            self.logger.info("=" * 80)
            self.logger.info(f"Timestamp: {datetime.now().isoformat()}")
            self.logger.info(f"Model: {self.model}")
            self.logger.info(f"Temperature: {self.temperature}")
            self.logger.info("-" * 80)
            self.logger.info("SUMMARY:")
            self.logger.info("-" * 80)
            self.logger.info(normalized_result.get("summary", "N/A"))
            self.logger.info("-" * 80)
            self.logger.info("PARTICIPANTS:")
            self.logger.info("-" * 80)
            for participant in normalized_result.get("participants", []):
                self.logger.info(f"  - {participant}")
            self.logger.info("-" * 80)
            self.logger.info("DECISIONS:")
            self.logger.info("-" * 80)
            for decision in normalized_result.get("decisions", []):
                self.logger.info(f"  - {decision}")
            self.logger.info("-" * 80)
            self.logger.info("ACTION ITEMS:")
            self.logger.info("-" * 80)
            for item in normalized_result.get("action_items", []):
                self.logger.info(f"  Task: {item.get('task', 'N/A')}")
                self.logger.info(f"    Assignee: {item.get('assignee', 'Unassigned')}")
                if item.get('deadline'):
                    self.logger.info(f"    Deadline: {item.get('deadline')}")
                self.logger.info("")
            self.logger.info("=" * 80)
            self.logger.info("FULL JSON RESPONSE:")
            self.logger.info("=" * 80)
            self.logger.info(json.dumps(normalized_result, indent=2, ensure_ascii=False))
            self.logger.info("=" * 80)
            
            return normalized_result
            
        except Exception as e:
            error_msg = f"Groq API error: {str(e)}"
            self.logger.error(f"ANALYSIS FAILED: {error_msg}")
            self.logger.error(f"Transcription length: {len(transcription)} characters")
            raise Exception(error_msg)
    
    def _extract_json_from_text(self, text: str) -> Dict:
        """Extract JSON from text response if not properly formatted"""
        # Try to find JSON object in the text
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        # Fallback: return empty structure
        return {
            "summary": text[:500] if text else "Unable to generate summary",
            "participants": [],
            "decisions": [],
            "action_items": []
        }
    
    def _normalize_response(self, response: Dict) -> Dict:
        """Normalize response to ensure all required fields exist"""
        return {
            "summary": response.get("summary", ""),
            "participants": response.get("participants", []),
            "decisions": response.get("decisions", []),
            "action_items": response.get("action_items", [])
        }

