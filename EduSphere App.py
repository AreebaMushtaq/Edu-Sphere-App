import streamlit as st

st.title("EduSphere Smart Portal")

# User Authentication
users = {
    "Admin": "12345",
    "Teacher": "teach123",
    "Student": "std123"
}

u = st.text_input("Enter Username: ")
p = st.text_input("Enter Password: ", type="password")

# Student Classes
class Person:
    def __init__(self, name, id):
        self.n = name
        self.id = id

class Student(Person):
    def __init__(self, name, id):
        super().__init__(name, id)
        self.__gpa = 0
        self.c = []

    def set_gpa(self, gpa):
        self.__gpa = gpa

    def show_gpa(self):
        return self.__gpa

    def add_course(self, course):
        self.c.append(course)

class Course:
    def __init__(self, course_name):
        self.course_name = course_name

class StemCourses(Course):
    def __init__(self, course_name):
        super().__init__(course_name)

py_course = StemCourses("Python Programming")
cyber_course = StemCourses("Cyber Security")
math_course = StemCourses("Mathematics")

courses = {
    "Python": py_course,
    "Cyber Security": cyber_course,
    "Maths": math_course
}

# Mini database
if "student_db" not in st.session_state:
    st.session_state.student_db = {}

# Grade Calculator
def grades(score):
    match score:
        case s if s >= 90:
            return "A+"
        case s if s >= 85:
            return "A"
        case s if s >= 70:
            return "B"
        case s if s >= 50:
            return "C"
        case _:
            return "Fail"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Login button
if st.button("Login"):
    if u in users and users[u] == p:
        st.session_state.logged_in = True
        st.success("Login Successful!")
    else:
        st.error("Access Denied")

# Show menu only if logged in
if st.session_state.logged_in:
    menu = st.sidebar.selectbox(
        "Navigation",
        ["Add Student", "Register Course", "View Students", "Calculate Grade"]
    )

    match menu:
        case "Add Student":
            st.header("Add Student")
            name = st.text_input("Student Name")
            stid = st.text_input("Student ID")
            if st.button("Add Student"):
                student = Student(name, stid)
                st.session_state.student_db[stid] = student
                st.success("Student Added")

        case "Register Course":
            st.header("Register Course")
            stid = st.text_input("Student ID")
            course_name = st.selectbox("Select Course", ["Python", "Cyber Security", "Maths"])
            if st.button("Register"):
                if stid in st.session_state.student_db:
                    st.session_state.student_db[stid].add_course(courses[course_name])
                    st.success("Course Registered")
                else:
                    st.error("Student not found")

        case "View Students":
            st.header("Student Records")
            for stid, student in st.session_state.student_db.items():
                st.write("Name:", student.n)
                st.write("ID:", student.id)
                st.write("Courses:")
                for c in student.c:
                    st.write("-", c.course_name)
                st.write("GPA:", student.show_gpa())
                st.write("----------------")

        case "Calculate Grade":
            st.header("Grade Calculator")
            stid = st.text_input("Student ID")
            score = st.number_input("Score", 0, 100)
            if st.button("Calculate"):
                grade = grades(score)
                if stid in st.session_state.student_db:
                    st.session_state.student_db[stid].set_gpa(score)
                    st.write("Grade:", grade)
                else:
                    st.error("Student not found")
