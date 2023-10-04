import sys
from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value=None):
        self.value = value

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value!r})'

    def __str__(self) -> str:
        return f'{self.value}'


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value=None):
        super().__init__(value)
        self.value = self._validate(value)
    
    def _validate (self, value):
        if not isinstance(value, str):
            raise ValueError(f'Phone bumber must be a string, not {type(value)}')
        value = value.strip()
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain exactly 10 digits")
        return value
    
    def __repr__(self):
        return f'{self.__class__.__name__} ({self.value!r})'

class Brirthday(Field):
    def __init__(self, value=None):
        super().__init__()
        self.value = self._validate(value)

    def _validate(self, value):
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError(f'Birthday must be a string in the format "DD-MM-YYYY", not {type(value)}')
        try:
            value = datetime.strptime(value, "%d-%m-%Y").date()
        except ValueError:
            raise ValueError(f"Birthday must be in the format 'DD-MM-YYYY'")
        today = datetime.now().date()
        if value.replace(year=today.year) < today:
            value = value.replace(year=today.year + 1)
        return value
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.value!r})'


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.add_phone(phone)
        self.birthday = Brirthday(birthday)

    def add_phone(self, phone):
        if phone is not None:
            p = Phone(phone)
            self.phones.append(p)

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone.value:
                self.phones.remove(p)
                return

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone.value:
                p.value = new_phone
                return

    def __repr__(self):
        return f'{self.__class__.__name__}(name={self.name!r}, phones={self.phones!r})'

    def days_to_birthday(self):
        if not self.birthday.value:
            return None
        today = datetime.now().date()
        next_birthday = self.birthday.value.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        return (next_birthday - today).days


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record
    
    def get_record(self, name):
        return self.data[name]
    
    def iterator(self, n=1):
        record = list(self.data.values())
        for i in range(0, len(record), n):
            yield record[i:i+n]


# Создаем записи
record1 = Record(Name('John Doe'))
record1.add_phone(Phone('+123456789'))
record1.add_phone(Phone('+987654321'))

record2 = Record(Name('Jane Smith'))
record2.add_phone(Phone('+111111111'))
record2.add_phone(Phone('+222222222'))

# Создаем книгу
book = AddressBook()
book.add_record(record1)
book.add_record(record2)

# Получаем запись из книги
record = book.get_record('John Doe')

# Редактируем телефон
record.edit_phone(Phone('+123456789'), Phone('+999999999'))

# Выводим записи из книги
for record in book.data.values():
    print(record)
