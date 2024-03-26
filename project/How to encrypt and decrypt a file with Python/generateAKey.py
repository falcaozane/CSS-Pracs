# Please if you can... Help me to help you! I really need your support!
# Donate: https://bit.ly/2Hdu9vb
# My udemy courses: https://linktr.ee/AllTechProgramming

# https://pypi.org/project/cryptography/
# 0) pip install cryptography

# 1) Generate a symmetric key
from cryptography.fernet import Fernet
key = Fernet.generate_key()

# 2) Save the key into a file
with open('myTopSecretKey.key', 'wb') as file:
    file.write(key)