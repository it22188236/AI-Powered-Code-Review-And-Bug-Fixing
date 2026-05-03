# core/orchestrator.py

from langgraph.graph import StateGraph, END
from core.state import ReviewState

# Import agent nodes
from agents.code_analyzer import code_analyzer_node
from agents.security_auditor import security_auditor_node
from agents.fix_suggester import fix_suggester_node


def create_linear_graph():
    """
    Creates a simple linear workflow for code review:
    
    CodeAnalyzer → SecurityAuditor → FixSuggester → END
    
    This version removes dynamic routing and coordinator logic
    for simplicity and predictability.
    """

    workflow = StateGraph(ReviewState)

    # Add nodes
    workflow.add_node("CodeAnalyzer", code_analyzer_node)
    workflow.add_node("SecurityAuditor", security_auditor_node)
    workflow.add_node("FixSuggester", fix_suggester_node)

    # Define execution flow
    workflow.set_entry_point("CodeAnalyzer")
    workflow.add_edge("CodeAnalyzer", "SecurityAuditor")
    workflow.add_edge("SecurityAuditor", "FixSuggester")
    workflow.add_edge("FixSuggester", END)

    # Compile graph
    return workflow.compile()


# Optional: expose a default graph instance
graph = create_linear_graph()