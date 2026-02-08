import subprocess
from pathlib import Path
from crewai.tools import tool

@tool("clone_repo")
def clone_repo(repo_url: str, base_dir: str = "repos") -> str:
    """
    Clone a git repository safely using shallow clone.
    Submodules are intentionally skipped.
    """
    base_path = Path(base_dir)
    base_path.mkdir(parents=True, exist_ok=True)

    repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    repo_path = base_path / repo_name

    if repo_path.exists():
        return str(repo_path)
    
    try:
        subprocess.run(
            [
                "git",
                "clone",
                "--depth", "1",
                "--branch", "main",
                "--single-branch",
                "--no-tags",
                "--recurse-submodules=no",  # 🔥 explicit
                repo_url,
                str(repo_path),
            ],
            check=True,
            timeout=180,
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"Git clone timed out for {repo_url}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Git clone failed: {e}")

    return str(repo_path)
