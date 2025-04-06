# from address_book.Models import Name, Phone, Record

class PhoneValidationError(Exception):
    """Кастомное исключение для ошибок валидации номера телефона."""
    pass


class BirthdayValidationError(Exception):
    """Кастомное исключение для ошибок валидации ДР."""
    pass


def input_error(func):
    """Декоратор для обробки помилок при додаванні нової записи"""
    def inner_func(*args, **qwargs):
        try:
            return func(*args, **qwargs)
        except ValueError:
            return 'Невірна команда \n'
        except PhoneValidationError as e:
            return f'{e}\n'
        except BirthdayValidationError as e:
            return f'{e}\n'
    return inner_func
