from unittest.mock import patch
from agents.fix_suggester import fix_suggester_node
from core.state import ReviewState

def mock_llm(system, user, model="phi3:mini"):
    return "# Mock Report\n\n## Issues\n- Fake fix suggestion\n- Additional issue to make length over 100 characters easily."

@patch("agents.fix_suggester.call_llm", side_effect=mock_llm)
@patch("agents.fix_suggester.write_report", return_value=True)
def test_fix_suggester_output_is_markdown(mock_write, mock_llm_func):
    state = ReviewState(
        user_input="dummy",
        code_content="x=1",
        analysis_result={},
        security_findings={}
    )
    result = fix_suggester_node(state)
    report = result["fix_suggestions"]
    # Check markdown-like content (no LLM call)
    assert report.startswith("#") or "Report" in report
    assert len(report) > 50   # Now passes because mock returns >50 chars
    assert "##" in report or "Issues" in report