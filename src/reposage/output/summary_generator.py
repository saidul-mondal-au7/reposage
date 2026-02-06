import json
from pathlib import Path


def generate_summary_json(
    scan_output: dict,
    architecture_output: dict,
    security_output: dict,
    performance_output: dict,
    roadmap_output: dict,
    output_path: str = "outputs/summary.json",
):
    """
    Aggregate agent outputs into a concise summary.json
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    repo_path = Path(scan_output.get("repo_path", "unknown"))
    repo_name = repo_path.name

    summary = {
        "repo_name": repo_name,
        "language_detected": scan_output.get("detected_languages", []),
        "frameworks": architecture_output.get("frameworks", []),
        "architecture_type": architecture_output.get("architecture_type"),
        "top_security_risks": [
            {
                "issue": issue["issue"],
                "severity": issue["severity"],
                "file": (issue.get("affected_files") or [None])[0],
            }
            for issue in security_output.get("issues", [])
            if issue["severity"] in ("High", "Medium")
        ][:5],
        "top_performance_risks": [
            {
                "issue": issue["issue"],
                "severity": issue["severity"],
                "file": issue.get("affected_file"),
            }
            for issue in performance_output.get("issues", [])
            if issue["severity"] in ("High", "Medium")
        ][:5],
        "roadmap": [
            {
                "priority": item["priority"],
                "task": item["task"],
                "effort": item["effort"],
            }
            for item in (
                roadmap_output.get("immediate_fixes", [])
                + roadmap_output.get("short_term", [])
            )
        ][:5],
    }

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"✅ summary.json written to {output_path.resolve()}")
    return output_path
