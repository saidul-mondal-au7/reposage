import os
from crewai.tools import tool
import subprocess

@tool("clone_repo")
def clone_repo(repo_url: str, base_dir: str = "repos") -> str:
    """
    Clone a GitHub repository if not already present.
    Returns local path to the repo.
    """
    os.makedirs(base_dir, exist_ok=True)
    repo_name = repo_url.rstrip("/").split("/")[-1]
    repo_path = os.path.join(base_dir, repo_name)

    if not os.path.exists(repo_path):
        subprocess.run(
            ["git", "clone", repo_url, repo_path],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    return repo_path
