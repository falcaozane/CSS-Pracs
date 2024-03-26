
# 1) Read the key from file
key = ''
with open('myTopSecretKey.key', 'rb') as file:
    key = file.read()

# 2) Read the encrypted data from file
encryptedData = ''
with open('myTopSecretInfo.txt', 'rb') as file:
    encryptedData = file.read()

# 3) Decrypt the data
from cryptography.fernet import Fernet

f = Fernet(key)

decryptedData = f.decrypt(encryptedData)



print('Encrypted data:', encryptedData.decode())

print()

print('Decrypted data:', decryptedData.decode())