import sqlite3
from database.db import session_db
from faker import Faker
import random
from datetime import datetime, timedelta
ser
# 1
"""TOP MIDDLE RANG ON A SPECIFIC SUBJECT"""


def search_top_rang_student(subject_id):
    # CONNECT DB
    session = session_db()

    # SQL REQUEST
    sql_query = """
            SELECT students.first_name, students.last_name, AVG(grades.grade) as average_grade
            FROM students
            INNER JOIN grades ON students.student_id = grades.student_id
            WHERE grades.subject_id = ?
            GROUP BY students.student_id
            ORDER BY average_grade DESC
            LIMIT 1
        """

    # REQUEST WITH PARAM
    session.execute(sql_query, (subject_id,))
    top_rang_student = session.fetchone()

    # RESULT
    if top_rang_student:
        first_name, last_name, average_grade = top_rang_student
        print("\n" + "*" * 10)
        print(f"Студент з найвищим середнім балом на предметі:")
        print(f"Ім'я: {first_name}, Прізвище: {last_name}, Середній бал: {average_grade:.2f}")
        print("*" * 10 + "\n")
    else:
        print("Студентів з оцінками на даному предметі не знайдено.")

    # CLOSE CONNECT DB
    connection_db.close()


# 2
""" """


def search_middle_rang_student():
    # CONNECT DB
    connection_db = sqlite3.connect("mydatabase.db")
    session = connection_db.session()

    # SQL REQUEST
    sql_query = """
            SELECT students.first_name, students.last_name, AVG(grades.grade) as average_grade
            FROM students
            INNER JOIN grades ON students.student_id = grades.student_id
            GROUP BY students.student_id
            ORDER BY average_grade DESC
        """

    # REQUEST
    session.execute(sql_query)
    middle_rang_student = session.fetchall()

    # RESULT
    if middle_rang_student:
        print("\n" + "*" * 10)
        print("Середній бал для кожного студента:")
        for student in middle_rang_student:
            first_name, last_name, average_grade = student
            print(f"Ім'я: {first_name}, Прізвище: {last_name}, Середній бал: {average_grade:.2f}")
            print("*" * 10 + "\n")
    else:
        print("Студентів з оцінками не знайдено.")
    # CLOSE CONNECT DB
    connection_db.close()


# 3
""" """


def search_teacher_course(subject_id):
    # CONNECT DB
    connection_db = sqlite3.connect("mydatabase.db")
    session = connection_db.session()

    # SQL REQUEST
    sql_query = '''
        SELECT teachers.teacher_first_name, teachers.teacher_last_name, subjects.subject_name
        FROM teachers
        INNER JOIN subjects ON teachers.teacher_id = subjects.teacher_id
        WHERE subjects.subject_id = ?;
    '''

    # REQUEST
    session.execute(sql_query, (subject_id,))
    result = session.fetchone()

    # RESULT
    if result:
        if len(result) == 3:
            teacher_first_name, teacher_last_name, subject_name = result
            print("\n" + "*" * 10)
            print(f"Предмет \033[1m{subject_name}\033[0m викладає викладач:")
            print(f"\033[1;34m{teacher_first_name} {teacher_last_name}\033[0m")
            print("*" * 10 + "\n")
        else:
            print(f"Помилка: Не вдалося знайти інформацію про предмет з ID {subject_id}.")
    else:
        print(f"Предмет з ID {subject_id} не знайдено або викладач для нього не призначений.")

    # CLOSE CONNECT DB
    connection_db.close()




# 4
"""SEARCH TOP STUDENTS"""


def search_students_top_points(limit):
    # CONNECT DB
    connection_db = sqlite3.connect("mydatabase.db")
    session = connection_db.session()

    # SQL request with param LIMIT
    sql_query = '''
        SELECT student_id, AVG(grade) AS average_grade
        FROM grades
        GROUP BY student_id
        ORDER BY average_grade DESC
        LIMIT ?;
    '''

    #
    session.execute(sql_query, (limit,))
    top_students = session.fetchall()

    # Res print
    for student in top_students:
        student_id, average_grade = student
        print("\n" + "*" * 10)
        print(f"Student ID: {student_id}, Средний балл: {average_grade}")
        print("*" * 10 + "\n")

    # TAKE LIMIT FROM USERS
    try:
        limit = int(input("Введите количество студентов для вывода: "))
        search_students_top_points(limit)
    except ValueError:
        print("Ошибка! Введите целое число.")

    # CLOSE CONNECT DB
    connection_db.close()


# 5
""" """


def students_group_list(group_id):
    # CONNECT DB
    connection_db = sqlite3.connect("mydatabase.db")
    session = connection_db.session()
    # SQL REQUEST
    sql_query = '''
            SELECT *
            FROM students
            WHERE group_id = ?;
        '''

    # REQUEST
    session.execute(sql_query, (group_id,))
    students_list = session.fetchall()

    # RESULT
    if students_list:
        for student in students_list:
            student_id, first_name, last_name, student_age, student_bday, student_email, student_phonenumber, group_id, student_course = student
            print("\n" + "*" * 10)
            print(
                f"ID студента: {student_id}, Ім'я студента: {first_name}, Прізвище студента: {last_name}, Вік: {student_age}, "
                f"Дата народження: {student_bday}, Email: {student_email}, Номер телефону: {student_phonenumber}, "
                f"ID групи: {group_id}, Курс студента: {student_course}")
            print("*" * 10 + "\n")
    else:
        print("Студенти у групі не знайдені.")

    # CLOSE CONNECT DB
    connection_db.close()


# 6
""" """


def students_group_grades(group_id, subject_id):
    # CONNECT DB
    connection_db = sqlite3.connect("mydatabase.db")
    session = connection_db.session()

    # SQL REQUEST
    sql_query = """SELECT students.first_name, students.last_name, grades.grade, grades.grade_ECTS, 
    grades.ects_points, grades.old_system_grade, grades.date_received FROM students INNER JOIN grades ON 
    students.student_id = grades.student_id INNER JOIN subjects ON grades.subject_id = subjects.subject_id WHERE 
    students.group_id = ? AND subjects.subject_id = ?"""

    # REQUEST
    session.execute(sql_query, (group_id, subject_id))
    students_grades = session.fetchall()

    # RESULT
    if students_grades:
        print("\n" + "*" * 15)
        print("Список оцінок студентів у групі за ID групи та ID предмета:")
        print("*" * 15)
        print("{:<15} {:<15} {:<10} {:<10} {:<15} {:<15} {:<15}".format(
            "Ім'я", "Прізвище", "Оцінка", "ECTS", "Бали", "Стара система", "Дата отримання"
        ))
        print("*" * 10 + "\n")
        for student in students_grades:
            first_name, last_name, grade, grade_ECTS, ects_points, old_system_grade, date_received = student
            print("{:<15} {:<15} {:<10} {:<10} {:<15} {:<15} {:<15}".format(
                first_name, last_name, grade, grade_ECTS, ects_points, old_system_grade, date_received
            ))
    else:
        print("Оцінки студентів у групі не знайдені.")

    # CLOSE CONNECT DB
    connection_db.close()
