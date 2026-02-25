from pathlib import Path

def ensure_directories() -> None:
    """
    Creates necessary output directories if they do not exist.
    
    Structure:
    - output/media/images
    - output/media/audio
    """
    base_output = Path("output")
    media_dir = base_output / "media"
    
    directories = [
        media_dir / "images",
        media_dir / "audio"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
    
    print("Directories are ready.")
