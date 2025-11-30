from django.test import TestCase
from .scoring import calculate_task_score


class ScoringTests(TestCase):
    def test_overdue_task_has_higher_score_than_future_task(self):
        """
        Overdue tasks should get a much higher score than future tasks
        with similar importance/effort.
        """
        overdue_task = {
            "title": "Overdue task",
            "due_date": "2020-01-01",
            "estimated_hours": 3,
            "importance": 5,
            "dependencies": [],
        }

        future_task = {
            "title": "Future task",
            "due_date": "2099-01-01",
            "estimated_hours": 3,
            "importance": 5,
            "dependencies": [],
        }

        overdue_score = calculate_task_score(overdue_task)["score"]
        future_score = calculate_task_score(future_task)["score"]

        self.assertGreater(
            overdue_score,
            future_score,
            msg="Overdue task should have a higher score than a future task.",
        )

    def test_fastest_wins_favors_low_effort_tasks(self):
        """
        Under 'fastest' strategy, a low-effort task should get
        a higher score than a high-effort task with same due date/importance.
        """
        low_effort = {
            "title": "Tiny task",
            "due_date": "2099-01-01",
            "estimated_hours": 1,
            "importance": 5,
            "dependencies": [],
        }

        high_effort = {
            "title": "Big task",
            "due_date": "2099-01-01",
            "estimated_hours": 10,
            "importance": 5,
            "dependencies": [],
        }

        low_score = calculate_task_score(low_effort, strategy="fastest")["score"]
        high_score = calculate_task_score(high_effort, strategy="fastest")["score"]

        self.assertGreater(
            low_score,
            high_score,
            msg="Under 'fastest' strategy, low-effort task should rank higher.",
        )

    def test_missing_fields_are_handled_gracefully(self):
        """
        If importance or estimated_hours are missing, the function should not crash
        and should still return a score.
        """
        incomplete_task = {
            "title": "Incomplete task",
            "due_date": "2099-01-01",
            # 'importance' and 'estimated_hours' intentionally omitted
            "dependencies": [],
        }

        result = calculate_task_score(incomplete_task)
        self.assertIn("score", result)
        self.assertIsInstance(result["score"], (int, float))
