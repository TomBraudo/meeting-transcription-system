"""Groq API service for meeting analysis"""
import os
import json
from groq import Groq
from typing import Dict, List, Optional


class GroqService:
    """Service for handling Groq API analysis"""
    
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-70b-versatile"  # Fast and capable model
        self.temperature = 0.3  # Lower temperature for more deterministic structured output
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for meeting analysis"""
        return """You are an expert meeting analyst. Analyze the following meeting transcription and extract key information.

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
}"""
    
    async def analyze_transcription(self, transcription: str) -> Dict:
        """
        Analyze transcription and extract meeting insights
        
        Args:
            transcription: The transcribed meeting text
        
        Returns:
            Dictionary with summary, participants, decisions, and action_items
        """
        try:
            user_prompt = f"TRANSCRIPTION:\n{transcription}\n\nAnalyze this transcription and provide the requested information in JSON format."
            
            # Try to use JSON mode if supported, otherwise rely on prompt engineering
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self._get_system_prompt()},
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
                        {"role": "system", "content": self._get_system_prompt()},
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
                result = self._extract_json_from_text(content)
            
            # Validate and normalize response structure
            return self._normalize_response(result)
            
        except Exception as e:
            raise Exception(f"Groq API error: {str(e)}")
    
    def _extract_json_from_text(self, text: str) -> Dict:
        """Extract JSON from text response if not properly formatted"""
        import re
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

