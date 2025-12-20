import random
import string

chars = " " + string.punctuation + string.digits + string.ascii_letters
characters = len(chars)
chars = list(chars)

key = chars.copy()
random.shuffle(key)

# print(key)

plain_text = input("Enter a message to encrypt")


for i in characters:
