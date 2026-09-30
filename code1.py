import streamlit as st
import json

st.set_page_config(page_title="Student Attendance Tracker", page_icon="🎓")

st.title("🎓 Student Attendance Tracker")
st.write("Manage student attendance using a JSON file.")

FILE_NAME = "attendance.json"


def load_data():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except:
        return []


def save_data(data):
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


if "attendance" not in st.session_state:
    st.session_state.attendance = load_data()


# ---------------- ADD ATTENDANCE ----------------

st.header("📝 Mark Attendance")

with st.form("attendance_form"):

    roll_no = st.text_input("Roll Number")
    name = st.text_input("Student Name")
    subject = st.text_input("Subject")
    date = st.text_input("Date", placeholder="DD-MM-YYYY")
    status = st.radio("Attendance", ["Present", "Absent"])

    submit = st.form_submit_button("Submit Attendance")

    if submit:

        if roll_no.strip() == "":
            st.error("Please enter Roll Number")

        elif name.strip() == "":
            st.error("Please enter Student Name")

        elif subject.strip() == "":
            st.error("Please enter Subject")

        elif date.strip() == "":
            st.error("Please enter Date")

        else:
            duplicate = False

            for record in st.session_state.attendance:
                if (
                    record["roll_no"] == roll_no
                    and record["subject"] == subject
                    and record["date"] == date
                ):
                    duplicate = True
                    break

            if duplicate:
                st.warning("Attendance already exists for this student on this date.")

            else:
                record = {
                    "roll_no": roll_no,
                    "name": name,
                    "subject": subject,
                    "date": date,
                    "status": status
                }

                st.session_state.attendance.append(record)
                save_data(st.session_state.attendance)

                st.success("Attendance saved successfully!")


# ---------------- DISPLAY RECORDS ----------------

st.header("📋 Attendance Records")

if len(st.session_state.attendance) == 0:

    st.info("No attendance records available.")

else:

    st.table(st.session_state.attendance)


# ---------------- ATTENDANCE CALCULATION ----------------

st.header("📊 Attendance Percentage")

roll_search = st.text_input("Enter Roll Number to calculate attendance")

if st.button("Calculate Attendance"):

    if roll_search.strip() == "":
        st.warning("Please enter a Roll Number.")

    else:

        total = 0
        present = 0
        student_name = ""

        for record in st.session_state.attendance:

            if record["roll_no"] == roll_search:

                total += 1
                student_name = record["name"]

                if record["status"] == "Present":
                    present += 1

        if total == 0:

            st.warning("No attendance records found.")

        else:

            absent = total - present
            percentage = (present / total) * 100

            st.write("### Student:", student_name)
            st.write("**Total Classes:**", total)
            st.write("**Present:**", present)
            st.write("**Absent:**", absent)
            st.write("**Attendance Percentage:**", round(percentage, 2), "%")

            if percentage < 75:
                st.warning("Attendance is below 75%.")

            else:
                st.success("Attendance is 75% or above.")


# ---------------- DELETE RECORD ----------------

st.header("🗑️ Delete Attendance")

delete_roll = st.text_input("Enter Roll Number to delete")

if st.button("Delete Attendance"):

    if delete_roll.strip() == "":
        st.warning("Please enter Roll Number.")

    else:

        old_count = len(st.session_state.attendance)

        st.session_state.attendance = [
            record
            for record in st.session_state.attendance
            if record["roll_no"] != delete_roll
        ]

        new_count = len(st.session_state.attendance)

        if old_count == new_count:
            st.warning("No record found.")

        else:
            save_data(st.session_state.attendance)
            st.success("Attendance records deleted successfully.")

