import streamlit as st
from datetime import time

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
pet_age = st.number_input("Pet age", min_value=0, max_value=100, value=3)

if "owner" not in st.session_state:
    st.session_state.owner = Owner("owner-1", owner_name, "jordan@example.com")
st.session_state.owner.name = owner_name

if st.button("Add pet"):
    pet_id = f"pet-{len(st.session_state.owner.pets) + 1}"
    st.session_state.owner.add_pet(Pet(pet_id, pet_name, species, int(pet_age)))
    st.success(f"Added {pet_name}.")

if st.session_state.owner.pets:
    st.write("Pets:")
    st.table(
        [
            {"name": pet.name, "species": pet.species, "age": pet.age}
            for pet in st.session_state.owner.pets
        ]
    )

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

selected_pet = None
if st.session_state.owner.pets:
    selected_pet_name = st.selectbox(
        "Add task to",
        [pet.name for pet in st.session_state.owner.pets],
    )
    selected_pet = next(
        pet for pet in st.session_state.owner.pets if pet.name == selected_pet_name
    )

if st.button("Add task"):
    if selected_pet is None:
        st.warning("Add a pet before adding a task.")
    else:
        task_id = f"task-{len(st.session_state.owner.get_all_tasks()) + 1}"
        task = Task(
            task_id,
            f"{task_title} ({int(duration)} min, {priority} priority)",
            time(9, 0),
            "once",
        )
        selected_pet.add_task(task)
        st.success(f"Added task for {selected_pet.name}.")

all_tasks = st.session_state.owner.get_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "pet": pet.name,
                "task": task.description,
                "complete": task.is_complete(),
            }
            for pet in st.session_state.owner.pets
            for task in pet.tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    if not all_tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        st.text(Scheduler().render_schedule(st.session_state.owner))
