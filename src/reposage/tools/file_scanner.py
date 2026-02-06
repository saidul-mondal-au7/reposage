import os

IGNORE_DIRS = {
    ".git", "node_modules", "dist", "build",
    "__pycache__", ".venv", "venv"
}

def scan_repository(root_path: str) -> list[str]:
    """
    Recursively scan repository and return list of file paths.
    """
    files = []

    for root, dirs, filenames in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file in filenames:
            files.append(os.path.join(root, file))

    return files
