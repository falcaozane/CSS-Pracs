import streamlit as st
import cv2
import numpy as np
from matplotlib import pyplot as plt

# Function to encrypt an image in the frequency domain
def encrypt_image(image, key):
    # Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform 2D Fourier transform
    f_transform = np.fft.fft2(gray_image)
    f_shift = np.fft.fftshift(f_transform)

    # Encrypt the frequency domain data
    encrypted_f_shift = f_shift * key

    # Inverse shift
    encrypted_f_transform = np.fft.ifftshift(encrypted_f_shift)

    # Inverse Fourier transform
    encrypted_image = np.fft.ifft2(encrypted_f_transform)
    encrypted_image = np.abs(encrypted_image)

    # Normalize encrypted image
    encrypted_image = cv2.normalize(encrypted_image, None, 0, 255, cv2.NORM_MINMAX)

    return encrypted_image.astype(np.uint8)

# Function to decrypt an encrypted image in the frequency domain
def decrypt_image(encrypted_image, key):
    # Perform 2D Fourier transform
    f_transform = np.fft.fft2(encrypted_image)
    f_shift = np.fft.fftshift(f_transform)

    # Decrypt the frequency domain data
    decrypted_f_shift = f_shift / key

    # Inverse shift
    decrypted_f_transform = np.fft.ifftshift(decrypted_f_shift)

    # Inverse Fourier transform
    decrypted_image = np.fft.ifft2(decrypted_f_transform)
    decrypted_image = np.abs(decrypted_image)

    # Normalize decrypted image
    decrypted_image = cv2.normalize(decrypted_image, None, 0, 255, cv2.NORM_MINMAX)

    return decrypted_image.astype(np.uint8)

# Create a Streamlit app
st.title("Frequency Domain Image Encryption and Decryption")

# Upload image
uploaded_file = st.file_uploader("Choose an image to encrypt/decrypt", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read the uploaded image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # Display original image
    st.subheader("Original Image")
    st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption="Original Image", use_column_width=True)

    # Generate a random encryption key
    key = np.random.random(image.shape[:2])
    st.write(key)

    # Encrypt button
    if st.button("Encrypt"):
        encrypted_image = encrypt_image(image, key)
        st.subheader("Encrypted Image")
        st.image(encrypted_image, caption="Encrypted Image", use_column_width=True)

        # Decrypt button
        if st.button("Decrypt"):
            decrypted_image = decrypt_image(encrypted_image, key)
            st.subheader("Decrypted Image")
            st.image(decrypted_image, caption="Decrypted Image", use_column_width=True)
