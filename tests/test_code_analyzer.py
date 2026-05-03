import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch
from agents.code_analyzer import code_analyzer_node
from core.state import ReviewState

# Mock LLM to return fast fake summary
def mock_llm(system, user, model="phi3:mini"):
    return "Mock analysis summary: syntax error detected."

@patch("agents.code_analyzer.call_llm", side_effect=mock_llm)
def test_code_analyzer_detects_syntax_error(mock_llm_func):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("def broken(")
        temp_path = f.name
    try:
        state = ReviewState(user_input=temp_path)
        result = code_analyzer_node(state)
        assert "syntax_errors" in result["analysis_result"]["ast"]
        assert len(result["analysis_result"]["ast"]["syntax_errors"]) > 0
    finally:
        Path(temp_path).unlink()