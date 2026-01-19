import os
import platform
import string
from colorama import init, Fore, Style as CStyle
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from cryptography.fernet import Fernet
from pathlib import Path
import ctypes
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style as PTStyle

style = PTStyle.from_dict({
    "prompt": "ansigreen dim",
    "": "bold ansibrightgreen",
})

current_folder = os.getcwd()
all_items = os.listdir(current_folder)
file = None
init(autoreset=True)
commnads = ["help", "show", "encrypt", "decrypt",
            "show key", "generate key", "exit", "without usbkey"]
files = [f for f in all_items if os.path.isfile(
    os.path.join(current_folder, f)) and f.endswith(".txt")]
commnads = commnads + files
command_completer = WordCompleter(commnads, ignore_case=True)

KEY_FILENAME = "secret.key"


def main():
    print(fr"""{CStyle.BRIGHT} {Fore.YELLOW}
,------.                                      ,--.            ,--.         ,--.                                      ,--.    
|  .---',--,--,  ,---.,--.--.,--. ,--.,---. ,-'  '-. ,---.  ,-|  |         |  | ,---. ,--.,--.,--.--. ,--,--.,--,--, |  |    
|  `--, |      \| .--'|  .--' \  '  /| .-. |'-.  .-'| .-. :' .-. |    ,--. |  || .-. ||  ||  ||  .--'' ,-.  ||      \|  |    
|  `---.|  ||  |\ `--.|  |     \   ' | '-' '  |  |  \   --.\ `-' |    |  '-'  /' '-' ''  ''  '|  |   \ '-'  ||  ||  ||  |    
`------'`--''--' `---'`--'   .-'  /  |  |-'   `--'   `----' `---'      `-----'  `---'  `----' `--'    `--`--'`--''--'`--'    
                             `---'   `--' 
          Welcome to my CLI project. Here you cand encrypt and decrypt your text files.
          Type 'help' to see available commands or read more information. {CStyle.RESET_ALL}
          """)

    while True:
        message = prompt(
            [("class:prompt", ">>> ")],
            style=style
        )
        parts = message.split()

        if message.lower() == "help":
            open_help()
            # Directory = Path(find_usb_key())
            # print(Directory.parent)
            # print(find_usb_key())

        elif message.lower() == "show":
            show_files()

        elif message.lower() == "exit":
            print("Exiting the program. Goodbye!")
            break

        elif message.lower() == "generate key":
            ask_if_generate_key()

        elif len(parts) == 2 and parts[0].lower() == 'encrypt' and parts[1] in files:
            file_to_encrypt = find_file(parts[1])
            Encrypt(file_to_encrypt, use_usbkey=True)
            file_to_encrypt.close()

        elif len(parts) == 4 and parts[0].lower() == 'encrypt' and parts[2] == 'without' and parts[3] == 'usbkey' and parts[1] in files:
            file_to_encrypt = find_file(parts[1])
            Encrypt(file_to_encrypt, use_usbkey=False)
            file_to_encrypt.close()

        elif len(parts) == 2 and parts[0].lower() == 'encrypt' and parts[1] not in files:
            print(f"File '{parts[1]}' does not exist.")

        elif len(parts) == 2 and parts[0].lower() == 'decrypt' and parts[1] in files:
            file_to_decrypt = find_file(parts[1])
            Decrypt(file_to_decrypt)
            file_to_decrypt.close()

        elif len(parts) == 4 and parts[0].lower() == 'decrypt' and parts[2] == 'without' and parts[3] == 'usbkey' and parts[1] in files:
            file_to_decrypt = find_file(parts[1])
            Decrypt(file_to_decrypt, use_usbkey=False)
            file_to_decrypt.close()

        elif message.lower() == "show key":
            show_key()

        elif message.strip().lower() != "":
            print("Invalid command. Type 'Help' to see available commands.")


def show_files():
    print("Text files in the current directory:")
    for f in files:
        print(f"- {f}")


def Generate_Key():
    key = Fernet.generate_key()
    return key


def Encrypt(files, use_usbkey):
    if use_usbkey:
        key_path = find_usb_key()
        if "secret.key" in key_path:
            with open(key_path, "rb") as key_file:
                key = key_file.read()
        else:
            print(
                f"{Fore.RED}ERROR: No USB key found! Please insert the USB drive containing the key.{CStyle.RESET_ALL}")
            return

    else:
        input_key = input("Enter the encryption key: ").strip()
        key = input_key.encode()
    fernet = Fernet(key)
    original = files.read()
    encrypted = fernet.encrypt(original)
    with open(files.name, "wb") as encrypted_file:
        encrypted_file.write(encrypted)
    print(f"File '{files.name}' has been encrypted.")


