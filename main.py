import sys
import json
from pathlib import Path
from src.utils import ensure_directories
from src.data_handler import read_words, save_data
from src.services.text_service import TextGenerationService
from src.services.image_service import ImageGenerationService

def main() -> None:
    """
    Main entry point for the English-Vocaby project.
    Generates word details and images, then saves everything to vocabulary.json.
    Old data is replaced on every run.
    """
    # 1. Ensure directory structure
    ensure_directories()

    # 2. Read words from input
    input_file = Path("input/words.txt")
    words = read_words(input_file)
    print(f"Loaded {len(words)} words from {input_file}")

    # 3. Initialize services
    data_file = Path("output/vocabulary.json")
    text_service = TextGenerationService()
    image_service = ImageGenerationService()
    vocabulary = []

    for word in words:
        print(f"\nProcessing: {word}")

        # 3a. Generate text details
        result = text_service.generate_word_details(word)
        if not result:
            print(f"  Skipped '{word}' -- text generation failed.")
            continue

        # 3b. Generate and download image
        image_prompt = result.get("image_prompt", "")
        if image_prompt:
            print(f"  Generating image...")
            image_url = image_service.generate_image_url(image_prompt)
            if image_url:
                image_path = image_service.download_image(image_url, word)
                result["image_path"] = image_path
                print(f"  [INFO] Image saved: {image_path}")
            else:
                result["image_path"] = ""
                print(f"  [WARN] No image URL returned.")
        else:
            result["image_path"] = ""

        vocabulary.append(result)

    # 4. Save fresh data
    save_data(data_file, vocabulary)
    print(f"\nSaved {len(vocabulary)} words to {data_file}")

if __name__ == "__main__":
    main()
