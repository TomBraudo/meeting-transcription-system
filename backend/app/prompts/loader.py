"""Prompt loader utility for loading prompts from files"""
from pathlib import Path
from typing import Optional


class PromptLoader:
    """Utility class for loading prompts from text files"""
    
    def __init__(self):
        self.prompts_dir = Path(__file__).parent
        self._cache = {}
    
    def load(self, prompt_name: str) -> str:
        """
        Load a prompt from a text file
        
        Args:
            prompt_name: Name of the prompt file (without .txt extension)
        
        Returns:
            Prompt content as string
        """
        # Check cache first
        if prompt_name in self._cache:
            return self._cache[prompt_name]
        
        # Load from file
        prompt_path = self.prompts_dir / f"{prompt_name}.txt"
        
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
        
        with open(prompt_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # Cache the prompt
        self._cache[prompt_name] = content
        
        return content
    
    def get_language_instruction(self, language: Optional[str] = None) -> str:
        """
        Get language-specific instruction prefix (supports English and Hebrew only)
        
        Args:
            language: Language code ('en' or 'he')
        
        Returns:
            Language instruction string
        """
        if not language or language == 'en':
            return ""
        
        if language in ['he', 'iw', 'hebrew']:
            return "The transcription is in Hebrew. Provide your analysis (summary, decisions, action items) in Hebrew as well. Keep the JSON structure in English but content in Hebrew.\n\n"
        
        return ""


# Global instance
prompt_loader = PromptLoader()
