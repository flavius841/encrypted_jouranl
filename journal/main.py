import requests
import os
from colorama import init, Fore, Style
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from cryptography.fernet import Fernet

current_folder = os.getcwd()
all_items = os.listdir(current_folder)
file = None
init(autoreset=True)
commnads = ["help", "create-file", "upload",
            "find", "count", "rename", "exit", "delete", "show"]
commands_find = ["yes", "no", "replace-everywhere",
                 "delete", "delete-everywhere"]
commands_count = ["words", "lines", "characters"]
files = [f for f in all_items if os.path.isfile(
    os.path.join(current_folder, f)) and f.endswith(".txt")]
txt_files = [f.replace(".txt", "") for f in files]

command_completer = WordCompleter(commnads, ignore_case=True)
find_completer = WordCompleter(commands_find, ignore_case=True)
count_completer = WordCompleter(commands_count, ignore_case=True)
list_completer = WordCompleter(txt_files, ignore_case=True)


def main():
    print("Welcome to my CLI project. Here you cand create edit and \nfind what you want in your text "
          "file \nType 'help' to see available commands or read more information.")

    while True:
        message = prompt(">>> ", completer=command_completer).strip()
        parts = message.split()

        if message.lower() == "help":
            # open_help()
            pass

        elif message.lower() == "show":
            show_files()

        elif message.lower() == "exit":
            print("Exiting the program. Goodbye!")
            break

        elif message.strip().lower() != "":
            print("Invalid command. Type 'Help' to see available commands.")

        elif len(parts) == 2 and parts[0].lower() == 'encrypt' and parts[1] in files:
            ask_if_generate_key()
            file_to_encrypt = find_file(parts[1])
            if file_to_encrypt:
                Encrypt(file_to_encrypt)
                file_to_encrypt.close()
                print(f"File '{parts[1]}' has been encrypted.")


def show_files():
    print("Text files in the current directory:")
    for f in files:
        print(f"- {f}")


def Generate_Key():
    key = Fernet.generate_key()
    return key


def Encrypt(files):
    with open("secret.key", "rb") as key_file:
        key = key_file.read()
    fernet = Fernet(key)
    original = files.read()
    encrypted = fernet.encrypt(original)
    with open(files.name, "wb") as encrypted_file:
        encrypted_file.write(encrypted)


# def Decrypt(key, files):


def ask_if_generate_key():
    choice = input("Generate a new key? (y/n): ")
    if choice.lower() == 'y':
        with open("secret.key", "wb") as key_file:
            key_file.write(Generate_Key())
    elif choice.lower() == 'n':
        pass
    else:
        print("Invalid choice. Please enter 'y' or 'n'.")
        ask_if_generate_key()


def find_file(filename):
    if os.path.exists(filename):
        print("File found! Opening it...")
        return open(filename, "a")
    else:
        print("That file does NOT exist.")
        return None
