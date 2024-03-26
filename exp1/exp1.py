import math
class PlayfairCipher():
    def __init__(self, key):
        self.key = self.process_key(key)
        self.matrix = self.generate_matrix()
    def process_key(self, key):
        key = key.replace(" ", "").upper()
        key = key.replace("J", "I") # Replace J with I
        key_set = set(key)
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        for char in key_set:
            alphabet = alphabet.replace(char, "")
        return key + alphabet
    def generate_matrix(self):
        matrix = [[0] * 5 for _ in range(5)]
        key_idx = 0
        for i in range(5):
            for j in range(5):
                matrix[i][j] = self.key[key_idx]
                key_idx += 1
        return matrix
    
    def find_position(self, char):
        for i in range(5):
            for j in range(5):
                if self.matrix[i][j] == char:
                    return i, j
                
    def encrypt(self, message):
        message = message.replace(" ", "").upper()
        message_pairs = []
        i = 0
        while i < len(message):
            if i == len(message) - 1 or message[i] == message[i + 1]:
                message_pairs.append(message[i] + "X")
                i += 1
            else:
                message_pairs.append(message[i] + message[i + 1])
                i += 2
        encrypted_message = ""  # Move this line outside the loop
        for pair in message_pairs:
            char1, char2 = pair[0], pair[1]
            row1, col1 = self.find_position(char1)
            row2, col2 = self.find_position(char2)
            if row1 == row2:  # Same row
                encrypted_message += self.matrix[row1][(col1 + 1) % 5] + self.matrix[row2][(col2+ 1) % 5]
            elif col1 == col2:  # Same column
                encrypted_message += self.matrix[(row1 + 1) % 5][col1] + self.matrix[(row2 + 1) %5][col2]
            else:  # Different row and column
                encrypted_message += self.matrix[row1][col2] + self.matrix[row2][col1]
        return encrypted_message  # Move this line outside the loop

                
def single_columnar_transposition_cipher(plaintext, key):
        cipher = ""
        k_indx = 0
        plaintext_len = float(len(plaintext))
        plaintext_lst = list(plaintext)
        key_lst = sorted(list(str(key))) # Ensure the key is converted to a string and sorted
        col = len(key)
        row = int(math.ceil(plaintext_len / col))
        fill_null = int((row * col) - plaintext_len)
        plaintext_lst.extend([''] * fill_null) # Use an empty string for padding
        matrix = [plaintext_lst[i: i + col] for i in range(0, len(plaintext_lst), col)]
        for _ in range(col):
            curr_idx = key.index(key_lst[k_indx])
            cipher += ''.join([row[curr_idx] for row in matrix])
            k_indx += 1
        return cipher
    
def double_columnar_transposition_cipher(plaintext, playfair_key, columnar_key):
        # Playfair Encryption
        playfair_cipher = PlayfairCipher(playfair_key)
        playfair_ct = playfair_cipher.encrypt(plaintext)
        # Single Columnar Transposition Encryption using Playfair ciphertext
        single_columnar_ct = single_columnar_transposition_cipher(playfair_ct, columnar_key)
        # Second Single Columnar Transposition Encryption using the first ciphertext
        double_columnar_ct = single_columnar_transposition_cipher(single_columnar_ct,columnar_key)
        return double_columnar_ct
    
def main():
    plaintext = input("Enter the plaintext: ")
    playfair_key = input("Enter the Playfair key: ")
    columnar_key = input("Enter the Double Columnar key: ")
    playfair_cipher = PlayfairCipher(playfair_key)
    playfair_ct = playfair_cipher.encrypt(plaintext)
    double_cipher = double_columnar_transposition_cipher(plaintext, playfair_key,columnar_key)
    print("CT after Playfair Cipher Encryption: ", playfair_ct)
    print("CT after Playfair Cipher Encryption + Double Columnar Transposition Cipher:",double_cipher)
    
    
    
main()
