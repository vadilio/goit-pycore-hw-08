from collections import UserDict
from address_book.Models import Record
from datetime import datetime, timedelta
import calendar
from typing import Optional


class AddressBook(UserDict):
    def __init__(self):
        self.selected_index = 0  # Индекс текущего выделенного контакта
        super().__init__()  # Это создаст self.data как пустой словарь

    def __str__(self):
        mess: str = 'Address book is empty\n'
        if len(self.data.items()) > 0:
            mess = f"{'Contact name':<10} | {'Phones':<44} | {'Birthday':<10} |\n{'-'*74}\n"
            for item in self.data:
                record = self.data.get(item, None)
                mess = f"{mess}{record}\n"
        return mess

    def add_record(self, record: Record):
        # self.selected_index = -1
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def remove_record_by_index(self, index):
        """Удаление контакта по индексу"""
        if 0 <= index < len(self.data):
            del self.data[index]
            self.selected_index = max(0, self.selected_index - 1)

    def get_record_by_index(self, index) -> Optional[Record]:
        """Получение контакта по индексу"""
        if 0 <= index < len(self.data):

            # Получить ключ по индексу
            # key = list(self.data.keys())[index]
            # print(f"Ключ на позиции {index}: {key}")

            # Получить значение по индексу
            # value = list(self.data.values())[index]
            # print(f"Значение на позиции {index}: {value}")

            # Получить пару ключ-значение по индексу
            # key_value = list(d.items())[index]
            # print(f"Пара на позиции {index}: {key_value}")
            key = list(self.data.keys())[index]

            return self.data[key]
        return None

    def update_record_by_index(self, index, new_record: Record):
        """Заменить существующий контакт новым по индексу"""
        if 0 <= index < len(self.data):
            key = list(self.data.keys())[index]
            # self.data[record.name.value] = record
            self.data[key] = new_record

            return True
        return False

    # get_upcoming_birthdays яка для контактів адресної книги повертає список користувачів, яких потрібно привітати по днях на наступному тижні.

    def get_upcoming_birthdays(self):

        today = datetime.today().date()  # поточна дата
        flag_current_year_isnot_leap = not calendar.isleap(today.year)
        flag_next_year_isnot_leap = not calendar.isleap(today.year+1)
        upcoming_birthdays = []
        result = ''
        # перебираємо всі словники (записи) в data.records
        for record in self.data.values():
            birth_str = record.get_birthday().value
            if not birth_str:
                continue
            birthday = datetime.strptime(birth_str, "%d.%m.%Y").date()
            # додати перевірку, чи є в загалі дата народження в запису!
            # задаємо ознаку того, що ДН у високосну дату
            flag_bd_in_leap_feb_29 = True if birthday.month == 2 and birthday.day == 29 else False

            # Перевірка, чи день народження вже був у цьому році
            # flag_pass_b - true якщо ДН вже був в цьому році
            # якщо ДН був у високосному році 29 лютого то та цей рік НЕ Є високосним, то
            # порівняння робимо з урахуванням -одного дня
            flag_pass_b = datetime(today.year, birthday.month, birthday.day-int(
                flag_bd_in_leap_feb_29*flag_current_year_isnot_leap)).date() < today
            # Якщо ДН вже був в цьому році, то змінюємо рік на наступний з урахуванням високосного року
            if flag_pass_b:
                # якщо дата народження була 29 лютого у високосному році,
                # и ДН вже в цьому році був, то переносимо на наступний рік, але якщо
                # наступний рік не є високосний - змінюемо день народженя 29 лютого на -1 день
                birthday = datetime(
                    today.year + 1, birthday.month, birthday.day-int(flag_bd_in_leap_feb_29*flag_next_year_isnot_leap)).date()
            else:
                birthday = datetime(today.year, birthday.month, birthday.day -
                                    int(flag_bd_in_leap_feb_29*flag_current_year_isnot_leap)).date()

        # Перевіряємо, чи дата народження припадає на наступні 7 днів
            if birthday-today <= timedelta(days=7):
                # Перевірка, чи день народження припадає на вихідний
                if birthday.weekday() >= 5:  # 5 - субота, 6 - неділя
                    # Якщо на вихідний, переносимо на наступний понеділок
                    days_to_monday = 7 - birthday.weekday()
                    birthday = birthday + timedelta(days=days_to_monday)

            # Додаємо до списку словник з ім'ям і датою привітання
                upcoming_birthdays.append({
                    "name": record.name.value,
                    "congratulation_date": birthday.strftime("%d.%m.%Y")
                })
        return ("\n".join(f'Name: {rec["name"]:<15}, congratulation date: {rec["congratulation_date"]:<35}' for rec in upcoming_birthdays))
