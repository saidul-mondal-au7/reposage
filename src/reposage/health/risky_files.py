from collections import defaultdict

SEVERITY_WEIGHT = {
    "High": 10,
    "Medium": 5,
    "Low": 2
}

def extract_top_risky_files(security: dict, performance: dict, limit: int = 5):
    """
    Returns top risky files sorted by cumulative risk score.
    """

    file_risk = defaultdict(lambda: {
        "score": 0,
        "security_issues": 0,
        "performance_issues": 0
    })

    # ---------------- Security issues ----------------
    for issue in security.get("issues", []):
        severity = issue.get("severity")
        weight = SEVERITY_WEIGHT.get(severity, 0)

        for f in issue.get("affected_files") or []:
            file_risk[f]["score"] += weight
            file_risk[f]["security_issues"] += 1

    # ---------------- Performance issues ----------------
    for issue in performance.get("issues", []):
        severity = issue.get("severity")
        weight = SEVERITY_WEIGHT.get(severity, 0)

        f = issue.get("affected_file")
        if f:
            file_risk[f]["score"] += weight
            file_risk[f]["performance_issues"] += 1

    # ---------------- Sort & return ----------------
    ranked = sorted(
        file_risk.items(),
        key=lambda x: x[1]["score"],
        reverse=True
    )

    return [
        {
            "file": file,
            "risk_score": data["score"],
            "security_issues": data["security_issues"],
            "performance_issues": data["performance_issues"],
        }
        for file, data in ranked[:limit]
    ]
