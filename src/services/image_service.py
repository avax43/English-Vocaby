import os
import re
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class ImageGenerationService:
    """Generates and downloads images using the Pixazo API."""

    def __init__(self) -> None:
        """Initializes the service with API endpoint and headers from .env."""
        self.url = "https://gateway.pixazo.ai/flux-1-schnell/v1/getData"
        self.headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "Ocp-Apim-Subscription-Key": os.getenv("Ocp-Apim-Subscription-Key", "")
        }
        self.output_dir = Path("output/media/images")

    def generate_image_url(self, prompt: str) -> str:
        """
        Calls the Pixazo API to generate an image from a prompt.

        Args:
            prompt: A text description for the image.

        Returns:
            The direct URL of the generated image, or empty string on failure.
        """
        payload = {
            "prompt": prompt,
            "num_steps": 4,
            "seed": 15,
            "height": 512,
            "width": 512
        }

        try:
            response = requests.post(
                self.url, json=payload, headers=self.headers, timeout=30
            )
            response.raise_for_status()
            data = response.json()
            return data.get("output", "")
        except Exception as e:
            print(f"Image generation error: {e}")
            return ""

    def download_image(self, url: str, filename: str) -> str:
        """
        Downloads an image from a URL and saves it locally.

        Args:
            url: Direct URL to the image.
            filename: Base name for the saved file (without extension).

        Returns:
            Relative path to the saved image, or empty string on failure.
        """
        safe_name = re.sub(r'[^\w\-]', '_', filename)
        file_path = self.output_dir / f"{safe_name}.png"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            with open(file_path, "wb") as f:
                f.write(response.content)
            return str(file_path)
        except Exception as e:
            print(f"Image download error for '{filename}': {e}")
            return ""
