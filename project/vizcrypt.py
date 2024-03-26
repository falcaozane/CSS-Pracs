import streamlit as st
from PIL import Image, ImageDraw
import random

# Function to create share for a given pixel
def create_share(pixel):
    if pixel == 1:  # Black pixel
        return Image.new("1", (2, 2), 1), Image.new("1", (2, 2), 1)  # Two white pixels
    else:  # White pixel
        return Image.new("1", (2, 2), 1), Image.new("1", (2, 2), 0)  # One white, one black pixel

# Function to combine shares to reconstruct original image
def combine_shares(share1, share2):
    share1_pixels = share1.load()
    share2_pixels = share2.load()
    width, height = share1.size
    combined_image = Image.new("1", (width * 2, height * 2))
    combined_pixels = combined_image.load()
    for i in range(width):
        for j in range(height):
            combined_pixels[i * 2, j * 2] = share1_pixels[i, j]
            combined_pixels[i * 2 + 1, j * 2] = share2_pixels[i, j]
    return combined_image

# Streamlit UI
st.title("Visual Cryptography with Streamlit")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Read uploaded image
    original_image = Image.open(uploaded_file).convert("L").point(lambda x: 0 if x < 128 else 1)  # Convert to black and white

    # Display original image
    st.subheader("Original Image")
    st.image(original_image, caption="Uploaded Image", use_column_width=True)

    # Button to generate and reconstruct shares
    if st.button("Generate and Reconstruct Shares"):
        # Create shares for each pixel in the original image
        shares = []
        for i in range(original_image.width):
            for j in range(original_image.height):
                share1, share2 = create_share(original_image.getpixel((i, j)))
                shares.append(share1)
                shares.append(share2)

        # Combine shares to reconstruct the original image
        reconstructed_image = Image.new("1", (original_image.width * 2, original_image.height * 2))
        for i in range(original_image.width * original_image.height):
            combined_share = combine_shares(shares[i * 2], shares[i * 2 + 1])
            reconstructed_image.paste(combined_share, (i % original_image.width * 2, i // original_image.width * 2))

        # Display reconstructed image
        st.subheader("Reconstructed Image")
        st.image(reconstructed_image, caption="Reconstructed Image", use_column_width=True)
