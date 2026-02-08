def calculate_health_score(
    scan: dict,
    architecture: dict,
    security: dict,
    performance: dict,
):
    score = 100
    breakdown = {}

    # -------------------------------
    # SECURITY (40)
    # -------------------------------
    sec_penalty = 0
    for issue in security.get("issues", []):
        if issue.get("severity") == "High":
            sec_penalty += 10
        elif issue.get("severity") == "Medium":
            sec_penalty += 6
        elif issue.get("severity") == "Low":
            sec_penalty += 3

    sec_penalty = min(sec_penalty, 40)
    breakdown["security"] = 40 - sec_penalty
    score -= sec_penalty

    # -------------------------------
    # PERFORMANCE (30)
    # -------------------------------
    perf_penalty = 0
    for issue in performance.get("issues", []):
        if issue.get("severity") == "High":
            perf_penalty += 8
        elif issue.get("severity") == "Medium":
            perf_penalty += 5
        elif issue.get("severity") == "Low":
            perf_penalty += 2

    perf_penalty = min(perf_penalty, 30)
    breakdown["performance"] = 30 - perf_penalty
    score -= perf_penalty

    # -------------------------------
    # ARCHITECTURE (20)
    # -------------------------------
    arch_score = 20
    arch_type = architecture.get("architecture_type")

    if arch_type == "monolith":
        arch_score -= 6
    elif arch_type == "modular monolith":
        arch_score -= 2

    if not architecture.get("detected_design_patterns"):
        arch_score -= 4

    breakdown["architecture"] = max(arch_score, 0)
    score -= (20 - breakdown["architecture"])

    # -------------------------------
    # REPO HYGIENE (10)
    # -------------------------------
    hygiene_score = 10

    if not scan.get("entry_points"):
        hygiene_score -= 3
    if not scan.get("dependency_files"):
        hygiene_score -= 3
    if scan.get("total_files_scanned", 0) < 5:
        hygiene_score -= 4

    breakdown["hygiene"] = max(hygiene_score, 0)
    score -= (10 - breakdown["hygiene"])

    return {
        "score": max(score, 0),
        "breakdown": breakdown,
        "grade": (
            "A" if score >= 85 else
            "B" if score >= 70 else
            "C" if score >= 50 else
            "D"
        )
    }
