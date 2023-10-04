import sys
from collections import UserDict

class Field:
    def __init__(self, value=None):
        self.value = value

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value!r})'


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return

    def __repr__(self):
        return f'{self.__class__.__name__}(name={self.name!r}, phones={self.phones!r})'

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record


# book = AddressBook()

