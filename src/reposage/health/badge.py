def health_badge(score: int):
    if score >= 85:
        return {
            "emoji": "🟢",
            "label": "Excellent",
            "color": "green"
        }
    elif score >= 70:
        return {
            "emoji": "🟡",
            "label": "Good",
            "color": "yellow"
        }
    elif score >= 50:
        return {
            "emoji": "🟠",
            "label": "Fair",
            "color": "orange"
        }
    else:
        return {
            "emoji": "🔴",
            "label": "Poor",
            "color": "red"
        }
