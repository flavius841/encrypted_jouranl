import os
import platform
import string
from colorama import init, Fore, Style
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from cryptography.fernet import Fernet

current_folder = os.getcwd()
all_items = os.listdir(current_folder)
file = None
init(autoreset=True)
commnads = ["help", "show", "encrypt", "decrypt",]
files = [f for f in all_items if os.path.isfile(
    os.path.join(current_folder, f)) and f.endswith(".txt")]
commnads = commnads + files
command_completer = WordCompleter(commnads, ignore_case=True)

KEY_FILENAME = "secret.key"


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

        elif message.lower() == "generate key":
            ask_if_generate_key()

        elif len(parts) == 2 and parts[0].lower() == 'encrypt' and parts[1] in files:
            file_to_encrypt = find_file(parts[1])
            Encrypt(file_to_encrypt)
            file_to_encrypt.close()
            print(f"File '{parts[1]}' has been encrypted.")

        elif len(parts) == 2 and parts[0].lower() == 'encrypt' and parts[1] not in files:
            print(f"File '{parts[1]}' does not exist.")

        elif len(parts) == 2 and parts[0].lower() == 'decrypt' and parts[1] in files:
            file_to_decrypt = find_file(parts[1])
            Decrypt(file_to_decrypt)
            file_to_decrypt.close()
            print(f"File '{parts[1]}' has been decrypted.")

        elif message.strip().lower() != "":
            print("Invalid command. Type 'Help' to see available commands.")


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


def Decrypt(files):
    with open("secret.key", "rb") as key_file:
        key = key_file.read()
    fernet = Fernet(key)
    original = files.read()
    decrypted = fernet.decrypt(original)
    with open(files.name, "wb") as decrypted_file:
        decrypted_file.write(decrypted)


def ask_if_generate_key():
    if os.path.exists("secret.key"):
        print(f"{Fore.RED}WARNING: A key already exists!{Style.RESET_ALL}")
        print("If you generate a new key, you will NOT be able to decrypt files")
        print("encrypted with the old key unless you backed it up.")
        confirm = input("Are you sure you want to overwrite it? (yes/no): ")
        if confirm.lower() != "yes":
            print("Key generation cancelled.")
            return
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
        return open(filename, "rb")
    else:
        return None


def open_help():
    help_text = f"""
    {Fore.BLUE}encrypted_journal Help:{Style.RESET_ALL}

    - To encrypt a file, enter the command{Fore.CYAN} 'encrypt <filename>'{Style.RESET_ALL}.
      Example: encrypt myfile.txt

    - To decrypt a file, enter the command{Fore.CYAN} 'decrypt <filename>'{Style.RESET_ALL}.
      Example: decrypt myfile.txt

    - Type{Fore.GREEN} 'exit'{Style.RESET_ALL} to quit the application.
    """
    print(help_text)


def find_usb_key():
    system = platform.system()
    potential_paths = []

    if system == "Windows":
        drives = [f"{d}:\\" for d in ]
