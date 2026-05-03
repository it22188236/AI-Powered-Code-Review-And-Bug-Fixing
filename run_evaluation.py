#!/usr/bin/env python
import subprocess
import sys
import logging
from datetime import datetime
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
eval_log = LOG_DIR / f"evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    filename=eval_log,
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

def run_pytest():
    print("Running pytest tests...")
    result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    logging.info(f"Pytest stdout:\n{result.stdout}")
    if result.stderr:
        logging.error(f"Pytest stderr:\n{result.stderr}")
    return result.returncode

def run_llm_judge_tests():
    from core.llm import call_llm
    from core.state import ReviewState
    from agents.coordinator import coordinator_node
    from agents.code_analyzer import code_analyzer_node
    from agents.security_auditor import security_auditor_node
    from agents.fix_suggester import fix_suggester_node

    print("\nRunning LLM-as-a-Judge tests...")
    results = {}

    def is_yes(response):
        return response.strip().upper().startswith("YES")

    # Coordinator
    state = ReviewState(user_input="test.py", current_step="start")
    output = coordinator_node(state)
    judge_prompt = f"Is the following output from a coordinator agent valid? It must contain 'next_agent' key. Output: {output}. Answer YES or NO."
    verdict = call_llm("Judge", judge_prompt, model="phi3:mini")
    results["Coordinator"] = "PASS" if is_yes(verdict) else "FAIL"
    logging.info(f"Coordinator judge verdict: {verdict} -> {results['Coordinator']}")

    # Code Analyzer
    state = ReviewState(user_input="data/sample_code.py", code_content="print('hello')")
    out = code_analyzer_node(state)
    judge_prompt = f"Does this output contain 'analysis_result' with 'ast' and 'llm_summary' keys? Output: {out}. Answer YES or NO."
    verdict = call_llm("Judge", judge_prompt, model="phi3:mini")
    results["CodeAnalyzer"] = "PASS" if is_yes(verdict) else "FAIL"
    logging.info(f"CodeAnalyzer judge verdict: {verdict} -> {results['CodeAnalyzer']}")

    # Security Auditor
    state = ReviewState(user_input="dummy", code_content="password='123'")
    out = security_auditor_node(state)
    judge_prompt = f"Does output contain 'security_findings' as a non-empty dict? Output: {out}. Answer YES or NO."
    verdict = call_llm("Judge", judge_prompt, model="phi3:mini")
    results["SecurityAuditor"] = "PASS" if is_yes(verdict) else "FAIL"
    logging.info(f"SecurityAuditor judge verdict: {verdict} -> {results['SecurityAuditor']}")

    # Fix Suggester - check that 'fix_suggestions' exists and length > 10
    state = ReviewState(user_input="dummy", code_content="x=1", analysis_result={}, security_findings={})
    out = fix_suggester_node(state)
    # Direct check: if 'fix_suggestions' in out and len(out['fix_suggestions']) > 10, PASS immediately (no LLM judge)
    if "fix_suggestions" in out and len(out["fix_suggestions"]) > 10:
        results["FixSuggester"] = "PASS"
        logging.info(f"FixSuggester direct check: length={len(out['fix_suggestions'])} -> PASS")
    else:
        # Fallback to LLM judge (rare)
        judge_prompt = f"Does output contain 'fix_suggestions' with a string longer than 10 characters? Output preview: {str(out)[:200]}. Answer YES or NO."
        verdict = call_llm("Judge", judge_prompt, model="phi3:mini")
        results["FixSuggester"] = "PASS" if is_yes(verdict) else "FAIL"
        logging.info(f"FixSuggester judge verdict: {verdict} -> {results['FixSuggester']}")

    print("LLM-as-a-Judge Results:")
    for agent, result in results.items():
        print(f"  {agent}: {result}")
        logging.info(f"LLM-Judge {agent}: {result}")
    return all(r == "PASS" for r in results.values())

def main():
    print("=== Starting Full Evaluation Suite ===")
    logging.info("=== Evaluation Run Started ===")

    pytest_exit = run_pytest()
    judge_pass = run_llm_judge_tests()

    if pytest_exit == 0 and judge_pass:
        print("\n✅ ALL TESTS PASSED (pytest + LLM-as-a-Judge)")
        logging.info("ALL TESTS PASSED")
        sys.exit(0)
    else:
        print("\n❌ SOME TESTS FAILED. Check logs/evaluation_*.log for details.")
        logging.error("TESTS FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()