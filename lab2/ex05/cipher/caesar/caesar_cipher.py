"""
Caesar Cipher Implementation

Công thức mã hóa Caesar:
E = (plaintext + key) % 26  - Encryption
D = (cipher - key) % 26     - Decryption

Ví dụ: 
- A (index=0) + key=3 = D (index=3)
- Z (index=25) + key=3 = C (index=2) vì (25+3)%26 = 2
"""

from cipher.caesar import ALPHABET

class CaesarCipher:
    def __init__(self):
        self.alphabet = ALPHABET
    
    def encrypt_text(self, text: str, key: int) -> str:
        alphabet_len = len(self.alphabet)
        text = text.upper()
        encrypted_text = []
        for letter in text:
            letter_index = self.alphabet.index(letter)
            output_index = (letter_index + key) % alphabet_len
            output_letter = self.alphabet[output_index]
            encrypted_text.append(output_letter)
        return "".join(encrypted_text)
    
    def decrypt_text(self, text: str, key: int) -> str:
        alphabet_len = len(self.alphabet)
        text = text.upper()
        decrypted_text = []
        for letter in text:
            letter_index = self.alphabet.index(letter)
            output_index = (letter_index - key) % alphabet_len
            output_letter = self.alphabet[output_index]
            decrypted_text.append(output_letter)
        return "".join(decrypted_text)