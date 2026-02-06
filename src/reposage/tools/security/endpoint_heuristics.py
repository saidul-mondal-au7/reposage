from typing import List, Dict
from crewai.tools import tool

UNSAFE_ENDPOINT_KEYWORDS = [
    "/admin",
    "/debug",
    "/internal",
    "/test",
]


@tool("detect_unsafe_endpoints")
def detect_unsafe_endpoints(file_path: str, content: str) -> List[Dict]:
    """
    Detect potentially unsafe or sensitive endpoints that may be exposed
    without proper authentication or authorization controls.
    """
    findings = []

    lowered = content.lower()

    for keyword in UNSAFE_ENDPOINT_KEYWORDS:
        if keyword in lowered:
            if "auth" not in lowered and "permission" not in lowered:
                findings.append({
                    "issue": f"Potentially exposed endpoint: {keyword}",
                    "severity": "High",
                    "file": file_path,
                    "recommended_fix": "Protect the endpoint with authentication and authorization checks",
                })

    return findings
