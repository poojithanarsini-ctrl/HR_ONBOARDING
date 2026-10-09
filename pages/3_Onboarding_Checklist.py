
import streamlit as st

from modules.database import (
    initialize_database,
    seed_onboarding_tasks,
    get_onboarding_tasks,
    set_task_progress,
    get_employee_progress,
)

st.title("✅ Employee Onboarding Checklist")

# Ensure the database and onboarding tasks exist
initialize_database()
seed_onboarding_tasks()

# Get the logged-in employee
user = st.session_state.get("user")

if not user:
    st.warning("Please log in to view your onboarding checklist.")
    st.stop()

employee_id = user["id"]

st.write(f"Welcome, {user['name']}!")
st.write("Complete these activities as you begin your new job.")

# Load tasks and this employee's saved progress
tasks = get_onboarding_tasks()
progress_rows = get_employee_progress(employee_id)

saved_progress = {
    row["id"]: bool(row["is_completed"])
    for row in progress_rows
}

completed = 0

for task in tasks:
    task_id = task["id"]
    task_name = task["title"]

    is_completed = saved_progress.get(task_id, False)

    checked = st.checkbox(
        task_name,
        value=is_completed,
        key=f"task_{employee_id}_{task_id}",
    )

    if checked != is_completed:
        set_task_progress(employee_id, task_id, checked)
        st.rerun()

    if checked:
        completed += 1

if tasks:
    progress = completed / len(tasks)
    st.progress(progress)
    st.write(f"Completed: {completed} out of {len(tasks)} tasks")

    if completed == len(tasks):
        st.success("Great work! You have completed all onboarding tasks.")
else:
    st.info("No onboarding tasks are available yet.")
