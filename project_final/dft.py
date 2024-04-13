import streamlit as st
import cv2
import numpy as np

# Check if the session state feature is available in your Streamlit version
if hasattr(st, 'session_state'):
    # If not, initialize it
    if not hasattr(st.session_state, 'encrypted_dft'):
        st.session_state.encrypted_dft = None
    if not hasattr(st.session_state, 'key'):
        st.session_state.key = None
else:
    st.error("Please upgrade to the latest version of Streamlit to use the session state feature.")

def encrypt_image(image):
    # Perform Discrete Fourier Transform (DFT)
    dft = cv2.dft(np.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)
    
    # Generate a random key for encryption
    key = np.random.randn(*dft.shape)
    
    # Element-wise multiplication with the key
    encrypted_dft = dft * key
    
    return encrypted_dft, key

def decrypt_image(encrypted_dft, key):
    # Element-wise division with the key to retrieve the original DFT
    decrypted_dft = encrypted_dft / key
    
    # Apply inverse DFT to get the decrypted image
    decrypted_image = cv2.idft(decrypted_dft, flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT)
    
    return decrypted_image

st.title('DFT Image Encryption and Decryption')

uploaded_file = st.file_uploader("Choose an image...", type="jpg")
if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    original_image = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)

    st.image(original_image, caption='Original Image', use_column_width=True)

    if st.button('Encrypt'):
        st.session_state.encrypted_dft, st.session_state.key = encrypt_image(original_image)
        encrypted_image = cv2.idft(st.session_state.encrypted_dft, flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT)
        st.image(np.abs(encrypted_image) / np.max(np.abs(encrypted_image)), caption='Encrypted Image', use_column_width=True)

    if st.button('Decrypt'):
        if st.session_state.encrypted_dft is not None and st.session_state.key is not None:
            decrypted_image = decrypt_image(st.session_state.encrypted_dft, st.session_state.key)
            st.image(np.abs(decrypted_image) / np.max(np.abs(decrypted_image)), caption='Decrypted Image', use_column_width=True)
        else:
            st.error('Please encrypt an image first before decrypting.')