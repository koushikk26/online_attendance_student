from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "attendance123"

DATABASE = "attendance.db"


# =====================================================
# STUDENTS
# =====================================================

STUDENTS = {
    "student1": "Karthik",
    "student2": "Ravi",
    "student3": "Keerthan",
    "student4": "Sunil",
    "student5": "Koushik"
}


# =====================================================
# DATABASE
# =====================================================

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_database():

    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student TEXT NOT NULL,
            subject TEXT NOT NULL,
            class_number INTEGER NOT NULL,
            status TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


create_database()


# =====================================================
# LOGIN
# =====================================================

@app.route("/", methods=["GET", "POST"])
def login():

    error = ""

    if request.method == "POST":

        username = request.form["username"].strip()
        password = request.form["password"].strip()

        # Faculty login
        if username == "faculty1" and password == "1234":

            session.clear()
            session["role"] = "faculty"

            return redirect("/faculty")

        # Student login
        elif username in STUDENTS and password == "1234":

            session.clear()

            session["role"] = "student"
            session["username"] = username
            session["student_name"] = STUDENTS[username]

            return redirect("/student")

        else:

            error = "Invalid username or password!"

    return render_template(
        "index.html",
        page="login",
        error=error
    )


# =====================================================
# FACULTY DASHBOARD
# =====================================================

@app.route("/faculty", methods=["GET", "POST"])
def faculty():

    if session.get("role") != "faculty":
        return redirect("/")

    message = ""
    error = ""

    if request.method == "POST":

        student = request.form["student"].strip()
        subject = request.form["subject"].strip()
        class_number = request.form["class_number"].strip()
        status = request.form["status"]

        # Check student
        if student not in STUDENTS.values():

            error = "Please select a valid student."

        else:

            conn = get_db()

            # Check duplicate
            existing = conn.execute("""
                SELECT *
                FROM attendance
                WHERE student = ?
                AND subject = ?
                AND class_number = ?
            """, (
                student,
                subject,
                class_number
            )).fetchone()

            if existing:

                error = (
                    "Attendance already recorded for "
                    + student
                    + " - Class "
                    + class_number
                )

            else:

                conn.execute("""
                    INSERT INTO attendance
                    (
                        student,
                        subject,
                        class_number,
                        status
                    )
                    VALUES (?, ?, ?, ?)
                """, (
                    student,
                    subject,
                    class_number,
                    status
                ))

                conn.commit()

                message = (
                    "Attendance saved successfully!"
                )

            conn.close()

    # Get all records
    conn = get_db()

    records = conn.execute("""
        SELECT *
        FROM attendance
        ORDER BY class_number, student
    """).fetchall()

    conn.close()

    return render_template(
        "index.html",
        page="faculty",
        records=records,
        message=message,
        error=error,
        students=list(STUDENTS.values())
    )


# =====================================================
# STUDENT DASHBOARD
# =====================================================

@app.route("/student")
def student():

    if session.get("role") != "student":
        return redirect("/")

    student_name = session.get("student_name")

    if not student_name:
        return redirect("/")

    conn = get_db()

    records = conn.execute("""
        SELECT *
        FROM attendance
        WHERE LOWER(student) = LOWER(?)
        ORDER BY class_number
    """, (student_name,)).fetchall()

    conn.close()

    # Total
    total = len(records)

    # Present
    present = sum(
        1 for record in records
        if record["status"] == "Present"
    )

    # Absent
    absent = sum(
        1 for record in records
        if record["status"] == "Absent"
    )

    # Subjects
    if records:

        subjects = list(
            dict.fromkeys(
                record["subject"]
                for record in records
            )
        )

        subject = ", ".join(subjects)

    else:

        subject = "No subject"

    # Percentage
    if total > 0:

        percentage = round(
            (present / total) * 100,
            2
        )

    else:

        percentage = 0

    return render_template(
        "index.html",
        page="student",
        student_name=student_name,
        subject=subject,
        records=records,
        total=total,
        present=present,
        absent=absent,
        percentage=percentage
    )


# =====================================================
# LOGOUT
# =====================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# =====================================================
# RUN
# =====================================================

if __name__ == "__main__":

    app.run(debug=True)