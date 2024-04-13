import streamlit as st
import cv2
import numpy as np
from numpy import random
from datetime import datetime
import io
import matplotlib.pyplot as plt

# Check if the session state feature is available in your Streamlit version
if hasattr(st, 'session_state'):
    # If not, initialize it
    if not hasattr(st.session_state, 'encrypted_dft'):
        st.session_state.encrypted_dft = None
    if not hasattr(st.session_state, 'dft_key'):
        st.session_state.dft_key = None
    if not hasattr(st.session_state, 'chaotic_key'):
        st.session_state.chaotic_key = None
    if not hasattr(st.session_state, 'xor_key'):
        st.session_state.xor_key = None
    if not hasattr(st.session_state, 'encrypted_image'):
        st.session_state.encrypted_image = None
else:
    st.error("Please upgrade to the latest version of Streamlit to use the session state feature.")

# DFT Encryption Functions
def dft_encrypt_image(image):
    t1 = datetime.now()
    dft = cv2.dft(np.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)
    key = np.random.randn(*dft.shape)
    encrypted_dft = dft * key
    t2 = datetime.now()
    print("DFT Encryption Time:", t2 - t1)
    return encrypted_dft, key

def dft_decrypt_image(encrypted_dft, key):
    t1 = datetime.now()
    decrypted_dft = encrypted_dft / key
    decrypted_image = cv2.idft(decrypted_dft, flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT)
    t2 = datetime.now()
    print("DFT Decryption Time:", t2 - t1)
    return decrypted_image

# Chaotic Encryption Functions
def logistic_map(r, x):
    return r * x * (1 - x)

def chaotic_encryption(image, key, iterations=1000):
    t1 = datetime.now()
    encrypted_image = np.zeros_like(image)
    np.random.seed(key)
    r = np.random.uniform(3.6, 4.0)
    x = np.random.rand()
    for i in range(iterations):
        x = logistic_map(r, x)
        idx = np.random.permutation(len(image))
        encrypted_image = image[idx]
    t2 = datetime.now()
    print("Chaotic Encryption Time:", t2 - t1)
    return encrypted_image

def chaotic_decryption(encrypted_image, key, iterations=1000):
    t1 = datetime.now()
    decrypted_image = np.zeros_like(encrypted_image)
    np.random.seed(key)
    r = np.random.uniform(3.6, 4.0)
    x = np.random.rand()
    for i in range(iterations):
        x = logistic_map(r, x)
        idx = np.argsort(np.random.permutation(len(encrypted_image)))
        decrypted_image = encrypted_image[idx]
    t2 = datetime.now()
    print("Chaotic Decryption Time:", t2 - t1)
    return decrypted_image

# XOR Encryption Functions
def xor_encrypt_image(image):
    t1 = datetime.now()
    r, c, t = image.shape
    key = random.randint(256, size=(r, c, t))
    encrypted_image = np.zeros((r, c, t), np.uint8)
    for row in range(r):
        for column in range(c):
            for depth in range(t):
                encrypted_image[row, column, depth] = image[row, column, depth] ^ key[row, column, depth]
    t2 = datetime.now()
    print("XOR Encryption Time:", t2 - t1)
    return encrypted_image, key

def xor_decrypt_image(encrypted_image, key):
    t1 = datetime.now()
    r, c, t = encrypted_image.shape
    decrypted_image = np.zeros((r, c, t), np.uint8)
    for row in range(r):
        for column in range(c):
            for depth in range(t):
                decrypted_image[row, column, depth] = encrypted_image[row, column, depth] ^ key[row, column, depth]
    t2 = datetime.now()
    print("XOR Decryption Time:", t2 - t1)
    return decrypted_image

# Streamlit UI
st.title('Image Encryption and Decryption')

# Menu options
menu = ["DFT", "Chaotic", "XOR"]
option = st.sidebar.selectbox("Choose an encryption algorithm:", menu)

if option == "DFT":
    st.header("DFT Encryption and Decryption")
    uploaded_file = st.file_uploader("Upload image to encrypt/decrypt (PNG, JPEG)", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        original_image = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
        st.image(original_image, caption='Original Image', use_column_width=True)
        if st.button('Encrypt'):
            st.session_state.encrypted_dft, st.session_state.dft_key = dft_encrypt_image(original_image)
            encrypted_image = cv2.idft(st.session_state.encrypted_dft, flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT)
            st.image(np.abs(encrypted_image) / np.max(np.abs(encrypted_image)), caption='Encrypted Image', use_column_width=True)
        if st.button('Decrypt'):
            if st.session_state.encrypted_dft is not None and st.session_state.dft_key is not None:
                decrypted_image = dft_decrypt_image(st.session_state.encrypted_dft, st.session_state.dft_key)
                st.image(np.abs(decrypted_image) / np.max(np.abs(decrypted_image)), caption='Decrypted Image', use_column_width=True)
            else:
                st.error('Please encrypt an image first before decrypting.')

elif option == "Chaotic":
    st.header("Chaotic Encryption and Decryption")
    uploaded_file = st.file_uploader("Upload image to encrypt/decrypt (PNG, JPEG)", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        image = plt.imread(uploaded_file)
        st.image(image, caption='Original Image', use_column_width=True)
        key = st.number_input("Enter an encryption key (integer)", min_value=0)
        if st.button("Encrypt"):
            encrypted_image = chaotic_encryption(image, key)
            st.image(encrypted_image, caption='Encrypted Image', use_column_width=True)
        if st.button("Decrypt"):
            decrypted_image = chaotic_decryption(encrypted_image, key)
            st.image(decrypted_image, caption='Decrypted Image', use_column_width=True)

elif option == "XOR":
    st.header("XOR Encryption and Decryption")
    uploaded_file = st.file_uploader("Upload image to encrypt/decrypt (PNG, JPEG)", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, 1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        st.image(image, caption='Original Image', use_column_width=True)
        if st.button('Encrypt'):
            st.session_state['encrypted_image'], st.session_state['xor_key'] = xor_encrypt_image(image)
            st.image(st.session_state['encrypted_image'], caption='Encrypted Image', use_column_width=True)
        if st.button('Decrypt'):
            if st.session_state['encrypted_image'] is not None and st.session_state['xor_key'] is not None:
                decrypted_image = xor_decrypt_image(st.session_state['encrypted_image'], st.session_state['xor_key'])
                st.image(decrypted_image, caption='Decrypted Image', use_column_width=True)
                st.image(decrypted_image, caption='Decrypted Image', use_column_width=True)
            else:
                st.error('Please encrypt an image first before decrypting.')
