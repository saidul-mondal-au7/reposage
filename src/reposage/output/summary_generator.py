import json
from pathlib import Path
from pydantic import BaseModel


def _force_dict(obj):
    """
    CrewAI 1.9.3–safe coercion:
    - dict → dict
    - Pydantic → dict
    - JSON string → dict
    - anything else → {}
    """
    if obj is None:
        return {}

    if isinstance(obj, dict):
        return obj

    if isinstance(obj, BaseModel):
        return obj.model_dump()

    if isinstance(obj, str):
        try:
            parsed = json.loads(obj)
            return parsed if isinstance(parsed, dict) else {}
        except Exception:
            return {}

    return {}


def generate_summary_json(
    scan_output,
    architecture_output,
    security_output,
    performance_output,
    roadmap_output,
    output_path: str = "outputs/summary.json",
):
    # --------------------------------------------------
    # Normalize safely (DO NOT DROP DATA)
    # --------------------------------------------------
    scan = _force_dict(scan_output)
    architecture = _force_dict(architecture_output)
    security = _force_dict(security_output)
    performance = _force_dict(performance_output)
    roadmap = _force_dict(roadmap_output)

    # --------------------------------------------------
    # Prepare output directory
    # --------------------------------------------------
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------
    # Repository metadata
    # --------------------------------------------------
    repo_path = scan.get("repo_path") or "unknown"
    repo_name = Path(repo_path).name if repo_path != "unknown" else "unknown"

    # --------------------------------------------------
    # Build summary
    # --------------------------------------------------
    summary = {
        "repo_name": repo_name,
        "repo_path": repo_path,
        "detected_languages": scan.get("detected_languages", []),
        "architecture_type": architecture.get("architecture_type"),

        "repo_health": {
            "total_files_scanned": scan.get("total_files_scanned", 0),
            "entry_points": scan.get("entry_points", []),
            "main_directories": scan.get("main_directories", []),
            "dependency_files": scan.get("dependency_files", []),
        },

        "top_security_risks": [
            {
                "issue": i.get("issue"),
                "severity": i.get("severity"),
                "file": (i.get("affected_files") or ["N/A"])[0],
            }
            for i in security.get("issues", [])
            if i.get("severity") in {"High", "Medium"}
        ][:5],

        "top_performance_risks": [
            {
                "issue": i.get("issue"),
                "severity": i.get("severity"),
                "file": i.get("affected_file"),
            }
            for i in performance.get("issues", [])
            if i.get("severity") in {"High", "Medium"}
        ][:5],

        "top_roadmap_items": [
            {
                "priority": r.get("priority"),
                "task": r.get("task"),
                "effort": r.get("effort"),
            }
            for r in (
                roadmap.get("immediate_fixes", [])
                + roadmap.get("short_term", [])
            )
        ][:5],
    }

    # --------------------------------------------------
    # Write file
    # --------------------------------------------------
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"✅ summary.json written to {output_path.resolve()}")
    return output_path
