from tools.vuln_scanner import VulnScanner

def test_security_scanner_finds_hardcoded_password():
    code = 'password = "secret123"'
    findings = VulnScanner.scan(code)
    assert len(findings["hardcoded_password"]) > 0

def test_security_scanner_finds_sql_injection():
    code = 'query = "SELECT * FROM users WHERE id = " + user_id'
    findings = VulnScanner.scan(code)
    assert len(findings["sql_injection"]) > 0

def test_security_scanner_finds_api_key():
    code = 'API_KEY = "abc123xyz"'
    findings = VulnScanner.scan(code)
    assert len(findings["api_key"]) > 0