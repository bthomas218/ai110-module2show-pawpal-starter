from datetime import date, time, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion_changes_status() -> None:
    task = Task("task-1", "Morning walk")

    task.mark_complete()

    assert task.is_complete() is True


def test_adding_task_increases_pet_task_count() -> None:
    pet = Pet("pet-1", "Mochi", "dog", 3)
    task = Task("task-1", "Morning walk")

    original_count = len(pet.tasks)
    pet.add_task(task)

    assert len(pet.tasks) == original_count + 1


def test_completing_daily_task_creates_next_instance() -> None:
    owner = Owner("owner-1", "Jordan", "jordan@example.com")
    pet = Pet("pet-1", "Mochi", "dog", 3)
    due_date = date(2026, 10, 14)
    pet.add_task(Task("task-1", "Morning walk", frequency="daily", due_date=due_date))
    owner.add_pet(pet)

    assert Scheduler().complete_task(owner, "task-1") is True

    assert pet.tasks[0].is_complete() is True
    assert len(pet.tasks) == 2
    assert pet.tasks[1].id == "task-1-next-1"
    assert pet.tasks[1].is_complete() is False
    assert pet.tasks[1].frequency == "daily"
    assert pet.tasks[1].due_date == due_date + timedelta(days=1)


def test_sort_tasks_returns_tasks_in_chronological_order() -> None:
    scheduler = Scheduler()
    evening = Task("task-evening", "Evening walk", time(18, 0))
    morning = Task("task-morning", "Morning walk", time(8, 0))
    afternoon = Task("task-afternoon", "Afternoon play", time(14, 0))

    sorted_tasks = scheduler.sort_tasks([evening, morning, afternoon])

    assert [task.id for task in sorted_tasks] == [
        "task-morning",
        "task-afternoon",
        "task-evening",
    ]


def test_sort_tasks_places_untimed_tasks_last_and_preserves_same_time_order() -> None:
    scheduler = Scheduler()
    first_at_eight = Task("task-first", "Breakfast", time(8, 0))
    second_at_eight = Task("task-second", "Medication", time(8, 0))
    untimed = Task("task-untimed", "Flexible play")

    sorted_tasks = scheduler.sort_tasks([untimed, second_at_eight, first_at_eight])

    assert [task.id for task in sorted_tasks] == [
        "task-second",
        "task-first",
        "task-untimed",
    ]


def test_build_schedule_excludes_completed_tasks_and_sorts_incomplete_tasks() -> None:
    owner = Owner("owner-1", "Jordan", "jordan@example.com")
    pet = Pet("pet-1", "Mochi", "dog", 3)
    completed = Task("task-completed", "Breakfast", time(7, 0))
    completed.mark_complete()
    pet.add_task(completed)
    pet.add_task(Task("task-late", "Evening walk", time(18, 0)))
    pet.add_task(Task("task-early", "Morning walk", time(8, 0)))
    owner.add_pet(pet)

    schedule = Scheduler().build_schedule(owner)

    assert [task.id for task in schedule] == ["task-early", "task-late"]


def test_completing_weekly_and_monthly_tasks_calculates_next_due_date() -> None:
    owner = Owner("owner-1", "Jordan", "jordan@example.com")
    pet = Pet("pet-1", "Mochi", "dog", 3)
    due_date = date(2026, 10, 14)
    pet.add_task(Task("task-weekly", "Medication", frequency="weekly", due_date=due_date))
    pet.add_task(Task("task-monthly", "Grooming", frequency="monthly", due_date=due_date))
    owner.add_pet(pet)

    scheduler = Scheduler()
    assert scheduler.complete_task(owner, "task-weekly") is True
    assert scheduler.complete_task(owner, "task-monthly") is True

    assert pet.tasks[2].due_date == due_date + timedelta(days=7)
    assert pet.tasks[3].due_date == due_date + timedelta(days=30)


def test_completing_one_time_task_does_not_create_next_instance() -> None:
    owner = Owner("owner-1", "Jordan", "jordan@example.com")
    pet = Pet("pet-1", "Mochi", "dog", 3)
    pet.add_task(Task("task-1", "Nail trim"))
    owner.add_pet(pet)

    assert Scheduler().complete_task(owner, "task-1") is True
    assert len(pet.tasks) == 1


def test_completing_daily_task_preserves_time_and_schedules_following_day() -> None:
    owner = Owner("owner-1", "Jordan", "jordan@example.com")
    pet = Pet("pet-1", "Mochi", "dog", 3)
    due_date = date(2026, 10, 17)
    pet.add_task(
        Task(
            "task-medication",
            "Medication",
            time(9, 30),
            frequency="DAILY",
            due_date=due_date,
        )
    )
    owner.add_pet(pet)

    assert Scheduler().complete_task(owner, "task-medication") is True

    next_task = pet.tasks[1]
    assert next_task.id == "task-medication-next-1"
    assert next_task.description == "Medication"
    assert next_task.time == time(9, 30)
    assert next_task.frequency == "DAILY"
    assert next_task.due_date == date(2026, 10, 18)
    assert next_task.is_complete() is False


