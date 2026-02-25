import json
from pathlib import Path
from typing import List, Dict

def read_words(file_path: str | Path) -> List[str]:
    """
    Reads words from a text file, stripping whitespace and ignoring empty lines.
    
    Args:
        file_path: Path to the input file.
        
    Returns:
        A list of clean word strings.
    """
    path = Path(file_path)
    if not path.exists():
        print(f"Warning: Input file {path} not found.")
        return []
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return [line.strip() for line in lines if line.strip()]
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return []

def load_data(file_path: str | Path) -> List[Dict]:
    """
    Loads vocabulary data from a JSON file.
    
    Args:
        file_path: Path to the JSON file.
        
    Returns:
        A list of dictionaries containing vocabulary data.
    """
    path = Path(file_path)
    if not path.exists():
        return []
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, Exception) as e:
        print(f"Error loading {path}: {e}")
        return []

def save_data(file_path: str | Path, data: List[Dict]) -> None:
    """
    Saves vocabulary data to a JSON file.
    
    Args:
        file_path: Path to the JSON file.
        data: List of dictionaries to save.
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving {path}: {e}")
