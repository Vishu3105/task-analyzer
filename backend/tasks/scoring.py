from datetime import date, datetime


def parse_due_date(raw):
    """
    Accepts either date object or 'YYYY-MM-DD' string.
    Returns date or None if invalid.
    """
    if raw is None:
        return None
    if isinstance(raw, date):
        return raw
    try:
        return datetime.strptime(str(raw), "%Y-%m-%d").date()
    except ValueError:
        return None


def calculate_task_score(task, strategy="smart"):
    """
    Calculates a priority score.
    Higher score = higher priority.

    strategy:
      - "smart"    -> balanced
      - "deadline" -> urgency heavy
      - "fastest"  -> low effort heavy
      - "impact"   -> importance heavy
    """
    today = date.today()
    due_date = parse_due_date(task.get("due_date"))

    # Safe defaults
    importance = task.get("importance", 5)
    estimated_hours = task.get("estimated_hours", 1)

    explanation = []

    # Urgency component
    urgency_points = 0
    if due_date:
        days_left = (due_date - today).days
        if days_left < 0:
            urgency_points = 100
            explanation.append("Task is overdue.")
        elif days_left <= 1:
            urgency_points = 60
            explanation.append("Task due today/tomorrow.")
        elif days_left <= 3:
            urgency_points = 40
            explanation.append("Task due within 3 days.")
        elif days_left <= 7:
            urgency_points = 20
            explanation.append("Task due within a week.")
        else:
            urgency_points = 5
            explanation.append("Task due later than a week.")
    else:
        explanation.append("No valid due date; treated as low urgency.")

    # Importance component
    importance_points = importance * 5
    explanation.append(f"Importance contributes {importance_points} points.")

    # Effort component (quick wins)
    effort_points = 0
    if estimated_hours <= 1:
        effort_points = 20
        explanation.append("Very small task (≤1h); strong quick-win bonus.")
    elif estimated_hours <= 3:
        effort_points = 10
        explanation.append("Small task (≤3h); quick-win bonus.")
    elif estimated_hours <= 6:
        effort_points = 0
        explanation.append("Medium task; neutral effort impact.")
    else:
        effort_points = -10
        explanation.append("Large task; slight penalty for high effort.")

    # Combine based on strategy
    strategy = (strategy or "smart").lower()

    if strategy == "deadline":
        # Deadline Driven: urgency dominates
        score = urgency_points * 2 + importance_points * 1 + effort_points * 0.5
        explanation.append("Strategy: Deadline Driven (urgency heavily weighted).")
    elif strategy == "fastest":
        # Fastest Wins: low effort dominates
        score = effort_points * 2 + importance_points * 1 + urgency_points * 0.5
        explanation.append("Strategy: Fastest Wins (low effort heavily weighted).")
    elif strategy == "impact":
        # High Impact: importance dominates
        score = importance_points * 2 + urgency_points * 1 + effort_points * 0.5
        explanation.append("Strategy: High Impact (importance heavily weighted).")
    else:
        # Smart Balance: fairly even
        score = (
            urgency_points * 1.3 +
            importance_points * 1.3 +
            effort_points * 1.0
        )
        explanation.append("Strategy: Smart Balance (balanced across factors).")

    return {
        "score": round(score, 2),
        "explanation": " ".join(explanation),
    }
