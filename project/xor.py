import streamlit as st
import cv2
import numpy as np

def xor_encrypt_decrypt(image, key):
    image_np = np.array(image)
    key_np = np.array(key)
    
    key_np = np.resize(key_np, image_np.shape)
    
    result = np.bitwise_xor(image_np, key_np)
    return result

# Create a Streamlit app
st.title("XOR Image Encryption and Decryption")

# Upload image
uploaded_file = st.file_uploader("Choose an image file (PNG, JPEG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Read the uploaded image
    image_bytes = uploaded_file.getvalue()
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Display original image
    st.subheader("Original Image")
    st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption="Original Image", use_column_width=True)

    # Generate a random key
    key = np.random.randint(0, 256, size=image.shape, dtype=np.uint8)

    # Encrypt button
    if st.button("Encrypt"):
        encrypted_image = xor_encrypt_decrypt(image, key)
        st.subheader("Encrypted Image")
        st.image(encrypted_image, caption="Encrypted Image", use_column_width=True)

    # Decrypt button
    if st.button("Decrypt"):
        decrypted_image = xor_encrypt_decrypt(encrypted_image, key)
        st.subheader("Decrypted Image")
        st.image(decrypted_image, caption="Decrypted Image", use_column_width=True)
