import requests
import os
from colorama import init, Fore, Style
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

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
            open_help()

        elif message.lower() == "show":
            show_files()

        elif message.lower() == "exit":
            print("Exiting the program. Goodbye!")
            break

        elif message.strip().lower() != "":
            print("Invalid command. Type 'Help' to see available commands.")


def show_files():
    print("Text files in the current directory:")
    for f in files:
        print(f"- {f}")
