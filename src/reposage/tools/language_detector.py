from collections import defaultdict
import os
from crewai.tools import tool

EXTENSION_LANGUAGE_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".java": "Java",
    ".go": "Go",
    ".rb": "Ruby",
    ".php": "PHP",
}

@tool("detect_languages")
def detect_languages(files: list[str]) -> list[str]:
    """
    Detect programming languages used in the repository by
    analyzing file extensions and mapping them to known languages.
    """
    counter = defaultdict(int)

    for f in files:
        ext = os.path.splitext(f)[1]
        if ext in EXTENSION_LANGUAGE_MAP:
            counter[EXTENSION_LANGUAGE_MAP[ext]] += 1

    return sorted(counter.keys())
