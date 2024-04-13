import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io

def logistic_map(r, x):
    return r * x * (1 - x)

def chaotic_encryption(image, key, iterations=1000):
    encrypted_image = np.zeros_like(image)
    np.random.seed(key)
    
    r = np.random.uniform(3.6, 4.0)  # Chaotic parameter (typically in the range [3.6, 4.0])
    x = np.random.rand()  # Initial condition
    
    for i in range(iterations):
        x = logistic_map(r, x)
        idx = np.random.permutation(len(image))  # Shuffle pixel indices
        encrypted_image = image[idx]  # Scramble pixel values based on shuffled indices
    
    return encrypted_image

def chaotic_decryption(encrypted_image, key, iterations=1000):
    decrypted_image = np.zeros_like(encrypted_image)
    np.random.seed(key)
    
    r = np.random.uniform(3.6, 4.0)  # Chaotic parameter (typically in the range [3.6, 4.0])
    x = np.random.rand()  # Initial condition
    
    for i in range(iterations):
        x = logistic_map(r, x)
        idx = np.argsort(np.random.permutation(len(encrypted_image)))  # Inverse shuffle pixel indices
        decrypted_image = encrypted_image[idx]  # Restore original pixel values based on inverse shuffled indices
    
    return decrypted_image

# Create a Streamlit app
st.title("Chaotic Image Encryption and Decryption")

# Menu options
menu = ["Encrypt", "Decrypt"]
option = st.sidebar.selectbox("Choose an option:", menu)

if option == "Encrypt":
    st.header("Encryption")
    # Upload image to encrypt
    uploaded_file = st.file_uploader("Upload image to encrypt (PNG, JPEG)", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # Read the uploaded image
        image = plt.imread(uploaded_file)
        
        # Generate a random key
        key = st.number_input("Enter an encryption key (integer)", min_value=0)

        # Encrypt button
        if st.button("Encrypt"):
            encrypted_image = chaotic_encryption(image, key)

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
        encrypted_image = plt.imread(uploaded_file)
        
        # Upload key for decryption
        key = st.number_input("Enter the decryption key", min_value=0)

        # Decrypt button
        if st.button("Decrypt"):
            decrypted_image = chaotic_decryption(encrypted_image, key)

            # Display encrypted and decrypted images
            st.subheader("Encrypted Image")
            st.image(encrypted_image, caption="Encrypted Image", use_column_width=True)

            st.subheader("Decrypted Image")
            st.image(decrypted_image, caption="Decrypted Image", use_column_width=True)

            # Download button for decrypted image
            decrypted_image_bytes = io.BytesIO()
            plt.imsave(decrypted_image_bytes, decrypted_image, format='png')
            st.download_button(label="Download Decrypted Image", data=decrypted_image_bytes.getvalue(), file_name="decrypted_image.png")
