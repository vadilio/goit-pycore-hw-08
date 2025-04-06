from address_book.Models import Record, Birthday
from address_book.Addressbook import AddressBook
from Validators.validators import input_error
from tests.test import generate_employees
import pickle
import sys
from tui.interface import ContactBookApp


def parse_input(user_input):
    if user_input:
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, *args
    return ""


# add [ім'я] [телефон]: Додати або новий контакт з іменем та телефонним
# номером, або телефонний номер к контакту який вже існує.
@input_error
def add_contact(args, book: AddressBook):
    name, phone, birthday, *_ = (args + [None, None])[:4]
    record = book.find(name)
    message = "Contact updated.\n"
    if record is None:
        record = Record(name, phone, birthday)
        book.add_record(record)
        message = "Contact added.\n"
        return message
    if phone:
        record.add_phone(phone)
    if birthday:
        record.add_birthday(birthday)
    return message


# change [ім'я] [старий телефон] [новий телефон]:
# Змінити телефонний номер для вказаного контакту.
@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    message = 'Contact not found.\n'
    if record:
        record.edit_phone(old_phone, new_phone)
        message = "Contact updated.\n"
    return message


def del_contact(args, book: AddressBook):
    name,  *_ = args
    record = book.find(name)
    message = 'Contact not found.\n'
    if record:
        book.delete(name)
        message = "Contact deleted.\n"
    return message


# all: Показати всі контакти в адресній книзі.
def all(args, book: AddressBook):
    return book


# phone [ім'я]: Показати телефонні номери для вказаного контакту.
@input_error
def show_phone(args, book: AddressBook):
    name, *_ = args
    result = 'Record not found\n'
    record = book.find(name)
    if record:
        return record.get_phones()
    return result


# add-birthday [ім'я] [дата народження]:
# Додати дату народження для вказаного контакту.
@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    message = 'Record not found\n'
    if record:
        record.add_birthday(Birthday(birthday))
        message = "Birthday added.\n"
    return message


# vshow-birthday [ім'я]: Показати дату народження
# для вказаного контакту.
@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    message = 'Record not found\n'
    if record:
        message = f'{record.get_birthday()}\n'
    return message


# birthdays: Показати дні народження,
# які відбудуться протягом наступного тижня.
def birthdays(book: AddressBook):
    return book.get_upcoming_birthdays()  # Addressbook.py


# Сбереження книги у файл
def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        print('Файл не знайдено або помилка при завантаженні \n')
        return AddressBook()


def main():
    book = load_data(filename="addressbook.pkl")
    # book = AddressBook()
    print("Welcome to the assistant bot!")
    menu_str = ("""
Hello - Привитання,
Exit or close - Для виходу,
All - Отримати список контактів,
Add [Name] [Phone] - Додати контакт,
Del [Name] - Зидалити запис
Change [Name] [Old_Phone] [New_Phone] - зміна контакту
Phone [Name] - Показати контакт
add-birthday [ім'я] [ДН:DD.MM.YYYY] - Додати ДН для вказаного контакту
show-birthday [ім'я]: Показати ДН для вказаного контакту
birthdays Показати ДН, які відбудуться протягом наступного тижня.
AUTO [кільк контактів] - сгенерувати книгу для тестування
tui - Text User Interface URWID
                    """)
    print(menu_str)
    error_message = f'Невірна команда!\n{menu_str}'
    while True:
        user_input = input("Enter a command: ")
        try:
            command, *args = parse_input(user_input)
        except ValueError:
            print(error_message)
            continue

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book, filename="addressbook.pkl")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "del":
            print(del_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(all(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(book))

        elif command == "auto":
            print(generate_employees(args, book))

        elif command == "tui":
            app = ContactBookApp(book)
            app.run()
        else:
            print("Невірна команда \n")


if __name__ == "__main__":
    main()
