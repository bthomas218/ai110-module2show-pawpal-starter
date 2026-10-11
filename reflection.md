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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

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
