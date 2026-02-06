from collections import defaultdict
import os

EXTENSION_LANGUAGE_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".java": "Java",
    ".go": "Go",
    ".rb": "Ruby",
    ".php": "PHP",
}

def detect_languages(files: list[str]) -> list[str]:
    counter = defaultdict(int)

    for f in files:
        ext = os.path.splitext(f)[1]
        if ext in EXTENSION_LANGUAGE_MAP:
            counter[EXTENSION_LANGUAGE_MAP[ext]] += 1

    return sorted(counter.keys())
