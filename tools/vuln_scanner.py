"""Regex-based scanner for security vulnerabilities."""
import re
from typing import List, Dict

class VulnScanner:
    """Scan code for hardcoded secrets, SQL injection, XSS patterns."""
    
    PATTERNS = {
        'hardcoded_password': re.compile(r'password\s*=\s*["\'][^"\']+["\']', re.IGNORECASE),
        'sql_injection': re.compile(r'(SELECT|INSERT|UPDATE|DELETE).*\+\s*', re.IGNORECASE),
        'xss': re.compile(r'(innerHTML|document\.write|eval)\s*\(', re.IGNORECASE),
        'api_key': re.compile(r'(api[_-]?key|token)\s*=\s*["\'][^"\']+["\']', re.IGNORECASE)
    }
    
    @staticmethod
    def scan(code: str) -> Dict[str, List[str]]:
        """
        Scan source code for security vulnerabilities.
        
        Args:
            code: Source code string.
            
        Returns:
            Dict mapping vulnerability type to list of matched lines/snippets.
        """
        findings = {k: [] for k in VulnScanner.PATTERNS.keys()}
        lines = code.splitlines()
        for i, line in enumerate(lines, 1):
            for vuln_type, pattern in VulnScanner.PATTERNS.items():
                if pattern.search(line):
                    findings[vuln_type].append(f"Line {i}: {line.strip()}")
        return findings