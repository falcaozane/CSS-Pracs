import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
import io

def encrypt_image(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    dft = np.fft.fft2(gray_image)
    shuffled_phase = np.random.permutation(dft)
    encrypted_image = np.fft.ifft2(shuffled_phase)
    encrypted_image = np.abs(encrypted_image).astype(np.uint8)
    return encrypted_image

def decrypt_image(encrypted_image):
    recovered_dft = np.fft.ifft2(encrypted_image)
    recovered_image = np.abs(recovered_dft).astype(np.uint8)
    return recovered_image

# Create a Streamlit app
st.title("Image Encryption and Decryption")

# Menu options
menu = ["Encrypt", "Decrypt"]
option = st.sidebar.selectbox("Choose an option:", menu)

if option == "Encrypt":
    st.header("Encryption")
    # Upload image to encrypt
    uploaded_file = st.file_uploader("Upload image to encrypt (PNG, JPEG)", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # Read the uploaded image
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Encrypt button
        if st.button("Encrypt"):
            encrypted_image = encrypt_image(image)

            # Display original and encrypted images
            st.subheader("Original Image")
            st.image(image, caption="Original Image", use_column_width=True)

            st.subheader("Encrypted Image")
            st.image(encrypted_image, caption="Encrypted Image", use_column_width=True)

            # Download button for encrypted image
            encrypted_image_bytes = io.BytesIO()
            plt.imsave(encrypted_image_bytes, encrypted_image, format='png')
            st.download_button(label="Download Encrypted Image", data=encrypted_image_bytes.getvalue(), file_name="encrypted_image.png")

elif option == "Decrypt":
    st.header("Decryption")
    # Upload encrypted image to decrypt
    uploaded_file = st.file_uploader("Upload encrypted image to decrypt (PNG, JPEG)", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # Read the uploaded encrypted image
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        encrypted_image = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)

        # Decrypt button
        if st.button("Decrypt"):
            decrypted_image = decrypt_image(encrypted_image)

            # Display encrypted and decrypted images
            st.subheader("Encrypted Image")
            st.image(encrypted_image, caption="Encrypted Image", use_column_width=True)

            st.subheader("Decrypted Image")
            st.image(decrypted_image, caption="Decrypted Image", use_column_width=True)

            # Download button for decrypted image
            decrypted_image_bytes = io.BytesIO()
            plt.imsave(decrypted_image_bytes, decrypted_image, format='png')
            st.download_button(label="Download Decrypted Image", data=decrypted_image_bytes.getvalue(), file_name="decrypted_image.png")
