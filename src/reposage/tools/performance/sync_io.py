from typing import List, Dict
from crewai.tools import tool

SYNC_IO_KEYWORDS = [
    "time.sleep",
    "open(",
    "read(",
    "write(",
    "requests.get",
    "requests.post",
]


@tool("detect_sync_io")
def detect_sync_io(file_path: str, content: str) -> List[Dict]:
    """
    Detect potentially blocking synchronous I/O operations that
    may reduce throughput or cause thread blocking under load.
    """
    findings = []

    lowered = content.lower()

    for keyword in SYNC_IO_KEYWORDS:
        if keyword in lowered:
            findings.append({
                "issue": "Potential blocking synchronous I/O operation",
                "severity": "Low",
                "file": file_path,
                "likely_symptoms": "Thread blocking and reduced throughput",
                "recommended_fix": "Use asynchronous I/O or move work to background workers",
            })
            break

    return findings
