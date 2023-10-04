"""
Файл генерации фейковых данных
"""
from database.db import Base, session_db
from sqlalchemy import func, text
import random
from faker import Faker
from database.models import Group, Subject, Teacher, Student
from seed.data_for_create_db import (
    courses_degree_data,
    courses_point_data,
    teacher_incumbency_data,
    teacher_degree_data,
)

# Устанавливаем новые параметры
groups_number = 3
subjects_number = 8
teachers_number = 5
students_number = 50
grades_number_min = 1
grades_number_max = 20

fake = Faker("uk-UA")


def generate_fake_data():
    session = session_db()

    # для групп
    for _ in range(groups_number):
        group_number = random.randint(1, groups_number)

        n_degree = random.randint(1, 3)
        group_degree = courses_degree_data[n_degree]

        if group_degree == courses_degree_data[3]:  # Аспирантура
            group_course = random.randint(1, 4)
            group_point = courses_point_data[group_course]
        elif group_degree == courses_degree_data[2]:  # Магистратура
            group_course = random.randint(1, 2)
            group_point = courses_point_data[group_course]
        else:  # Бакалавр
            group_degree == courses_degree_data[1]
            group_course = random.randint(1, 5)
            group_point = courses_point_data[group_course]

        session.add(
            Group(
                group_number=group_number,
                group_point=group_point,
                group_degree=group_degree,
            )
        )

    session.commit()

    # Преподы
    for _ in range(teachers_number):
        teacher_first_name = fake.first_name()
        teacher_last_name = fake.last_name()

        n_incumbency = random.randint(1, 5)
        teacher_incumbency = teacher_incumbency_data[n_incumbency]

        n_degree = random.randint(1, 2)
        teacher_degree = teacher_degree_data[n_degree]

        session.add(
            Teacher(
                teacher_first_name=teacher_first_name,
                teacher_last_name=teacher_last_name,
                teacher_incumbency=teacher_incumbency,
                teacher_degree=teacher_degree,
            )
        )

    session.commit()

    # Предметы
    for _ in range(subjects_number):
        subject_name = fake.catch_phrase()
        teacher = session.query(Teacher).order_by(func.random()).first()
        if not teacher:
            teacher = Teacher(
                teacher_first_name=fake.first_name(),
                teacher_last_name=fake.last_name(),
                teacher_incumbency=random.choice(teacher_incumbency_data),
                teacher_degree=random.choice(teacher_degree_data),
            )
            session.add(teacher)
            session.commit()

        subject = Subject(subject_name=subject_name, teacher_id=teacher.id)
        session.add(subject)

    session.commit()

    # Студенты
    for _ in range(students_number):
        first_name = fake.first_name()
        last_name = fake.last_name()
        student_age = random.randint(18, 45)
        student_bday = fake.date_between(start_date="-45y", end_date="-18y")
        student_email = fake.email()
        student_phonenumber = fake.phone_number()

        # Выбор рандомно групы
        group = session.query(Group).order_by(func.random()).first()
        if not group:
            # Если группы нет, создадим её и выполним коммит
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
                group_course = random.randint(1, 5)
                group_point = courses_point_data[group_course]

            group = Group(
                group_number=group_number,
                group_point=group_point,
                group_degree=group_degree,
            )
            session.add(group)
            session.commit()

        group_id = group.group_id
        student_course = group.group_degree

        student = Student(
            student_first_name=first_name,
            student_last_name=last_name,
            student_age=student_age,
            student_birthday=student_bday,
            student_email=student_email,
            student_phone_number=student_phonenumber,
            group_id=group_id,
            student_course=student_course,
        )
        session.add(student)

    session.commit()


    # оценки
    for student_id in range(1, students_number + 1):  # Increment students_number to include the last student
        for subject_id in range(1, subjects_number + 1):  # Increment subjects_number to include the last subject
            num_grade = random.randint(grades_number_min, grades_number_max)
            for _ in range(num_grade):
                grade = random.randint(0, 200)
                date_received = fake.date_between(start_date="-1y", end_date="today")

                # Дополнительно определить значения для оценок ECTS, баллов и столбцов оценок старой системы.
                if grade >= 180:
                    grade_ects = "A"
                    ects_points = random.randint(180, 200)
                    old_system_grade = "відмінно"
                elif grade >= 160:
                    grade_ects = "B"
                    ects_points = random.randint(160, 179)
                    old_system_grade = "добре"
                elif grade >= 140:
                    grade_ects = "C"
                    ects_points = random.randint(140, 159)
                    old_system_grade = "добре"
                elif grade >= 120:
                    grade_ects = "D"
                    ects_points = random.randint(120, 139)
                    old_system_grade = "задовільно"
                elif grade >= 100:
                    grade_ects = "E"
                    ects_points = random.randint(100, 119)
                    old_system_grade = "задовільно"
                elif grade >= 0:
                    grade_ects = "FX"
                    ects_points = random.randint(100, 119)
                    old_system_grade = "незадовільно"

                session.execute(
                    text(
                        "INSERT INTO grades (student_id, subject_id, grade, grade_ects, ects_points, old_system_grade, "
                        "date_received) VALUES (:student_id, :subject_id, :grade, :grade_ects, :ects_points, "
                        ":old_system_grade, :date_received)"
                    ),
                    {
                        "student_id": student_id,
                        "subject_id": subject_id,
                        "grade": grade,
                        "grade_ects": grade_ects,
                        "ects_points": ects_points,
                        "old_system_grade": old_system_grade,
                        "date_received": date_received,
                    },
                )

    session.commit()
    session.close()

if __name__ == "__main__":
    generate_fake_data()
