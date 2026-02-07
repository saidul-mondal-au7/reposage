from typing import List
from pathlib import Path
import json
from pydantic import BaseModel

# from reposage.health.scorer import calculate_health_score
# from reposage.health.badge import health_badge



# ==========================================================
# Safe coercion (CrewAI 1.9.3 compatible)
# ==========================================================
def _force_dict(obj):
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


# ==========================================================
# Severity ranking
# ==========================================================
SEVERITY_ORDER = {
    "High": 3,
    "Medium": 2,
    "Low": 1,
}


# ==========================================================
# Repo Health Score
# ==========================================================
def calculate_repo_score(security: dict, performance: dict) -> int:
    score = 100

    for issue in security.get("issues", []):
        score -= {"High": 10, "Medium": 6, "Low": 3}.get(issue.get("severity"), 0)

    for issue in performance.get("issues", []):
        score -= {"High": 8, "Medium": 5, "Low": 2}.get(issue.get("severity"), 0)

    return max(score, 0)


# ==========================================================
# Quick Wins
# ==========================================================
def extract_top_quick_wins(roadmap: dict, limit: int = 5):
    candidates = []

    for item in roadmap.get("immediate_fixes", []) + roadmap.get("short_term", []):
        if item.get("priority") in ("P0", "P1"):
            candidates.append(item)

    candidates.sort(key=lambda x: 0 if x.get("priority") == "P0" else 1)
    return candidates[:limit]


# ==========================================================
# Markdown Report Generator
# ==========================================================
def generate_report_md(
    scan_output,
    architecture_output,
    security_output,
    performance_output,
    roadmap_output,
    output_path: str = "outputs/report.md",
):
    """
    Generate a human-readable Markdown report.
    Guaranteed not to drop CrewAI data.
    """

    # --------------------------------------------------
    # Normalize safely (NO DATA LOSS)
    # --------------------------------------------------
    scan = _force_dict(scan_output)
    architecture = _force_dict(architecture_output)
    security = _force_dict(security_output)
    performance = _force_dict(performance_output)
    roadmap = _force_dict(roadmap_output)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines: List[str] = []

    # ==========================================================
    # Title
    # ==========================================================
    lines.append("# Repository Analysis Report\n")

    # ==========================================================
    # Repository Overview
    # ==========================================================
    lines.append("## Repository Overview\n")
    lines.append(f"- **Repository Path**: `{scan.get('repo_path', 'unknown')}`")
    lines.append(f"- **Total Files Scanned**: {scan.get('total_files_scanned', 0)}")
    lines.append(
        f"- **Detected Languages**: {', '.join(scan.get('detected_languages', []))}\n"
    )

    # ==========================================================
    # Repository Health Score
    # ==========================================================
    repo_score = calculate_repo_score(security, performance)

    lines.append("## Repository Health Score\n")
    lines.append(f"**Overall Score: {repo_score} / 100**\n")

    if repo_score >= 85:
        lines.append("🟢 **Excellent** – Minimal risk, well-structured codebase.\n")
    elif repo_score >= 70:
        lines.append("🟡 **Good** – Some issues present, manageable with planned improvements.\n")
    elif repo_score >= 50:
        lines.append("🟠 **Fair** – Multiple risks detected; remediation recommended.\n")
    else:
        lines.append("🔴 **Poor** – High-risk codebase; immediate action required.\n")

    # ==========================================================
    # Top 10 Critical Issues
    # ==========================================================
    lines.append("## Top 10 Critical Issues\n")

    combined_issues = []

    for issue in security.get("issues", []):
        combined_issues.append({
            "category": "Security",
            "issue": issue.get("issue"),
            "severity": issue.get("severity"),
            # "file": ", ".join(issue.get("affected_files", [])) or "N/A",
            "file": ", ".join(issue.get("affected_files") or []) or "N/A",
            "fix": issue.get("recommended_fix"),
        })

    for issue in performance.get("issues", []):
        combined_issues.append({
            "category": "Performance",
            "issue": issue.get("issue"),
            "severity": issue.get("severity"),
            "file": issue.get("affected_file") or "N/A",
            "fix": issue.get("recommended_fix"),
        })

    combined_issues.sort(
        key=lambda x: SEVERITY_ORDER.get(x["severity"], 0),
        reverse=True,
    )

    lines.append(
        "| # | Category | Issue | Severity | File | Recommended Fix |\n"
        "|---|----------|-------|----------|------|-----------------|\n"
    )

    for idx, issue in enumerate(combined_issues[:10], start=1):
        lines.append(
            f"| {idx} | {issue['category']} | {issue['issue']} | "
            f"{issue['severity']} | {issue['file']} | {issue['fix']} |\n"
        )

    # ==========================================================
    # Top 5 Quick Wins
    # ==========================================================
    lines.append("\n## Top 5 Quick Wins\n")

    quick_wins = extract_top_quick_wins(roadmap)

    if not quick_wins:
        lines.append("No immediate quick wins identified.\n")
    else:
        for idx, item in enumerate(quick_wins, start=1):
            lines.append(
                f"{idx}. **[{item.get('priority')}] {item.get('task')}**\n"
                f"   - Impact: {item.get('impact')}\n"
                f"   - Effort: {item.get('effort')}\n"
                f"   - Risk: {item.get('risk')}\n"
            )

    # ==========================================================
    # Architecture Summary
    # ==========================================================
    lines.append("\n## Architecture Summary\n")
    lines.append(f"- **Architecture Type**: {architecture.get('architecture_type')}")
    lines.append(f"- **Key Modules**: {', '.join(architecture.get('key_modules', []))}")
    lines.append(
        f"- **Detected Design Patterns**: "
        f"{', '.join(architecture.get('detected_design_patterns', []))}\n"
    )
    lines.append("### Runtime Flow\n")
    lines.append(f"{architecture.get('runtime_flow_summary', '')}\n")

    # ==========================================================
    # Roadmap
    # ==========================================================
    lines.append("## Roadmap / Improvement Plan\n")

    def render_phase(title: str, items):
        lines.append(f"### {title}\n")
        if not items:
            lines.append("- No items identified.\n")
            return
        for item in items:
            lines.append(
                f"- **[{item.get('priority')}] {item.get('task')}**\n"
                f"  - Impact: {item.get('impact')}\n"
                f"  - Effort: {item.get('effort')}\n"
                f"  - Risk: {item.get('risk')}\n"
                f"  - Justification: {item.get('justification')}\n"
            )

    render_phase("Immediate Fixes (1–2 days)", roadmap.get("immediate_fixes", []))
    render_phase("Short Term (1–2 weeks)", roadmap.get("short_term", []))
    render_phase("Medium Term (1–2 months)", roadmap.get("medium_term", []))

    # ==========================================================
    # Write file
    # ==========================================================
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ report.md written to {output_path.resolve()}")

    return output_path
