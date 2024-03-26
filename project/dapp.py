import streamlit as st
from PIL import Image
from stegano import lsb
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib
import os
import string
import random

def generate_aes_key():
    characters = string.ascii_uppercase + string.digits
    key = ''.join(random.choice(characters) for _ in range(32))
    return key.encode()


# Encrypt message using AES
def encrypt_message(message, key):
    st.write(key)
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    st.write(ct_bytes)
    return ct_bytes

# Decrypt message using AES
def decrypt_message(ct_bytes, key):
    try:
        cipher = AES.new(key, AES.MODE_CBC)
        pt = unpad(cipher.decrypt(ct_bytes), AES.block_size)
        return pt.decode()
    except ValueError:
        return None

# Function to hide a message in an image
def hide_message(image_path, message, key):
    encrypted_message = encrypt_message(message, key)
    secret_image = lsb.hide(image_path, encrypted_message)
    output_path = "output.png"
    secret_image.save(output_path)
    return output_path

# Function to extract a message from an image
def extract_message(image_path, key):
    encrypted_message = lsb.reveal(image_path)
    st.write(encrypted_message)
    decrypted_message = decrypt_message(encrypted_message, key)
    
    if decrypted_message is not None:
        return decrypted_message
    else:
        raise ValueError("Invalid encryption key. Please make sure the key is a valid AES key.")

# Streamlit UI
st.title("Image Steganography with AES Encryption")

option = st.sidebar.selectbox(
    'Choose an option:',
    ('Hide Message', 'Extract Message'))

if option == 'Hide Message':
    st.header("Hide Message in Image")
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        message_to_hide = st.text_area("Enter the message to hide")

        if st.button("Hide Message"):
            if message_to_hide:
                key = generate_aes_key()
                output_image_path = hide_message(uploaded_file, message_to_hide, key)
                st.image(output_image_path, caption='Image with Hidden Message', use_column_width=True)
                st.success("Message hidden successfully! You can download the image with the hidden message below.")
                st.download_button(
                    label="Download Image with Hidden Message",
                    data=open(output_image_path, "rb").read(),
                    file_name="hidden_image.png",
                    mime="image/png",
                )
                st.info(f"Encryption Key: {key}")
            else:
                st.error("Please enter a message to hide")
                
elif option == 'Extract Message':
    st.header("Extract Message from Image")
    uploaded_file = st.file_uploader("Upload an image with hidden message", type=["png", "jpg", "jpeg"])
    encryption_key = st.text_input("Enter the encryption key")

    if uploaded_file is not None and encryption_key:
        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

        if st.button("Extract Message"):
            try:
                extracted_message = extract_message(uploaded_file, encryption_key.encode())
                st.success(f"Extracted message: {extracted_message}")
            except ValueError as e:
                st.error(str(e))
