"""Core domain model and scheduling behavior for PawPal+."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import time as Time


OwnerId = str
PetId = str
TaskId = str


@dataclass
class Task:
    """A single activity for a pet."""

    id: TaskId
    description: str
    time: Time | None = None
    frequency: str = "once"
    completion_status: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completion_status = True

    def is_complete(self) -> bool:
        """Return whether this task has been completed."""
        return self.completion_status


@dataclass
class Pet:
    """A pet and the activities associated with it."""

    id: PetId
    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet."""
        self.tasks.remove(task)


@dataclass
class Owner:
    """An owner who manages multiple pets."""

    id: OwnerId
    name: str
    email: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's collection."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from the owner's collection."""
        self.pets.remove(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return every task belonging to every pet owned by this owner."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """The scheduling service for tasks across all of an owner's pets."""

    def build_schedule(self, owner: Owner) -> list[Task]:
        """Return incomplete tasks from all pets, ordered by scheduled time.

        The scheduler deliberately retrieves tasks through ``owner`` instead
        of reading a particular pet directly. Tasks without a time are placed
        after timed tasks while preserving their original order.
        """
        tasks = [task for task in owner.get_all_tasks() if not task.is_complete()]
        return sorted(tasks, key=lambda task: (task.time is None, task.time or Time.max))

    def complete_task(self, owner: Owner, task_id: TaskId) -> bool:
        """Complete a task found across the owner's pets.

        Return ``True`` when a matching task is found, otherwise ``False``.
        """
        for task in owner.get_all_tasks():
            if task.id == task_id:
                task.mark_complete()
                return True
        return False

    def render_schedule(self, owner: Owner) -> str:
        """Render the owner's incomplete tasks as a simple text schedule."""
        lines = [f"Schedule for {owner.name}"]
        for task in self.build_schedule(owner):
            task_time = task.time.strftime("%H:%M") if task.time else "Any time"
            lines.append(f"{task_time} - {task.description} ({task.frequency})")
        return "\n".join(lines)
