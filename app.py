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

try:

    conn = sqlite3.connect(
        "student_schedule.db",
        check_same_thread=False
    )

    cursor = conn.cursor()

    # Create Events Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        date TEXT,
        time TEXT
    )
    """)

    # Create Assignments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assignments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT,
        deadline TEXT,
        priority TEXT
    )
    """)

    conn.commit()

except Exception as e:

    st.error(f"Database Error: {e}")
    st.stop()

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

    try:

        cursor.execute(
            "SELECT COUNT(*) FROM events"
        )

        event_count = cursor.fetchone()[0]

    except:

        event_count = 0

    try:

        cursor.execute(
            "SELECT COUNT(*) FROM assignments"
        )

        assignment_count = cursor.fetchone()[0]

    except:

        assignment_count = 0

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Total Events",
            event_count
        )

    with col2:

        st.metric(
            "Total Assignments",
            assignment_count
        )

    st.subheader("Weekly Schedule")

    try:

        events_df = pd.read_sql_query(
            "SELECT * FROM events",
            conn
        )

        st.dataframe(events_df)

    except Exception as e:

        st.warning(
            f"Unable to load events: {e}"
        )

# -----------------------------------
# EVENTS
# -----------------------------------

elif menu == "Events":

    st.header("Event Management")

    event = st.text_input(
        "Enter Event"
    )

    date = st.date_input(
        "Select Event Date"
    )

    time = st.time_input(
        "Select Event Time"
    )

    if st.button("Add Event"):

        cursor.execute(
            """
            SELECT *
            FROM events
            WHERE date=? AND time=?
            """,
            (
                str(date),
                str(time)
            )
        )

        conflict = cursor.fetchone()

        if conflict:

            st.error(
                "Time Conflict Detected"
            )

        else:

            cursor.execute(
                """
                INSERT INTO events(
                    title,
                    date,
                    time
                )
                VALUES(?,?,?)
                """,
                (
                    event,
                    str(date),
                    str(time)
                )
            )

            conn.commit()

            st.success(
                "Event Added Successfully"
            )

    if st.button("Show Timetable"):

        df = pd.read_sql_query(
            "SELECT * FROM events",
            conn
        )

        st.dataframe(df)

# -----------------------------------
# ASSIGNMENTS
# -----------------------------------

elif menu == "Assignments":

    st.header("Assignment Tracker")

    subject = st.text_input(
        "Subject"
    )

    deadline = st.date_input(
        "Deadline"
    )

    priority = st.selectbox(
        "Priority",
        [
            "High",
            "Medium",
            "Low"
        ]
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

        st.success(
            "Assignment Added Successfully"
        )

    if st.button("Show Assignments"):

        df = pd.read_sql_query(
            "SELECT * FROM assignments",
            conn
        )

        st.dataframe(df)

# -----------------------------------
# AI PLANNER
# -----------------------------------

elif menu == "AI Planner":

    st.header("AI Study Planner")

    study_hours = st.slider(
        "Study Hours",
        min_value=1,
        max_value=10,
        value=3
    )

    if st.button(
        "Generate Plan"
    ):

        try:

            plan = generate_study_plan(
                study_hours
            )

            st.write(plan)

        except Exception as e:

            st.error(
                f"AI Error: {e}"
            )

# -----------------------------------
# FREE SLOT FINDER
# -----------------------------------

elif menu == "Free Slots":

    st.header("Free Time Slots")

    search_date = st.date_input(
        "Choose Date For Free Slots"
    )

    if st.button(
        "Find Free Slots"
    ):

        cursor.execute(
            """
            SELECT time
            FROM events
            WHERE date=?
            """,
            (
                str(search_date),
            )
        )

        booked = cursor.fetchall()

        booked_times = [
            item[0]
            for item in booked
        ]

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

                free_slots.append(
                    slot
                )

        st.success(
            "Available Free Slots"
        )

        st.write(
            free_slots
        )

        st.subheader(
            "High Priority Assignments"
        )

        query = """
        SELECT *
        FROM assignments
        WHERE priority='High'
        """

        df = pd.read_sql_query(
            query,
            conn
        )

        st.dataframe(df)

# -----------------------------------
# CLOSE DATABASE
# -----------------------------------

conn.close()