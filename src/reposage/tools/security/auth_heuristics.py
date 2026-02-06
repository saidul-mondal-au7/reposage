from typing import List, Dict
from crewai.tools import tool

AUTH_KEYWORDS = [
    "login",
    "signin",
    "authenticate",
    "jwt",
    "token",
    "session",
]


@tool("analyze_auth_logic")
def analyze_auth_logic(file_path: str, content: str) -> List[Dict]:
    """
    Analyze authentication-related code to detect weak or unsafe
    authentication practices such as missing validation checks
    or plaintext password handling.
    """
    findings = []

    lowered = content.lower()

    if any(k in lowered for k in AUTH_KEYWORDS):
        if "verify" not in lowered and "validate" not in lowered:
            findings.append({
                "issue": "Authentication logic without explicit validation checks",
                "severity": "Medium",
                "file": file_path,
                "recommended_fix": "Ensure tokens and credentials are properly validated",
            })

        if "password" in lowered and "hash" not in lowered:
            findings.append({
                "issue": "Possible plaintext password handling",
                "severity": "High",
                "file": file_path,
                "recommended_fix": "Use strong password hashing (bcrypt, argon2, scrypt)",
            })

    return findings
