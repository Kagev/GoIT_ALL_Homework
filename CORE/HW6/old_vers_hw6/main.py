import sqlite3
from generation_data import (
    data_groups_table,
    data_teacher_table,
    data_subjects_table,
    data_students_table,
    data_grade_table,
)
from main_menu import main_menu




def create_db():
    # CONNECT DB
    connection_db = sqlite3.connect("mydatabase.db")
    cursor = connection_db.cursor()

    # CREATE STUDENTS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            student_age INTEGER CHECK (student_age >= 18 AND student_age <= 90),
            student_bday DATE,
            student_email TEXT,
            student_phonenumber TEXT,
            group_id INTEGER NOT NULL,
            student_course INTEGER NOT NULL,
            FOREIGN KEY (group_id) REFERENCES groups(group_id)
        )
    ''')

    # CREATE GROUPS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            group_id INTEGER PRIMARY KEY,
            group_number TEXT NOT NULL,
            group_degree TEXT NOT NULL,
            group_point TEXT NOT NULL
        )
    ''')

    # CREATE TEACHER TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            teacher_id INTEGER PRIMARY KEY,
            teacher_first_name TEXT NOT NULL,
            teacher_last_name TEXT NOT NULL,
            teacher_incumbency TEXT NOT NULL,
            teacher_degree TEXT
        )
    ''')

    # CREATE SUBJECT TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            subject_id INTEGER PRIMARY KEY,
            subject_name TEXT NOT NULL,
            teacher_id INTEGER NOT NULL,
            FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
        )
    ''')

    # CREATE RATING TABLE
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS grades (
                grade_id INTEGER PRIMARY KEY,
                student_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                grade INTEGER NOT NULL,
                grade_ECTS TEXT NOT NULL,
                ects_points INTEGER NOT NULL,
                old_system_grade TEXT NOT NULL, 
                date_received DATE NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
            )
        ''')
    # SAVE AND CLOSING

    connection_db.commit()
    cursor.close()
    connection_db.close()

# FUNCTION TO ADD DATA TO DB
def add_data_to_db():
    connection_db = sqlite3.connect("mydatabase.db")
    cursor = connection_db.cursor()
    # CREATE DB
    create_db()

    # ADD DATA TO DB
    data_groups_table(cursor)
    data_teacher_table(cursor)
    data_subjects_table(cursor)
    data_students_table(cursor)
    data_grade_table(cursor)

    # CLOSE CURSOR AND CONNECTION
    connection_db.commit()
    cursor.close()
    connection_db.close()


if __name__ == "__main__":
    add_data_to_db()
    main_menu()
