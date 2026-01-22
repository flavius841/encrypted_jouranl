# encrypted_jouranl

This is a **CLI (Command Line Interface) project** that allows you to:
1. generate a key used for encryption and decryption
2. encrypt your text file
3. decrypt your text file

---

## Usage

### Getting Started

1. Prepare a USB flash drive to store your encryption key.
2. Plug the USB drive into your computer.

### Commands

With a USB drive connected, you can run the following commands:

- Generate a key  
  generate key

- Encrypt a file  
  encrypt <filename.txt>

- Decrypt a file  
  decrypt <filename.txt>

### Without a USB Drive

You can also encrypt and decrypt files without using a USB drive:

- Encrypt without USB  
  encrypt <filename.txt> without USB

- Decrypt without USB  
  decrypt <filename.txt> without USB

### Other

- Display the generated key  
  show key


---

## Notes

- This CLI only works in the directory you are currently in.
- Make sure **Python**, **pipx**, and **Git** are installed correctly before running the CLI.
- Make sure you do **not already have a file named `secret.key`** on your USB stick that you use for something else.

If you want to keep your existing `secret.key` file:

1. Download this repository.
2. Open `main.py`.
3. Find all occurrences of `secret.key`.
4. Use the **“Change all occurrences”** option in your editor.
5. Rename it to a new filename that will be used by this CLI.
6. Rebuild the CLI so the changes take effect.

---


## Prerequisites

To run this project, you need to have **Python** and **Git** installed on your system.

---
If you already have Python and Git, you can jump to the Running the CLI section.

---

## Installing Python

### **macOS**

1. Go to the official site: [https://www.python.org/downloads/macos/](https://www.python.org/downloads/macos/)
2. Download the `.pkg` installer.
3. Open it and follow the instructions.

Then, install **pipx**:

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

Restart your terminal after running `ensurepath`.

---

### **Linux (Ubuntu/Debian)**

Install Python:

```bash
sudo apt update
sudo apt install python3
```

Then, install pip and pipx:

```bash
sudo apt install python3-pip
sudo apt update
sudo apt install pipx
```

---

### **Windows**

1. Download Python from: [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
2. Run the installer.
   **Important:** Check the box **“Add Python to PATH”** before clicking “Install Now.”
3. After installation, install pipx:

```cmd
python -m pip install --user pipx
python -m pipx ensurepath
```

Restart Command Prompt after running `ensurepath`.

---

## Installing Git

### **macOS**

If you have Homebrew:

```bash
brew install git
```

### **Linux (Ubuntu/Debian)**

```bash
sudo apt update
sudo apt install git
```

### **Windows**

1. Go to: [https://git-scm.com/download/win](https://git-scm.com/download/win)
2. Download the installer and follow the prompts (default options are fine).

---

## Running the CLI

After installing Python, pipx, and Git, you can install the CLI project:

```bash
pipx install git+https://github.com/flavius841/encrypted_jouranl
```

Now, you can run the CLI by typing:

```bash
encrypted_journal
```

in your terminal or Command Prompt.




