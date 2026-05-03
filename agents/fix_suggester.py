from tools.file_writer import write_report
from core.llm import call_llm
from core.logger import log_tool_call, log_agent_output

SYSTEM_PROMPT = """You are Fix Suggester. Based on code analysis and security findings, produce a concrete fix report in Markdown. Include line suggestions."""

def fix_suggester_node(state):
    code = state.code_content
    analysis = state.analysis_result
    security = state.security_findings
    prompt = f"""Code:
{code}

Analysis: {analysis}
Security issues: {security}

Write a detailed markdown report titled "Code Review Report" with sections: 1. Summary, 2. Code Issues (syntax/logic), 3. Security Vulnerabilities, 4. Recommended Fixes (with code examples)."""
    
    report = call_llm(SYSTEM_PROMPT, prompt)
    # Write report to file
    output_path = "data/review_report.md"
    success = write_report(report, output_path)
    log_tool_call("FixSuggester", "write_report", {"output_path": output_path}, f"success={success}")
    
    state.fix_suggestions = report
    state.current_step = "completed"
    log_agent_output("FixSuggester", {"fix_suggestions_length": len(report), "report_path": output_path})
    # ✅ Return the actual report content, not just the path
    return {"fix_suggestions": report, "current_step": state.current_step}