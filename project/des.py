# Import necessary libraries
import streamlit as st
from Crypto.Cipher import DES3
from hashlib import md5
import os

# Function to perform encryption
def encrypt_file(file_bytes, key):
    # Hash the key using md5 and adjust parity
    key_hash = md5(key.encode('ascii')).digest()
    tdes_key = DES3.adjust_key_parity(key_hash)

    # Create a Triple DES cipher
    cipher = DES3.new(tdes_key, DES3.MODE_EAX, nonce=b'0')

    # Encrypt the file
    encrypted_file_bytes, tag = cipher.encrypt_and_digest(file_bytes)

    return encrypted_file_bytes, tag

# Function to perform decryption
def decrypt_file(file_bytes, key, tag):
    # Hash the key using md5 and adjust parity
    key_hash = md5(key.encode('ascii')).digest()
    tdes_key = DES3.adjust_key_parity(key_hash)

    # Create a Triple DES cipher
    cipher = DES3.new(tdes_key, DES3.MODE_EAX, nonce=b'0')

    # Decrypt the file
    decrypted_file_bytes = cipher.decrypt_and_verify(file_bytes, tag)

    return decrypted_file_bytes

# Create a Streamlit app
st.title("Triple DES Encryption and Decryption")

# Operation selection
operation = st.radio('Choose operation:', ['Encryption', 'Decryption'])

# Upload file
uploaded_file = st.file_uploader('Upload file', type=['txt', 'pdf', 'jpg', 'png'])

# Key input
key = st.text_input('Enter Triple DES key:')

if uploaded_file is not None:
    # Convert uploaded file to bytes
    file_bytes = uploaded_file.read()

    if operation == 'Encryption':
        encrypted_file_bytes, tag = encrypt_file(file_bytes, key)
        st.write('Encryption completed successfully!')
        st.write('Authentication tag:', tag.hex())
        # Save encrypted file
        with open('encrypted_file', 'wb') as f:
            f.write(encrypted_file_bytes)
        st.download_button(label='Download encrypted file', data=encrypted_file_bytes, file_name='encrypted_file')
    elif operation == 'Decryption':
        tag_hex = st.text_input('Enter authentication tag:')
        tag = bytes.fromhex(tag_hex)
        decrypted_file_bytes = decrypt_file(file_bytes, key, tag)
        st.write('Decryption completed successfully!')
        # Save decrypted file
        with open('decrypted_file', 'wb') as f:
            f.write(decrypted_file_bytes)
        st.download_button(label='Download decrypted file', data=decrypted_file_bytes, file_name='decrypted_file')
