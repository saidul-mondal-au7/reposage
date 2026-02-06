import re
from typing import List, Dict
from crewai.tools import tool

SECRET_PATTERNS = {
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "Generic API Key": r"api[_-]?key\s*=\s*['\"][A-Za-z0-9_\-]{16,}['\"]",
    "JWT Secret": r"jwt[_-]?secret\s*=\s*['\"].+['\"]",
    "Password Assignment": r"password\s*=\s*['\"].+['\"]",
    "Private Key": r"-----BEGIN (RSA|EC|DSA)? PRIVATE KEY-----",
}


@tool("scan_for_secrets")
def scan_for_secrets(file_path: str, content: str) -> List[Dict]:
    """
    Scan source code for hardcoded secrets such as API keys,
    passwords, JWT secrets, and private keys using regex patterns.
    """
    findings = []

    for name, pattern in SECRET_PATTERNS.items():
        if re.search(pattern, content, re.IGNORECASE):
            findings.append({
                "issue": f"Hardcoded secret detected: {name}",
                "severity": "High",
                "file": file_path,
                "recommended_fix": "Move secrets to environment variables or a secure secret manager",
            })

    return findings
