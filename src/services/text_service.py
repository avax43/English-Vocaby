import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

class TextGenerationService:
    """Generates vocabulary word details using Google Gemini API."""

    def __init__(self) -> None:
        """Initializes the Gemini client using GEMINI_API_KEY from .env."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment.")
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-3-flash-preview"

    def generate_word_details(self, word: str) -> dict:
        """
        Generates enriched details for a given English word.

        Args:
            word: A single English word to enrich.

        Returns:
            A dictionary with keys: word, translation, sentence, image_prompt.
            Returns an empty dict on failure.
        """
        prompt = f"""You are an English Language Teacher. For the word '{word}', return a VALID JSON object ONLY.
Do not use Markdown formatting, no code blocks, no backticks.
Return exactly this structure:
{{
    "word": "{word}",
    "translation": "Arabic translation of the word",
    "sentence": "A simple A2-level English sentence using the word (3-7 words)",
    "image_prompt": "A specific visual description for an AI image generator, minimalist vector art style, no text"
}}"""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            clean_text = response.text.strip().replace("```json", "").replace("```", "").strip()
            return json.loads(clean_text)
        except json.JSONDecodeError as e:
            print(f"JSON parse error for '{word}': {e}")
            return {}
        except Exception as e:
            print(f"API error for '{word}': {e}")
            return {}
