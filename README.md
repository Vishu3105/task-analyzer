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
- #### Frontend: HTML5, CSS3, Vanilla JavaScript
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
| Project setup                | 40 minutes |
| Scoring algorithm design     | 90 minutes |
| Backend APIs                 | 60 minutes |
| Frontend UI & responsiveness | 90 minutes |
| Testing & debugging          | 30 minutes |
| Documentation                | 60 minutes |

---
## 📈 Future Improvements

- Checkbox-based dependency selection (instead of manual IDs)
- Circular dependency detection and visualization
- User-configurable strategy weights
- Persistent frontend task storage
- Authentication & multi-user support

---
## ✅ Conclusion

This project demonstrates clean backend design, thoughtful algorithmic decision-making, frontend usability, and robust error handling. The focus was on clarity, correctness, and explainability rather than over-engineering.