def Decrypt(files, use_usbkey=True):
    if use_usbkey:
        key_path = find_usb_key()
        if "secret.key" not in key_path:
            print(
                f"{Fore.RED}ERROR: No USB key found! Please insert the USB drive containing the key.{CStyle.RESET_ALL}")
            return

        with open(key_path, "rb") as key_file:
            key = key_file.read()

    else:
        input_key = input("Enter the decryption key: ").strip()
        key = input_key.encode()
    try:
        fernet = Fernet(key)
        original = files.read()
        decrypted = fernet.decrypt(original)
        with open(files.name, "wb") as decrypted_file:
            decrypted_file.write(decrypted)
        print(f"File '{files.name}' has been decrypted.")

    except Exception as e:
        print(
            f"{Fore.RED}ERROR: Decryption failed{str(e)}{CStyle.RESET_ALL}, maybe the key is incorrect?")


def ask_if_generate_key():
    system = platform.system()
    key_path = find_usb_key()

    if "secret.key" in key_path:
        print(f"{Fore.RED}WARNING: A key already exists!{CStyle.RESET_ALL}")
        print("If you generate a new key, you will NOT be able to decrypt files")
        print("encrypted with the old key unless you backed it up.")
        confirm = input("Are you sure you want to overwrite it? (yes/no): ")
        if confirm.lower().strip() == "no":
            print("Key generation cancelled.")
            return
        elif confirm.lower().strip() != "no" and confirm.lower().strip() != "yes":
            print("Invalid choice. Please enter 'yes' or 'no'.")
            ask_if_generate_key()

    if system == "Windows":
        key_path = key_path.replace("\\secret.key", "")
        with open(f"{key_path}\\secret.key", "wb") as key_file:
            key_file.write(Generate_Key())
            print(f"New key generated and saved to {key_path}\\secret.key")
        return

    key_path = key_path.replace("/secret.key", "")

    with open(f"{key_path}/secret.key", "wb") as key_file:
        key_file.write(Generate_Key())
        print(f"New key generated and saved to {key_path}/secret.key")


def find_file(filename):
    if os.path.exists(filename):
        return open(filename, "rb")
    else:
        return None


def open_help():
    help_text = f"""
    {Fore.BLUE}encrypted_journal Help:{CStyle.RESET_ALL}

    - To encrypt a file, enter the command{Fore.CYAN} 'encrypt <filename>'{CStyle.RESET_ALL}.
      Example: encrypt myfile.txt

    - To decrypt a file, enter the command{Fore.CYAN} 'decrypt <filename>'{CStyle.RESET_ALL}.
      Example: decrypt myfile.txt
    
    - To encrypt a file without using the USB key, enter the command
      {Fore.CYAN} 'encrypt <filename> without usbkey'{CStyle.RESET_ALL}.
      Example: encrypt myfile.txt without usbkey

    - To decrypt a file without using the USB key, enter the command
      {Fore.CYAN} 'decrypt <filename> without usbkey'{CStyle.RESET_ALL}.
      Example: decrypt myfile.txt without usbkey

    - To generate a new encryption key on your USB drive, type{Fore.CYAN} 'generate key'{CStyle.RESET_ALL}.

    - To view the current encryption key stored on your USB drive, type{Fore.CYAN} 'show key'{CStyle.RESET_ALL}.

    - Type{Fore.CYAN} 'show'{CStyle.RESET_ALL} to list all text files in the current directory.

    - Type{Fore.GREEN} 'exit'{CStyle.RESET_ALL} to quit the application.
    """
    print(help_text)


def find_usb_key(find_directory=False):
    system = platform.system()
    potential_paths = []

    if system == "Windows":
        drives = [f"{d}:\\" for d in string.ascii_uppercase if d not in "ABC"]
        for drive in drives:
            if os.path.exists(drive) and is_removable(drive):
                potential_paths.append(os.path.join(drive, KEY_FILENAME))

            if find_directory and is_removable(drive) and os.path.exists(drive):
                potential_paths.append(drive)

    elif system == "Linux":
        user = os.environ.get('USER', 'root')
        base_mounts = [f"/media/{user}", "mnt", "/media", f"/run/media/{user}"]
        for base in base_mounts:
            if os.path.exists(base):
                for mount in os.listdir(base):
                    potential_paths.append(
                        os.path.join(base, mount, KEY_FILENAME))

                    if find_directory:
                        potential_paths.append(os.path.join(base, mount))

    elif system == "Darwin":
        base = "/Volumes"
        if os.path.exists(base):
            for mount in os.listdir(base):
                potential_paths.append(
                    os.path.join(base, mount, KEY_FILENAME))
                if find_directory:
                    potential_paths.append(os.path.join(base, mount))

    for path in potential_paths:
        if os.path.exists(path):
            return path

    if not find_directory:
        return find_usb_key(find_directory=True)


def show_key():
    key_path = find_usb_key()
    if "secret.key" in key_path:
        with open(key_path, "rb") as key_file:
            key = key_file.read()
        print(f"Key found at {key_path}: {key.decode()}")
    else:
        print(f"{Fore.RED}ERROR: No USB key found! Please insert the USB drive containing the key.{Style.RESET_ALL}")


def is_removable(drive_path):
    if platform.system() == "Windows":
        drive_type = ctypes.windll.kernel32.GetDriveTypeW(drive_path)
        return drive_type == 2
    return True
