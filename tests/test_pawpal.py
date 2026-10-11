from pawpal_system import Pet, Task


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
