# reposage/health/badge.py

def health_badge(score: int) -> str:
    if score >= 85:
        color = "brightgreen"
    elif score >= 70:
        color = "yellow"
    elif score >= 50:
        color = "orange"
    else:
        color = "red"

    return f"https://img.shields.io/badge/Repo%20Health-{score}%25-{color}"