def test_completing_recurring_task_avoids_existing_next_task_id() -> None:
    owner = Owner("owner-1", "Jordan", "jordan@example.com")
    pet = Pet("pet-1", "Mochi", "dog", 3)
    due_date = date(2026, 10, 17)
    pet.add_task(Task("task-1", "Walk", frequency="daily", due_date=due_date))
    pet.add_task(Task("task-1-next-1", "Existing task"))
    owner.add_pet(pet)

    assert Scheduler().complete_task(owner, "task-1") is True

    assert pet.tasks[2].id == "task-1-next-2"


def test_unknown_task_id_does_not_change_owner_tasks() -> None:
    owner = Owner("owner-1", "Jordan", "jordan@example.com")
    pet = Pet("pet-1", "Mochi", "dog", 3)
    pet.add_task(Task("task-1", "Walk"))
    owner.add_pet(pet)

    assert Scheduler().complete_task(owner, "missing-task") is False
    assert pet.tasks[0].is_complete() is False
    assert len(pet.tasks) == 1


def test_detect_conflicts_returns_warning_for_tasks_at_same_time() -> None:
    owner = Owner("owner-1", "Jordan", "jordan@example.com")
    mochi = Pet("pet-1", "Mochi", "dog", 3)
    luna = Pet("pet-2", "Luna", "cat", 5)
    mochi.add_task(Task("task-1", "Morning walk", time(8, 0), duration_minutes=30))
    luna.add_task(Task("task-2", "Breakfast", time(8, 15), duration_minutes=15))
    owner.add_pet(mochi)
    owner.add_pet(luna)

    warnings = Scheduler().detect_conflicts(owner)

    assert len(warnings) == 1
    assert "Warning:" in warnings[0]
    assert "08:00-08:30" in warnings[0]
    assert "08:15-08:30" in warnings[0]
    assert "Mochi" in warnings[0]
    assert "Luna" in warnings[0]


def test_detect_conflicts_flags_duplicate_times() -> None:
    owner = Owner("owner-1", "Jordan", "jordan@example.com")
    mochi = Pet("pet-1", "Mochi", "dog", 3)
    luna = Pet("pet-2", "Luna", "cat", 5)
    same_time = time(8, 0)
    mochi.add_task(Task("task-1", "Morning walk", same_time, duration_minutes=30))
    luna.add_task(Task("task-2", "Breakfast", same_time, duration_minutes=15))
    owner.add_pet(mochi)
    owner.add_pet(luna)

    warnings = Scheduler().detect_conflicts(owner)

    assert len(warnings) == 1
    assert "Morning walk" in warnings[0]
    assert "Breakfast" in warnings[0]
    assert "08:00-08:30" in warnings[0]
    assert "08:00-08:15" in warnings[0]


def test_detect_conflicts_ignores_completed_tasks_and_different_dates() -> None:
    owner = Owner("owner-1", "Jordan", "jordan@example.com")
    pet = Pet("pet-1", "Mochi", "dog", 3)
    first = Task(
        "task-first", "First walk", time(8, 0), due_date=date(2026, 10, 17), duration_minutes=30
    )
    completed = Task(
        "task-completed", "Completed walk", time(8, 0), due_date=date(2026, 10, 17), duration_minutes=30
    )
    completed.mark_complete()
    different_date = Task(
        "task-other-date", "Next day walk", time(8, 0), due_date=date(2026, 10, 18), duration_minutes=30
    )
    pet.tasks.extend([first, completed, different_date])
    owner.add_pet(pet)

    assert Scheduler().detect_conflicts(owner) == []


def test_detect_conflicts_allows_adjacent_tasks() -> None:
    owner = Owner("owner-1", "Jordan", "jordan@example.com")
    pet = Pet("pet-1", "Mochi", "dog", 3)
    due_date = date(2026, 10, 17)
    pet.add_task(Task("task-first", "Walk", time(8, 0), due_date=due_date, duration_minutes=30))
    pet.add_task(Task("task-next", "Breakfast", time(8, 30), due_date=due_date, duration_minutes=15))
    owner.add_pet(pet)

    assert Scheduler().detect_conflicts(owner) == []


def test_empty_owner_builds_and_renders_empty_schedule() -> None:
    owner = Owner("owner-1", "Jordan", "jordan@example.com")
    scheduler = Scheduler()

    assert scheduler.build_schedule(owner) == []
    assert scheduler.render_schedule(owner) == "Schedule for Jordan"


def test_filter_tasks_matches_pet_name_case_insensitively() -> None:
    owner = Owner("owner-1", "Jordan", "jordan@example.com")
    mochi = Pet("pet-1", "Mochi", "dog", 3)
    luna = Pet("pet-2", "Luna", "cat", 5)
    mochi.add_task(Task("task-mochi", "Walk"))
    luna.add_task(Task("task-luna", "Feed"))
    owner.add_pet(mochi)
    owner.add_pet(luna)

    matching_tasks = Scheduler().filter_tasks(owner, pet_name="mOcHi")

    assert [task.id for task in matching_tasks] == ["task-mochi"]
