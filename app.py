import streamlit as st
import sys
import os
from pathlib import Path
import tempfile
import subprocess

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.state import ReviewState, create_initial_state
from agents.code_analyzer import code_analyzer_node
from agents.security_auditor import security_auditor_node
from agents.fix_suggester import fix_suggester_node

st.set_page_config(page_title="Multi-Agent Code Reviewer", layout="wide")

st.title("🤖 Multi-Agent Code Review System")
st.markdown("Upload a Python file → 4 Agents analyze → Get Security & Fix Report")

# Sidebar for tests
with st.sidebar:
    st.header("🧪 Run Tests")
    if st.button("Run All Pytest Tests"):
        with st.spinner("Running tests..."):
            result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"], 
                                    capture_output=True, text=True)
            if result.returncode == 0:
                st.success("✅ All 6 tests passed!")
                st.code(result.stdout, language="text")
            else:
                st.error("❌ Some tests failed")
                st.code(result.stdout + "\n\n" + result.stderr, language="text")
    
    st.divider()
    st.header("📊 Agent Status")
    st.write("1. Coordinator - receives file")
    st.write("2. Code Analyzer - syntax/logic")
    st.write("3. Security Auditor - passwords/SQL/XSS")
    st.write("4. Fix Suggester - generates report")

# Main area: file upload and analysis
uploaded_file = st.file_uploader("📁 Upload a Python file (.py)", type=["py"])

if uploaded_file is not None:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name
    
    st.success(f"File uploaded: {uploaded_file.name}")
    
    if st.button("🚀 Run Code Review", type="primary"):
        with st.spinner("Agents are analyzing... (may take 1-2 minutes)"):
            try:
                # Create initial state as a ReviewState object
                state = create_initial_state(tmp_path)
                
                # Step 1: Code Analyzer (modifies state in place)
                st.info("🔍 Agent 2: Code Analyzer working...")
                code_analyzer_node(state)   # don't capture return
                st.write("✅ Code Analyzer done")
                
                # Step 2: Security Auditor (modifies state in place)
                st.info("🔒 Agent 3: Security Auditor working...")
                security_auditor_node(state)
                st.write("✅ Security Auditor done")
                
                # Step 3: Fix Suggester (modifies state in place)
                st.info("📝 Agent 4: Fix Suggester generating report...")
                fix_suggester_node(state)
                st.write("✅ Fix Suggester done")
                
                # Now state contains all results
                report = state.fix_suggestions
                findings = state.security_findings
                
                # Display results
                st.divider()
                st.header("📄 Code Review Report")
                st.markdown(report)
                
                # Show security findings summary
                st.subheader("🔐 Security Findings (raw)")
                if findings:
                    for vuln_type, lines in findings.items():
                        if lines:
                            st.write(f"**{vuln_type}**")
                            for line in lines:
                                st.code(line)
                else:
                    st.write("No security issues found.")
                
                # Download button
                st.download_button(
                    label="⬇️ Download Report as Markdown",
                    data=report,
                    file_name="review_report.md",
                    mime="text/markdown"
                )
                
            except Exception as e:
                st.error(f"Error: {e}")
                import traceback
                st.code(traceback.format_exc())
            finally:
                # Clean up temp file
                os.unlink(tmp_path)
    
    # Option to view existing report
    report_path = Path("data/review_report.md")
    if report_path.exists():
        with open(report_path, "r") as f:
            existing = f.read()
        with st.expander("📄 Last generated report (data/review_report.md)"):
            st.markdown(existing)

st.divider()
st.caption("Multi-Agent System using Ollama phi3:mini | LangGraph | Custom Tools")