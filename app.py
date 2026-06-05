import streamlit as st
import sqlite3
import pandas as pd
from backend.agent import generate_study_plan

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Smart Timetable Assistant",
    page_icon="📅",
    layout="wide"
)

# -----------------------------------
# DATABASE CONNECTION
# -----------------------------------

conn = sqlite3.connect("student_schedule.db")
cursor = conn.cursor()

# -----------------------------------
# TITLE
# -----------------------------------

st.title("📅 Smart Timetable Assistant")

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("Menu")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Events",
        "Assignments",
        "AI Planner",
        "Free Slots"
    ]
)

st.sidebar.markdown("---")
st.sidebar.write("Smart Timetable Assistant")
st.sidebar.write("Week 7 Dashboard")

# -----------------------------------
# DASHBOARD
# -----------------------------------

if menu == "Dashboard":

    st.header("Dashboard")

    st.success("Welcome to Smart Timetable Assistant")

    cursor.execute("SELECT COUNT(*) FROM events")
    event_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM assignments")
    assignment_count = cursor.fetchone()[0]

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Events", event_count)

    with col2:
        st.metric("Total Assignments", assignment_count)

    st.subheader("Weekly Schedule")

    events_df = pd.read_sql_query(
        "SELECT * FROM events",
        conn
    )

    st.dataframe(events_df)

    st.subheader("Monthly Schedule")

    st.write("All events scheduled this month")

    st.dataframe(events_df)

# -----------------------------------
# DATABASE CONNECTION
# -----------------------------------

conn = sqlite3.connect("student_schedule.db")
cursor = conn.cursor()

# -----------------------------------
# EVENT MANAGEMENT
# -----------------------------------

st.header("Event Management")

event = st.text_input("Enter Event")
date = st.date_input("Select Event Date")
time = st.time_input("Select Event Time")

if st.button("Add Event"):

    cursor.execute(
        "SELECT * FROM events WHERE date=? AND time=?",
        (str(date), str(time))
    )

    conflict = cursor.fetchone()

    if conflict:

        st.error("Time Conflict Detected")

    else:

        cursor.execute(
            "INSERT INTO events(title,date,time) VALUES(?,?,?)",
            (
                event,
                str(date),
                str(time)
            )
        )

        conn.commit()

        st.success("Event Added Successfully")

if st.button("Show Timetable"):

    df = pd.read_sql_query(
        "SELECT * FROM events",
        conn
    )

    st.dataframe(df)

# -----------------------------------
# ASSIGNMENT TRACKER
# -----------------------------------

st.header("Assignment Tracker")

subject = st.text_input("Subject")
deadline = st.date_input("Deadline")

priority = st.selectbox(
    "Priority",
    ["High", "Medium", "Low"]
)

if st.button("Add Assignment"):

    cursor.execute(
        """
        INSERT INTO assignments(
            subject,
            deadline,
            priority
        )
        VALUES(?,?,?)
        """,
        (
            subject,
            str(deadline),
            priority
        )
    )

    conn.commit()

    st.success("Assignment Added Successfully")

if st.button("Show Assignments"):

    df = pd.read_sql_query(
        "SELECT * FROM assignments",
        conn
    )

    st.dataframe(df)

# -----------------------------------
# AI STUDY PLANNER
# -----------------------------------

st.header("AI Study Planner")

study_hours = st.slider(
    "Study Hours",
    min_value=1,
    max_value=10,
    value=3
)

if st.button("Generate Plan"):

    try:

        plan = generate_study_plan(
            study_hours
        )

        st.write(plan)

    except Exception as e:

        st.error(
            f"Error: {e}"
        )

# -----------------------------------
# FREE SLOT FINDER
# -----------------------------------

st.header("Free Time Slots")

search_date = st.date_input(
    "Choose Date For Free Slots"
)

if st.button("Find Free Slots"):

    cursor.execute(
        """
        SELECT time
        FROM events
        WHERE date=?
        """,
        (str(search_date),)
    )

    booked = cursor.fetchall()

    booked_times = [item[0] for item in booked]

    all_slots = [
        "09:00:00",
        "10:00:00",
        "11:00:00",
        "12:00:00",
        "14:00:00",
        "15:00:00",
        "16:00:00",
        "17:00:00"
    ]

    free_slots = []

    for slot in all_slots:

        if slot not in booked_times:

            free_slots.append(slot)

    st.success("Available Free Slots")

    st.write(free_slots)

# -----------------------------------
# SMART STUDY SUGGESTIONS
# -----------------------------------

st.header("Smart Study Suggestions")

if st.button("Suggest Study Session"):

    query = """
    SELECT *
    FROM assignments
    WHERE priority='High'
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    st.write(
        "Focus on these High Priority Assignments:"
    )

    st.dataframe(df)

# -----------------------------------
# CLOSE DATABASE
# -----------------------------------

conn.close()