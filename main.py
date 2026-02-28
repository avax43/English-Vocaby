import sys
import json
from pathlib import Path
from src.utils import ensure_directories
from src.data_handler import read_words, save_data
from src.services.text_service import TextGenerationService

def main() -> None:
    """
    Main entry point for the English-Vocaby project.
    Generates word details via Gemini and saves them to vocabulary.json.
    Old data is replaced on every run.
    """
    # 1. Ensure directory structure
    ensure_directories()

    # 2. Read words from input
    input_file = Path("input/words.txt")
    words = read_words(input_file)
    print(f"Loaded {len(words)} words from {input_file}")

    # 3. Generate enriched data for each word and collect results
    data_file = Path("output/vocabulary.json")
    service = TextGenerationService()
    vocabulary = []

    for word in words:
        print(f"Processing: {word}")
        result = service.generate_word_details(word)
        if result:
            vocabulary.append(result)
        else:
            print(f"Skipped '{word}' due to API error.")

    # 4. Save fresh data, replacing old content
    save_data(data_file, vocabulary)
    print(f"\nSaved {len(vocabulary)} words to {data_file}")

if __name__ == "__main__":
    main()
