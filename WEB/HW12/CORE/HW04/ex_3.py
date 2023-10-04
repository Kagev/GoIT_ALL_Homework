# Реалізувати рекурсивний прохід по дереву дирекорій.
# І потрібно вивести всі папки і файли які зберігаються в середині
# Назва папки задається як параметр через командний рядок

import sys
from pathlib import Path

path = Path(sys.argv[1])  # sys.argv[1] == test


# def parse_folder(path):
#     for element in path.iterdir():
#         if element.is_dir():
#             print(f'parse_folder: This is folder - {element.name}')
#         else:
#             print(f'parse_folder: This is file - {element.name}')

# parse_folder: This is folder - usr
# parse_folder: This is file - 3.svg


def parse_folder_recursion(path):
    for element in path.iterdir():
        if element.is_dir():
            print(f'parse_folder: This is folder - {element.name}')
            parse_folder_recursion(element)  # рекурсія
        else:
            print(f'parse_folder: This is file - {element.name}')


if __name__ == "__main__":
    parse_folder_recursion(path)
