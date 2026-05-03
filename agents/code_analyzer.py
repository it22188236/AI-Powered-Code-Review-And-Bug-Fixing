from tools.file_reader import read_file
from tools.ast_parser import ASTAnalysis
from core.llm import call_llm
from core.logger import log_tool_call, log_agent_output

SYSTEM_PROMPT = """You are Code Analyzer Agent. You use tools:
- read_file(file_path) to get source code.
- ASTAnalysis.parse_and_analyze(code) to detect syntax errors and code smells.

Based on tool results, produce a concise analysis summary.
"""

def code_analyzer_node(state):
    # Use tool: read file
    try:
        log_tool_call("CodeAnalyzer", "read_file", {"file_path": state.user_input}, "")
        code = read_file(state.user_input)
        state.code_content = code
    except Exception as e:
        state.errors.append(str(e))
        return {"errors": state.errors, "next_agent": "FINISH"}
    
    # Use tool: AST analysis
    ast_result = ASTAnalysis.parse_and_analyze(code)
    log_tool_call("CodeAnalyzer", "ASTAnalysis.parse_and_analyze", {"code_length": len(code)}, str(ast_result))
    
    # Call LLM to summarize
    prompt = f"Analyze this code:\n{code}\n\nAST analysis: {ast_result}\nProvide a short report of issues."
    llm_out = call_llm(SYSTEM_PROMPT, prompt)
    state.analysis_result = {"ast": ast_result, "llm_summary": llm_out}
    state.current_step = "analysis_done"
    log_agent_output("CodeAnalyzer", state.analysis_result)
    return {"analysis_result": state.analysis_result, "code_content": state.code_content, "current_step": state.current_step}