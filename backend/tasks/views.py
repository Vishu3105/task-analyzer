import json
from datetime import date

from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from .scoring import calculate_task_score
from .models import Task


@csrf_exempt
def analyze_tasks(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    try:
        tasks = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not isinstance(tasks, list):
        return JsonResponse({"error": "Expected a list of tasks"}, status=400)

    # Read strategy from query: ?strategy=fastest / deadline / impact / smart
    strategy = request.GET.get("strategy", "smart")

    result = []

    for task in tasks:
        if not isinstance(task, dict):
            continue

        # NOW we actually USE strategy here
        score_info = calculate_task_score(task, strategy=strategy)
        enriched_task = task.copy()
        enriched_task["score"] = score_info["score"]
        enriched_task["explanation"] = score_info["explanation"]

        result.append(enriched_task)

    result.sort(key=lambda t: t["score"], reverse=True)

    return JsonResponse(result, safe=False)

def suggest_tasks(request):
    """
    GET /api/tasks/suggest/
    Returns top 3 tasks from DB based on score.
    """
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    # Read strategy from query: ?strategy=fastest / deadline / impact / smart
    strategy = request.GET.get("strategy", "smart")

    tasks_qs = Task.objects.all()
    scored = []

    for t in tasks_qs:
        task_data = {
            "title": t.title,
            "due_date": t.due_date.isoformat(),
            "estimated_hours": t.estimated_hours,
            "importance": t.importance,
            "dependencies": t.dependencies,
        }

        # pass strategy here
        score_info = calculate_task_score(task_data, strategy=strategy)
        enriched = task_data.copy()
        enriched["id"] = t.id
        enriched["score"] = score_info["score"]
        enriched["explanation"] = score_info["explanation"]

        scored.append(enriched)

    scored.sort(key=lambda item: item["score"], reverse=True)
    top3 = scored[:3]

    return JsonResponse(top3, safe=False)
