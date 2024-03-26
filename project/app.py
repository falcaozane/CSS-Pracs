import streamlit as st
from PIL import Image
from stegano import lsb

# Function to hide a message in an image
def hide_message(image_path, message):
    secret_image = lsb.hide(image_path, message)
    output_path = "output.png"
    secret_image.save(output_path)
    return output_path

# Function to extract a message from an image
def extract_message(image_path):
    secret_message = lsb.reveal(image_path)
    return secret_message

# Streamlit UI
st.title("Image Steganography")

option = st.sidebar.selectbox(
    'Choose an option:',
    ('Hide Message', 'Extract Message'))

if option == 'Hide Message':
    st.header("Hide Message in Image")
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        message_to_hide = st.text_area("Enter the message to hide")

        if st.button("Hide Message"):
            if message_to_hide:
                output_image_path = hide_message(uploaded_file, message_to_hide)
                st.image(output_image_path, caption='Image with Hidden Message', use_column_width=True)
                st.success("Message hidden successfully! You can download the image with the hidden message below.")
                st.download_button(
                    label="Download Image with Hidden Message",
                    data=open(output_image_path, "rb").read(),
                    file_name="hidden_image.png",
                    mime="image/png",
                )
            else:
                st.error("Please enter a message to hide")
                
elif option == 'Extract Message':
    st.header("Extract Message from Image")
    uploaded_file = st.file_uploader("Upload an image with hidden message", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

        if st.button("Extract Message"):
            extracted_message = extract_message(uploaded_file)
            st.success(f"Extracted message: {extracted_message}")
