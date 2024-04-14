import cv2
import numpy as np
import random
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime


def substitution_encrypt(image):
    t1 = datetime.now()
    height, width = image.shape[:2]
    encrypted_image = np.zeros((height, width), dtype=np.uint8)
    lut = list(range(256))
    random.shuffle(lut)
    for i in range(height):
        for j in range(width):
            encrypted_image[i, j] = lut[image[i, j]]
    t2 = datetime.now()
    print("Substitution Encryption Time:", t2-t1)
    return encrypted_image, lut

def substitution_decrypt(encrypted_image, lut):
    t1 = datetime.now()
    height, width = encrypted_image.shape[:2]
    decrypted_image = np.zeros((height, width), dtype=np.uint8)
    lut_inverse = [0] * 256
    for i, val in enumerate(lut):
        lut_inverse[val] = i
    for i in range(height):
        for j in range(width):
            decrypted_image[i, j] = lut_inverse[encrypted_image[i, j]]
    t2 = datetime.now()
    print("Substitution Decryption Time:", t2-t1)
    return decrypted_image

def permutation_encrypt(image):
    t1 = datetime.now()
    height, width = image.shape[:2]
    indices = list(range(height * width))
    random.shuffle(indices)
    encrypted_image = np.zeros((height, width), dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            idx = indices[i * width + j]
            encrypted_image[i, j] = image[idx // width, idx % width]
    t2 = datetime.now()
    print("Permutation Encryption Time:", t2-t1)
    return encrypted_image, indices

def permutation_decrypt(encrypted_image, indices):
    t1 = datetime.now()
    height, width = encrypted_image.shape[:2]
    decrypted_image = np.zeros((height, width), dtype=np.uint8)
    for i, idx in enumerate(indices):
        decrypted_image[idx // width, idx % width] = encrypted_image[i // width, i % width]
    t2 = datetime.now()
    print("Permutation Decryption Time:", t2-t1)
    return decrypted_image

def main():
    st.title("Image Encryption and Decryption")

    image_path = st.file_uploader("Upload an image", type=['jpg', 'jpeg', 'png'])
    if image_path:
        original_image = cv2.imdecode(np.fromstring(image_path.read(), np.uint8), 0)

        # Encrypt the image
        encrypted_substitution, lut = substitution_encrypt(original_image)
        encrypted_permutation, indices = permutation_encrypt(original_image)

        # Decrypt the images
        decrypted_substitution = substitution_decrypt(encrypted_substitution, lut)
        decrypted_permutation = permutation_decrypt(encrypted_permutation, indices)

        # Display the results
        st.subheader("Original Image")
        st.image(original_image, caption='Original Image', use_column_width=True)

        st.subheader("Encrypted Substitution")
        st.image(encrypted_substitution, caption='Encrypted Substitution', use_column_width=True)

        st.subheader("Encrypted Permutation")
        st.image(encrypted_permutation, caption='Encrypted Permutation', use_column_width=True)

        st.subheader("Decrypted Substitution")
        st.image(decrypted_substitution, caption='Decrypted Substitution', use_column_width=True)

        st.subheader("Decrypted Permutation")
        st.image(decrypted_permutation, caption='Decrypted Permutation', use_column_width=True)

if __name__ == "__main__":
    main()
