import sqlite3
from search_queries import (
    search_top_rang_student,
    search_middle_rang_student,
    search_teacher_course,
    students_group_list,
    students_group_grades,
)


def main_menu():
    connection_db = sqlite3.connect("mydatabase.db")
    cursor = connection_db.cursor()
    while True:
        print("\nМеню:")
        print("1. Пошук студента з найвищим середнім балом з конкретного предмета")
        print("2. Пошук середнього балу для кожного студента")
        print("3. Пошук курсів викладача за ID викладача")
        print("4. Список студентів у групі за ID групи")
        print("5. Оцінки студентів у групі за ID групи та ID предмета")
        print("0. Вихід")

        choice = input("Виберіть опцію: ")

        if choice == "1":
            subject_id = input("Введіть ID предмета: ")
            search_top_rang_student(subject_id)
        elif choice == "2":
            search_middle_rang_student()
        elif choice == "3":
            teacher_id = input("Введіть ID викладача: ")
            search_teacher_course(teacher_id)
        elif choice == "4":
            group_id = input("Введіть ID групи: ")
            students_group_list(group_id)
        elif choice == "5":
            group_id = input("Введіть ID групи: ")
            subject_id = input("Введіть ID предмета: ")
            students_group_grades(group_id, subject_id)
        elif choice == "0":
            break
        else:
            print("Невірний вибір. Введіть число зі списку опцій.")
    connection_db.close()


if __name__ == "__main__":
    main_menu()
