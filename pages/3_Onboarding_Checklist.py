import streamlit as st

from modules.database import (
    initialize_database,
    seed_onboarding_tasks,
    get_onboarding_tasks,
    set_task_progress,
    get_employee_progress,
)

st.title("✅ Employee Onboarding Checklist")
initialize_database()
seed_onboarding_tasks()

st.write("Complete these activities as you begin your new job.")


tasks = get_onboarding_tasks()
progress_rows = get_employee_progress(1)

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
        key=f"task_{task_id}",
    )

    if checked != is_completed:
        set_task_progress(1, task_id, checked)
        st.rerun()

    if checked:
        completed += 1


progress = completed / len(tasks)

st.progress(progress)

st.write(f"Completed: {completed} out of {len(tasks)} tasks")

if completed == len(tasks):
    st.success("Great work! You have completed all onboarding tasks.")