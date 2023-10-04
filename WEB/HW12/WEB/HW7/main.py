import colorama
from database.db import session_db as session_db, Base
from colorama import init, Fore, Style
from database import models
import subprocess
from scripts.test_connect_db import test_connection
from seed.generation_data import generate_fake_data
from scripts.my_selec import (
    select_1,
    select_2,
    select_3,
    select_4,
    select_5,
    select_6,
    select_7,
    select_8,
    select_9,
    select_10,
)
# from scripts.search_queries import (
#     search_top_rang_student,
#     search_middle_rang_student,
#     search_teacher_course,
#     students_group_list,
#     students_group_grades,
# )

colorama.init()

def main_menu():
    # session = session()
    while True:
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "Меню:" + Style.RESET_ALL)
        print(Fore.LIGHTCYAN_EX + "1. Перевірити з'єднання з DB")
        print("2. Створити таблиці в DB")
        print("3. Заповнити базу (Faker)")
        print("4. Меню пошуку по DB")
        print("5. Створення міграції (alembic)")
        print("0. Вихід" + Style.RESET_ALL)

        choice = input(Fore.RED + "Виберіть опцію: " + Style.RESET_ALL).lower()

        if choice == "1":
            test_connection()
        elif choice == "2":
            session = session_db()
            Base.metadata.create_all(session.bind)
            session.commit()
            session.close()
        elif choice == "5":
            generate_fake_data()
        elif choice == "3":
            search_menu()
        elif choice == "4":
            revision_name = input(Fore.YELLOW + "Назва міграції: " + Style.RESET_ALL)
            subprocess.run(["alembic", "revision", "--autogenerate", "-m", revision_name])
        elif choice == "0":
            print(Fore.BLUE + "Good luck")

            break
        else:
            print(Fore.YELLOW + "Невірний вибір. Спробуйте ще раз." + Style.RESET_ALL)


def search_menu():
    db_session = session_db()
    while True:
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "Меню:" + Style.RESET_ALL)
        print(Fore.LIGHTCYAN_EX + "1. Знайти 5 студентов з найбільшим середнім балом по всім предметам.")
        print("2. Знайти студента з найвишим середнім балом по вказаному предмету.")
        print("3. Знайти середній бал у групі по вказаному предмету.")
        print("4. Знайти середній бал на потоці(по усій таблиці оцінок).")
        print("5. Знайти які курси читає вказаний викладач.")
        print("6. Знайти список студентів вказаной групі.")
        print("7. Знайти оцінки студентів вказаной групі по вказаному предмету.")
        print("8. Знайти середній бал, який ставить конкретний викладач по своїм предметам.")
        print("9. Знайти список курсів, які відвідували конкретні студенти.")
        print("10. Список курсів, як конкретному студенту читає конкретний викладач.")
        print("0. Вихід" + Style.RESET_ALL)

        choice = input(Fore.RED + "Виберіть опцію: " + Style.RESET_ALL)

        if choice == "1":
            search_1_result = select_1(db_session)
            print("Результат пошуку:")
            for student, avg_grade in search_1_result:
                print(f"{student}: {avg_grade}")

        elif choice == "2":
            subject_id = input("Введіть ID предмету: ")
            search_2_result = select_2(db_session, subject_id)
            if search_2_result:
                print(f"Студент з найвишим середнім балом по предмету {subject_id}:")
                print(f"{search_2_result[0]}: {search_2_result[1]}")
            else:
                print("Студент з таким предметом не знайден.")

        elif choice == "3":
            subject_id = input("Введіть ID предмету: ")
            search_3_result = select_3(db_session, subject_id)
            if search_3_result:
                print(f"Середній бал в групі по предмету {subject_id}:")
                for group, avg_grade in search_3_result:
                    print(f"{group}: {avg_grade}")
            else:
                print("Данні не знайдені.")

        elif choice == "4":
            search_4_result = select_4(db_session)
            print(f"Середній бал на потоці: {search_4_result}")

        elif choice == "5":
            teacher_id = input("Введіть ID викладача: ")
            search_5_result = select_5(db_session, teacher_id)
            if search_5_result:
                print(f"Курси, які читає викладач {teacher_id}:")
                for subject in search_5_result:
                    print(subject.subject_name)
            else:
                print("Викладач з таким ID не знайден.")

        elif choice == "6":
            group_id = input("Введіть ID группы: ")
            search_6_result = select_6(db_session, group_id)
            if search_6_result:
                print(f"Студент в групі {group_id}:")
                for student in search_6_result:
                    print(student.fullname)
            else:
                print("Групі з таким ID не знайдена.")

        elif choice == "7":
            group_id = input("Введіть ID группы: ")
            subject_id = input("Введіть ID предмету: ")
            search_7_result = select_7(db_session, group_id, subject_id)
            if search_7_result:
                print(f"Оцінка студентів в групі {group_id} по предмету {subject_id}:")
                for student, grade, date_received in search_7_result:
                    print(f"{student}, оцінка: {grade}, дата: {date_received}")
            else:
                print("Данні не знайдено.")

        elif choice == "8":
            teacher_id = input("Введіть ID викладача: ")
            search_8_result = select_8(db_session, teacher_id)
            print(f"Середній балл по викладачу {teacher_id}: {search_8_result}")

        elif choice == "9":
            student_id = input("Введіть ID студента: ")
            search_9_result = select_9(db_session, student_id)
            if search_9_result:
                print(f"Курси, які відвідувал студент {student_id}:")
                for subject in search_9_result:
                    print(subject.subject_name)
            else:
                print("Студент з таким ID не знайден.")

        elif choice == "10":
            student_id = input("Введіть ID студента: ")
            teacher_id = input("Введіть ID викладача: ")
            search_10_result = select_10(db_session, student_id, teacher_id)
            if search_10_result:
                print(f"Курси, які читає викладач {teacher_id} студенту {student_id}:")
                for subject in search_10_result:
                    print(subject.subject_name)
            else:
                print("Данні не знайдены.")

        elif choice == "0":
            db_session.close()
            break
        else:
            print("Невірний вибір. Введіть число зі списку опцій.")



if __name__ == "__main__":
    main_menu()
