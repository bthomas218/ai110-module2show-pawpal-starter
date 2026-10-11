"""Command-line demonstration of the PawPal+ scheduler."""

from datetime import time

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner("owner-1", "Jordan", "jordan@example.com")

    mochi = Pet("pet-1", "Mochi", "dog", 3)
    luna = Pet("pet-2", "Luna", "cat", 5)
    owner.add_pet(mochi)
    owner.add_pet(luna)

    mochi.add_task(Task("task-1", "Morning walk", time(8, 0), "daily"))
    luna.add_task(Task("task-2", "Breakfast", time(8, 30), "daily"))
    mochi.add_task(Task("task-3", "Evening play", time(18, 0), "daily"))

    print("Today's Schedule")
    print(Scheduler().render_schedule(owner))


if __name__ == "__main__":
    main()
