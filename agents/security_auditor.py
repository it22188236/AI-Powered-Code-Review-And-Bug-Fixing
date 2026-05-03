from tools.vuln_scanner import VulnScanner
from core.llm import call_llm
from core.logger import log_tool_call, log_agent_output

SYSTEM_PROMPT = """You are Security Auditor. Use VulnScanner.scan(code) to find hardcoded passwords, SQL injection, XSS. Then explain risks."""
def security_auditor_node(state):
    code = state.code_content
    findings = VulnScanner.scan(code)
    log_tool_call("SecurityAuditor", "VulnScanner.scan", {"code_length": len(code)}, str(findings))
    
    prompt = f"Security scan found:\n{findings}\nExplain each risk briefly."
    llm_analysis = call_llm(SYSTEM_PROMPT, prompt)
    state.security_findings = findings
    state.current_step = "security_done"
    log_agent_output("SecurityAuditor", {"findings": findings, "llm_analysis": llm_analysis})
    return {"security_findings": findings, "current_step": state.current_step}