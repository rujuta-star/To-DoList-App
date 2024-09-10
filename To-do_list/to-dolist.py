import streamlit as st
import pandas as pd
import datetime
from plyer import notification

# Initializing global state
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "priorities" not in st.session_state:
    st.session_state.priorities = []
if "tags" not in st.session_state:
    st.session_state.tags = []
if "statuses" not in st.session_state:
    st.session_state.statuses = []
if "deadlines" not in st.session_state:
    st.session_state.deadlines = []
if "notes" not in st.session_state:
    st.session_state.notes = []
if "attachments" not in st.session_state:
    st.session_state.attachments = []
if "habit_tracker" not in st.session_state:
    st.session_state.habit_tracker = []
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = [False] * len(st.session_state.tasks)

# Update `edit_mode` to match the length of tasks
def update_edit_mode():
    # Ensure `edit_mode` has the same length as `tasks`
    if len(st.session_state.edit_mode) < len(st.session_state.tasks):
        st.session_state.edit_mode.extend([False] * (len(st.session_state.tasks) - len(st.session_state.edit_mode)))
    elif len(st.session_state.edit_mode) > len(st.session_state.tasks):
        st.session_state.edit_mode = st.session_state.edit_mode[:len(st.session_state.tasks)]

# Call this after every task addition/removal
update_edit_mode()

# Feature: Add New Task
def add_task(task, priority, tag, status, deadline, note, attachment):
    st.session_state.tasks.append(task)
    st.session_state.priorities.append(priority)
    st.session_state.tags.append(tag)
    st.session_state.statuses.append(status)
    st.session_state.deadlines.append(deadline)
    st.session_state.notes.append(note)
    st.session_state.attachments.append(attachment)
    update_edit_mode()  

# Feature: Remove Task
def remove_task(index):
    del st.session_state.tasks[index]
    del st.session_state.priorities[index]
    del st.session_state.tags[index]
    del st.session_state.statuses[index]
    del st.session_state.deadlines[index]
    del st.session_state.notes[index]
    del st.session_state.attachments[index]
    update_edit_mode()

# Feature: Add Habit to Tracker
def add_habit(habit_name, frequency, start_date):
    st.session_state.habit_tracker.append({"habit": habit_name, "frequency": frequency, "start_date": start_date, "completed": False})

# Task form and sidebar
st.title("📋 To-Do List for Students")
st.markdown("<style>body{background-color: #F9F9F9;}</style>", unsafe_allow_html=True)

st.sidebar.title("📝 Add a New Task")
task_name = st.sidebar.text_input("Task Name")
priority = st.sidebar.selectbox("Priority", ["Low", "Medium", "High"])
tag = st.sidebar.text_input("Tag (e.g., assignment, study, project)")
status = st.sidebar.selectbox("Status", ["Not Started", "In Progress", "Completed"])
deadline = st.sidebar.date_input("Deadline", datetime.date.today())
note = st.sidebar.text_area("Notes")
attachment = st.sidebar.file_uploader("Attach File", type=["pdf", "docx", "txt", "jpg", "png"])

# Button to add task
if st.sidebar.button("Add Task"):
    if task_name:
        add_task(task_name, priority, tag, status, deadline, note, attachment)
        st.sidebar.success(f"Task '{task_name}' added!")
    else:
        st.sidebar.warning("Please enter a task name")

# Habit Tracker
st.sidebar.title("💪 Add a Habit")
habit_name = st.sidebar.text_input("Habit Name")
frequency = st.sidebar.selectbox("Frequency", ["Daily", "Weekly", "Monthly"])
start_date = st.sidebar.date_input("Start Date", datetime.date.today())

if st.sidebar.button("Add Habit"):
    if habit_name:
        add_habit(habit_name, frequency, start_date)
        st.sidebar.success(f"Habit '{habit_name}' added to tracker!")
    else:
        st.sidebar.warning("Please enter a habit name")

# Display Habits
st.header("Your Habit Tracker")
if len(st.session_state.habit_tracker) == 0:
    st.write("No habits added yet!")
else:
    for i, habit in enumerate(st.session_state.habit_tracker):
        st.write(f"**Habit:** {habit['habit']} | **Frequency:** {habit['frequency']} | **Start Date:** {habit['start_date'].strftime('%d-%m-%Y')}")
        if st.checkbox(f"Mark Completed", key=f"habit_complete_{i}"):
            st.session_state.habit_tracker[i]["completed"] = True
            st.success(f"Habit '{habit['habit']}' marked completed!")

