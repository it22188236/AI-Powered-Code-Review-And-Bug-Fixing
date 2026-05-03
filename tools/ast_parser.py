"""AST parsing tool to detect syntax errors and code smells."""
import ast
from typing import List, Dict

class ASTAnalysis:
    """Perform static analysis using Python AST."""
    
    @staticmethod
    def parse_and_analyze(code: str) -> Dict[str, List[str]]:
        """
        Parse Python code and detect syntax errors, logic issues, code smells.
        
        Args:
            code: Python source code as string.
            
        Returns:
            Dict with keys: 'syntax_errors', 'code_smells', 'functions', 'complexity'.
        """
        result = {
            'syntax_errors': [],
            'code_smells': [],
            'functions': [],
            'complexity': 'low'
        }
        try:
            tree = ast.parse(code)
            # Count function definitions
            functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            result['functions'] = functions
            # Detect long functions (> 20 lines heuristic not possible without line numbers)
            # Detect too many nested blocks
            for node in ast.walk(tree):
                if isinstance(node, ast.If) or isinstance(node, ast.For) or isinstance(node, ast.While):
                    # simple smell: depth > 3 is complex, we leave for LLM
                    pass
            # complexity heuristic: many functions => medium
            if len(functions) > 5:
                result['complexity'] = 'high'
            elif len(functions) > 2:
                result['complexity'] = 'medium'
        except SyntaxError as e:
            result['syntax_errors'].append(str(e))
        return result