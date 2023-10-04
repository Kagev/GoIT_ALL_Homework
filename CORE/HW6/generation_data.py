"""
Фаил генерации фейковых данных
"""

import sqlite3
from faker import Faker
import random
from datetime import datetime, timedelta
from data_for_create_db import (
    groups_number,
    courses_degree_data,
    courses_point_data,
    teachers_number,
    teacher_incumbency_data,
    teacher_degree_data,
    subjects_number,
    students_number,
    grades_number_min,
    grades_number_max,
)

fake = Faker("uk-UA")

connection_db = sqlite3.connect("mydatabase.db")
cursor = connection_db.cursor()


# data for groups
def data_groups_table(cursor):
    for _ in range(groups_number):
        group_number = random.randint(1, groups_number)

        n_degree = random.randint(1, 3)
        group_degree = courses_degree_data[n_degree]

        if group_degree == courses_degree_data[2]:  # Магистратура
            group_course = random.randint(1, 2)
            group_point = courses_point_data[group_course]
        elif group_degree == courses_degree_data[3]:  # Аспирантура
            group_course = random.randint(1, 4)
            group_point = courses_point_data[group_course]
        else:  # Бакалавр
            n_point = random.randint(1, 5)
            group_point = courses_point_data[n_point]
            group_course = n_point

        cursor.execute(
            "INSERT INTO groups (group_number, group_point, group_degree) VALUES (?,?,?)",
            (
                group_number,
                group_point,
                group_degree,
            ),
        )


# Generation data for teacher table
def data_teacher_table(cursor):
    for _ in range(teachers_number):
        teacher_first_name = fake.first_name()
        teacher_last_name = fake.last_name()

        n_incumbency = random.randint(1, 5)
        teacher_incumbency = teacher_incumbency_data[n_incumbency]

        n_degree = random.randint(1, 2)
        teacher_degree = teacher_degree_data[n_degree]

        cursor.execute(
            "INSERT INTO teachers (teacher_first_name, teacher_last_name, teacher_incumbency, teacher_degree) "
            "VALUES (?,?,?,?)",
            (
                teacher_first_name,
                teacher_last_name,
                teacher_incumbency,
                teacher_degree,
            ),
        )


# Generation data for subjects table
def data_subjects_table(cursor):
    for _ in range(subjects_number):
        subject_name = fake.catch_phrase()
        teacher_id = random.randint(1, teachers_number)
        cursor.execute(
            "INSERT INTO subjects (subject_name, teacher_id) VALUES (?, ?)",
            (subject_name, teacher_id),
        )


# Generation data for student table
def data_students_table(cursor):
    for _ in range(50):
        first_name = fake.first_name()
        last_name = fake.last_name()
        student_age = random.randint(18, 45)
        student_bday = fake.date_between(start_date="-45y", end_date="-18y")
        student_email = fake.email()
        student_phonenumber = fake.phone_number()
        group_id = random.randint(1, groups_number)

        # Get the corresponding course for the group and use it as student_course
        cursor.execute(
            "SELECT group_degree FROM groups WHERE group_id = ?", (group_id,)
        )
        group_degree_result = cursor.fetchone()
        if group_degree_result:
            group_degree = group_degree_result[0]
        else:
            # If no corresponding group is found, set the group_degree to an appropriate default value
            group_degree = "Абітурієнт"  # Or any other default value you want to use

        cursor.execute(
            "INSERT INTO students (first_name, last_name, student_age, student_bday, student_email, "
            "student_phonenumber,"
            "group_id, student_course) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                first_name,
                last_name,
                student_age,
                student_bday,
                student_email,
                student_phonenumber,
                group_id,
                group_degree,
            ),
        )


# Generation data for grades table
def data_grade_table(cursor):
    for student_id in range(1, students_number):
        for subject_id in range(1, subjects_number):
            num_grade = random.randint(grades_number_min, grades_number_max)
            for _ in range(num_grade):
                grade = random.randint(0, 200)
                date_received = fake.date_between(start_date="-1y", end_date="today")

                # Дополнительно, определите значения для колонок с оценками по ECTS, баллами и старой системой
                if grade >= 180:
                    grade_ECTS = "A"
                    ects_points = random.randint(180, 200)
                    old_system_grade = "відмінно"
                elif grade >= 160:
                    grade_ECTS = "B"
                    ects_points = random.randint(160, 179)
                    old_system_grade = "добре"
                elif grade >= 140:
                    grade_ECTS = "C"
                    ects_points = random.randint(140, 159)
                    old_system_grade = "добре"
                elif grade >= 120:
                    grade_ECTS = "D"
                    ects_points = random.randint(120, 139)
                    old_system_grade = "задовільно"
                elif grade >= 100:
                    grade_ECTS = "E"
                    ects_points = random.randint(100, 119)
                    old_system_grade = "задовільно"
                elif grade >= 0:
                    grade_ECTS = "FX"
                    ects_points = random.randint(100, 119)
                    old_system_grade = "незадовільно"

                cursor.execute(
                    "INSERT INTO grades (student_id, subject_id, grade, grade_ECTS, ects_points, old_system_grade, "
                    "date_received) VALUES(?, ?, ?, ?, ?, ?, ?)",
                    (
                        student_id,
                        subject_id,
                        grade,
                        grade_ECTS,
                        ects_points,
                        old_system_grade,
                        date_received,
                    ),
                )


if __name__ == "__main__":
    connection_db = sqlite3.connect("mydatabase.db")
    cursor = connection_db.cursor()

    data_students_table(cursor)
    data_grade_table(cursor)
    data_subjects_table(cursor)
    data_teacher_table(cursor)
    data_groups_table(cursor)

    connection_db.commit()
    cursor.close()
    connection_db.close()
