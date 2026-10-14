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


def test_detect_conflicts_returns_warning_for_tasks_at_same_time() -> None:
    owner = Owner("owner-1", "Jordan", "jordan@example.com")
    mochi = Pet("pet-1", "Mochi", "dog", 3)
    luna = Pet("pet-2", "Luna", "cat", 5)
    mochi.add_task(Task("task-1", "Morning walk", time(8, 0)))
    luna.add_task(Task("task-2", "Breakfast", time(8, 0)))
    owner.add_pet(mochi)
    owner.add_pet(luna)

    warnings = Scheduler().detect_conflicts(owner)

    assert len(warnings) == 1
    assert "Warning:" in warnings[0]
    assert "08:00" in warnings[0]
    assert "Mochi" in warnings[0]
    assert "Luna" in warnings[0]
