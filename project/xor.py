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

def main():
    st.title("XOR Image Encryption and Decryption")

    # Sidebar options
    mode = st.sidebar.selectbox("Select Mode", ["Encryption", "Decryption"])

    # Upload image
    uploaded_file = st.file_uploader("Choose an image file (PNG, JPEG)", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # Read the uploaded image
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Display original image
        st.subheader("Original Image")
        st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption="Original Image", use_column_width=True)

        # Initialize encrypted_image
        encrypted_image = None

        # Generate a random key
        key = np.random.randint(0, 256, size=image.shape, dtype=np.uint8)

        if mode == "Encryption":
            # Encrypt button
            if st.button("Encrypt"):
                encrypted_image = xor_encrypt_decrypt(image, key)
                st.subheader("Encrypted Image")
                st.image(encrypted_image, caption="Encrypted Image", use_column_width=True)

                # Convert encrypted image to bytes
                encrypted_image_bytes = cv2.imencode('.png', encrypted_image)[1].tobytes()

                # Download button for encrypted image
                st.download_button(label="Download Encrypted Image", data=encrypted_image_bytes, file_name="encrypted_image.png", mime="image/png")

        elif mode == "Decryption" and encrypted_image is not None:
            # Decrypt button
            if st.button("Decrypt"):
                decrypted_image = xor_encrypt_decrypt(encrypted_image, key)
                st.subheader("Decrypted Image")
                st.image(decrypted_image, caption="Decrypted Image", use_column_width=True)

if __name__ == "__main__":
    main()
