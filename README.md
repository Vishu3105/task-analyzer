# 🧠 Smart Task Analyzer #

## Overview

Smart Task Analyzer is a mini web application that intelligently scores and prioritizes tasks to help users decide what to work on first. Each task is evaluated based on urgency, importance, effort, and dependencies. The system supports multiple prioritization strategies and provides clear explanations for every score.

This project was built as part of the Singularium Technologies – Software Development Intern technical assessment.

---
# ✨ Features

- Add tasks using an admin-like form or JSON input
- Intelligent priority scoring with explanations
- Multiple sorting strategies:
  - Smart Balance
  - Deadline Driven
  - Fastest Wins
  - High Impact
- Visual priority indicators (High / Medium / Low)
- Responsive UI (desktop & mobile)
- Database-backed task suggestions (Top 3)
- Robust handling of missing/invalid data
- Unit tests for core scoring logic
---
## 🛠 Tech Stack

- #### Backend: Python 3.8+, Django 4.x 
- #### Frontend: HTML5, CSS3, JavaScript
- #### Database: SQLite (default Django DB)
- #### Testing: Django Test Framework
---
## 🚀 Setup Instructions

### 1. Clone the Repository
bash
```
git clone <github-repo-url>
cd task-analyzer
```
### 2. Create and activate virtual environment
```
python -m venv venv
venv\Scripts\Activate   # Windows
source venv/bin/activate  # macOS/Linux
```
### 3. Install dependencies
```
pip install -r requirements.txt
```
### 4. Run migrations
```
cd backend
python manage.py migrate
```
### 5. Start the server
```
python manage.py runserver
```
### 6. Open the app
```
App UI: http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/
```
---
## 🔗 API Endpoints

| Method | Endpoint                           | Description                  |
| ------ | ---------------------------------- | ---------------------------- |
| POST   | `/api/tasks/analyze/?strategy=...` | Analyze and prioritize tasks |
| GET    | `/api/tasks/suggest/?strategy=...` | Get top 3 task suggestions   |

---

## 🧮 Algorithm Explanation (Priority Scoring)

The core of the application is the `calculate_task_score` function.  
Each task is evaluated using the following components:

### 1. Urgency
- Based on the difference between today’s date and the task’s due date
- Overdue tasks receive a significant score boost
- Tasks due soon score higher than those with distant deadlines

### 2. Importance
- User-defined value between **1–10**
- Importance is multiplied to give it meaningful weight in final scoring

### 3. Effort (Quick Wins)
- Low-effort tasks are rewarded to encourage fast progress
- Very small tasks receive bonus points
- Large tasks receive a slight penalty to reduce blocking behavior


### 4. Strategy-Based Weighting
Different strategies rebalance these components:

| Strategy        | Description                                           |
| --------------- | ----------------------------------------------------- |
| Smart Balance   | Even weighting across urgency, importance, and effort |
| Deadline Driven | Urgency is heavily prioritized                        |
| Fastest Wins    | Low effort is heavily prioritized                     |
| High Impact     | Importance is heavily prioritized                     |

Each task’s final score is a weighted combination of these components, and the task list is sorted by score in descending order.  
Each score also includes a human-readable explanation describing why the task received that priority.

A key design goal of the scoring algorithm was explainability. Instead of returning only a
numerical priority value, the system also generates a human-readable explanation for
each task. This ensures users can understand how urgency, importance, effort, and
selected strategy contributed to the final score. The algorithm uses additive scoring
rather than hard thresholds so that tasks can be compared smoothly across multiple
dimensions, resulting in more realistic and flexible prioritization behavior.

---
## 🤔 Design Decisions

- Used an additive/scored-based priority calculation instead of rule-based ranking to
  allow smoother comparison between tasks.

- Implemented multiple prioritization strategies by re-weighting a single core scoring
  function, avoiding code duplication and simplifying future extensions.

- Chose to handle missing or invalid task data using safe default values to maximize
  robustness and prevent runtime failures.

- Treated effort as a “quick win” indicator rather than only a penalty, encouraging
  completion of smaller tasks when appropriate.

- Represented task dependencies using task ID lists instead of a visual dependency
  graph to keep the implementation simple and focused within the assignment scope.

- Built the frontend using plain HTML, CSS, and JavaScript to reduce complexity and
  maintain alignment with the project requirements.

---
## ⚠️ Handling Edge Cases

- Missing or invalid due dates → Treated as low urgency  
- Missing importance → Defaults to a neutral value of **5**  
- Missing estimated hours → Assumed to be a small task  
- Invalid JSON input → Rejected with clear error messages  
- Strategy not provided → Defaults to **Smart Balance**

This design prevents crashes and ensures meaningful output even with imperfect data.

---
## 🚦 Visual Priority Indicators

Tasks are visually categorized:

| Priority | Color    |
| -------- | -------- |
| High     | 🔴 Red   |
| Medium   | 🟠 Amber |
| Low      | 🟢 Green |

This allows users to understand urgency at a glance.

---
## 🧪 Unit Tests

Three unit tests validate the core scoring logic:

 - Overdue tasks rank higher than future tasks.
 - Fastest Wins strategy favors low-effort tasks.
 - Missing fields are handled gracefully without errors.

Run tests using:
```
python manage.py test tasks
```

---
## ⏱️Time Breakdown

| Task                         | Time       |
| ---------------------------- | ---------- |
| Project setup                | 30 minutes |
| Scoring algorithm design     | 90 minutes |
| Backend APIs                 | 90 minutes |
| Frontend UI & responsiveness | 120 minutes|
| Testing & debugging          | 30 minutes |
| Documentation                | 60 minutes |

---
## 🏆 Bonus Challenges Attempted

- **Unit Tests:**  
  Wrote unit tests for the task scoring algorithm to validate critical behaviors such as
  overdue task prioritization, strategy-specific weighting (e.g., Fastest Wins), and
  graceful handling of missing task data. These tests help ensure correctness and
  maintainability of the core logic.

The remaining optional challenges (dependency graph visualization, date intelligence,
Eisenhower matrix view, and learning system) were not implemented due to time
constraints and scope prioritization.

---
## 📈 Future Improvements

- Checkbox-based dependency selection (instead of manual IDs)
- Circular dependency detection and visualization
- Date Intelligence: Consider weekends/holidays when calculating urgency 
- Eisenhower Matrix View: Display tasks on a 2D grid (Urgent vs Important)
- User-configurable strategy weights
- Persistent frontend task storage
- Authentication & multi-user support

---
## ✅ Conclusion

This project demonstrates clean backend design, thoughtful algorithmic decision-making, frontend usability, and robust error handling. The focus was on clarity, correctness, and explainability rather than over-engineering.
