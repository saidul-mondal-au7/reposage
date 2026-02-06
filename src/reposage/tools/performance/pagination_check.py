from typing import List, Dict
from crewai.tools import tool

PAGINATION_KEYWORDS = [
    "limit",
    "offset",
    "page",
    "pagesize",
    "cursor",
]


@tool("detect_missing_pagination")
def detect_missing_pagination(file_path: str, content: str) -> List[Dict]:
    """
    Detect API endpoints or database queries that return large result sets
    without implementing pagination mechanisms.
    """
    findings = []

    lowered = content.lower()

    if "get" in lowered or "list" in lowered:
        if "select" in lowered or "find(" in lowered:
            if not any(k in lowered for k in PAGINATION_KEYWORDS):
                findings.append({
                    "issue": "API endpoint without pagination",
                    "severity": "Medium",
                    "file": file_path,
                    "likely_symptoms": "High memory usage and slow response times",
                    "recommended_fix": "Add pagination using limit/offset or cursor-based pagination",
                })

    return findings
