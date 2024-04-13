import cv2
import numpy as np
from numpy import random

# Load original image
demo = cv2.imread('zenithzest.jpeg')
r, c, t = demo.shape

# Display original image
cv2.imshow("Original image", demo)
cv2.waitKey()

# Create random key
key = random.randint(256, size = (r, c, t))

# Encryption
# Iterate over the image
encrypted_image = np.zeros((r, c, t), np.uint8)
for row in range(r):
    for column in range(c):
        for depth in range(t):
            encrypted_image[row, column, depth] = demo[row, column, depth] ^ key[row, column, depth] 
            
cv2.imshow("Encrypted image", encrypted_image)
cv2.waitKey()

# Decryption
# Iterate over the encrypted image
decrypted_image = np.zeros((r, c, t), np.uint8)
for row in range(r):
    for column in range(c):
        for depth in range(t):
            decrypted_image[row, column, depth] = encrypted_image[row, column, depth] ^ key[row, column, depth] 
            
cv2.imshow("Decrypted Image", decrypted_image)

cv2.waitKey()
cv2.destroyAllWindows()