from typing import Optional

from console_bot.services.decorators import input_error
from console_bot.services.types import Command
from console_bot.services.utils import ADDRESS_BOOK, Record
from .register_handlers import DICT_FUNC


def hello() -> str:
    """
    Отвечает в консоль "How can I help you?"
    """
    return "\nHow can I help you?"


@input_error
def add_user(command: Command) -> str:
    """
    По этой команде бот сохраняет в памяти новый контакт.
    Пользователь вводит команду add, имя и номер телефона, обязательно через пробел.
    Пример команды: add Taras 0961233214
    """
    if ADDRESS_BOOK.get(command.name):
        raise ValueError(f"\nContact with the name {command.name} already exists. "
                         f"To add a new number to an existing contact, use the <change> command.")

    ADDRESS_BOOK.add_record(Record(**command.__dict__))

    return f"\nSuccessfully created a new contact '{command.name}'"


@input_error
def add_phone(command: Command) -> str:
    """
    По этой команде бот сохраняет в памяти новый номер телефона для существующего контакта.
    Пользователь вводит команду add-phone, имя и новый номер телефона, обязательно через пробел.
    Пример команды: add-phone Taras 0961233032
    """
    if not ADDRESS_BOOK.get(command.name):
        raise KeyError(command.name)

    phone = ADDRESS_BOOK[command.name].add_phone(command.phone)

    return f"\nContact phone number {command.name} '{phone.value}' successfully added"


@input_error
def change_phone(command: Command) -> Optional[str]:
    """
    По этой команде бот заменяет старый номер телефона новым для существующего контакта.
    Пользователь вводит команду change-phone, имя и новый номер телефона, обязательно через пробел.
    Далее пользователю будет предложено выбрать из списка номер, который необходимо заменить новым.
    Пример команды: change-phone Taras 0961233789
    """
    while True:
        print(user_phone(command))

        try:
            index = int(input("Enter the index number of the phone from the list you want to replace: "))
        except ValueError:
            print("\nChoose a number from the list!")
            print("\n(Enter 0 to cancel)")
            continue

        if index == 0:
            return

        try:
            old_phone, new_phone = ADDRESS_BOOK[command.name].replace_phone(index, command.phone)
        except IndexError:
            print("\nChoose a number from the list!")
            print("\n(Enter 0 to cancel)")
        else:
            break

    return f"\nContact phone number {command.name} '{old_phone.value}' " \
           f"has been successfully replaced by '{new_phone.value}'"


@input_error
def remove_phone(command: Command) -> Optional[str]:
    """
    По этой команде бот удаляет номер телефона существующего контакта.
    Пользователь вводит команду change, имя и номер телефона, который необходимо удалить, обязательно через пробел.
    Пользователь может не вводить номер телефона, тогда ему будет предложено выбрать номер из списка.
    Пример команды: remove-phone Taras 0961233214
    """
    index = None

    if command.phone:
        try:
            _phone = str(int(command.phone))

            for num, phone in enumerate(ADDRESS_BOOK[command.name].phones, 1):
                if _phone in str(phone.value):
                    index = num
                    break

        except ValueError:
            pass

    while True:
        if not index:
            print(user_phone(command))

            try:
                index = int(input("Enter the index number of the phone from the list you want to replace: "))
            except ValueError:
                print("\nChoose a number from the list!")
                print("\n(Enter 0 to cancel)")
                continue

        if index == 0:
            return

        try:
            old_phone = ADDRESS_BOOK[command.name].remove_phone(index)
        except IndexError:
            print("\nChoose a number from the list!")
            print("\n(Enter 0 to cancel)")
            index = None
        else:
            break

    return f"\nContact phone number {command.name} '{old_phone.value}' deleted successfully"


@input_error
def user_phone(command: Command) -> str:
    """
    По этой команде бот выводит в консоль номера телефонов для указанного контакта.
    Пользователь вводит команду phone и имя контакта, чьи номера нужно показать, обязательно через пробел.
    Пример команды: phone Taras
    """
    return (f"Phone numbers of {command.name}\n\t" +
            "\n\t".join([f"{num}. {x.value}" for num, x in enumerate(ADDRESS_BOOK[command.name].phones, 1)]))


@input_error
def show_all_users() -> str:
    """
    По этой команде бот выводит все сохраненные контакты с номерами телефонов и датами рождений в консоль.
    """
    format_users = []

    for user in ADDRESS_BOOK.values():
        phones = ', '.join([str(x.value) for x in user.phones])
        birthday = user.birthday.value if user.birthday else '–'

        format_users.append(f"{user.name.value:<10} : {birthday} : {phones:^12}")

    return '\n'.join(format_users)


def help_command() -> str:
    """
    Выводит список доступных команд
    """
    bot_commands = {}

    for key, value in DICT_FUNC.items():
        _function = value["function"] if isinstance(value, dict) else value

        if _function in bot_commands:
            bot_commands[_function] += f", {key}"
        else:
            bot_commands[_function] = key

    return '\n'.join([s for s in [cmd + func.__doc__ for func, cmd in bot_commands.items()]])


def close_bot() -> str:
    """
    По любой из команд: "good bye", "close", "exit",
    бот завершает свою роботу после того, как выведет в консоль "Good bye!".
    """
    return "Good bye!"
