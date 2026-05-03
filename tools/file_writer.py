"""Tool to write reports to local file."""
from pathlib import Path
from typing import Union

def write_report(content: str, output_path: Union[str, Path]) -> bool:
    """
    Write review report to a markdown file.
    
    Args:
        content: Report text (Markdown).
        output_path: Destination file path.
        
    Returns:
        True if successful.
        
    Raises:
        IOError: If write fails.
    """
    path = Path(output_path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        raise IOError(f"Failed to write report: {e}")