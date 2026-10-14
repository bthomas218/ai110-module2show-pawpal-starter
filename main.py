"""Command-line demonstration of the PawPal+ scheduler."""

from datetime import time

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner("owner-1", "Jordan", "jordan@example.com")

    mochi = Pet("pet-1", "Mochi", "dog", 3)
    luna = Pet("pet-2", "Luna", "cat", 5)
    owner.add_pet(mochi)
    owner.add_pet(luna)

    # Add tasks out of chronological order to demonstrate sorting.
    mochi.add_task(Task("task-1", "Evening play", time(18, 0), "daily"))
    luna.add_task(Task("task-2", "Breakfast", time(8, 0), "daily"))
    mochi.add_task(Task("task-3", "Morning walk", time(8, 0), "daily"))

    scheduler = Scheduler()

    print("Today's Schedule")
    print(scheduler.render_schedule(owner))

    print("\nConflict Check")
    conflict_warnings = scheduler.detect_conflicts(owner)
    if conflict_warnings:
        for warning in conflict_warnings:
            print(warning)
    else:
        print("No scheduling conflicts detected.")

    print("\nMochi's Tasks (filtered by pet)")
    for task in scheduler.sort_tasks(scheduler.filter_tasks(owner, pet_name="Mochi")):
        print(f"{task.time.strftime('%H:%M')} - {task.description}")

    scheduler.complete_task(owner, "task-1")
    print("\nIncomplete Tasks (filtered by completion status)")
    incomplete_tasks = scheduler.filter_tasks(owner, completion_status=False)
    for task in scheduler.sort_tasks(incomplete_tasks):
        print(f"{task.time.strftime('%H:%M')} - {task.description}")


if __name__ == "__main__":
    main()
