import sys

phone_book = {}

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "This contact does not exist"
        except ValueError:
            return "Please enter a valid name and phone number separated by a space"
        except IndexError:
            return "Please enter a name"
    return inner

@input_error
def add_contact(name, phone):
    phone_book[name] = phone
    return f"Contact {name} with phone number {phone} has been added"

@input_error
def change_phone(name, phone):
    phone_book[name] = phone
    return f"Phone number for {name} has been changed to {phone}"

@input_error
def get_phone(name):
    return phone_book[name]

def show_all():
    if not phone_book:
        return "The phone book is empty"
    return "\n".join(f"{name}: {phone}" for name, phone in phone_book.items())

def handle_command(command):
    command_parts = command.lower().split()

    if command_parts[0] == "hello":
        return "How can I help you?"

    if command_parts[0] == "add":
        if len(command_parts) < 3:
            raise ValueError
        name, phone = command_parts[1], command_parts[2]
        return add_contact(name, phone)

    if command_parts[0] == "change":
        if len(command_parts) < 3:
            raise ValueError
        name, phone = command_parts[1], command_parts[2]
        return change_phone(name, phone)

    if command_parts[0] == "phone":
        if len(command_parts) < 2:
            raise IndexError
        name = command_parts[1]
        return get_phone(name)

    if command_parts[0] == "show" and command_parts[1] == "all":
        return show_all()

    if command_parts[0] in ["good", "bye", "close", "exit"]:
        print("Good bye!")
        sys.exit()

    return "Unknown command"

def main():
    while True:
        command = input('Please enter command and args: ')
        response = handle_command(command)
        print(response)

if __name__ == '__main__':
    main()
