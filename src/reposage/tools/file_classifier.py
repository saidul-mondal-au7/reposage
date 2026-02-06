import os
from crewai.tools import tool

ENTRY_POINT_HINTS = {
    "main.py", "app.py", "server.py", "index.js",
    "main.js", "app.js", "Application.java"
}

CONFIG_EXTENSIONS = (".env", ".yaml", ".yml", ".json", ".toml", ".ini")

DEPENDENCY_FILES = {
    "requirements.txt",
    "pyproject.toml",
    "package.json",
    "pom.xml",
    "build.gradle"
}

@tool("classify_files")
def classify_files(files: list[str]) -> dict:
    """
    Classify repository files into entry points, configuration files,
    and dependency/manifest files based on file names and extensions.
    """
    entry_points = []
    config_files = []
    dependency_files = []

    for f in files:
        name = os.path.basename(f)

        if name in ENTRY_POINT_HINTS:
            entry_points.append(f)

        if name.endswith(CONFIG_EXTENSIONS):
            config_files.append(f)

        if name in DEPENDENCY_FILES:
            dependency_files.append(f)

    return {
        "entry_points": entry_points,
        "config_files": config_files,
        "dependency_files": dependency_files
    }
