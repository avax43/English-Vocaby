import sys
import json
from pathlib import Path
from src.utils import ensure_directories
from src.data_handler import read_words, load_data, save_data
from src.services.text_service import TextGenerationService

def main() -> None:
    """
    Main entry point for the English-Vocaby project.
    Generates word details via Gemini and prints results for verification.
    """
    # 1. Ensure directory structure
    ensure_directories()

    # 2. Read words from input
    input_file = Path("input/words.txt")
    words = read_words(input_file)
    print(f"Loaded {len(words)} words from {input_file}")

    # 3. Handle data/database
    data_file = Path("output/vocabulary.json")
    vocabulary = load_data(data_file)

    # 4. Sync words with vocabulary
    existing_words = {entry["word"] for entry in vocabulary}
    added_count = 0

    for word in words:
        if word not in existing_words:
            vocabulary.append({
                "word": word,
                "translation": "",
                "example": ""
            })
            existing_words.add(word)
            added_count += 1

    if added_count > 0:
        print(f"Added {added_count} new words to vocabulary.")

    # 5. Save data
    save_data(data_file, vocabulary)
    print(f"Data saved to {data_file}. Total words: {len(vocabulary)}")

    # 6. Generate word details via Gemini (print only, no save yet)
    print("\n--- Gemini Word Details ---")
    service = TextGenerationService()
    for word in words:
        result = service.generate_word_details(word)
        if result:
            output = json.dumps(result, ensure_ascii=False, indent=2)
            sys.stdout.buffer.write(output.encode("utf-8") + b"\n")
        else:
            print(f"Failed to get details for '{word}'.")

if __name__ == "__main__":
    main()
