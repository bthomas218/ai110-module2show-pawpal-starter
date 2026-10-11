"""Core domain model for PawPal+.

The data classes own the application's state. Scheduler is a stateless service
that reads a user's pets and builds a plan from their tasks.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


UserId = str
PetId = str
TaskId = str


@dataclass
class Task:
    """A care task that should be completed for a pet."""

    id: TaskId
    description: str
    due_date: date | None = None
    duration_minutes: int = 0
    priority: str = "medium"
    completion_status: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completion_status = True


@dataclass
class Pet:
    """A pet and the care tasks associated with it."""

    id: PetId
    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's task list."""
        self.tasks.remove(task)


@dataclass
class User:
    """A PawPal+ user and the pets they manage."""

    id: UserId
    name: str
    email: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this user's pets."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this user's pets."""
        self.pets.remove(pet)


class Scheduler:
    """Builds schedules from the tasks already owned by a user's pets."""

    def build_schedule(
        self,
        user: User,
        schedule_date: date,
        available_minutes: int | None = None,
    ) -> dict[PetId, list[Task]]:
        """Return the user's tasks grouped by pet for a given date.

        Scheduling and prioritization logic will be implemented after the
        domain model is finalized.
        """
        raise NotImplementedError

    def render_schedule(self, user: User, schedule_date: date) -> str:
        """Render a user's schedule for display."""
        raise NotImplementedError
