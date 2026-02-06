from typing import List, Dict
from crewai.tools import tool

DB_QUERY_KEYWORDS = [
    "select ",
    "find(",
    "find_one",
    "query(",
    ".execute(",
    ".fetchall(",
]


@tool("detect_n_plus_one")
def detect_n_plus_one(file_path: str, content: str) -> List[Dict]:
    """
    Detect possible N+1 database query patterns by identifying
    repeated query execution inside loops.
    """
    findings = []

    lowered = content.lower()

    if "for " in lowered or "foreach" in lowered:
        query_hits = sum(1 for q in DB_QUERY_KEYWORDS if q in lowered)

        if query_hits >= 2:
            findings.append({
                "issue": "Possible N+1 database query pattern",
                "severity": "Medium",
                "file": file_path,
                "likely_symptoms": "High database latency under load",
                "recommended_fix": "Batch queries or use eager loading / joins",
            })

    return findings
