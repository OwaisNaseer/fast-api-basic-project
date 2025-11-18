import os

def save_to_file(content: str, file_path: str) -> None:
    """
    Save string content to a file.
    
    Args:
        content (str): Content to save
        file_path (str): Full file path
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
