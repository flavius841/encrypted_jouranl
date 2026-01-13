from cryptography.fernet import Fernet

# def Generate_Key():

# def Encrypt(key, files):

# def Decrypt(key, files):

if __name__ == "__main__":
    choice = input("Generate a new key? (y/n): ")

    if choice.lower() == 'y':
        with open("secret.key", "wb") as key_file:
            key_file.write(Generate_Key())

    choice2 = input("Encrypt or Decrypt? (e/d): ")
