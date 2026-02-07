import os
from pathlib import Path
from crewai.tools import tool

IGNORE_DIRS = {
    ".git", "node_modules", "dist", "build",
    "__pycache__", ".venv", "venv"
}

@tool("scan_repository")
def scan_repository(repo_path: str) -> dict:
    """
    Scan repository and return COMPLETE structured metadata
    required by all downstream agents.
    """

    repo_path = os.path.abspath(repo_path)

    all_files = []
    main_dirs = set()
    entry_points = []
    config_files = []
    dependency_files = []

    ENTRY_NAMES = {"main.py", "app.py", "index.js", "server.py", "manage.py"}
    CONFIG_EXTS = {".env", ".yml", ".yaml", ".json", ".toml", ".ini"}
    DEP_FILES = {
        "requirements.txt",
        "pyproject.toml",
        "Pipfile",
        "package.json",
        "pnpm-lock.yaml",
        "poetry.lock",
    }

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for d in dirs:
            main_dirs.add(d)

        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, repo_path)
            all_files.append(rel_path)

            if file in ENTRY_NAMES:
                entry_points.append(rel_path)

            if Path(file).suffix in CONFIG_EXTS:
                config_files.append(rel_path)

            if file in DEP_FILES:
                dependency_files.append(rel_path)

    # 🔑 THIS IS CRITICAL
    return {
        "repo_path": repo_path,
        "total_files_scanned": len(all_files),
        "main_directories": sorted(main_dirs),
        "entry_points": sorted(entry_points),
        "config_files": sorted(config_files),
        "dependency_files": sorted(dependency_files),
        "files": all_files,
        "detected_languages": [],     # ✅ REQUIRED
        "file_summaries": {},         # ✅ REQUIRED
    }

