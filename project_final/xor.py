import streamlit as st
import cv2
import numpy as np
from numpy import random
from datetime import datetime


# Check if this is the first time running this script, if so, create a new session state
if 'first_run' not in st.session_state:
    st.session_state['first_run'] = True
    st.session_state['key'] = None
    st.session_state['encrypted_image'] = None

def encrypt_image(image):
    t1 = datetime.now()
    r, c, t = image.shape
    key = random.randint(256, size = (r, c, t))
    encrypted_image = np.zeros((r, c, t), np.uint8)
    for row in range(r):
        for column in range(c):
            for depth in range(t):
                encrypted_image[row, column, depth] = image[row, column, depth] ^ key[row, column, depth]
    t2 = datetime.now()
    print("Encryption Time:", t2-t1)
    return encrypted_image, key

def decrypt_image(encrypted_image, key):
    t1 = datetime.now()
    r, c, t = encrypted_image.shape
    decrypted_image = np.zeros((r, c, t), np.uint8)
    for row in range(r):
        for column in range(c):
            for depth in range(t):
                decrypted_image[row, column, depth] = encrypted_image[row, column, depth] ^ key[row, column, depth]
    t2 = datetime.now()
    print("Decryption Time:", t2-t1)
    return decrypted_image

st.title('XOR Image Encryption and Decryption')

uploaded_file = st.file_uploader("Choose an image...", type="jpg")
if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    
    if st.button('Encrypt'):
        st.session_state['encrypted_image'], st.session_state['key'] = encrypt_image(image)
        st.image(st.session_state['encrypted_image'], caption='Encrypted Image.', use_column_width=True)
        
    if st.button('Decrypt'):
        if st.session_state['encrypted_image'] is not None and st.session_state['key'] is not None:
            decrypted_image = decrypt_image(st.session_state['encrypted_image'], st.session_state['key'])
            st.image(decrypted_image, caption='Decrypted Image.', use_column_width=True)
