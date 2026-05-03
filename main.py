from core.state import create_initial_state
from core.orchestrator import create_linear_graph
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_python_file>")
        return
    file_path = sys.argv[1]
    initial_state = create_initial_state(file_path)
    app = create_linear_graph()
    final_state = app.invoke(initial_state)
    print("Review completed. Report saved at data/review_report.md")
    print("Logs saved in logs/ folder")

if __name__ == "__main__":
    main()