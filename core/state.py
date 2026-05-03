"""Global state structure for passing data between agents."""
from typing import Dict, Any, List
from pydantic import BaseModel

class ReviewState(BaseModel):
    """Shared state across all agents."""
    user_input: str = ""                # original request or file path
    code_content: str = ""              # source code read from file
    analysis_result: Dict[str, Any] = {}  # from Code Analyzer
    security_findings: Dict[str, List[str]] = {}  # from Security Auditor
    fix_suggestions: str = ""           # final report from Fix Suggester
    current_step: str = "start"
    errors: List[str] = []

# Helper to create initial state
def create_initial_state(file_path: str) -> ReviewState:
    return ReviewState(
        user_input=file_path,
        current_step="file_reading"
    )