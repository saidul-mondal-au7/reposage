from typing import List
from pathlib import Path

# ==========================================================
# Severity ranking for sorting issues
# ==========================================================
SEVERITY_ORDER = {
    "High": 3,
    "Medium": 2,
    "Low": 1,
}


# ==========================================================
# Repo Health Score Calculation
# ==========================================================
def calculate_repo_score(security, performance) -> int:
    """
    Calculate repository health score (0–100) based on
    severity-weighted security and performance issues.
    """
    score = 100

    for issue in security.issues:
        score -= {"High": 10, "Medium": 6, "Low": 3}.get(issue.severity, 0)

    for issue in performance.issues:
        score -= {"High": 8, "Medium": 5, "Low": 2}.get(issue.severity, 0)

    return max(score, 0)


# ==========================================================
# Quick Wins Extraction
# ==========================================================
def extract_top_quick_wins(roadmap, limit: int = 5):
    """
    Extract top quick wins from P0 / P1 roadmap items.
    """
    candidates = [
        item
        for item in roadmap.immediate_fixes + roadmap.short_term
        if item.priority in ("P0", "P1")
    ]

    candidates.sort(key=lambda x: 0 if x.priority == "P0" else 1)
    return candidates[:limit]


# ==========================================================
# Markdown Report Generator
# ==========================================================
def generate_report_md(
    scan,
    architecture,
    security,
    performance,
    roadmap,
    output_path: str = "outputs/report.md",
):
    """
    Generate a human-readable Markdown report from agent outputs.
    """

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
    lines.append(f"- **Repository Path**: `{scan.repo_path}`")
    lines.append(f"- **Total Files Scanned**: {scan.total_files_scanned}")
    lines.append(f"- **Detected Languages**: {', '.join(scan.detected_languages)}\n")

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

    for issue in security.issues:
        combined_issues.append({
            "category": "Security",
            "issue": issue.issue,
            "severity": issue.severity,
            "file": ", ".join(issue.affected_files) if issue.affected_files else "N/A",
            "fix": issue.recommended_fix,
        })

    for issue in performance.issues:
        combined_issues.append({
            "category": "Performance",
            "issue": issue.issue,
            "severity": issue.severity,
            "file": issue.affected_file or "N/A",
            "fix": issue.recommended_fix,
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
                f"{idx}. **[{item.priority}] {item.task}**\n"
                f"   - Impact: {item.impact}\n"
                f"   - Effort: {item.effort}\n"
                f"   - Risk: {item.risk}\n"
            )

    # ==========================================================
    # Architecture Summary
    # ==========================================================
    lines.append("\n## Architecture Summary\n")
    lines.append(f"- **Architecture Type**: {architecture.architecture_type}")
    lines.append(f"- **Key Modules**: {', '.join(architecture.key_modules)}")
    lines.append(
        f"- **Detected Design Patterns**: "
        f"{', '.join(architecture.detected_design_patterns)}\n"
    )
    lines.append("### Runtime Flow\n")
    lines.append(f"{architecture.runtime_flow_summary}\n")

    # ==========================================================
    # Security Risks
    # ==========================================================
    lines.append("## Security Risks\n")

    if not security.issues:
        lines.append("- No significant security risks detected.\n")
    else:
        for issue in security.issues:
            lines.append(
                f"- **{issue.issue}** (Severity: {issue.severity})\n"
                f"  - Affected Files: {issue.affected_files or 'N/A'}\n"
                f"  - Recommended Fix: {issue.recommended_fix}\n"
            )

    # ==========================================================
    # Performance & Scalability Risks
    # ==========================================================
    lines.append("## Performance & Scalability Risks\n")

    if not performance.issues:
        lines.append("- No significant performance risks detected.\n")
    else:
        for issue in performance.issues:
            lines.append(
                f"- **{issue.issue}** (Severity: {issue.severity})\n"
                f"  - File: {issue.affected_file or 'N/A'}\n"
                f"  - Likely Symptoms: {issue.likely_symptoms or 'N/A'}\n"
                f"  - Recommended Fix: {issue.recommended_fix}\n"
            )

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
                f"- **[{item.priority}] {item.task}**\n"
                f"  - Impact: {item.impact}\n"
                f"  - Effort: {item.effort}\n"
                f"  - Risk: {item.risk}\n"
                f"  - Justification: {item.justification}\n"
            )

    render_phase("Immediate Fixes (1–2 days)", roadmap.immediate_fixes)
    render_phase("Short Term (1–2 weeks)", roadmap.short_term)
    render_phase("Medium Term (1–2 months)", roadmap.medium_term)

    # ==========================================================
    # Write Report
    # ==========================================================
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ report.md written to {output_path.resolve()}")

    return output_path
