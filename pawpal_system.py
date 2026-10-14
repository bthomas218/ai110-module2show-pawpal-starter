"""Core domain model and scheduling behavior for PawPal+."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, time as Time, timedelta


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
    due_date: date | None = None
    duration_minutes: int = 0

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

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Return tasks ordered by scheduled time."""
        return sorted(
            tasks,
            key=lambda task: (task.time is None, task.time or Time.max),
        )

    def filter_tasks(
        self,
        owner: Owner,
        completion_status: bool | None = None,
        pet_name: str | None = None,
    ) -> list[Task]:
        """Return an owner's tasks matching completion status and/or pet name."""
        matching_tasks: list[Task] = []
        for pet in owner.pets:
            if pet_name is not None and pet.name.lower() != pet_name.lower():
                continue
            for task in pet.tasks:
                if (
                    completion_status is None
                    or task.is_complete() == completion_status
                ):
                    matching_tasks.append(task)
        return matching_tasks

    def detect_conflicts(self, owner: Owner) -> list[str]:
        """Return warnings for incomplete tasks with overlapping time ranges."""
        scheduled_tasks: list[tuple[str, Task]] = []
        for pet in owner.pets:
            for task in pet.tasks:
                if not task.is_complete() and task.time is not None:
                    scheduled_tasks.append((pet.name, task))

        warnings: list[str] = []
        for index, (pet_name, task) in enumerate(scheduled_tasks):
            for other_pet_name, other_task in scheduled_tasks[index + 1 :]:
                if task.due_date != other_task.due_date:
                    continue
                if not self._tasks_overlap(task, other_task):
                    continue
                warnings.append(
                    "Warning: overlapping tasks - "
                    f"{pet_name}: {task.description} "
                    f"({self._task_time_range(task)}) and "
                    f"{other_pet_name}: {other_task.description} "
                    f"({self._task_time_range(other_task)})."
                )
        return warnings

    def _tasks_overlap(self, first: Task, second: Task) -> bool:
        """Return whether two scheduled tasks overlap in time."""
        first_start = self._minutes_since_midnight(first)
        second_start = self._minutes_since_midnight(second)
        first_end = first_start + max(first.duration_minutes, 0)
        second_end = second_start + max(second.duration_minutes, 0)

        if first.duration_minutes <= 0 or second.duration_minutes <= 0:
            return first_start == second_start
        return first_start < second_end and second_start < first_end

    def _minutes_since_midnight(self, task: Task) -> int:
        if task.time is None:
            return 0
        return task.time.hour * 60 + task.time.minute

    def _task_time_range(self, task: Task) -> str:
        start = self._minutes_since_midnight(task)
        end = start + max(task.duration_minutes, 0)
        end_hour, end_minute = divmod(end, 60)
        end_hour %= 24
        return (
            f"{task.time:%H:%M}-{end_hour:02d}:{end_minute:02d}"
            if task.time is not None
            else "Any time"
        )

    def build_schedule(self, owner: Owner) -> list[Task]:
        """Return incomplete tasks from all pets, ordered by scheduled time."""
        tasks = self.filter_tasks(owner, completion_status=False)
        return self.sort_tasks(tasks)

    def complete_task(self, owner: Owner, task_id: TaskId) -> bool:
        """Complete a task and schedule its next recurring instance when needed."""
        for pet in owner.pets:
            for task in pet.tasks:
                if task.id != task_id:
                    continue

                task.mark_complete()
                if task.frequency.lower() in {"daily", "weekly", "monthly"}:
                    next_task_id = self._next_task_id(owner, task.id)
                    pet.add_task(
                        Task(
                            id=next_task_id,
                            description=task.description,
                            time=task.time,
                            frequency=task.frequency,
                            due_date=self._next_due_date(task),
                        )
                    )
                return True
        return False

    def _next_due_date(self, task: Task) -> date:
        """Return the next due date for a recurring task.

        Monthly recurrence uses a 30-day interval, as requested, rather than
        requiring an additional calendar library for variable-length months.
        """
        recurrence_days = {
            "daily": 1,
            "weekly": 7,
            "monthly": 30,
        }
        interval = recurrence_days[task.frequency.lower()]
        current_due_date = task.due_date or date.today()
        return current_due_date + timedelta(days=interval)

    def _next_task_id(self, owner: Owner, completed_task_id: TaskId) -> TaskId:
        """Generate a unique ID for the next recurring task instance."""
        existing_ids = {task.id for task in owner.get_all_tasks()}
        instance_number = 1
        next_task_id = f"{completed_task_id}-next-{instance_number}"
        while next_task_id in existing_ids:
            instance_number += 1
            next_task_id = f"{completed_task_id}-next-{instance_number}"
        return next_task_id

    def render_schedule(self, owner: Owner) -> str:
        """Render the owner's incomplete tasks as a simple text schedule."""
        lines = [f"Schedule for {owner.name}"]
        for task in self.build_schedule(owner):
            task_time = task.time.strftime("%H:%M") if task.time else "Any time"
            lines.append(f"{task_time} - {task.description} ({task.frequency})")
        return "\n".join(lines)
