"""Core domain model skeleton for PawPal+.

The classes in this module mirror the initial UML design. Scheduling behavior
can be implemented incrementally without changing the basic data model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


UserId = str
PetId = str
TaskId = str
ScheduleKey = tuple[UserId, PetId]


@dataclass
class Task:
    """A care task that should be completed for a pet."""

    id: TaskId
    description: str
    due_date: date | None = None
    completion_status: bool = False

    def set_description(self, description: str) -> None:
        raise NotImplementedError

    def set_due_date(self, due_date: date) -> None:
        raise NotImplementedError

    def set_completion_status(self, status: bool) -> None:
        raise NotImplementedError

    def get_description(self) -> str:
        raise NotImplementedError

    def get_due_date(self) -> date | None:
        raise NotImplementedError

    def get_completion_status(self) -> bool:
        raise NotImplementedError

    def mark_complete(self) -> None:
        raise NotImplementedError

    def get_id(self) -> TaskId:
        raise NotImplementedError


@dataclass
class Pet:
    """A pet and the care tasks associated with it."""

    id: PetId
    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def set_name(self, name: str) -> None:
        raise NotImplementedError

    def set_species(self, species: str) -> None:
        raise NotImplementedError

    def set_age(self, age: int) -> None:
        raise NotImplementedError

    def add_task(self, task: Task) -> None:
        raise NotImplementedError

    def remove_task(self, task: Task) -> None:
        raise NotImplementedError

    def get_tasks(self) -> list[Task]:
        raise NotImplementedError

    def get_id(self) -> PetId:
        raise NotImplementedError


@dataclass
class User:
    """A PawPal+ user and the pets they manage."""

    id: UserId
    name: str
    email: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        raise NotImplementedError

    def remove_pet(self, pet: Pet) -> None:
        raise NotImplementedError

    def get_pets(self) -> list[Pet]:
        raise NotImplementedError

    def get_name(self) -> str:
        raise NotImplementedError

    def get_email(self) -> str:
        raise NotImplementedError

    def set_name(self, name: str) -> None:
        raise NotImplementedError

    def set_email(self, email: str) -> None:
        raise NotImplementedError

    def get_id(self) -> UserId:
        raise NotImplementedError


@dataclass
class Scheduler:
    """Stores tasks grouped by user and pet until scheduling is implemented."""

    schedule: dict[ScheduleKey, list[Task]] = field(default_factory=dict)

    def add_task_for_pet(
        self, user_id: UserId, task_id: TaskId, pet_id: PetId
    ) -> None:
        raise NotImplementedError

    def get_tasks_for_pet(
        self, user_id: UserId, pet_id: PetId
    ) -> list[Task]:
        raise NotImplementedError

    def remove_task_for_pet(self, user_id: UserId, pet_id: PetId) -> None:
        raise NotImplementedError

    def render_schedule(self, user_id: UserId) -> str:
        raise NotImplementedError
