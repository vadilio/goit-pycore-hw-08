import re
from datetime import datetime
from Validators.validators import input_error, PhoneValidationError, BirthdayValidationError


# Field: Базовий клас для полів запису.
class Field():
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


# Name: Клас для зберігання імені контакту. Обов'язкове поле.
class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name field cannot be empty")
        self.value = str(value).capitalize()
        super().__init__(self.value)


# Phone: Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
class Phone(Field):
    def __init__(self, value):
        if not re.fullmatch(r'\d{10}', value):
            raise PhoneValidationError(
                f'Невірний номер: {value} (має бути 10 цифр)')
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        birthday = ''
        try:
            birthday = (datetime.strptime(
                value, "%d.%m.%Y").date().strftime("%d.%m.%Y"))
        except ValueError:
            raise BirthdayValidationError(
                f"{value}: Invalid date format. Use DD.MM.YYYY")
        self.value = birthday

    def __str__(self):
        return str(self.value)


# Record: Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
# - Додавання телефонів.
# - Видалення телефонів.
# - Редагування телефонів.
# - Пошук телефону.
class Record():
    def __init__(self, name, phone=None, birthday=None, email=None, address=None, notes=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = birthday
        self.email = email
        self.address = address
        self.notes = notes
        if phone:
            self.add_phone(phone)
        if birthday:
            self.add_birthday(birthday)

    def __str__(self):
        return f"{self.name.value:<12} | {self.get_phones():<44} | {str(self.birthday):<10} |"

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = Phone(new_phone).value
                return
        raise ValueError("Phone number not found")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    # get_phones - Вивод всі номера телефонів для record
    def get_phones(self):
        return str('; '.join(p.value for p in self.phones))

    def get_name(self) -> str:
        return self.name.value

    def get_birthday(self) -> str:
        return str(self.birthday)

    def get_email(self) -> str:
        return str(self.email)

    def get_address(self) -> str:
        return str(self.address)

    def get_notes(self) -> str:
        return str(self.notes)

    # add_birthday - додає день народження до контакту.

    def add_birthday(self, birthday: Birthday):
        self.birthday = Birthday(birthday)
