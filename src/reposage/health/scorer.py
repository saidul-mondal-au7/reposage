# reposage/health/scorer.py

def calculate_health_score(security: dict, performance: dict) -> int:
    score = 100

    for issue in security.get("issues", []):
        score -= {
            "High": 15,
            "Medium": 8,
            "Low": 3
        }.get(issue.get("severity"), 0)

    for issue in performance.get("issues", []):
        score -= {
            "High": 10,
            "Medium": 5,
            "Low": 2
        }.get(issue.get("severity"), 0)

    return max(score, 0)


def score_grade(score: int) -> str:
    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    if score >= 60:
        return "C"
    if score >= 40:
        return "D"
    return "F"
