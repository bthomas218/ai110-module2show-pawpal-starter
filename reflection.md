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

The design changed in three main ways. First, `User` remains the owner of its
`Pet` objects, and each `Pet` remains the owner of its `Task` objects. The
`Scheduler` no longer keeps a second map of user IDs, pet IDs, and tasks. It
now reads the user's pets and builds a schedule from their existing tasks.
This avoids two sources of truth that could become inconsistent.

Second, `Task`, `Pet`, and `User` use Python dataclasses with direct public
fields instead of boilerplate getters and setters. The fields are easier to
read and update, while meaningful behavior such as `mark_complete`,
`add_task`, and `add_pet` remains as methods.

Finally, `Task` now includes `duration_minutes` and `priority`. These fields
were added because the project requires scheduling based on available time
and task importance. The scheduler also accepts a target date and optional
available time so the later implementation can support the project's
"today's schedule" use case.

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
