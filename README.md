# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Implementation Summary

The core implementation uses dataclasses for `Task`, `Pet`, and `Owner`.
Each pet owns its task list, and an owner manages multiple pets and exposes
`get_all_tasks()` to return tasks across the entire household. `Scheduler` is
a separate service that reads tasks through the owner, removes completed
tasks, orders the remaining tasks by time, and can render or complete tasks.
The command-line demo in `main.py` connects these classes, while pytest tests
cover task completion and adding tasks to pets.

## Getting started

### Setup

```bash
uv sync
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Run the command-line demonstration with:

```bash
uv run python main.py
```

Example terminal output:

```
Today's Schedule
Schedule for Jordan
08:00 - Morning walk (daily)
08:30 - Breakfast (daily)
18:00 - Evening play (daily)
```

## 🧪 Testing PawPal+

Run the full test suite with:

```bash
uv run pytest
```

The tests cover task completion, adding tasks to pets, chronological sorting,
untimed and same-time tasks, incomplete-task filtering, daily/weekly/monthly
recurrence, recurring-task ID collisions, unknown task IDs, conflict detection,
empty schedules, and case-insensitive pet filtering.

Successful test output:

```
============================= test session starts ==============================
platform linux -- Python 3.13.11, pytest-9.1.1, pluggy-1.6.1
rootdir: /home/brady/workspace/github.com/bthomas218/ai110-module2show-pawpal-starter
configfile: pyproject.toml
plugins: anyio-4.15.1
collected 17 items

tests/test_pawpal.py .................                                   [100%]

============================== 17 passed in 0.02s ==============================
```

Confidence Level: ★★★★☆ (4/5)

The full automated suite passes, covering the scheduler's core behaviors and
important edge cases. This confidence level leaves room for broader UI and
integration testing beyond the current unit-test coverage.

## 📐 Smarter Scheduling

The scheduler combines filtering, sorting, conflict detection, and recurring
task creation to build a practical household care schedule.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sorting behavior | `Scheduler.sort_tasks()` and `Scheduler.build_schedule()` | Sorts tasks by scheduled time. Tasks without a time appear after timed tasks. `build_schedule()` combines this with incomplete-task filtering. |
| Filtering by completion status | `Scheduler.filter_tasks(owner, completion_status=...)` | Filters tasks to completed or incomplete tasks. The normal schedule includes only incomplete tasks. |
| Filtering by pet | `Scheduler.filter_tasks(owner, pet_name=...)` | Returns tasks for a selected pet, using case-insensitive pet-name matching. Completion and pet filters can be combined. |
| Conflict detection | `Scheduler.detect_conflicts()` | Checks incomplete tasks for overlapping time intervals, using each task's `time` and `duration_minutes`. Returns warning messages instead of crashing or automatically changing the schedule. |
| Recurring tasks | `Scheduler.complete_task()` and `Scheduler._next_due_date()` | Completing a `daily`, `weekly`, or `monthly` task creates a new incomplete instance for the same pet. The next due date uses `timedelta(days=1)`, `timedelta(days=7)`, or `timedelta(days=30)`. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
