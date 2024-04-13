import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt

def xor_encrypt_decrypt(image, key):
    image_np = np.array(image)
    key_np = np.array(key)
  
    key_np = np.resize(key_np, image_np.shape)
  
    result = np.bitwise_xor(image_np, key_np)
    return result

def display_images(original, encrypted, decrypted):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    axes[0].set_title('Original Image')
    axes[0].axis('off')

    axes[1].imshow(encrypted, cmap='gray')
    axes[1].set_title('Encrypted Image')
    axes[1].axis('off')

    axes[2].imshow(cv2.cvtColor(decrypted, cv2.COLOR_BGR2RGB))
    axes[2].set_title('Decrypted Image')
    axes[2].axis('off')

    st.pyplot(fig)

# Streamlit App
st.title("Image Encryption with XOR")

uploaded_file = st.file_uploader("Choose an Image", type="png")
if uploaded_file is not None:
    # Read the uploaded image
    image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Define your key
    key = np.array([
        [[54, 162, 12], [176, 238, 231], [37, 47, 85]],
        [[62, 152, 72], [119, 86, 244], [133, 52, 50]],
        [[224, 13, 145], [27, 24, 140], [177, 29, 81]]
    ], dtype=np.uint8)

    # Encrypt or decrypt the image
    if st.button("Encrypt/Decrypt"):
        if "encrypted_image" not in st.session_state:
            st.session_state.encrypted_image = xor_encrypt_decrypt(image, key)
            st.button("Decrypt")
            st.image(st.session_state.encrypted_image, caption='Encrypted Image', use_column_width=True)
        else:
            decrypted_image = xor_encrypt_decrypt(st.session_state.encrypted_image, key)
            st.image(decrypted_image, caption='Decrypted Image', use_column_width=True)