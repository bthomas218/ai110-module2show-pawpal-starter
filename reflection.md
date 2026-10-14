# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

### Three Core Actions

1. Add a pet
2. Schedule tasks for pets
3. View today's schedule

### Classes and Responsibilities

- **Pet**: Represents a pet in the system. Responsibilities include storing pet information and managing its tasks.
  - Attributes: id, name, species, age, tasks (list of Task objects)
  - Methods: setName(String), setSpecies(String), setAge(int), addTask(Task), removeTask(Task), getTasks(), getId()
- **Task**: Represents a task to be performed for a pet. Responsibilities include storing task details and tracking its completion status.
  - Attributes: id, description, dueDate, completionStatus
  - Methods: setDescription(String), setDueDate(Date), setCompletionStatus(boolean), getDescription(), getDueDate(), getCompletionStatus(), markComplete() getId()
- **Scheduler**: Manages the scheduling of tasks for pets. Responsibilities include retrieving, organizing, and managing tasks across multiple pets.
  - Attributes: schedule (map of tuple (UserId, PetId) to list of Task objects)
  - Methods: addTaskForPet(UserId, TaskId, PetId), getTasksForPet(UserId, PetId), removeTaskForPet(UserId, PetId), renderSchedule(UserId)
- **User**: Represents the user interacting with the system. Responsibilities include storing user information and managing their pets.
  - Attributes: id, name, email, pets (list of Pet objects)
  - Methods: addPet(Pet), removePet(Pet), getPets(), getName(), getEmail(), setName(String), setEmail(String), getId()

**b. Design changes**

The design changed in several ways during implementation. The original
`User` class is now named `Owner` to match the domain language. `Owner` owns
the collection of `Pet` objects and provides `get_all_tasks()`, which flattens
the tasks from every pet into one collection.

The `Scheduler` no longer stores a duplicate map of users, pets, and tasks.
Instead, it must retrieve tasks through `Owner.get_all_tasks()`, then filter
out completed tasks and order the remaining tasks by their scheduled time.
This keeps ownership in the domain objects and gives the scheduler one clear
entry point for working across multiple pets.

`Task` was also changed to represent the requested activity data directly:
description, time, frequency, and completion status. Dataclasses expose these
fields without boilerplate getters and setters, while behavior that changes
state—such as `mark_complete`, adding pets, and adding tasks—remains on the
appropriate class. The scheduler additionally provides `complete_task()` and
`render_schedule()` so it can manage and present the combined task list.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers whether a task is complete, the task's scheduled time,
the pet it belongs to, its duration, and its recurrence frequency. The daily
schedule removes completed tasks and sorts the remaining tasks by time. Tasks
without a time are placed after tasks with scheduled times. The scheduler also
checks whether two incomplete tasks overlap, including tasks belonging to
different pets, and reports those conflicts as warnings.

For recurring tasks, the scheduler creates the next incomplete instance after
completion. Daily tasks move forward one day, weekly tasks move forward seven
days, and monthly tasks move forward thirty days. I treated completion status
and scheduled time as the most important constraints because the owner first
needs to know what still needs to be done and when it should happen. Duration
and pet ownership are then used to identify practical conflicts in the plan.

**b. Tradeoffs**

The conflict detector uses a simple pairwise comparison of scheduled tasks. It
checks each task against the tasks that follow it and returns a readable
warning when their time intervals overlap. This is easy to understand and
handles both same-pet and cross-pet conflicts, but it is less efficient than a
sweep-line or interval-tree algorithm for a very large number of tasks.

The scheduler also reports the conflict instead of automatically moving,
deleting, or rejecting either task. This means the owner still decides which
care activity should change, so the program does not make an unsafe assumption
about medication, feeding, or pet-care timing. The tradeoff is reasonable for
this small household scheduling app because the number of tasks is expected to
be small, and a clear warning is more useful than silently changing the owner's
plan.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI to review the initial UML design, create the first Mermaid diagram,
draft the Python dataclasses, and identify gaps in the scheduling model. The
most useful prompts asked the AI to compare the design with the project
requirements and to point out duplicate ownership, unclear method signatures,
and missing scheduling information.

The AI also helped create the command-line demonstration and draft the two
pytest tests for task completion and task addition.

**b. Judgment and verification**

I did not accept the idea of giving `Scheduler` its own map of users, pets,
and tasks as the final design. After reviewing it, I chose to keep ownership
in `Owner` and `Pet`, then added `Owner.get_all_tasks()` so the scheduler could
work across pets without duplicating state. I also rejected unnecessary
getter and setter methods because Python dataclasses provide direct field
access.

I verified the revised design by checking that the scheduler calls
`Owner.get_all_tasks()`, running the command-line demo, compiling the Python
modules, and running the pytest suite. The final tests passed for task
completion and task addition.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