# Display To-Do List
st.header("Your To-Do List")
if len(st.session_state.tasks) == 0:
    st.write("No tasks yet! Add tasks from the sidebar.")
else:
    for i, task in enumerate(st.session_state.tasks):
        col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 1, 1, 1, 2, 1, 1])

        if not st.session_state.edit_mode[i]:
            # Normal display mode
            with col1:
                st.markdown(f"### **{task}**")
            with col2:
                st.write(f"**Priority:** {st.session_state.priorities[i]}")
            with col3:
                st.write(f"**Status:** {st.session_state.statuses[i]}")
            with col4:
                st.write(f"**Deadline:** {st.session_state.deadlines[i].strftime('%d-%m-%Y')}")
            with col5:
                st.write(f"**Tag:** {st.session_state.tags[i]}")
            
            with col6:
                if st.button("Edit", key=f"edit_{i}"):
                    st.session_state.edit_mode[i] = True  # Enable edit mode for this task

            with col7:
                if st.button("Delete", key=f"delete_{i}"):
                    remove_task(i)
                    st.warning(f"Task '{task}' removed!")
                if st.checkbox("Mark as Complete", key=f"complete_{i}"):
                    st.session_state.statuses[i] = "Completed"
                    st.success(f"Task '{task}' marked as completed!")
        else:
            # Edit mode
            with col1:
                new_task_name = st.text_input("Edit Task Name", value=task, key=f"task_name_{i}")
            with col2:
                new_priority = st.selectbox("Edit Priority", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(st.session_state.priorities[i]), key=f"priority_{i}")
            with col3:
                new_status = st.selectbox("Edit Status", ["Not Started", "In Progress", "Completed"], index=["Not Started", "In Progress", "Completed"].index(st.session_state.statuses[i]), key=f"status_{i}")
            with col4:
                new_deadline = st.date_input("Edit Deadline", value=st.session_state.deadlines[i], key=f"deadline_{i}")
            with col5:
                new_tag = st.text_input("Edit Tag", value=st.session_state.tags[i], key=f"tag_{i}")
            
            with col6:
                if st.button("Save Changes", key=f"save_{i}"):
                    # Update task information in session state
                    st.session_state.tasks[i] = new_task_name
                    st.session_state.priorities[i] = new_priority
                    st.session_state.tags[i] = new_tag
                    st.session_state.statuses[i] = new_status
                    st.session_state.deadlines[i] = new_deadline
                    st.session_state.edit_mode[i] = False  # Disable edit mode
                    st.success(f"Task '{new_task_name}' updated!")

            with col7:
                if st.button("Cancel", key=f"cancel_{i}"):
                    st.session_state.edit_mode[i] = False  # Cancel edit mode

# Calculate progress in terms of fraction (between 0.0 and 1.0)
completed_tasks = st.session_state.statuses.count("Completed")
total_tasks = len(st.session_state.tasks)

if total_tasks > 0:
    progress_fraction = completed_tasks / total_tasks  # This gives a value between 0.0 and 1.0
    st.progress(progress_fraction)
    st.write(f"🎯 Completed {completed_tasks} out of {total_tasks} tasks!")
# Deadline warnings and notifications
for i, deadline in enumerate(st.session_state.deadlines):
    days_remaining = (deadline - datetime.date.today()).days
    if st.session_state.statuses[i] != "Completed" and days_remaining <= 2:
        st.warning(f"⚠️ Task '{st.session_state.tasks[i]}' is due in {days_remaining} days!")
    if days_remaining == 0 and st.session_state.statuses[i] != "Completed":
        notification.notify(
            title=f"Reminder for task: {st.session_state.tasks[i]}",
            message=f"Your task is due today!",
            timeout=10
        )

# Task Analytics
st.header("Task Analytics")
if total_tasks > 0:
    task_count_by_priority = pd.Series(st.session_state.priorities).value_counts()
    st.bar_chart(task_count_by_priority)

    task_count_by_tag = pd.Series(st.session_state.tags).value_counts()
    st.bar_chart(task_count_by_tag)
